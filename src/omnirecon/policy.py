"""Central permission checks for future tool adapters."""
from dataclasses import dataclass

@dataclass(frozen=True)
class ToolPolicy:
    name: str
    description: str
    requires_authorization: bool = True
    enabled_by_default: bool = False

POLICIES = (
    ToolPolicy("web_research", "Retrieve public web information"),
    ToolPolicy("repository_read", "Read an explicitly selected repository"),
    ToolPolicy("repository_write", "Modify an explicitly selected repository"),
    ToolPolicy("defensive_scan", "Assess explicitly authorized assets"),
)

def require_tool_permission(tool_name: str, *, authorized: bool, enabled: bool) -> None:
    policy = next((item for item in POLICIES if item.name == tool_name), None)
    if policy is None:
        raise ValueError(f"Unknown tool: {tool_name}")
    if not enabled:
        raise PermissionError(f"Tool '{tool_name}' is disabled")
    if policy.requires_authorization and not authorized:
        raise PermissionError(f"Tool '{tool_name}' requires explicit authorization")
