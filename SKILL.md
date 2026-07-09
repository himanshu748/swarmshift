# SwarmShift

SwarmShift assigns dependent tasks across capable AI agents to minimize completion time and cost, then deterministically replans when an agent fails.

Base URL: https://swarmshift.vercel.app

The live service serves its authoritative, host-correct instructions at `/skill.md`. See that file for every endpoint, a real curl call and response, and numbered agent steps.

- `POST /v1/plan` — create a deterministic execution plan.
- `POST /v1/replan` — preserve completed work and replan around failed agents.
- `GET /health` — check liveness.

No authentication or API key is required.

