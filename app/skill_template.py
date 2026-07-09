from __future__ import annotations


def render_skill(base_url: str) -> str:
    base = base_url.rstrip("/")
    return f"""# SwarmShift

SwarmShift assigns dependent tasks across capable AI agents to minimize completion time and cost, then deterministically replans when an agent fails.

Base URL: {base}

No authentication or API key is required. Send and receive JSON.

## POST /v1/plan

Create a deterministic execution plan from tasks, dependencies, agent capabilities, hourly costs, and an optimization objective.

Example call:

```bash
curl -sS -X POST {base}/v1/plan \\
  -H 'Content-Type: application/json' \\
  -d '{{
    "tasks": [
      {{"id":"research","duration_minutes":20,"requires":["web"],"depends_on":[],"priority":5}},
      {{"id":"build","duration_minutes":35,"requires":["python"],"depends_on":["research"],"priority":5}},
      {{"id":"verify","duration_minutes":15,"requires":["qa"],"depends_on":["build"],"priority":4}}
    ],
    "agents": [
      {{"id":"scout","capabilities":["web"],"cost_per_hour":0.50}},
      {{"id":"builder","capabilities":["python"],"cost_per_hour":0.90}},
      {{"id":"reviewer","capabilities":["qa"],"cost_per_hour":0.60}}
    ],
    "objective": {{"mode":"balanced","cost_weight":0.35,"deadline_minutes":90}}
  }}'
```

Example response:

```json
{{
  "plan_hash": "a stable SHA-256 hash",
  "assignments": [
    {{"task_id":"research","agent_id":"scout","start_minute":0,"end_minute":20,"duration_minutes":20,"cost":0.1667,"critical":true,"reasons":["scout satisfies: web.","Selected using the 'balanced' objective."]}}
  ],
  "waves": [{{"start_minute":0,"task_ids":["research"]}}],
  "critical_path": ["research","build","verify"],
  "metrics": {{"makespan_minutes":70,"critical_path_minutes":70,"total_cost":0.8417,"deadline_met":true,"parallelism_peak":1}},
  "explanation": ["Critical path: research -> build -> verify (70 minutes)."],
  "warnings": []
}}
```

## POST /v1/replan

Preserve completed work, remove failed agents, and reschedule the remaining task graph from the current minute.

Example call:

```bash
curl -sS -X POST {base}/v1/replan \\
  -H 'Content-Type: application/json' \\
  -d '{{
    "mission": {{
      "tasks": [
        {{"id":"research","duration_minutes":20,"requires":["web"],"depends_on":[]}},
        {{"id":"build","duration_minutes":35,"requires":["python"],"depends_on":["research"]}},
        {{"id":"verify","duration_minutes":15,"requires":["qa"],"depends_on":["build"]}}
      ],
      "agents": [
        {{"id":"scout","capabilities":["web","python"],"cost_per_hour":0.50}},
        {{"id":"builder","capabilities":["python"],"cost_per_hour":0.90}},
        {{"id":"reviewer","capabilities":["qa"],"cost_per_hour":0.60}}
      ],
      "objective": {{"mode":"fastest"}}
    }},
    "current_minute": 20,
    "completed": [{{"task_id":"research","agent_id":"scout","ended_at_minute":20}}],
    "failed_agent_ids": ["builder"]
  }}'
```

Example response:

```json
{{
  "replanned_from_minute": 20,
  "completed_task_ids": ["research"],
  "removed_agent_ids": ["builder"],
  "plan": {{"plan_hash":"a new stable SHA-256 hash","assignments":[],"waves":[],"critical_path":["build","verify"],"metrics":{{"makespan_minutes":50,"critical_path_minutes":50,"total_cost":0.4417,"deadline_met":null,"parallelism_peak":1}},"explanation":[],"warnings":[]}},
  "changes": ["Preserved 1 completed task(s).","Removed 1 failed agent(s): builder.","Rescheduled 2 task(s) from minute 20."]
}}
```

## GET /health

Check service liveness.

Example call:

```bash
curl -sS {base}/health
```

Example response:

```json
{{"status":"ok","service":"swarmshift","version":"0.1.0"}}
```

## How an agent should use SwarmShift

1. Convert the goal into tasks. Give every task a unique `id`, an estimated `duration_minutes`, required capabilities, and direct prerequisite IDs in `depends_on`.
2. List available agents with unique IDs, capabilities, hourly costs, and optional `max_parallel` capacity.
3. Choose `fastest`, `cheapest`, or `balanced`. Use `balanced` unless the user clearly prioritizes speed or price.
4. Call `POST /v1/plan`. If the service returns an error, fix the named dependency, cycle, duplicate ID, or missing capability and call it again.
5. Execute assignments in `waves`. A task may start at its `start_minute` only after its listed dependencies are complete.
6. Save the `plan_hash` with the execution record. Identical inputs return the same hash.
7. If an agent fails, call `POST /v1/replan` with the original mission, completed tasks, failed agent IDs, and current minute. Continue with the returned plan; do not redo completed tasks.
"""
