from collections.abc import Callable
from dataclasses import dataclass
from typing import Any


@dataclass
class ToolSpec:
    """Metadata and callable for a registered agent tool."""

    name: str
    fn: Callable[..., Any]
    required_args: tuple[str, ...]
    risk: str
    max_amount: float | None = None


@dataclass
class RequestContext:
    """Per-request authorization scope and optional confirmation token."""

    request_id: str
    role: str
    allowed_tools: frozenset[str] | set[str]
    confirmation_token: str | None = None


class ScopedRegistry:
    """Tool registry enforcing allowlists, arg filtering, policy caps, and audit logs."""

    def __init__(self) -> None:
        self._tools: dict[str, ToolSpec] = {}
        self.audit_log: list[dict[str, str]] = []

    def register(self, spec: ToolSpec) -> None:
        """Register a ToolSpec, raising ValueError on duplicate name or invalid risk."""
        # TODO: validate spec.risk in ("read", "write", "destructive") and unique spec.name.
        pass

    def execute(
        self,
        name: str,
        args: dict[str, Any],
        ctx: RequestContext,
        confirm_fn: Callable[[str, str, dict[str, Any], str], bool] | None = None,
    ) -> dict[str, Any]:
        """Execute a tool under strict permission, policy, and confirmation checks."""
        # TODO: implement strict status priority:
        # unknown_tool -> denied_scope -> invalid_args -> denied_policy
        # -> needs_confirmation -> denied_confirmation -> ok / tool_error
        # Always append an audit_log entry.
        pass
