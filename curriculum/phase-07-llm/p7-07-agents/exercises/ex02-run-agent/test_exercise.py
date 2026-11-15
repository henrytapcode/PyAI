import json

from exercise import run_agent
from pyai_llm import FakeLLM

ORDER_TOOL = {
    "name": "lookup_order",
    "description": "order status carrier",
    "parameters": {
        "type": "object",
        "properties": {"order_id": {"type": "string"}, "note": {"type": "string"}},
        "required": ["order_id"],
    },
}
DELIVERY_TOOL = {
    "name": "estimate_delivery",
    "description": "delivery estimate carrier",
    "parameters": {
        "type": "object",
        "properties": {"carrier": {"type": "string"}},
        "required": ["carrier"],
    },
}
TOOLS = [ORDER_TOOL, DELIVERY_TOOL]


def _lookup_order(order_id: str, note: str = "ok") -> dict:
    if order_id == "bad":
        raise ValueError("invalid order id")
    return {"order_id": order_id, "status": "shipped", "carrier": "FastPost", "note": note}


def _estimate_delivery(carrier: str) -> str:
    return f"2 business days via {carrier}"


REGISTRY = {"lookup_order": _lookup_order, "estimate_delivery": _estimate_delivery}


class _SpyClient:
    def __init__(self, script=None) -> None:
        self._inner = FakeLLM(script=script)
        self.chat_calls: list[list[dict]] = []

    def chat(self, messages: list[dict], **kwargs):
        self.chat_calls.append([dict(m) for m in messages])
        return self._inner.chat(messages, **kwargs)


def test_three_step_scripted_task_reaches_final():
    client = FakeLLM(script=[
        {"tool_calls": [{"name": "lookup_order", "arguments": {"order_id": "1042", "note": ""}}]},
        {"tool_calls": [{"name": "estimate_delivery", "arguments": {"carrier": "FastPost"}}]},
        "Order 1042 arrives in 2 business days via FastPost.",
    ])
    res = run_agent(client, "When will order 1042 arrive?", TOOLS, REGISTRY)
    assert res["stopped_reason"] == "final"
    assert res["steps"] == 3
    assert "2 business days" in res["answer"]
    assert len(res["trace"]) == 2
    assert res["trace"][0]["step"] == 1
    assert res["trace"][0]["tool"] == "lookup_order"
    assert res["trace"][0]["args"] == {"order_id": "1042", "note": ""}
    assert json.loads(res["trace"][0]["observation"])["status"] == "shipped"
    assert res["trace"][1]["step"] == 2
    assert res["trace"][1]["tool"] == "estimate_delivery"
    assert res["trace"][1]["observation"] == "2 business days via FastPost"


def test_no_tool_needed_finishes_in_one_step():
    res = run_agent(FakeLLM(), "Tell me a joke", TOOLS, REGISTRY)
    assert res["stopped_reason"] == "final"
    assert res["steps"] == 1
    assert res["trace"] == []
    assert "Tell me a joke" in res["answer"]


def test_stops_at_max_steps_when_script_keeps_calling_tools():
    client = FakeLLM(script=[
        {"tool_calls": [{"name": "lookup_order", "arguments": {"order_id": "1"}}]},
        {"tool_calls": [{"name": "lookup_order", "arguments": {"order_id": "2"}}]},
        {"tool_calls": [{"name": "lookup_order", "arguments": {"order_id": "3"}}]},
        {"tool_calls": [{"name": "lookup_order", "arguments": {"order_id": "4"}}]},
    ])
    res = run_agent(client, "Loop forever", TOOLS, REGISTRY, max_steps=3)
    assert res["stopped_reason"] == "max_steps"
    assert res["steps"] == 3
    assert res["answer"] == ""
    assert len(res["trace"]) == 3


def test_repeat_guard_stops_before_running_duplicate_tool_call():
    calls = 0

    def tracked_lookup(order_id: str) -> str:
        nonlocal calls
        calls += 1
        return f"shipped:{order_id}"

    client = FakeLLM(script=[
        {"tool_calls": [{"name": "lookup_order", "arguments": {"order_id": "1042"}}]},
        {"tool_calls": [{"name": "lookup_order", "arguments": {"order_id": "1042"}}]},
        "Should not reach step 3",
    ])
    res = run_agent(
        client,
        "Check 1042",
        [ORDER_TOOL],
        {"lookup_order": tracked_lookup},
        max_steps=5,
    )
    assert res["stopped_reason"] == "repeat"
    assert res["steps"] == 2
    assert res["answer"] == ""
    assert calls == 1
    assert len(res["trace"]) == 1


def test_stops_with_budget_when_token_budget_is_exceeded():
    client = FakeLLM(script=[
        {"tool_calls": [{"name": "lookup_order", "arguments": {"order_id": "1042"}}]},
        "Done.",
    ])
    res = run_agent(client, "Check 1042", TOOLS, REGISTRY, max_steps=5, token_budget=5)
    assert res["stopped_reason"] == "budget"
    assert res["steps"] == 1
    assert res["answer"] == ""
    assert res["trace"] == []


def test_unknown_tool_records_error_observation_and_continues():
    client = FakeLLM(script=[
        {"tool_calls": [{"name": "drop_db", "arguments": {}}]},
        "Could not run that tool.",
    ])
    res = run_agent(client, "Drop db", TOOLS, REGISTRY)
    assert res["stopped_reason"] == "final"
    assert res["steps"] == 2
    assert res["trace"][0]["observation"].startswith("error: unknown tool")
    assert "drop_db" in res["trace"][0]["observation"]


def test_tool_exception_records_error_observation_and_continues():
    client = FakeLLM(script=[
        {"tool_calls": [{"name": "lookup_order", "arguments": {"order_id": "bad"}}]},
        {"tool_calls": [{"name": "lookup_order", "arguments": {"order_id": "1042"}}]},
        "Recovered with order 1042.",
    ])
    res = run_agent(client, "Check order", TOOLS, REGISTRY)
    assert res["stopped_reason"] == "final"
    assert res["steps"] == 3
    assert res["trace"][0]["observation"].startswith("error:")
    assert "invalid order id" in res["trace"][0]["observation"]
    assert res["answer"] == "Recovered with order 1042."


def test_spy_checks_assistant_and_tool_message_order_and_id():
    spy = _SpyClient(script=[
        {"tool_calls": [{"name": "lookup_order", "arguments": {"order_id": "1042"}}]},
        "Done.",
    ])
    run_agent(spy, "Check 1042", TOOLS, REGISTRY)
    assert len(spy.chat_calls) == 2
    msgs = spy.chat_calls[1]
    assert msgs[0]["role"] == "user"
    assert msgs[1]["role"] == "assistant"
    assert msgs[1]["content"] is None
    tc = msgs[1]["tool_calls"][0]
    tc_id = tc["id"] if isinstance(tc, dict) else tc.id
    assert msgs[2]["role"] == "tool"
    assert msgs[2]["tool_call_id"] == tc_id


def test_return_keys_and_inputs_not_mutated():
    tools = [json.loads(json.dumps(ORDER_TOOL))]
    registry = {"lookup_order": _lookup_order}
    tools_snap = json.loads(json.dumps(tools))
    reg_snap = dict(registry)

    res = run_agent(FakeLLM(script=["ok"]), "Hi", tools, registry)
    assert set(res) == {"answer", "stopped_reason", "steps", "trace"}
    assert tools == tools_snap
    assert registry == reg_snap
