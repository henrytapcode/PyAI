from exercise import RequestContext, ScopedRegistry, ToolSpec


def _build_registry():
    calls = []

    def lookup_order(order_id: str) -> dict:
        calls.append(("lookup_order", order_id))
        return {"order_id": order_id, "status": "shipped"}

    def issue_refund(order_id: str, amount: float = 0.0) -> dict:
        calls.append(("issue_refund", order_id, amount))
        return {"order_id": order_id, "refunded": amount}

    def delete_account(user_id: str) -> str:
        calls.append(("delete_account", user_id))
        return f"deleted:{user_id}"

    reg = ScopedRegistry()
    reg.register(ToolSpec("lookup_order", lookup_order, ("order_id",), "read"))
    reg.register(
        ToolSpec("issue_refund", issue_refund, ("order_id",), "write", max_amount=50.0)
    )
    reg.register(ToolSpec("delete_account", delete_account, ("user_id",), "destructive"))
    return reg, calls


def test_register_rejects_invalid_risk_and_duplicate_name():
    reg = ScopedRegistry()
    reg.register(ToolSpec("ping", lambda: "pong", (), "read"))

    invalid_raised = False
    try:
        reg.register(ToolSpec("bad", lambda: None, (), "admin"))
    except ValueError:
        invalid_raised = True
    assert invalid_raised, "invalid risk tier must raise ValueError"

    dup_raised = False
    try:
        reg.register(ToolSpec("ping", lambda: "pong2", (), "read"))
    except ValueError:
        dup_raised = True
    assert dup_raised, "duplicate tool name must raise ValueError"


def test_unknown_tool_records_audit_with_unknown_risk():
    reg, calls = _build_registry()
    ctx = RequestContext("r1", "support", frozenset({"lookup_order"}))
    res = reg.execute("drop_db", {"x": 1}, ctx)
    assert res["ok"] is False
    assert res["status"] == "unknown_tool"
    assert res["result"] is None
    assert isinstance(res["error"], str) and len(res["error"]) > 0
    assert calls == []
    assert reg.audit_log == [
        {
            "request_id": "r1",
            "role": "support",
            "tool": "drop_db",
            "risk": "unknown",
            "status": "unknown_tool",
        }
    ]


def test_denied_scope_beats_invalid_args():
    reg, calls = _build_registry()
    ctx = RequestContext("r2", "viewer", frozenset({"lookup_order"}))
    res = reg.execute("issue_refund", {"amount": "not-a-number"}, ctx)
    assert res["ok"] is False
    assert res["status"] == "denied_scope"
    assert calls == []
    assert reg.audit_log[-1]["risk"] == "write"
    assert reg.audit_log[-1]["status"] == "denied_scope"


def test_invalid_args_missing_required_and_bad_amount_types():
    reg, calls = _build_registry()
    ctx = RequestContext("r3", "support", frozenset({"lookup_order", "issue_refund"}))

    r_missing = reg.execute("lookup_order", {}, ctx)
    assert r_missing["status"] == "invalid_args"

    for bad_amount in (None, True, False, "25", [10]):
        r_bad = reg.execute(
            "issue_refund", {"order_id": "O1", "amount": bad_amount}, ctx
        )
        assert r_bad["ok"] is False
        assert r_bad["status"] == "invalid_args"
    assert calls == []


def test_invalid_args_beats_denied_policy_and_confirmation():
    reg, calls = _build_registry()
    ctx = RequestContext(
        "r4", "admin", frozenset({"issue_refund", "delete_account"}), confirmation_token=None
    )
    r_write = reg.execute("issue_refund", {"amount": 999.0}, ctx)
    assert r_write["status"] == "invalid_args"

    r_dest = reg.execute("delete_account", {}, ctx)
    assert r_dest["status"] == "invalid_args"
    assert calls == []


def test_write_max_amount_policy_and_zero_cap():
    reg, calls = _build_registry()
    reg.register(
        ToolSpec(
            "zero_cap",
            lambda item, amount=0.0: {"item": item, "amount": amount},
            ("item",),
            "write",
            max_amount=0.0,
        )
    )
    ctx = RequestContext("r5", "support", frozenset({"issue_refund", "zero_cap"}))

    r_over = reg.execute("issue_refund", {"order_id": "O2", "amount": 50.01}, ctx)
    assert r_over["ok"] is False
    assert r_over["status"] == "denied_policy"

    r_exact = reg.execute("issue_refund", {"order_id": "O2", "amount": 50.0}, ctx)
    assert r_exact["ok"] is True
    assert r_exact["status"] == "ok"
    assert r_exact["result"] == {"order_id": "O2", "refunded": 50.0}

    r_zero_over = reg.execute("zero_cap", {"item": "x", "amount": 1.0}, ctx)
    assert r_zero_over["status"] == "denied_policy"

    r_zero_ok = reg.execute("zero_cap", {"item": "x", "amount": 0.0}, ctx)
    assert r_zero_ok["status"] == "ok"
    assert len(calls) == 1


