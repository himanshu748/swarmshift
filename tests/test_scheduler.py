from __future__ import annotations

import pytest

from app.schemas import PlanRequest, ReplanRequest
from app.services.scheduler import PlannerError, create_plan, replan


def mission() -> PlanRequest:
    return PlanRequest.model_validate(
        {
            "tasks": [
                {"id": "research", "duration_minutes": 20, "requires": ["web"], "depends_on": []},
                {
                    "id": "build",
                    "duration_minutes": 35,
                    "requires": ["python"],
                    "depends_on": ["research"],
                },
                {
                    "id": "verify",
                    "duration_minutes": 15,
                    "requires": ["qa"],
                    "depends_on": ["build"],
                },
                {
                    "id": "docs",
                    "duration_minutes": 10,
                    "requires": ["writing"],
                    "depends_on": ["research"],
                },
            ],
            "agents": [
                {"id": "scout", "capabilities": ["web", "writing", "python"], "cost_per_hour": 0.5},
                {"id": "builder", "capabilities": ["python"], "cost_per_hour": 0.9},
                {"id": "reviewer", "capabilities": ["qa"], "cost_per_hour": 0.6},
            ],
            "objective": {"mode": "balanced", "cost_weight": 0.35, "deadline_minutes": 90},
        }
    )


def test_plan_is_deterministic_and_respects_dependencies() -> None:
    first = create_plan(mission())
    second = create_plan(mission())
    assert first.plan_hash == second.plan_hash
    assignments = {item.task_id: item for item in first.assignments}
    assert assignments["build"].start_minute >= assignments["research"].end_minute
    assert assignments["verify"].start_minute >= assignments["build"].end_minute
    assert first.metrics.deadline_met is True
    assert first.critical_path == ["research", "build", "verify"]


def test_parallel_tasks_start_after_shared_parent() -> None:
    result = create_plan(mission())
    assignments = {item.task_id: item for item in result.assignments}
    assert assignments["docs"].start_minute >= assignments["research"].end_minute
    assert result.metrics.parallelism_peak >= 2


def test_cycle_is_explained() -> None:
    payload = mission().model_dump()
    payload["tasks"][0]["depends_on"] = ["verify"]
    with pytest.raises(PlannerError) as exc:
        create_plan(PlanRequest.model_validate(payload))
    assert exc.value.code == "dependency_cycle"
    assert set(exc.value.details["cycle_task_ids"]) == {"build", "research", "verify"}


def test_missing_capability_is_explained() -> None:
    payload = mission().model_dump()
    payload["tasks"][0]["requires"] = ["quantum"]
    with pytest.raises(PlannerError) as exc:
        create_plan(PlanRequest.model_validate(payload))
    assert exc.value.code == "no_eligible_agent"
    assert exc.value.details["required_capabilities"] == ["quantum"]


def test_replan_preserves_completed_and_removes_failed_agent() -> None:
    result = replan(
        ReplanRequest.model_validate(
            {
                "mission": mission().model_dump(),
                "current_minute": 20,
                "completed": [{"task_id": "research", "agent_id": "scout", "ended_at_minute": 20}],
                "failed_agent_ids": ["builder"],
            }
        )
    )
    assert result.completed_task_ids == ["research"]
    assert result.removed_agent_ids == ["builder"]
    assert "research" not in {item.task_id for item in result.plan.assignments}
    assert "builder" not in {item.agent_id for item in result.plan.assignments}
    assert min(item.start_minute for item in result.plan.assignments) >= 20
