"""Conservative task planner; it does not execute external actions."""

from omnirecon.schemas import PlannedStep, TaskPlanRequest, TaskPlanResponse


def plan_task(request: TaskPlanRequest) -> TaskPlanResponse:
    objective = request.objective.strip()
    steps = [
        PlannedStep(
            agent="coordinator",
            action="Clarify scope, constraints, and desired deliverable",
            rationale="Establish a bounded task before delegating work.",
        ),
        PlannedStep(
            agent="research",
            action="Identify evidence and information requirements",
            rationale="Separate verified facts from assumptions.",
        ),
        PlannedStep(
            agent="engineering",
            action="Assess implementation or validation needs",
            rationale="Turn findings into testable work items.",
        ),
    ]

    if any(word in objective.lower() for word in ("security", "vulnerability", "threat", "osint")):
        steps.append(
            PlannedStep(
                agent="defense",
                action="Define an authorized, asset-scoped defensive review",
                rationale="Security work must have explicit permission and scope.",
            )
        )

    note = (
        "Plan only. No network requests, scans, code execution, or external tool calls were made. "
        "Execution adapters require separate configuration and permission checks."
    )
    if not request.authorized:
        note += " Authorization was not confirmed; any future execution must remain disabled."

    return TaskPlanResponse(
        objective=objective,
        authorized=request.authorized,
        steps=steps,
        execution_note=note,
    )
