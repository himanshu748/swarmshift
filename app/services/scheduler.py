from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass

from app.schemas import (
    Assignment,
    PlanMetrics,
    PlanRequest,
    PlanResponse,
    PlanWave,
    ReplanRequest,
    ReplanResponse,
    TaskSpec,
)


class PlannerError(ValueError):
    def __init__(self, code: str, message: str, details: dict[str, object] | None = None):
        super().__init__(message)
        self.code = code
        self.message = message
        self.details = details or {}


@dataclass(frozen=True)
class _Candidate:
    agent_id: str
    slot_index: int
    start: int
    end: int
    cost: float
    score: tuple[float, ...]


def _find_cycle_nodes(tasks: dict[str, TaskSpec]) -> list[str]:
    state: dict[str, int] = {task_id: 0 for task_id in tasks}
    stack: list[str] = []

    def visit(task_id: str) -> list[str] | None:
        if state[task_id] == 1:
            start = stack.index(task_id)
            return stack[start:]
        if state[task_id] == 2:
            return None
        state[task_id] = 1
        stack.append(task_id)
        for dependency in tasks[task_id].depends_on:
            cycle = visit(dependency)
            if cycle:
                return cycle
        stack.pop()
        state[task_id] = 2
        return None

    for task_id in sorted(tasks):
        cycle = visit(task_id)
        if cycle:
            return sorted(cycle)
    return []


def _validate_mission(mission: PlanRequest) -> tuple[dict[str, TaskSpec], list[str]]:
    task_ids = [task.id for task in mission.tasks]
    agent_ids = [agent.id for agent in mission.agents]
    duplicate_tasks = sorted({item for item in task_ids if task_ids.count(item) > 1})
    duplicate_agents = sorted({item for item in agent_ids if agent_ids.count(item) > 1})
    if duplicate_tasks or duplicate_agents:
        raise PlannerError(
            "duplicate_id",
            "Task and agent IDs must be unique.",
            {"duplicate_task_ids": duplicate_tasks, "duplicate_agent_ids": duplicate_agents},
        )

    tasks = {task.id: task for task in mission.tasks}
    missing: dict[str, list[str]] = {}
    for task in mission.tasks:
        unknown = sorted(set(task.depends_on) - tasks.keys())
        if unknown:
            missing[task.id] = unknown
        if task.id in task.depends_on:
            raise PlannerError(
                "self_dependency",
                f"Task '{task.id}' cannot depend on itself.",
                {"task_id": task.id},
            )
    if missing:
        raise PlannerError(
            "unknown_dependency",
            "Every dependency must reference a task in the same mission.",
            {"missing_by_task": missing},
        )

    indegree = {task_id: 0 for task_id in tasks}
    children: dict[str, list[str]] = defaultdict(list)
    for task in mission.tasks:
        indegree[task.id] = len(task.depends_on)
        for parent in task.depends_on:
            children[parent].append(task.id)

    queue = sorted(task_id for task_id, degree in indegree.items() if degree == 0)
    topological: list[str] = []
    while queue:
        current = queue.pop(0)
        topological.append(current)
        for child in sorted(children[current]):
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)
                queue.sort()
    if len(topological) != len(tasks):
        cycle_nodes = _find_cycle_nodes(tasks)
        raise PlannerError(
            "dependency_cycle",
            "The task graph contains a dependency cycle.",
            {"cycle_task_ids": cycle_nodes},
        )
    return tasks, topological


def _critical_path(
    tasks: dict[str, TaskSpec], topological: list[str]
) -> tuple[list[str], int, dict[str, int]]:
    best_total: dict[str, int] = {}
    predecessor: dict[str, str | None] = {}
    for task_id in topological:
        task = tasks[task_id]
        if not task.depends_on:
            best_total[task_id] = task.duration_minutes
            predecessor[task_id] = None
            continue
        parent = max(task.depends_on, key=lambda item: (best_total[item], item))
        best_total[task_id] = best_total[parent] + task.duration_minutes
        predecessor[task_id] = parent

    end = max(topological, key=lambda item: (best_total[item], item))
    path: list[str] = []
    cursor: str | None = end
    while cursor is not None:
        path.append(cursor)
        cursor = predecessor[cursor]
    path.reverse()

    children: dict[str, list[str]] = defaultdict(list)
    for task in tasks.values():
        for parent in task.depends_on:
            children[parent].append(task.id)
    downstream: dict[str, int] = {}
    for task_id in reversed(topological):
        child_rank = max((downstream[child] for child in children[task_id]), default=0)
        downstream[task_id] = tasks[task_id].duration_minutes + child_rank
    return path, best_total[end], downstream


