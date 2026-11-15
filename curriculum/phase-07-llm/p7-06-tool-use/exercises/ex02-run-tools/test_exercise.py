import json

from exercise import run_with_tools
from pyai_llm import FakeLLM

WEATHER_TOOL = {
    "name": "get_weather",
    "description": "weather city temperature",
    "parameters": {
        "type": "object",
        "properties": {"city": {"type": "string"}, "unit": {"type": "string"}},
        "required": ["city"],
    },
}
ORDER_TOOL = {
    "name": "lookup_order",
    "description": "order status delivery",
    "parameters": {
        "type": "object",
        "properties": {"order_id": {"type": "string"}},
        "required": ["order_id"],
    },
}


def _get_weather(city: str, unit: str = "C") -> str:
    if city == "Hanoi":
        return f"31{unit} and sunny"
    raise ValueError(f"unknown city {city}")


def _lookup_order(order_id: str) -> dict:
    return {"order_id": order_id, "status": "shipped", "eta_days": 2}


class _SpyClient:
    def __init__(self, script=None) -> None:
        self._inner = FakeLLM(script=script)
        self.chat_calls: list[list[dict]] = []

    def chat(self, messages: list[dict], **kwargs):
        self.chat_calls.append([dict(m) for m in messages])
        return self._inner.chat(messages, **kwargs)


def test_weather_question_uses_tool_and_records_called():
    ans, called = run_with_tools(
        FakeLLM(),
        "What is the weather in Hanoi?",
        [WEATHER_TOOL],
        {"get_weather": _get_weather},
    )
    assert "31C and sunny" in ans
    assert called == ["get_weather"]


def test_no_tool_needed_returns_answer_and_empty_called():
    ans, called = run_with_tools(
        FakeLLM(),
        "Tell me a joke",
        [WEATHER_TOOL],
        {"get_weather": _get_weather},
    )
    assert "Tell me a joke" in ans
    assert called == []


def test_unknown_tool_returns_error_message_without_crashing():
    spy = _SpyClient(script=[
        {"tool_calls": [{"name": "drop_db", "arguments": {}}]},
        "Sorry, I cannot run that tool.",
    ])
    ans, called = run_with_tools(spy, "Drop db", [WEATHER_TOOL], {"get_weather": _get_weather})
    assert "Sorry" in ans
    assert len(spy.chat_calls) == 2
    tool_msgs = [m for m in spy.chat_calls[1] if m["role"] == "tool"]
    assert len(tool_msgs) == 1
    assert "error: unknown tool" in tool_msgs[0]["content"]
    assert "drop_db" in tool_msgs[0]["content"]


def test_tool_exception_is_sent_back_as_error_string():
    spy = _SpyClient(script=[
        {"tool_calls": [{"name": "get_weather", "arguments": {"city": "Atlantis"}}]},
        "City was not found.",
    ])
    ans, called = run_with_tools(
        spy,
        "Weather in Atlantis?",
        [WEATHER_TOOL],
        {"get_weather": _get_weather},
    )
    assert ans == "City was not found."
    tool_msgs = [m for m in spy.chat_calls[1] if m["role"] == "tool"]
    assert tool_msgs[0]["content"].startswith("error:")
    assert "unknown city Atlantis" in tool_msgs[0]["content"]


def test_dict_tool_result_is_serialized_with_json_dumps():
    spy = _SpyClient()
    ans, called = run_with_tools(
        spy,
        'Check order status for "1042"',
        [ORDER_TOOL],
        {"lookup_order": _lookup_order},
    )
    assert called == ["lookup_order"]
    assert "shipped" in ans
    tool_msgs = [m for m in spy.chat_calls[1] if m["role"] == "tool"]
    assert isinstance(tool_msgs[0]["content"], str)
    expected = {"order_id": "1042", "status": "shipped", "eta_days": 2}
    assert json.loads(tool_msgs[0]["content"]) == expected


def test_stops_after_max_rounds_on_repeated_tool_calls():
    client = FakeLLM(script=[
        {"tool_calls": [{"name": "get_weather", "arguments": {"city": "Hanoi"}}]}
    ] * 5)
    ans, called = run_with_tools(
        client,
        "Weather in Hanoi?",
        [WEATHER_TOOL],
        {"get_weather": _get_weather},
        max_rounds=2,
    )
    assert "stopped" in ans.lower()
    assert called == ["get_weather", "get_weather"]


def test_spy_checks_assistant_before_tool_and_tool_call_id():
    spy = _SpyClient()
    run_with_tools(
        spy,
        "What is the weather in Hanoi?",
        [WEATHER_TOOL],
        {"get_weather": _get_weather},
    )
    assert len(spy.chat_calls) == 2
    second_call_msgs = spy.chat_calls[1]
    assert second_call_msgs[0]["role"] == "user"
    assert second_call_msgs[1]["role"] == "assistant"
    assert second_call_msgs[1]["content"] is None
    assert len(second_call_msgs[1]["tool_calls"]) == 1
    first_tc = second_call_msgs[1]["tool_calls"][0]
    tc_id = first_tc["id"] if isinstance(first_tc, dict) else first_tc.id
    assert second_call_msgs[2]["role"] == "tool"
    assert second_call_msgs[2]["tool_call_id"] == tc_id


def test_return_type_and_inputs_not_mutated():
    tools = [dict(WEATHER_TOOL)]
    registry = {"get_weather": _get_weather}
    tools_snapshot = json.loads(json.dumps(tools))
    registry_snapshot = dict(registry)

    res = run_with_tools(FakeLLM(), "What is the weather in Hanoi?", tools, registry)
    assert isinstance(res, tuple) and len(res) == 2
    assert isinstance(res[0], str)
    assert isinstance(res[1], list)
    assert all(isinstance(name, str) for name in res[1])
    assert tools == tools_snapshot
    assert registry == registry_snapshot
