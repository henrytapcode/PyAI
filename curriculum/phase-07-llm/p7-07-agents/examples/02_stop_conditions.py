# Stop conditions: run the same agent with four scripts to trigger final, max_steps, repeat, and budget.
import json

from pyai_llm import FakeLLM

ORDERS = {"1042": {"status": "shipped", "carrier": "FastPost"}}
CARRIERS = {"FastPost": "2 business days"}


def lookup_order(order_id: str) -> str:
    order = ORDERS.get(order_id)
    return f"{order['status']} ({order['carrier']})" if order else f"error: unknown {order_id}"


def estimate_delivery(carrier: str) -> str:
    return CARRIERS.get(carrier, f"error: unknown {carrier}")


TOOLS = [
    {
        "name": "lookup_order",
        "description": "order status carrier",
        "parameters": {"type": "object", "properties": {"order_id": {"type": "string"}}, "required": ["order_id"]},
    },
    {
        "name": "estimate_delivery",
        "description": "delivery estimate carrier",
        "parameters": {"type": "object", "properties": {"carrier": {"type": "string"}}, "required": ["carrier"]},
    },
]
REGISTRY = {"lookup_order": lookup_order, "estimate_delivery": estimate_delivery}


def run_agent(
    client: FakeLLM,
    task: str,
    max_steps: int = 4,
    token_budget: int | None = None,
) -> dict:
    messages = [{"role": "user", "content": task}]
    trace = []
    total_tokens = 0
    for step in range(1, max_steps + 1):
        resp = client.chat(messages, tools=TOOLS)
        total_tokens += resp.usage.total_tokens
        if token_budget is not None and total_tokens > token_budget:
            return {"stopped_reason": "budget", "steps": step, "tokens": total_tokens, "trace": trace}
        if not resp.tool_calls:
            return {"stopped_reason": "final", "steps": step, "tokens": total_tokens, "trace": trace}
        tc = resp.tool_calls[0]
        args = dict(tc.arguments)
        if trace and trace[-1]["tool"] == tc.name and trace[-1]["args"] == args:
            return {"stopped_reason": "repeat", "steps": step, "tokens": total_tokens, "trace": trace}
        fn = REGISTRY.get(tc.name)
        out = fn(**args) if fn else f"error: unknown tool {tc.name}"
        obs = json.dumps(out) if isinstance(out, dict) else str(out)
        messages.append({
            "role": "assistant",
            "content": None,
            "tool_calls": [{"id": tc.id, "name": tc.name, "arguments": args}],
        })
        messages.append({"role": "tool", "tool_call_id": tc.id, "content": obs})
        trace.append({"step": step, "tool": tc.name, "args": args, "observation": obs})
    return {"stopped_reason": "max_steps", "steps": max_steps, "tokens": total_tokens, "trace": trace}


scenarios = [
    (
        "normal completion",
        [
            {"tool_calls": [{"name": "lookup_order", "arguments": {"order_id": "1042"}}]},
            "Order 1042 is shipped via FastPost.",
        ],
        4,
        None,
    ),
    (
        "alternating tools past cap",
        [
            {"tool_calls": [{"name": "lookup_order", "arguments": {"order_id": "1042"}}]},
            {"tool_calls": [{"name": "estimate_delivery", "arguments": {"carrier": "FastPost"}}]},
            {"tool_calls": [{"name": "lookup_order", "arguments": {"order_id": "1042"}}]},
            {"tool_calls": [{"name": "estimate_delivery", "arguments": {"carrier": "FastPost"}}]},
        ],
        3,
        None,
    ),
    (
        "stuck repeating same call",
        [
            {"tool_calls": [{"name": "lookup_order", "arguments": {"order_id": "1042"}}]},
            {"tool_calls": [{"name": "lookup_order", "arguments": {"order_id": "1042"}}]},
        ],
        5,
        None,
    ),
    (
        "tight token budget",
        [
            {"tool_calls": [{"name": "lookup_order", "arguments": {"order_id": "1042"}}]},
            {"tool_calls": [{"name": "estimate_delivery", "arguments": {"carrier": "FastPost"}}]},
            "Done.",
        ],
        5,
        25,
    ),
]

for label, script, cap, budget in scenarios:
    res = run_agent(FakeLLM(script=script), "Check order 1042", max_steps=cap, token_budget=budget)
    print(f"{label:26s} -> stopped_reason={res['stopped_reason']}, steps={res['steps']}, tokens={res['tokens']}")
