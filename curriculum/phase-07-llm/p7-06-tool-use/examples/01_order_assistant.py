# Order assistant: route order and delivery questions through two local tools.
import json

from pyai_llm import FakeLLM

ORDERS = {
    "1042": {"item": "Mechanical Keyboard", "status": "shipped", "carrier": "FastPost"},
    "1043": {"item": "USB-C Hub", "status": "packed", "carrier": "CityExpress"},
}
CARRIER_DAYS = {"FastPost": 2, "CityExpress": 4}


def lookup_order(order_id: str) -> dict:
    return ORDERS.get(order_id, {"error": f"order {order_id} not found"})


def estimate_delivery(carrier: str) -> str:
    days = CARRIER_DAYS.get(carrier)
    if days is None:
        return f"error: unknown carrier {carrier}"
    return f"estimated delivery in {days} business days via {carrier}"


TOOLS = [
    {
        "name": "lookup_order",
        "description": "order status item carrier",
        "parameters": {"type": "object", "properties": {"order_id": {"type": "string"}}, "required": ["order_id"]},
    },
    {
        "name": "estimate_delivery",
        "description": "delivery estimate carrier days",
        "parameters": {"type": "object", "properties": {"carrier": {"type": "string"}}, "required": ["carrier"]},
    },
]
REGISTRY = {
    "lookup_order": lookup_order,
    "estimate_delivery": estimate_delivery,
}


def ask_assistant(question: str) -> None:
    client = FakeLLM()
    messages = [{"role": "user", "content": question}]
    resp = client.chat(messages, tools=TOOLS)
    print("Q:", question)
    if not resp.tool_calls:
        print("A:", resp.content)
        return
    tc = resp.tool_calls[0]
    raw = REGISTRY[tc.name](**tc.arguments)
    result = json.dumps(raw) if isinstance(raw, dict) else str(raw)
    print(f"  tool={tc.name} args={tc.arguments}")
    print(f"  result={result}")
    messages.append({
        "role": "assistant",
        "content": None,
        "tool_calls": [{"id": tc.id, "name": tc.name, "arguments": tc.arguments}],
    })
    messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})
    final = client.chat(messages, tools=TOOLS)
    print("A:", final.content)


for q in [
    'Check status for order "1042"',
    'Estimate delivery days for carrier "FastPost"',
]:
    ask_assistant(q)
