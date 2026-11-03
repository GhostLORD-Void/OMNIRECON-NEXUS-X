"""Sequential multi-agent reasoning runtime. It never invokes external tools."""
from pydantic import BaseModel, Field

from omnirecon.providers import HybridModelRouter


class AgentRunRequest(BaseModel):
    objective: str = Field(min_length=8, max_length=4000)
    context: str = Field(default="", max_length=12000)
    authorized: bool = False


class AgentRunResponse(BaseModel):
    status: str
    objective: str
    provider_trace: list[str]
    agent_outputs: dict[str, str]
    final_synthesis: str
    execution_boundary: str


AGENT_PROMPTS = {
    "coordinator": "You are the coordinator. Decompose the objective into clear subproblems, constraints and acceptance criteria.",
    "research": "You are the research analyst. Identify evidence needed, distinguish facts from assumptions, and state uncertainty. Do not invent citations.",
    "engineering": "You are the engineering specialist. Produce a practical technical approach, risks and verifiable tests.",
    "defense": "You are a defensive security specialist. Only reason about explicitly authorized assets. Do not provide instructions for unauthorized access, persistence, evasion or destructive actions.",
}


async def run_agent_team(request: AgentRunRequest) -> AgentRunResponse:
    router = HybridModelRouter()
    outputs: dict[str, str] = {}
    trace: list[str] = []
    context = request.context.strip()
    for agent, role in AGENT_PROMPTS.items():
        if agent == "defense" and not any(
            word in request.objective.lower()
            for word in ("security", "vulnerability", "threat", "osint", "defensive")
        ):
            continue
        prompt = (
            f"{role}\n\nOBJECTIVE:\n{request.objective}\n\n"
            f"USER CONTEXT:\n{context or '(none)'}\n\n"
            f"PREVIOUS AGENT NOTES:\n{outputs or '(none)'}\n\n"
            "Return concise, structured analysis. Clearly label assumptions and unknowns."
        )
        result = await router.complete(prompt)
        outputs[agent] = result.text
        trace.append(f"{agent}:{result.provider}/{result.model}")
    synthesis_prompt = (
        "You are the lead analyst. Synthesize the specialist notes into a coherent answer. "
        "Separate verified inputs, assumptions, recommendations, and next steps.\n"
        f"OBJECTIVE: {request.objective}\nNOTES: {outputs}"
    )
    final = await router.complete(synthesis_prompt)
    trace.append(f"synthesis:{final.provider}/{final.model}")
    return AgentRunResponse(
        status="completed",
        objective=request.objective,
        provider_trace=trace,
        agent_outputs=outputs,
        final_synthesis=final.text,
        execution_boundary=(
            "Reasoning only. No shell commands, network scans, file modifications, or external tools "
            "were executed. Authorization flag is informational and does not enable tool execution."
        ),
    )
