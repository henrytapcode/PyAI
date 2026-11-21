# Scoped tool permissions, write caps, and audit logging

**What it shows:** Enforcing per-request tool allowlists, `max_amount` write caps, and destructive confirmation gates in `ScopedRegistry`, while recording every outcome to `audit_log`.

**Step by step**
1. Lines 7–21 define `ToolSpec` (tool metadata, `risk` tier, optional `max_amount`) and `RequestContext` (caller `role`, `allowed_tools`, optional `confirmation_token`).
2. Lines 24–58 implement `ScopedRegistry.execute()`, checking unknown tools, scope allowlists, required arguments, `max_amount` policy caps, and `confirm_fn` in strict priority order before appending to `audit_log`.
3. Lines 61–67 register three tools (`lookup_order`, `issue_refund` capped at `50.0`, `delete_account`) and build a `support_ctx` and an `admin_ctx`.
4. Lines 69–73 execute four calls—an allowed read, an over-cap refund, an out-of-scope delete, and a confirmed admin delete—and print the results and `audit_log` statuses.

**Notice:** Both denied calls (`"denied_policy"` and `"denied_scope"`) block the underlying function from running while still appending an entry to `audit_log`.

**Try it yourself:** Change `support_ctx` to call `issue_refund` with `amount: 25.0`, and verify the status flips from `"denied_policy"` to `"ok"`.
