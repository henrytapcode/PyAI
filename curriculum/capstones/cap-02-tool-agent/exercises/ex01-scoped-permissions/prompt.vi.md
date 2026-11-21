Hãy cài đặt `ToolSpec`, `RequestContext`, và `ScopedRegistry` trong `starter.py` để áp đặt allowlist (danh sách tool được phép) theo từng request, kiểm tra và lọc tham số, trần số tiền cho quyền `write`, cổng xác nhận cho quyền `destructive`, cô lập ngoại lệ và ghi audit log đầy đủ.

**Ví dụ**

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

**Quy tắc**

- **`ToolSpec`**: dataclass gồm các trường `(name: str, fn: Callable, required_args: tuple[str, ...], risk: str, max_amount: float | None = None)`.
- **`RequestContext`**: dataclass gồm các trường `(request_id: str, role: str, allowed_tools: frozenset[str] | set[str], confirmation_token: str | None = None)`.
- **`ScopedRegistry.register(spec)`**: ném `ValueError` nếu `spec.risk` không thuộc `("read", "write", "destructive")` hoặc nếu `spec.name` đã được đăng ký trước đó.
- **`ScopedRegistry.execute(name, args, ctx, confirm_fn=None)`**: trả về `{"ok": bool, "status": str, "result": Any, "error": str | None}` và kiểm tra theo đúng thứ tự ưu tiên:
  1. `"unknown_tool"`: `name` chưa được đăng ký. Ghi `"risk": "unknown"` vào `audit_log`.
  2. `"denied_scope"`: `name` không nằm trong `ctx.allowed_tools`.
  3. `"invalid_args"`: thiếu bất kỳ khóa nào trong `spec.required_args`; HOẶC `spec.risk == "write"`, `spec.max_amount is not None` và `"amount"` có trong `args` nhưng mang giá trị `None`, `bool`, hoặc không phải `int`/`float`.
  4. `"denied_policy"`: `spec.risk == "write"`, `spec.max_amount is not None` và `args.get("amount", 0) > spec.max_amount`.
  5. `"needs_confirmation"`: `spec.risk == "destructive"` và (`not ctx.confirmation_token` hoặc `confirm_fn is None`).
  6. `"denied_confirmation"`: `spec.risk == "destructive"` và `confirm_fn(ctx.request_id, name, filtered_args, ctx.confirmation_token)` trả về giá trị falsy.
  7. `"ok"` / `"tool_error"`: gọi `spec.fn(**filtered_args)` trong `try...except Exception as exc:`. Nếu có ngoại lệ, trả về `{"ok": False, "status": "tool_error", "result": None, "error": str(exc)}`.
- **Lọc tham số**: trước khi gọi `confirm_fn` hoặc `spec.fn`, chỉ giữ lại các khóa có trong `spec.required_args`, cộng thêm `"amount"` khi `spec.risk == "write"` và `spec.max_amount is not None` (nếu `"amount"` có mặt trong `args`). Mọi khóa lạ khác đều bị loại bỏ.
- **Audit log**: ở **mọi** lần gọi `execute` (kể cả `"unknown_tool"` và `"tool_error"`), nối thêm `{"request_id": ctx.request_id, "role": ctx.role, "tool": name, "risk": spec.risk if spec else "unknown", "status": status}` vào `self.audit_log`. Không bao giờ gọi `spec.fn` khi bị từ chối.
