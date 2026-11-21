# Enforce per-request tool allowlists, write caps, and confirmation gates.
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ToolSpec:
    name: str
    fn: Callable[..., Any]
    required_args: tuple[str, ...]
    risk: str  # "read" | "write" | "destructive"
    max_amount: float | None = None


@dataclass(frozen=True)
class RequestContext:
    request_id: str
    role: str
    allowed_tools: frozenset[str]
    confirmation_token: str | None = None


@dataclass
class ScopedRegistry:
    specs: dict[str, ToolSpec] = field(default_factory=dict)
    audit_log: list[dict[str, Any]] = field(default_factory=list)

    def register(self, spec: ToolSpec) -> None:
        self.specs[spec.name] = spec

    def execute(
        self,
        name: str,
        args: dict[str, Any],
        ctx: RequestContext,
        confirm_fn: Callable[[str, str, dict[str, Any], str], bool] | None = None,
    ) -> dict[str, Any]:
        spec = self.specs.get(name)
        if spec is None:
            status, result = "unknown_tool", None
        elif name not in ctx.allowed_tools:
            status, result = "denied_scope", None
        elif any(k not in args for k in spec.required_args):
            status, result = "invalid_args", None
        elif spec.risk == "write" and spec.max_amount is not None and args.get("amount", 0) > spec.max_amount:
            status, result = "denied_policy", None
        elif spec.risk == "destructive" and (not ctx.confirmation_token or confirm_fn is None):
            status, result = "needs_confirmation", None
        elif spec.risk == "destructive" and not confirm_fn(ctx.request_id, name, args, ctx.confirmation_token or ""):
            status, result = "denied_confirmation", None
        else:
            status, result = "ok", spec.fn(**args)

        self.audit_log.append({
            "request_id": ctx.request_id,
            "role": ctx.role,
            "tool": name,
            "risk": spec.risk if spec else "unknown",
            "status": status,
        })
        return {"ok": status == "ok", "status": status, "result": result}


registry = ScopedRegistry()
registry.register(ToolSpec("lookup_order", lambda order_id: {"order_id": order_id, "total": 42.0}, ("order_id",), "read"))
registry.register(ToolSpec("issue_refund", lambda order_id, amount: {"refunded": amount, "order_id": order_id}, ("order_id", "amount"), "write", max_amount=50.0))
registry.register(ToolSpec("delete_account", lambda account_id: {"deleted": account_id}, ("account_id",), "destructive"))

support_ctx = RequestContext("req-1", "support", frozenset({"lookup_order", "issue_refund"}))
admin_ctx = RequestContext("req-2", "admin", frozenset({"lookup_order", "delete_account"}), confirmation_token="tok-99")

print("1. read ok       :", registry.execute("lookup_order", {"order_id": "ORD-7"}, support_ctx))
print("2. write over cap:", registry.execute("issue_refund", {"order_id": "ORD-7", "amount": 200.0}, support_ctx))
print("3. out of scope  :", registry.execute("delete_account", {"account_id": "ACC-1"}, support_ctx))
print("4. admin confirm :", registry.execute("delete_account", {"account_id": "ACC-1"}, admin_ctx, lambda r, n, a, t: t == "tok-99"))
print("Audit entries    :", len(registry.audit_log), [e["status"] for e in registry.audit_log])
