# Approval gate: pause before side-effect tools and execute only when a human approver confirms.
import json

from pyai_llm import FakeLLM

ORDERS = {"1042": {"status": "delayed", "total": 45.0}}
APPROVAL_REQUIRED = {"issue_refund"}


def lookup_order(order_id: str) -> str:
    order = ORDERS.get(order_id)
    if order is None:
        return f"error: order {order_id} not found"
    return f"{order['status']} (${order['total']:.2f})"


def issue_refund(order_id: str, amount: float) -> str:
    if order_id not in ORDERS:
        return f"error: unknown order {order_id}"
    return f"refunded ${amount:.2f} for order {order_id}"


TOOLS = [
    {
        "name": "lookup_order",
        "description": "order status total",
        "parameters": {"type": "object", "properties": {"order_id": {"type": "string"}}, "required": ["order_id"]},
    },
    {
        "name": "issue_refund",
        "description": "refund order amount",
        "parameters": {
            "type": "object",
            "properties": {"order_id": {"type": "string"}, "amount": {"type": "number"}},
            "required": ["order_id", "amount"],
        },
    },
]
REGISTRY = {"lookup_order": lookup_order, "issue_refund": issue_refund}


def run_with_approval(client: FakeLLM, task: str, max_steps: int = 5) -> dict:
    messages = [{"role": "user", "content": task}]
    trace = []
    for step in range(1, max_steps + 1):
        resp = client.chat(messages, tools=TOOLS)
        if not resp.tool_calls:
            return {"stopped_reason": "final", "answer": resp.content or "", "pending": None, "trace": trace}
        tc = resp.tool_calls[0]
        args = dict(tc.arguments)
        if tc.name in APPROVAL_REQUIRED:
            return {
                "stopped_reason": "needs_approval",
                "answer": "",
                "pending": {"id": tc.id, "tool": tc.name, "args": args},
                "trace": trace,
            }
        out = REGISTRY[tc.name](**args)
        obs = json.dumps(out) if isinstance(out, dict) else str(out)
        messages.append({"role": "assistant", "content": None, "tool_calls": [{"id": tc.id, "name": tc.name, "arguments": args}]})
        messages.append({"role": "tool", "tool_call_id": tc.id, "content": obs})
        trace.append({"step": step, "tool": tc.name, "args": args, "observation": obs})
    return {"stopped_reason": "max_steps", "answer": "", "pending": None, "trace": trace}


def handle_approval(pending: dict, approved: bool) -> str:
    if not approved:
        return f"rejected: {pending['tool']}({pending['args']})"
    return REGISTRY[pending["tool"]](**pending["args"])


script = [
    {"tool_calls": [{"name": "lookup_order", "arguments": {"order_id": "1042"}}]},
    {"tool_calls": [{"name": "issue_refund", "arguments": {"order_id": "1042", "amount": 45.0}}]},
]

res = run_with_approval(FakeLLM(script=script), "Refund delayed order 1042")
print("stopped_reason:", res["stopped_reason"])
print("pending:", res["pending"])
for item in res["trace"]:
    print(f"step {item['step']}: {item['tool']}({item['args']}) -> {item['observation']}")

approved_by_human = False
print("decision (False):", handle_approval(res["pending"], approved_by_human))
approved_by_human = True
print("decision (True) :", handle_approval(res["pending"], approved_by_human))
