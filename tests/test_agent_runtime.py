import pytest

from omnirecon.agent_runtime import AgentRunRequest, run_agent_team
from omnirecon.providers import ProviderResult


@pytest.mark.asyncio
async def test_agent_team_delegates_and_synthesizes(monkeypatch):
    from omnirecon import agent_runtime

    calls = []

    async def fake_complete(self, prompt):
        calls.append(prompt)
        return ProviderResult(provider="mock", model="test-model", text=f"result-{len(calls)}")

    monkeypatch.setattr(agent_runtime.HybridModelRouter, "complete", fake_complete)
    result = await run_agent_team(AgentRunRequest(objective="Prepare a software delivery plan"))
    assert result.status == "completed"
    assert set(result.agent_outputs) == {"coordinator", "research", "engineering"}
    assert len(calls) == 4
    assert result.provider_trace[-1] == "synthesis:mock/test-model"
    assert "No shell commands" in result.execution_boundary


@pytest.mark.asyncio
async def test_defense_agent_only_added_for_security_objective(monkeypatch):
    from omnirecon import agent_runtime

    async def fake_complete(self, prompt):
        return ProviderResult(provider="mock", model="test", text="ok")

    monkeypatch.setattr(agent_runtime.HybridModelRouter, "complete", fake_complete)
    result = await run_agent_team(AgentRunRequest(objective="Review security posture"))
    assert "defense" in result.agent_outputs