def _peak_parallelism(assignments: Iterable[Assignment]) -> int:
    events: list[tuple[int, int]] = []
    for assignment in assignments:
        events.append((assignment.start_minute, 1))
        events.append((assignment.end_minute, -1))
    active = 0
    peak = 0
    for _, delta in sorted(events, key=lambda event: (event[0], event[1])):
        active += delta
        peak = max(peak, active)
    return peak


def create_plan(mission: PlanRequest, *, base_start: int = 0) -> PlanResponse:
    tasks, topological = _validate_mission(mission)
    critical_path, critical_minutes, downstream = _critical_path(tasks, topological)
    critical_set = set(critical_path)

    slots = {agent.id: [base_start for _ in range(agent.max_parallel)] for agent in mission.agents}
    finish_times: dict[str, int] = {}
    unscheduled = set(tasks)
    assignments: list[Assignment] = []

    while unscheduled:
        ready = [
            tasks[task_id]
            for task_id in unscheduled
            if all(parent in finish_times for parent in tasks[task_id].depends_on)
        ]
        if not ready:
            raise PlannerError("dependency_cycle", "No schedulable task remains.")
        ready.sort(key=lambda task: (-downstream[task.id], -task.priority, task.id))
        task = ready[0]
        dependency_ready = max(
            (finish_times[parent] for parent in task.depends_on),
            default=base_start,
        )
        required = set(task.requires)
        eligible = [agent for agent in mission.agents if required.issubset(set(agent.capabilities))]
        if not eligible:
            raise PlannerError(
                "no_eligible_agent",
                f"No agent has every capability required by task '{task.id}'.",
                {"task_id": task.id, "required_capabilities": sorted(required)},
            )

        candidates: list[_Candidate] = []
        for agent in eligible:
            for slot_index, available in enumerate(slots[agent.id]):
                start = max(dependency_ready, available)
                end = start + task.duration_minutes
                cost = round((task.duration_minutes / 60) * agent.cost_per_hour, 4)
                deadline_penalty = 0.0
                if mission.objective.deadline_minutes is not None:
                    absolute_deadline = base_start + mission.objective.deadline_minutes
                    if end > absolute_deadline:
                        deadline_penalty = 1_000_000.0 + (end - absolute_deadline) * 10_000.0
                if mission.objective.mode == "fastest":
                    score = (deadline_penalty + end, cost, agent.id, slot_index)
                elif mission.objective.mode == "cheapest":
                    score = (deadline_penalty + cost, end, agent.id, slot_index)
                else:
                    weighted = end + mission.objective.cost_weight * cost * 60
                    score = (deadline_penalty + weighted, end, cost, agent.id, slot_index)
                candidates.append(_Candidate(agent.id, slot_index, start, end, cost, score))

        chosen = min(candidates, key=lambda candidate: candidate.score)
        slots[chosen.agent_id][chosen.slot_index] = chosen.end
        finish_times[task.id] = chosen.end
        unscheduled.remove(task.id)
        reasons = [
            f"{chosen.agent_id} satisfies: {', '.join(task.requires) if task.requires else 'no special capability'}.",
            f"Selected using the '{mission.objective.mode}' objective.",
        ]
        if task.depends_on:
            reasons.append(f"Waited for: {', '.join(task.depends_on)}.")
        assignments.append(
            Assignment(
                task_id=task.id,
                agent_id=chosen.agent_id,
                start_minute=chosen.start,
                end_minute=chosen.end,
                duration_minutes=task.duration_minutes,
                cost=chosen.cost,
                critical=task.id in critical_set,
                reasons=reasons,
            )
        )

    assignments.sort(key=lambda item: (item.start_minute, item.end_minute, item.task_id))
    makespan = max(item.end_minute for item in assignments) - base_start
    total_cost = round(sum(item.cost for item in assignments), 4)
    deadline = mission.objective.deadline_minutes
    deadline_met = None if deadline is None else makespan <= deadline
    grouped: dict[int, list[str]] = defaultdict(list)
    for assignment in assignments:
        grouped[assignment.start_minute].append(assignment.task_id)
    waves = [
        PlanWave(start_minute=start, task_ids=sorted(task_ids))
        for start, task_ids in sorted(grouped.items())
    ]
    warnings: list[str] = []
    if deadline_met is False:
        warnings.append(
            f"The best deterministic plan found misses the {deadline}-minute deadline by {makespan - deadline} minutes."
        )
    if makespan > critical_minutes:
        warnings.append(
            f"Resource contention adds {makespan - critical_minutes} minutes beyond the dependency-only critical path."
        )

    canonical = {
        "mission": mission.model_dump(mode="json"),
        "base_start": base_start,
        "assignments": [item.model_dump(mode="json") for item in assignments],
    }
    plan_hash = hashlib.sha256(
        json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    explanation = [
        f"Critical path: {' -> '.join(critical_path)} ({critical_minutes} minutes).",
        f"Makespan: {makespan} minutes across {len(mission.agents)} agents; total cost: ${total_cost:.2f}.",
        "Equal inputs always produce the same assignments and plan hash.",
    ]
    return PlanResponse(
        plan_hash=plan_hash,
        assignments=assignments,
        waves=waves,
        critical_path=critical_path,
        metrics=PlanMetrics(
            makespan_minutes=makespan,
            critical_path_minutes=critical_minutes,
            total_cost=total_cost,
            deadline_met=deadline_met,
            parallelism_peak=_peak_parallelism(assignments),
        ),
        explanation=explanation,
        warnings=warnings,
    )


def replan(request: ReplanRequest) -> ReplanResponse:
    original_tasks, _ = _validate_mission(request.mission)
    completed_ids = {item.task_id for item in request.completed}
    unknown_completed = sorted(completed_ids - original_tasks.keys())
    if unknown_completed:
        raise PlannerError(
            "unknown_completed_task",
            "Completed tasks must exist in the original mission.",
            {"task_ids": unknown_completed},
        )

    original_agents = {agent.id for agent in request.mission.agents}
    failed_ids = set(request.failed_agent_ids)
    unknown_failed = sorted(failed_ids - original_agents)
    if unknown_failed:
        raise PlannerError(
            "unknown_failed_agent",
            "Failed agents must exist in the original mission.",
            {"agent_ids": unknown_failed},
        )

    remaining_agents = [agent for agent in request.mission.agents if agent.id not in failed_ids]
    if not remaining_agents:
        raise PlannerError("no_agents_remaining", "Every agent was marked failed.")

    remaining_tasks = []
    for task in request.mission.tasks:
        if task.id in completed_ids:
            continue
        remaining_tasks.append(
            task.model_copy(
                update={
                    "depends_on": [
                        dependency
                        for dependency in task.depends_on
                        if dependency not in completed_ids
                    ]
                }
            )
        )
    if not remaining_tasks:
        raise PlannerError("nothing_to_replan", "All tasks are already complete.")

    revised_mission = request.mission.model_copy(
        update={"tasks": remaining_tasks, "agents": remaining_agents}
    )
    plan = create_plan(revised_mission, base_start=request.current_minute)
    changes = [
        f"Preserved {len(completed_ids)} completed task(s).",
        f"Removed {len(failed_ids)} failed agent(s): {', '.join(sorted(failed_ids)) or 'none'}.",
        f"Rescheduled {len(remaining_tasks)} task(s) from minute {request.current_minute}.",
    ]
    return ReplanResponse(
        replanned_from_minute=request.current_minute,
        completed_task_ids=sorted(completed_ids),
        removed_agent_ids=sorted(failed_ids),
        plan=plan,
        changes=changes,
    )
