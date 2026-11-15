# Order support agent: a bounded 3-step loop with three read-only tools and trace output.
import json

from pyai_llm import FakeLLM

ORDERS = {
    "1042": {"status": "shipped", "carrier": "FastPost"},
    "1043": {"status": "packed", "carrier": "CityExpress"},
}
DELIVERY_DAYS = {"FastPost": 2, "CityExpress": 4}
POLICIES = {
    "shipped": "Refund allowed if delayed over 5 days.",
    "packed": "Cancel anytime before shipment.",
}


def lookup_order(order_id: str) -> str:
    order = ORDERS.get(order_id)
    if order is None:
        return f"error: order {order_id} not found"
    return f"{order['status']} ({order['carrier']})"


def estimate_delivery(carrier: str) -> str:
    days = DELIVERY_DAYS.get(carrier)
    if days is None:
        return f"error: unknown carrier {carrier}"
    return f"{days} business days"


def check_policy(status: str) -> str:
    return POLICIES.get(status, f"error: no policy for {status}")


TOOLS = [
    {
        "name": "lookup_order",
        "description": "order status carrier",
        "parameters": {"type": "object", "properties": {"order_id": {"type": "string"}}, "required": ["order_id"]},
    },
    {
        "name": "estimate_delivery",
        "description": "delivery estimate carrier days",
        "parameters": {"type": "object", "properties": {"carrier": {"type": "string"}}, "required": ["carrier"]},
    },
    {
        "name": "check_policy",
        "description": "refund policy order status",
        "parameters": {"type": "object", "properties": {"status": {"type": "string"}}, "required": ["status"]},
    },
]
REGISTRY = {
    "lookup_order": lookup_order,
    "estimate_delivery": estimate_delivery,
    "check_policy": check_policy,
}


def dispatch(name: str, args: dict, registry: dict) -> str:
    fn = registry.get(name)
    if fn is None:
        return f"error: unknown tool {name}"
    clean = {k: v for k, v in args.items() if v not in ("", None)}
    try:
        out = fn(**clean)
    except Exception as err:
        return f"error: {err}"
    return json.dumps(out) if isinstance(out, dict) else str(out)


def run_agent(client: FakeLLM, task: str, max_steps: int = 5) -> dict:
    messages = [{"role": "user", "content": task}]
    trace = []
    for step in range(1, max_steps + 1):
        resp = client.chat(messages, tools=TOOLS)
        if not resp.tool_calls:
            return {"answer": resp.content or "", "stopped_reason": "final", "steps": step, "trace": trace}
        tc = resp.tool_calls[0]
        args = dict(tc.arguments)
        obs = dispatch(tc.name, args, REGISTRY)
        messages.append({
            "role": "assistant",
            "content": None,
            "tool_calls": [{"id": tc.id, "name": tc.name, "arguments": args}],
        })
        messages.append({"role": "tool", "tool_call_id": tc.id, "content": obs})
        trace.append({"step": step, "tool": tc.name, "args": args, "observation": obs})
    return {"answer": "", "stopped_reason": "max_steps", "steps": max_steps, "trace": trace}


script = [
    {"tool_calls": [{"name": "lookup_order", "arguments": {"order_id": "1042"}}]},
    {"tool_calls": [{"name": "estimate_delivery", "arguments": {"carrier": "FastPost"}}]},
    "Order 1042 shipped via FastPost and arrives in 2 business days.",
]

result = run_agent(FakeLLM(script=script), "When will order 1042 arrive?", max_steps=5)
print("stopped_reason:", result["stopped_reason"], "steps:", result["steps"])
for item in result["trace"]:
    print(f"step {item['step']}: {item['tool']}({item['args']}) -> {item['observation']}")
print("answer:", result["answer"])
