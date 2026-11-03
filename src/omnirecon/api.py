"""FastAPI application entry point."""
from uuid import UUID

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from omnirecon import __version__
from omnirecon.agents import list_agents
from omnirecon.agent_runtime import AgentRunRequest, AgentRunResponse, run_agent_team
from omnirecon.config import settings
from omnirecon.dashboard import DASHBOARD_HTML
from omnirecon.orchestrator import plan_task
from omnirecon.providers import HybridModelRouter, ProviderNotConfigured
from omnirecon.schemas import HealthResponse, TaskPlanRequest, TaskPlanResponse
from omnirecon.storage import TaskStore

app = FastAPI(title=settings.app_name, version=__version__,
              description="A modular multi-agent platform with explicit authorization boundaries.")
store = TaskStore(settings.database_path)


class ChatRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=12000)


class ChatResponse(BaseModel):
    provider: str
    model: str
    response: str


@app.get("/health", response_model=HealthResponse, tags=["system"])
def health() -> HealthResponse:
    return HealthResponse(status="ok", service=settings.app_name, version=__version__)


@app.get("/dashboard", response_class=HTMLResponse, tags=["dashboard"])
def dashboard() -> str:
    return DASHBOARD_HTML


@app.get(f"{settings.api_prefix}/agents", tags=["agents"])
def agents():
    return {"agents": list_agents()}


@app.get(f"{settings.api_prefix}/providers", tags=["AI"])
def providers():
    router = HybridModelRouter()
    configured = router.configured()
    return {"strategy": "ordered-fallback", "configured": [
        {"provider": name, "model": model} for name, model in configured
    ], "secrets_exposed": False}


@app.post(f"{settings.api_prefix}/agents/run", response_model=AgentRunResponse, tags=["agents"])
async def run_agents(request: AgentRunRequest) -> AgentRunResponse:
    try:
        return await run_agent_team(request)
    except ProviderNotConfigured as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail="Agent execution failed; check provider configuration and logs") from exc


@app.post(f"{settings.api_prefix}/tasks/plan", response_model=TaskPlanResponse, tags=["tasks"])
def create_task_plan(request: TaskPlanRequest) -> TaskPlanResponse:
    task = plan_task(request)
    store.save(task)
    return task


@app.get(f"{settings.api_prefix}/tasks", response_model=list[TaskPlanResponse], tags=["tasks"])
def list_tasks(limit: int = Query(default=20, ge=1, le=100)) -> list[TaskPlanResponse]:
    return store.list(limit)


@app.get(f"{settings.api_prefix}/tasks/{{task_id}}", response_model=TaskPlanResponse, tags=["tasks"])
def get_task(task_id: UUID) -> TaskPlanResponse:
    task = store.get(str(task_id))
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.post(f"{settings.api_prefix}/chat", response_model=ChatResponse, tags=["AI"])
async def chat(request: ChatRequest) -> ChatResponse:
    try:
        result = await HybridModelRouter().complete(request.prompt)
    except ProviderNotConfigured as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail="All configured model providers failed") from exc
    return ChatResponse(provider=result.provider, model=result.model, response=result.text)
