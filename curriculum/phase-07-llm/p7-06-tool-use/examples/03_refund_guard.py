# Refund guard: enforce allowlist, human confirmation, and amount cap on side effects.
import json

from pyai_llm import FakeLLM

ORDERS = {
    "1042": {"total": 45.0, "status": "delivered"},
    "1043": {"total": 250.0, "status": "delivered"},
}
ALLOWED_TOOLS = {"issue_refund"}
MAX_AUTO_REFUND = 100.0
ACTION_LOG: list[str] = []


def issue_refund(order_id: str, amount: float) -> str:
    if order_id not in ORDERS:
        return f"error: unknown order {order_id}"
    return json.dumps({"status": "refunded", "order_id": order_id, "amount": amount})


def guarded_dispatch(name: str, args: dict, confirmed: bool) -> str:
    if name not in ALLOWED_TOOLS:
        ACTION_LOG.append(f"BLOCKED {name}: not in allowlist")
        return f"error: tool {name} is not allowed"
    if not confirmed:
        ACTION_LOG.append(f"BLOCKED {name} {args}: missing human confirmation")
        return "blocked: user confirmation required"
    amount = args.get("amount", 0)
    if not isinstance(amount, (int, float)) or isinstance(amount, bool) or amount <= 0 or amount > MAX_AUTO_REFUND:
        ACTION_LOG.append(f"BLOCKED {name} {args}: exceeds limit {MAX_AUTO_REFUND}")
        return f"blocked: amount {amount} exceeds cap {MAX_AUTO_REFUND}"
    result = issue_refund(**args)
    ACTION_LOG.append(f"APPROVED {name} {args} -> {result}")
    return result


scripted = FakeLLM(script=[
    {"tool_calls": [{"name": "issue_refund", "arguments": {"order_id": "1042", "amount": 45.0}}]},
    "Refund of 45.0 for order 1042 is complete.",
    {"tool_calls": [{"name": "issue_refund", "arguments": {"order_id": "1043", "amount": 250.0}}]},
    "Refund of 250.0 was blocked because it exceeds the 100.0 limit.",
])

scenarios = [
    ("Refund order 1042 ($45)", True),
    ("Refund order 1043 ($250)", True),
]

for question, user_confirmed in scenarios:
    messages = [{"role": "user", "content": question}]
    resp = scripted.chat(messages)
    tc = resp.tool_calls[0]
    tool_output = guarded_dispatch(tc.name, tc.arguments, confirmed=user_confirmed)
    messages.append({
        "role": "assistant",
        "content": None,
        "tool_calls": [{"id": tc.id, "name": tc.name, "arguments": tc.arguments}],
    })
    messages.append({"role": "tool", "tool_call_id": tc.id, "content": tool_output})
    final = scripted.chat(messages)
    print(f"User: {question} -> {final.content}")

print("\nAction log:")
for entry in ACTION_LOG:
    print(" -", entry)
