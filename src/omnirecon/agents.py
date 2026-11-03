"""Agent catalogue. Agents describe capabilities; integrations are added separately."""

from omnirecon.schemas import AgentDescriptor


AGENTS: tuple[AgentDescriptor, ...] = (
    AgentDescriptor(
        name="coordinator",
        description="Breaks objectives into reviewable steps and routes work.",
        capabilities=["task_decomposition", "routing", "status_reporting"],
    ),
    AgentDescriptor(
        name="research",
        description="Structures research questions and evidence requirements.",
        capabilities=["research_planning", "source_quality", "summarization"],
    ),
    AgentDescriptor(
        name="engineering",
        description="Supports code review, design analysis, and test planning.",
        capabilities=["code_review_planning", "architecture", "testing"],
    ),
    AgentDescriptor(
        name="defense",
        description="Plans authorized defensive security assessments.",
        capabilities=["asset_inventory_planning", "risk_review", "remediation"],
    ),
    AgentDescriptor(
        name="analytics",
        description="Defines data analysis workflows and reporting.",
        capabilities=["data_quality", "metrics", "reporting"],
    ),
)


def list_agents() -> list[AgentDescriptor]:
    """Return a copy of the public agent catalogue."""
    return list(AGENTS)
