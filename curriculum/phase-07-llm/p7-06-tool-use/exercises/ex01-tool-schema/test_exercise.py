import pytest
from exercise import tool_schema
from pyai_llm import FakeLLM


def test_returns_expected_top_level_shape():
    schema = tool_schema("get_weather", "weather city", {"city": "string"}, ["city"])
    assert set(schema) == {"name", "description", "parameters"}
    assert schema["name"] == "get_weather"
    assert schema["description"] == "weather city"
    params = schema["parameters"]
    assert params["type"] == "object"
    assert set(params) == {"type", "properties", "required"}


def test_builds_properties_from_params():
    schema = tool_schema(
        "convert_currency",
        "convert currency amount",
        {"amount": "number", "to": "string", "round_up": "boolean", "decimals": "integer"},
        ["amount", "to"],
    )
    assert schema["parameters"]["properties"] == {
        "amount": {"type": "number"},
        "to": {"type": "string"},
        "round_up": {"type": "boolean"},
        "decimals": {"type": "integer"},
    }


def test_preserves_required_order_and_copies_list():
    req = ["to", "amount"]
    schema = tool_schema(
        "convert_currency",
        "convert currency",
        {"amount": "number", "to": "string"},
        req,
    )
    assert schema["parameters"]["required"] == ["to", "amount"]
    req.append("extra")
    assert schema["parameters"]["required"] == ["to", "amount"]


def test_deduplicates_required_preserving_order():
    schema = tool_schema(
        "convert_currency",
        "convert currency",
        {"amount": "number", "to": "string"},
        ["to", "amount", "to"],
    )
    assert schema["parameters"]["required"] == ["to", "amount"]


def test_raises_value_error_for_unknown_required_field():
    with pytest.raises(ValueError):
        tool_schema("get_weather", "weather city", {"city": "string"}, ["city", "country"])


def test_raises_value_error_for_unsupported_type():
    with pytest.raises(ValueError):
        tool_schema("tag_item", "tag item", {"tags": "array"}, ["tags"])


def test_schema_works_with_fakellm_tool_selection():
    schema = tool_schema(
        "get_weather",
        "weather city temperature",
        {"city": "string", "unit": "string"},
        ["city"],
    )
    resp = FakeLLM().chat(
        [{"role": "user", "content": "What is the weather in Hanoi?"}],
        tools=[schema],
    )
    assert resp.finish_reason == "tool_calls"
    assert len(resp.tool_calls) == 1
    assert resp.tool_calls[0].name == "get_weather"
    assert resp.tool_calls[0].arguments["city"] == "Hanoi"
