"""FastAPI application entry point."""

from fastapi import FastAPI

from omnirecon import __version__
from omnirecon.agents import list_agents
from omnirecon.config import settings
from omnirecon.orchestrator import plan_task
from omnirecon.schemas import HealthResponse, TaskPlanRequest, TaskPlanResponse

app = FastAPI(
    title=settings.app_name,
    version=__version__,
    description="A modular multi-agent platform with explicit authorization boundaries.",
)


@app.get("/health", response_model=HealthResponse, tags=["system"])
def health() -> HealthResponse:
    return HealthResponse(status="ok", service=settings.app_name, version=__version__)


@app.get(f"{settings.api_prefix}/agents", tags=["agents"])
def agents():
    return {"agents": list_agents()}


@app.post(
    f"{settings.api_prefix}/tasks/plan",
    response_model=TaskPlanResponse,
    tags=["tasks"],
)
def create_task_plan(request: TaskPlanRequest) -> TaskPlanResponse:
    return plan_task(request)
