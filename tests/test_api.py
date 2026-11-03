from fastapi.testclient import TestClient

from omnirecon.api import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_agent_catalogue() -> None:
    response = client.get("/v1/agents")
    assert response.status_code == 200
    names = {agent["name"] for agent in response.json()["agents"]}
    assert {"coordinator", "research", "engineering", "defense"} <= names


def test_plan_requires_authorization_field_but_defaults_safe() -> None:
    response = client.post(
        "/v1/tasks/plan",
        json={"objective": "Review application security posture"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["authorized"] is False
    assert payload["status"] == "planned"
    assert "No network requests" in payload["execution_note"]


def test_short_objective_rejected() -> None:
    response = client.post("/v1/tasks/plan", json={"objective": "short"})
    assert response.status_code == 422
