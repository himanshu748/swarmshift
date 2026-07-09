# SwarmShift

SwarmShift is a deterministic scheduling service for AI-agent teams. Give it tasks, dependencies, capabilities, hourly costs, and an objective; it returns an executable schedule with assignments, waves, critical path, cost, deadline status, explanations, and a stable SHA-256 plan hash. If an agent fails, SwarmShift preserves completed work and replans only what remains.

It is designed for agents to use directly from [`SKILL.md`](./SKILL.md): no account, API key, model, database, or paid dependency is required.

## Why it exists

Multi-agent systems are good at splitting work but bad at answering three operational questions consistently:

1. Which capable agent should own each task?
2. What can safely run in parallel without violating dependencies?
3. What changes when an agent fails halfway through?

SwarmShift makes those decisions explicit and replayable. Identical JSON produces identical assignments and the same `plan_hash`, which makes a plan easy to audit or attach to a run record.

## API

- `POST /v1/plan` — create a deterministic schedule.
- `POST /v1/replan` — remove failed agents, preserve completed tasks, and reschedule the remainder.
- `GET /health` — liveness check.
- `GET /skill.md` — complete agent instructions with live-host examples.
- `GET /docs` — interactive OpenAPI documentation.

### Plan a mission

```bash
curl -sS -X POST http://127.0.0.1:8000/v1/plan \
  -H 'Content-Type: application/json' \
  --data @examples/mission.json | python -m json.tool
```

## Scheduling model

SwarmShift validates the dependency graph, rejects cycles and missing capabilities, calculates the dependency-only critical path, ranks ready tasks by downstream criticality and priority, and then assigns each task to the best eligible agent slot.

The objective changes candidate ranking:

- `fastest`: earliest completion, then lower cost.
- `cheapest`: lower task cost, then earlier completion.
- `balanced`: earlier completion plus a configurable cost penalty.

A declared deadline adds a deterministic penalty to assignments that miss it. The response distinguishes dependency critical-path length from total makespan, so resource contention is visible instead of hidden.

This is an explainable list scheduler, not an exponential exact optimizer. That tradeoff keeps latency predictable for up to 100 tasks and 50 agents.

## Run locally

```bash
uv sync
uv run uvicorn app.main:app --reload
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Verify

```bash
uv run ruff check .
uv run ruff format --check .
uv run pytest --cov=app --cov-report=term-missing
```

## Deploy to Vercel

```bash
vercel deploy --prod
```

The FastAPI application is exported from `api/index.py`; `vercel.json` routes the public surface to that function.

## Architecture

```text
Agent / demo UI
      │ JSON
      ▼
FastAPI contract ── validation + stable error shape
      │
      ▼
Deterministic scheduler ── DAG validation, critical path,
      │                    capability matching, list scheduling
      ▼
Plan + waves + metrics + explanations + SHA-256 hash
```

## Privacy and safety

- The service is stateless and does not persist request bodies.
- It performs no outbound calls.
- It executes no submitted code or shell command.
- IDs and capabilities are treated as labels, not instructions.
- Request size and collection lengths are bounded by the Pydantic contract.

## License

Apache-2.0. See [LICENSE](./LICENSE).

