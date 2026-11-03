"""Typed API contracts."""

from datetime import datetime, timezone
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: Literal["ok"]
    service: str
    version: str


class AgentDescriptor(BaseModel):
    name: str
    description: str
    capabilities: list[str]
    enabled: bool = True


class TaskPlanRequest(BaseModel):
    objective: str = Field(min_length=8, max_length=2000)
    authorized: bool = Field(
        default=False,
        description="Explicitly confirm you are authorized to perform the requested work.",
    )


class PlannedStep(BaseModel):
    agent: str
    action: str
    rationale: str


class TaskPlanResponse(BaseModel):
    task_id: UUID = Field(default_factory=uuid4)
    objective: str
    status: Literal["planned"] = "planned"
    authorized: bool
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    steps: list[PlannedStep]
    execution_note: str
