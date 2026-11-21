from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

VALID_RISKS = ("read", "write", "destructive")


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
        if spec.risk not in VALID_RISKS:
            raise ValueError(f"Invalid risk tier: {spec.risk!r}")
        if spec.name in self._tools:
            raise ValueError(f"Duplicate tool name: {spec.name!r}")
        self._tools[spec.name] = spec

    def _record(
        self,
        ctx: RequestContext,
        name: str,
        risk: str,
        ok: bool,
        status: str,
        result: Any,
        error: str | None,
    ) -> dict[str, Any]:
        self.audit_log.append(
            {
                "request_id": ctx.request_id,
                "role": ctx.role,
                "tool": name,
                "risk": risk,
                "status": status,
            }
        )
        return {"ok": ok, "status": status, "result": result, "error": error}

    def execute(
        self,
        name: str,
        args: dict[str, Any],
        ctx: RequestContext,
        confirm_fn: Callable[[str, str, dict[str, Any], str], bool] | None = None,
    ) -> dict[str, Any]:
        """Execute a tool under strict permission, policy, and confirmation checks."""
        spec = self._tools.get(name)
        if spec is None:
            return self._record(
                ctx, name, "unknown", False, "unknown_tool", None, f"Unknown tool: {name}"
            )

        if name not in ctx.allowed_tools:
            return self._record(
                ctx,
                name,
                spec.risk,
                False,
                "denied_scope",
                None,
                f"Tool {name!r} is not allowed for role {ctx.role!r}",
            )

        for req_key in spec.required_args:
            if req_key not in args:
                return self._record(
                    ctx,
                    name,
                    spec.risk,
                    False,
                    "invalid_args",
                    None,
                    f"Missing required argument: {req_key}",
                )

        has_cap = spec.risk == "write" and spec.max_amount is not None
        if has_cap and "amount" in args:
            raw_amount = args["amount"]
            if (
                raw_amount is None
                or isinstance(raw_amount, bool)
                or not isinstance(raw_amount, (int, float))
            ):
                return self._record(
                    ctx,
                    name,
                    spec.risk,
                    False,
                    "invalid_args",
                    None,
                    "Argument 'amount' must be numeric",
                )

        allowed_keys = set(spec.required_args)
        if has_cap:
            allowed_keys.add("amount")
        filtered_args = {k: v for k, v in args.items() if k in allowed_keys}

        if has_cap and args.get("amount", 0) > spec.max_amount:
            return self._record(
                ctx,
                name,
                spec.risk,
                False,
                "denied_policy",
                None,
                f"Amount {args.get('amount', 0)} exceeds max_amount {spec.max_amount}",
            )

        if spec.risk == "destructive":
            if not ctx.confirmation_token or confirm_fn is None:
                return self._record(
                    ctx,
                    name,
                    spec.risk,
                    False,
                    "needs_confirmation",
                    None,
                    "Confirmation token and confirm_fn are required",
                )
            if not confirm_fn(ctx.request_id, name, filtered_args, ctx.confirmation_token):
                return self._record(
                    ctx,
                    name,
                    spec.risk,
                    False,
                    "denied_confirmation",
                    None,
                    "Confirmation rejected",
                )

        try:
            result = spec.fn(**filtered_args)
        except Exception as exc:
            return self._record(ctx, name, spec.risk, False, "tool_error", None, str(exc))

        return self._record(ctx, name, spec.risk, True, "ok", result, None)
