# Bounded agent with an approval gate on side-effect tools across three tasks.
import json
from pyai_llm import FakeLLM

ORDERS = {
    "1042": {"status": "delayed", "carrier": "FastShip", "total": 50.0, "days_late": 4},
    "1044": {"status": "delayed", "carrier": "GoPost", "total": 120.0, "days_late": 5},
}
REFUNDS = {}


def lookup_order(order_id: str) -> dict:
    o = ORDERS[order_id]
    return {"status": o["status"], "total": o["total"], "late": o["days_late"]}


def check_refund_policy(days_late: int) -> str:
    return "eligible: max 20% refund" if days_late >= 3 else "not eligible"


def issue_refund(order_id: str, amount: float) -> str:
    REFUNDS[order_id] = amount
    return f"refunded ${amount:.2f} for {order_id}"


TOOLS = {
    "lookup_order": (lookup_order, False),
    "check_refund_policy": (check_refund_policy, False),
    "issue_refund": (issue_refund, True),
}
SCHEMAS = [
    {"name": "lookup_order", "description": "lookup order", "parameters": {"type": "object", "properties": {"order_id": {"type": "string"}}, "required": ["order_id"]}},
    {"name": "check_refund_policy", "description": "refund policy", "parameters": {"type": "object", "properties": {"days_late": {"type": "integer"}}, "required": ["days_late"]}},
    {"name": "issue_refund", "description": "issue refund", "parameters": {"type": "object", "properties": {"order_id": {"type": "string"}, "amount": {"type": "number"}}, "required": ["order_id", "amount"]}},
]


def run_support_agent(client, task: str, approve=None, approver: str = "none", max_steps: int = 6) -> dict:
    messages = [{"role": "user", "content": task}]
    trace = []
    audit = []
    for step in range(1, max_steps + 1):
        resp = client.chat(messages, tools=SCHEMAS)
        if not resp.tool_calls:
            return {"stopped_reason": "final", "answer": resp.content or "", "pending": None, "trace": trace, "audit": audit}
        tc = resp.tool_calls[0]
        args = dict(tc.arguments)
        if trace and trace[-1]["tool"] == tc.name and trace[-1]["args"] == args:
            return {"stopped_reason": "repeat", "answer": "", "pending": None, "trace": trace, "audit": audit}
        fn, is_side = TOOLS[tc.name]
        if is_side:
            ok = bool(approve(tc.name, dict(args))) if approve is not None else False
            audit.append({"tool": tc.name, "approved": ok, "by": approver})
            if not ok:
                return {"stopped_reason": "needs_approval", "answer": "", "pending": {"tool": tc.name, "args": args}, "trace": trace, "audit": audit}
        raw = fn(**args)
        obs = json.dumps(raw) if isinstance(raw, dict) else str(raw)
        messages.append({"role": "assistant", "content": None, "tool_calls": [{"id": tc.id, "name": tc.name, "arguments": args}]})
        messages.append({"role": "tool", "tool_call_id": tc.id, "content": obs})
        trace.append({"step": step, "tool": tc.name, "args": args, "observation": obs})
    return {"stopped_reason": "max_steps", "answer": "", "pending": None, "trace": trace, "audit": audit}


def policy_gate(name: str, args: dict) -> bool:
    order = ORDERS.get(args.get("order_id", ""))
    return bool(order and order["days_late"] >= 3 and 0 < args.get("amount", 0) <= round(order["total"] * 0.2, 2))


tasks = [
    ("read_only", "Status of 1042?", None, "none", [
        {"tool_calls": [{"name": "lookup_order", "arguments": {"order_id": "1042"}}]},
        {"tool_calls": [{"name": "check_refund_policy", "arguments": {"days_late": 4}}]},
        "Order 1042 is delayed 4d (20% max refund).",
    ]),
    ("approved ", "Refund $10 for 1042", lambda n, a: True, "supervisor", [
        {"tool_calls": [{"name": "lookup_order", "arguments": {"order_id": "1042"}}]},
        {"tool_calls": [{"name": "issue_refund", "arguments": {"order_id": "1042", "amount": 10.0}}]},
        "Refunded $10.00 for order 1042.",
    ]),
    ("rejected ", "Refund $50 for 1044", policy_gate, "policy_gate", [
        {"tool_calls": [{"name": "lookup_order", "arguments": {"order_id": "1044"}}]},
        {"tool_calls": [{"name": "issue_refund", "arguments": {"order_id": "1044", "amount": 50.0}}]},
    ]),
]

for label, prompt, gate, who, sc in tasks:
    out = run_support_agent(FakeLLM(script=sc), prompt, approve=gate, approver=who)
    print(f"[{label}] stopped={out['stopped_reason']}")
    if out["pending"] is not None:
        p = out["pending"]
        print(f"  pending: {p['tool']} {p['args']}")
    for t in out["trace"]:
        print(f"  s{t['step']} {t['tool']}: {t['observation']}")
    if out["audit"]:
        a = out["audit"][0]
        print(f"  audit: {a['tool']} ok={a['approved']} by={a['by']}")
print("refunds_ledger:", REFUNDS)
