# Full deterministic scenario suite and summary report for the support agent.
import json
from pyai_llm import FakeLLM

ORDERS = {
    "1042": {"status": "delayed", "carrier": "FastShip", "total": 50.0, "days_late": 4},
    "1043": {"status": "shipped", "carrier": "FastShip", "total": 35.0, "days_late": 0},
    "1044": {"status": "delayed", "carrier": "GoPost", "total": 120.0, "days_late": 5},
}
SHIPMENTS = {("FastShip", "1042"): "hub delay (+4d)"}
REFUNDS = {}


def lookup_order(order_id: str) -> dict:
    if order_id not in ORDERS:
        return {"error": f"order {order_id} not found"}
    o = ORDERS[order_id]
    return {"status": o["status"], "total": o["total"], "late": o["days_late"]}


def track_shipment(carrier: str, order_id: str) -> str:
    return SHIPMENTS.get((carrier, order_id), "error: no tracking")


def check_refund_policy(days_late: int) -> str:
    return "eligible: max 20% refund" if days_late >= 3 else "not eligible"


def issue_refund(order_id: str, amount: float) -> str:
    REFUNDS[order_id] = amount
    return f"refunded ${amount:.2f} for {order_id}"


TOOL_MAP = {
    "lookup_order": (lookup_order, False),
    "track_shipment": (track_shipment, False),
    "check_refund_policy": (check_refund_policy, False),
    "issue_refund": (issue_refund, True),
}
SCHEMAS = [
    {"name": name, "description": name, "parameters": {"type": "object", "properties": {}, "required": []}}
    for name in TOOL_MAP
]


def run_agent(client, task: str, approve=None, max_steps: int = 6, token_budget: int | None = None) -> dict:
    messages = [{"role": "user", "content": task}]
    trace = []
    tokens = 0
    for step in range(1, max_steps + 1):
        resp = client.chat(messages, tools=SCHEMAS)
        tokens += resp.usage.total_tokens
        if token_budget is not None and tokens > token_budget:
            return {"stopped_reason": "budget", "answer": "", "tokens": tokens, "trace": trace}
        if not resp.tool_calls:
            return {"stopped_reason": "final", "answer": resp.content or "", "tokens": tokens, "trace": trace}
        tc = resp.tool_calls[0]
        args = dict(tc.arguments)
        if trace and trace[-1]["tool"] == tc.name and trace[-1]["args"] == args:
            return {"stopped_reason": "repeat", "answer": "", "tokens": tokens, "trace": trace}
        fn, side_effect = TOOL_MAP[tc.name]
        if side_effect:
            if approve is None:
                return {"stopped_reason": "needs_approval", "answer": "", "tokens": tokens, "trace": trace}
            if not approve(tc.name, dict(args)):
                return {"stopped_reason": "rejected", "answer": "", "tokens": tokens, "trace": trace}
        raw = fn(**args)
        obs = json.dumps(raw) if isinstance(raw, dict) else str(raw)
        messages.append({"role": "assistant", "content": None, "tool_calls": [{"id": tc.id, "name": tc.name, "arguments": args}]})
        messages.append({"role": "tool", "tool_call_id": tc.id, "content": obs})
        trace.append({"step": step, "tool": tc.name, "args": args, "observation": obs})
    return {"stopped_reason": "max_steps", "answer": "", "tokens": tokens, "trace": trace}


def policy_approve(name: str, args: dict) -> bool:
    order = ORDERS.get(args.get("order_id", ""))
    return bool(order and order["days_late"] >= 3 and 0 < args.get("amount", 0) <= round(order["total"] * 0.2, 2))