def test_unknown_args_filtered_before_fn_and_confirm():
    seen_fn_kwargs = []
    seen_confirm_args = []

    def strict_tool(order_id: str) -> str:
        seen_fn_kwargs.append({"order_id": order_id})
        return f"ok:{order_id}"

    def confirm_spy(req_id: str, tool: str, args: dict, token: str) -> bool:
        seen_confirm_args.append((req_id, tool, dict(args), token))
        return True

    reg = ScopedRegistry()
    reg.register(ToolSpec("strict", strict_tool, ("order_id",), "destructive"))
    ctx = RequestContext(
        "r6", "admin", frozenset({"strict"}), confirmation_token="tok-123"
    )
    res = reg.execute(
        "strict",
        {"order_id": "O9", "injected": "evil", "extra": 42},
        ctx,
        confirm_fn=confirm_spy,
    )
    assert res["ok"] is True
    assert res["result"] == "ok:O9"
    assert seen_confirm_args == [("r6", "strict", {"order_id": "O9"}, "tok-123")]
    assert seen_fn_kwargs == [{"order_id": "O9"}]


def test_destructive_needs_confirmation_and_denied_confirmation():
    reg, calls = _build_registry()

    ctx_no_tok = RequestContext("r7a", "admin", frozenset({"delete_account"}))
    r1 = reg.execute(
        "delete_account", {"user_id": "u1"}, ctx_no_tok, confirm_fn=lambda *_: True
    )
    assert r1["status"] == "needs_confirmation"

    ctx_empty_tok = RequestContext(
        "r7b", "admin", frozenset({"delete_account"}), confirmation_token=""
    )
    r2 = reg.execute(
        "delete_account", {"user_id": "u1"}, ctx_empty_tok, confirm_fn=lambda *_: True
    )
    assert r2["status"] == "needs_confirmation"

    ctx_ok_tok = RequestContext(
        "r7c", "admin", frozenset({"delete_account"}), confirmation_token="tok"
    )
    r3 = reg.execute("delete_account", {"user_id": "u1"}, ctx_ok_tok, confirm_fn=None)
    assert r3["status"] == "needs_confirmation"

    r4 = reg.execute(
        "delete_account", {"user_id": "u1"}, ctx_ok_tok, confirm_fn=lambda *_: False
    )
    assert r4["status"] == "denied_confirmation"
    assert calls == []


def test_destructive_approved_and_tool_error_containment():
    def boom(target: str) -> None:
        raise RuntimeError(f"failed on {target}")

    reg, calls = _build_registry()
    reg.register(ToolSpec("boom", boom, ("target",), "read"))
    ctx = RequestContext(
        "r8",
        "admin",
        frozenset({"delete_account", "boom"}),
        confirmation_token="tok-ok",
    )

    r_ok = reg.execute(
        "delete_account", {"user_id": "u9"}, ctx, confirm_fn=lambda *_: True
    )
    assert r_ok == {"ok": True, "status": "ok", "result": "deleted:u9", "error": None}
    assert calls == [("delete_account", "u9")]

    r_err = reg.execute("boom", {"target": "db"}, ctx)
    assert r_err["ok"] is False
    assert r_err["status"] == "tool_error"
    assert r_err["result"] is None
    assert "failed on db" in r_err["error"]


def test_audit_log_records_every_call_in_order():
    reg, _ = _build_registry()
    ctx = RequestContext("r9", "support", frozenset({"lookup_order", "issue_refund"}))
    reg.execute("missing", {}, ctx)
    reg.execute("delete_account", {"user_id": "u1"}, ctx)
    reg.execute("lookup_order", {"order_id": "A1"}, ctx)
    reg.execute("issue_refund", {"order_id": "A1", "amount": 100.0}, ctx)

    statuses = [entry["status"] for entry in reg.audit_log]
    assert statuses == ["unknown_tool", "denied_scope", "ok", "denied_policy"]
    for entry in reg.audit_log:
        assert set(entry.keys()) == {"request_id", "role", "tool", "risk", "status"}
