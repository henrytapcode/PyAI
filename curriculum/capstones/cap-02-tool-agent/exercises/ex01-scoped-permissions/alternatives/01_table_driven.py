from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

RISK_TIERS = frozenset({"read", "write", "destructive"})


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


def _is_numeric(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _filter_args(spec: ToolSpec, args: dict[str, Any]) -> dict[str, Any]:
    permitted = set(spec.required_args)
    if spec.risk == "write" and spec.max_amount is not None:
        permitted.add("amount")
    return {key: val for key, val in args.items() if key in permitted}


def _check_scope(
    spec: ToolSpec,
    args: dict[str, Any],
    ctx: RequestContext,
    filtered: dict[str, Any],
    confirm_fn: Callable[[str, str, dict[str, Any], str], bool] | None,
) -> tuple[str, str] | None:
    if spec.name not in ctx.allowed_tools:
        return ("denied_scope", f"Tool {spec.name!r} not in allowed_tools")
    return None


def _check_args(
    spec: ToolSpec,
    args: dict[str, Any],
    ctx: RequestContext,
    filtered: dict[str, Any],
    confirm_fn: Callable[[str, str, dict[str, Any], str], bool] | None,
) -> tuple[str, str] | None:
    for key in spec.required_args:
        if key not in args:
            return ("invalid_args", f"Missing required arg: {key}")
    if spec.risk == "write" and spec.max_amount is not None and "amount" in args:
        if not _is_numeric(args["amount"]):
            return ("invalid_args", "Amount must be numeric")
    return None


def _check_policy(
    spec: ToolSpec,
    args: dict[str, Any],
    ctx: RequestContext,
    filtered: dict[str, Any],
    confirm_fn: Callable[[str, str, dict[str, Any], str], bool] | None,
) -> tuple[str, str] | None:
    if spec.risk == "write" and spec.max_amount is not None:
        if args.get("amount", 0) > spec.max_amount:
            return ("denied_policy", "Amount exceeds max_amount")
    return None


def _check_confirmation(
    spec: ToolSpec,
    args: dict[str, Any],
    ctx: RequestContext,
    filtered: dict[str, Any],
    confirm_fn: Callable[[str, str, dict[str, Any], str], bool] | None,
) -> tuple[str, str] | None:
    if spec.risk != "destructive":
        return None
    if not ctx.confirmation_token or confirm_fn is None:
        return ("needs_confirmation", "Missing confirmation token or confirm_fn")
    if not confirm_fn(ctx.request_id, spec.name, filtered, ctx.confirmation_token):
        return ("denied_confirmation", "Confirmation callback returned False")
    return None


_GUARD_PIPELINE = (
    _check_scope,
    _check_args,
    _check_policy,
    _check_confirmation,
)


class ScopedRegistry:
    """Table-driven guard pipeline for tool permissions and audit logging."""

    def __init__(self) -> None:
        self._tools: dict[str, ToolSpec] = {}
        self.audit_log: list[dict[str, str]] = []

    def register(self, spec: ToolSpec) -> None:
        """Register a ToolSpec, raising ValueError on duplicate name or invalid risk."""
        if spec.risk not in RISK_TIERS:
            raise ValueError(f"Unsupported risk: {spec.risk!r}")
        if spec.name in self._tools:
            raise ValueError(f"Tool already registered: {spec.name!r}")
        self._tools[spec.name] = spec

    def execute(
        self,
        name: str,
        args: dict[str, Any],
        ctx: RequestContext,
        confirm_fn: Callable[[str, str, dict[str, Any], str], bool] | None = None,
    ) -> dict[str, Any]:
        """Run ordered guard checks, dispatch tool, and append an audit entry."""
        spec = self._tools.get(name)
        risk = spec.risk if spec is not None else "unknown"
        ok = False
        result: Any = None
        error: str | None = None
        status = "unknown_tool"

        if spec is None:
            error = f"Unknown tool: {name}"
        else:
            filtered = _filter_args(spec, args)
            denial = None
            for guard in _GUARD_PIPELINE:
                denial = guard(spec, args, ctx, filtered, confirm_fn)
                if denial is not None:
                    break

            if denial is not None:
                status, error = denial
            else:
                try:
                    result = spec.fn(**filtered)
                    ok = True
                    status = "ok"
                except Exception as exc:
                    status = "tool_error"
                    error = str(exc)

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
