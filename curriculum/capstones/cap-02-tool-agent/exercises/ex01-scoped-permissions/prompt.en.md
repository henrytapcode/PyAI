Implement `ToolSpec`, `RequestContext`, and `ScopedRegistry` in `starter.py` to enforce per-request tool allowlists, argument validation and filtering, `write` amount caps, `destructive` confirmation gates, error containment, and complete audit logging.

**Example**

```python
reg = ScopedRegistry()
reg.register(ToolSpec("lookup_order", lambda order_id: {"id": order_id}, ("order_id",), "read"))
reg.register(ToolSpec("issue_refund", lambda order_id, amount=0: amount, ("order_id",), "write", max_amount=50.0))

ctx = RequestContext("req-1", "support", frozenset({"lookup_order", "issue_refund"}))

reg.execute("lookup_order", {"order_id": "A1", "extra": 99}, ctx)
# -> {"ok": True, "status": "ok", "result": {"id": "A1"}, "error": None}

reg.execute("issue_refund", {"order_id": "A1", "amount": 120.0}, ctx)
# -> {"ok": False, "status": "denied_policy", "result": None, "error": "..."}
```

**Rules**

- **`ToolSpec`**: dataclass with fields `(name: str, fn: Callable, required_args: tuple[str, ...], risk: str, max_amount: float | None = None)`.
- **`RequestContext`**: dataclass with fields `(request_id: str, role: str, allowed_tools: frozenset[str] | set[str], confirmation_token: str | None = None)`.
- **`ScopedRegistry.register(spec)`**: raises `ValueError` if `spec.risk` is not in `("read", "write", "destructive")` or if `spec.name` is already registered.
- **`ScopedRegistry.execute(name, args, ctx, confirm_fn=None)`**: returns `{"ok": bool, "status": str, "result": Any, "error": str | None}` and evaluates checks in strict priority order:
  1. `"unknown_tool"`: `name` is not registered. Record `"risk": "unknown"` in `audit_log`.
  2. `"denied_scope"`: `name` is not in `ctx.allowed_tools`.
  3. `"invalid_args"`: any key in `spec.required_args` is missing from `args`; OR `spec.risk == "write"` and `spec.max_amount is not None` and `"amount"` is in `args` with a value that is `None`, `bool`, or not `int`/`float`.
  4. `"denied_policy"`: `spec.risk == "write"` and `spec.max_amount is not None` and `args.get("amount", 0) > spec.max_amount`.
  5. `"needs_confirmation"`: `spec.risk == "destructive"` and (`not ctx.confirmation_token` or `confirm_fn is None`).
  6. `"denied_confirmation"`: `spec.risk == "destructive"` and `confirm_fn(ctx.request_id, name, filtered_args, ctx.confirmation_token)` returns a falsy value.
  7. `"ok"` / `"tool_error"`: call `spec.fn(**filtered_args)` inside `try...except Exception as exc:`. On exception, return `{"ok": False, "status": "tool_error", "result": None, "error": str(exc)}`.
- **Argument filtering**: before calling `confirm_fn` or `spec.fn`, keep only keys in `spec.required_args`, plus `"amount"` when `spec.risk == "write"` and `spec.max_amount is not None` (if `"amount"` is present in `args`). Drop all other unknown keys.
- **Audit log**: on **every** `execute` call (including `"unknown_tool"` and `"tool_error"`), append `{"request_id": ctx.request_id, "role": ctx.role, "tool": name, "risk": spec.risk if spec else "unknown", "status": status}` to `self.audit_log`. Never invoke `spec.fn` on any denial.
