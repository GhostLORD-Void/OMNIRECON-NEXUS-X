import pytest
from omnirecon.policy import require_tool_permission

def test_tool_requires_enablement():
    with pytest.raises(PermissionError):
        require_tool_permission("repository_read", authorized=True, enabled=False)

def test_tool_requires_authorization():
    with pytest.raises(PermissionError):
        require_tool_permission("defensive_scan", authorized=False, enabled=True)

def test_unknown_tool_rejected():
    with pytest.raises(ValueError):
        require_tool_permission("arbitrary_shell", authorized=True, enabled=True)
