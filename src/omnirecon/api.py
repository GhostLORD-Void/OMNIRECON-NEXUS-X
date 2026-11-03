"""FastAPI application entry point."""
from uuid import UUID

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from omnirecon import __version__
from omnirecon.agents import list_agents
from omnirecon.config import settings
from omnirecon.dashboard import DASHBOARD_HTML
from omnirecon.orchestrator import plan_task
from omnirecon.providers import OpenAICompatibleProvider, ProviderNotConfigured
from omnirecon.schemas import HealthResponse, TaskPlanRequest, TaskPlanResponse
from omnirecon.storage import TaskStore

app = FastAPI(
    title=settings.app_name,
    version=__version__,
    description="A modular multi-agent platform with explicit authorization boundaries.",
)
store = TaskStore(settings.database_path)


class ChatRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=12000)


class ChatResponse(BaseModel):
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
        provider = OpenAICompatibleProvider(
            base_url=settings.model_base_url,
            api_key=settings.model_api_key,
            model=settings.model_name,
            timeout=settings.model_timeout_seconds,
        )
    except (ProviderNotConfigured, ValueError) as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    try:
        answer = await provider.complete(request.prompt)
    except Exception as exc:
        raise HTTPException(status_code=502, detail="Configured model provider request failed") from exc
    return ChatResponse(model=settings.model_name, response=answer)
