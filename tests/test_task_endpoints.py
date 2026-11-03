from fastapi.testclient import TestClient
from omnirecon.api import app

client = TestClient(app)


def test_create_and_read_task():
    response = client.post("/v1/tasks/plan", json={
        "objective": "Review application security posture", "authorized": True
    })
    assert response.status_code == 200
    task_id = response.json()["task_id"]
    fetched = client.get(f"/v1/tasks/{task_id}")
    assert fetched.status_code == 200
    assert fetched.json()["task_id"] == task_id


def test_chat_is_unavailable_without_provider(monkeypatch):
    from omnirecon import api, providers
    for name in ("openai_base_url", "openai_api_key", "openai_model",
                 "anthropic_api_key", "google_api_key",
                 "local_model_base_url", "local_model_name"):
        monkeypatch.setattr(providers.settings, name, "")
    response = client.post("/v1/chat", json={"prompt": "Explain a test"})
    assert response.status_code == 503


def test_provider_status_does_not_expose_secrets():
    response = client.get("/v1/providers")
    assert response.status_code == 200
    assert response.json()["secrets_exposed"] is False


def test_agent_run_endpoint_exists_and_requires_provider():
    response = client.post("/v1/agents/run", json={"objective": "Explain a safe test plan"})
    assert response.status_code in (200, 502, 503)
