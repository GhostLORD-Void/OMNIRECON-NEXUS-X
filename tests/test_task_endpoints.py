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
    from omnirecon import api
    monkeypatch.setattr(api.settings, "model_base_url", "")
    monkeypatch.setattr(api.settings, "model_api_key", "")
    monkeypatch.setattr(api.settings, "model_name", "")
    response = client.post("/v1/chat", json={"prompt": "Explain a test"})
    assert response.status_code == 503