SCENARIOS = [
    {
        "name": "happy_lookup",
        "task": "Check order 1042 and refund policy.",
        "script": [
            {"tool_calls": [{"name": "lookup_order", "arguments": {"order_id": "1042"}}]},
            {"tool_calls": [{"name": "check_refund_policy", "arguments": {"days_late": 4}}]},
            "Order 1042 is delayed 4d; eligible for 20% refund.",
        ],
        "approve": None,
        "expect": {"stopped_reason": "final", "tools": ["lookup_order", "check_refund_policy"], "answer_contains": "20%"},
    },
    {
        "name": "missing_order",
        "task": "Check order 9999.",
        "script": [
            {"tool_calls": [{"name": "lookup_order", "arguments": {"order_id": "9999"}}]},
            "Order 9999 was not found.",
        ],
        "approve": None,
        "expect": {"stopped_reason": "final", "tools": ["lookup_order"], "answer_contains": "not found"},
    },
    {
        "name": "repeat_guard",
        "task": "Track order 1042.",
        "max_steps": 4,
        "script": [
            {"tool_calls": [{"name": "lookup_order", "arguments": {"order_id": "1042"}}]},
            {"tool_calls": [{"name": "lookup_order", "arguments": {"order_id": "1042"}}]},
        ],
        "approve": None,
        "expect": {"stopped_reason": "repeat", "tools": ["lookup_order"], "answer_contains": ""},
    },
    {
        "name": "max_steps_cap",
        "task": "Check everything on 1042.",
        "max_steps": 2,
        "script": [
            {"tool_calls": [{"name": "lookup_order", "arguments": {"order_id": "1042"}}]},
            {"tool_calls": [{"name": "track_shipment", "arguments": {"carrier": "FastShip", "order_id": "1042"}}]},
            {"tool_calls": [{"name": "check_refund_policy", "arguments": {"days_late": 4}}]},
        ],
        "approve": None,
        "expect": {"stopped_reason": "max_steps", "tools": ["lookup_order", "track_shipment"], "answer_contains": ""},
    },
    {
        "name": "refund_approved",
        "task": "Refund order 1042.",
        "script": [
            {"tool_calls": [{"name": "lookup_order", "arguments": {"order_id": "1042"}}]},
            {"tool_calls": [{"name": "check_refund_policy", "arguments": {"days_late": 4}}]},
            {"tool_calls": [{"name": "issue_refund", "arguments": {"order_id": "1042", "amount": 10.0}}]},
            "Refund of $10.00 issued.",
        ],
        "approve": policy_approve,
        "expect": {"stopped_reason": "final", "tools": ["lookup_order", "check_refund_policy", "issue_refund"], "answer_contains": "$10.00"},
    },
    {
        "name": "refund_rejected",
        "task": "Refund $50 for 1044.",
        "script": [
            {"tool_calls": [{"name": "lookup_order", "arguments": {"order_id": "1044"}}]},
            {"tool_calls": [{"name": "issue_refund", "arguments": {"order_id": "1044", "amount": 50.0}}]},
        ],
        "approve": policy_approve,
        "expect": {"stopped_reason": "rejected", "tools": ["lookup_order"], "answer_contains": ""},
    },
    {
        "name": "budget_stop",
        "task": "Check order 1043.",
        "token_budget": 10,
        "script": [
            {"tool_calls": [{"name": "lookup_order", "arguments": {"order_id": "1043"}}]},
            "Order 1043 is shipped.",
        ],
        "approve": None,
        "expect": {"stopped_reason": "budget", "tools": [], "answer_contains": ""},
    },
]

results = []
for sc in SCENARIOS:
    res = run_agent(
        FakeLLM(script=sc["script"]),
        sc["task"],
        approve=sc["approve"],
        max_steps=sc.get("max_steps", 6),
        token_budget=sc.get("token_budget"),
    )
    got_tools = [t["tool"] for t in res["trace"]]
    exp = sc["expect"]
    reasons = []
    if res["stopped_reason"] != exp["stopped_reason"]:
        reasons.append("stopped_reason")
    if got_tools != exp["tools"]:
        reasons.append("tools")
    if exp["answer_contains"] and exp["answer_contains"].lower() not in res["answer"].lower():
        reasons.append("answer")
    results.append({
        "name": sc["name"],
        "expected": f"{exp['stopped_reason']}({len(exp['tools'])})",
        "got": f"{res['stopped_reason']}({len(got_tools)})",
        "passed": not reasons,
        "reasons": reasons,
        "stopped_reason": res["stopped_reason"],
        "tokens": res["tokens"],
    })

for r in results:
    mark = "PASS" if r["passed"] else "FAIL"
    print(f"{r['name']:<16} | {r['expected']:<17} | {r['got']:<17} | {mark}")

counts = {}
for r in results:
    sr = r["stopped_reason"]
    counts[sr] = counts.get(sr, 0) + 1
print(f"passed: {sum(r['passed'] for r in results)}/{len(results)}")
print("total_tokens:", sum(r["tokens"] for r in results))
for sr in sorted(counts):
    print(f"  {sr}: {counts[sr]}")
print("failures:", [r["name"] for r in results if not r["passed"]] or "none")
