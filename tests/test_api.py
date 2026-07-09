from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def sample_payload() -> dict:
    return {
        "tasks": [
            {"id": "collect", "duration_minutes": 12, "requires": ["web"], "depends_on": []},
            {
                "id": "summarize",
                "duration_minutes": 8,
                "requires": ["writing"],
                "depends_on": ["collect"],
            },
        ],
        "agents": [{"id": "generalist", "capabilities": ["web", "writing"], "cost_per_hour": 1.0}],
        "objective": {"mode": "fastest", "deadline_minutes": 30},
    }


def test_health_and_skill_are_reachable() -> None:
    health = client.get("/health")
    assert health.status_code == 200
    assert health.json()["status"] == "ok"
    assert health.headers["x-content-type-options"] == "nosniff"

    skill = client.get("/skill.md")
    assert skill.status_code == 200
    assert "# SwarmShift" in skill.text
    assert "POST /v1/plan" in skill.text
    assert "curl -sS" in skill.text


def test_plan_contract() -> None:
    response = client.post("/v1/plan", json=sample_payload())
    assert response.status_code == 200
    body = response.json()
    assert body["metrics"]["makespan_minutes"] == 20
    assert body["metrics"]["deadline_met"] is True
    assert len(body["plan_hash"]) == 64


def test_validation_errors_have_stable_shape() -> None:
    payload = sample_payload()
    payload["tasks"][0]["duration_minutes"] = 0
    response = client.post("/v1/plan", json=payload)
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "invalid_request"


def test_home_contains_real_interactive_surface() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "Plan the swarm. Keep the deadline." in response.text
    assert "fetch('/v1/plan'" in response.text
