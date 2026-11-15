import json
import pytest
from exercise import ToolBox


@pytest.fixture
def sample_schemas() -> dict[str, dict]:
    return {
        "lookup": {
            "name": "lookup_order",
            "description": "Look up an order by id",
            "parameters": {
                "type": "object",
                "properties": {"order_id": {"type": "string"}, "verbose": {"type": "boolean"}},
                "required": ["order_id"],
            },
        },
        "policy": {
            "name": "check_policy",
            "description": "Check policy rules",
            "parameters": {
                "type": "object",
                "properties": {"days_late": {"type": "integer"}, "tier": {"type": "string"}},
                "required": ["days_late", "tier"],
            },
        },
        "refund": {
            "name": "issue_refund",
            "description": "Issue refund for order",
            "parameters": {
                "type": "object",
                "properties": {"order_id": {"type": "string"}, "amount": {"type": "number"}},
                "required": ["order_id", "amount"],
            },
        },
    }


def test_register_and_schemas_preserves_order(sample_schemas):
    box = ToolBox()
    box.register(lambda order_id: order_id, sample_schemas["lookup"])
    box.register(lambda days_late, tier: tier, sample_schemas["policy"])
    box.register(lambda order_id, amount: amount, sample_schemas["refund"], side_effect=True)
    got = box.schemas()
    assert isinstance(got, list)
    assert [s["name"] for s in got] == ["lookup_order", "check_policy", "issue_refund"]


def test_register_duplicate_name_raises_value_error(sample_schemas):
    box = ToolBox()
    box.register(lambda order_id: order_id, sample_schemas["lookup"])
    with pytest.raises(ValueError):
        box.register(lambda order_id: "other", sample_schemas["lookup"])


def test_schemas_returns_independent_copy(sample_schemas):
    box = ToolBox()
    box.register(lambda order_id: order_id, sample_schemas["lookup"])
    copy_one = box.schemas()
    assert isinstance(copy_one, list) and len(copy_one) == 1
    copy_one[0]["name"] = "tampered"
    copy_one[0]["parameters"]["required"].append("injected")
    copy_one.clear()
    copy_two = box.schemas()
    assert copy_two[0]["name"] == "lookup_order"
    assert copy_two[0]["parameters"]["required"] == ["order_id"]


def test_is_side_effect_flag_and_unknown_tool(sample_schemas):
    box = ToolBox()
    box.register(lambda order_id: order_id, sample_schemas["lookup"], side_effect=False)
    box.register(lambda order_id, amount: amount, sample_schemas["refund"], side_effect=True)
    assert box.is_side_effect("lookup_order") is False
    assert box.is_side_effect("issue_refund") is True
    assert box.is_side_effect("nonexistent_tool") is False


def test_call_serializes_dict_and_list_as_json(sample_schemas):
    box = ToolBox()
    box.register(lambda order_id: {"order_id": order_id, "days": 4}, sample_schemas["lookup"])
    box.register(lambda days_late, tier: [days_late, tier], sample_schemas["policy"])
    dict_out = box.call("lookup_order", {"order_id": "1042"})
    list_out = box.call("check_policy", {"days_late": 0, "tier": "vip"})
    assert json.loads(dict_out) == {"order_id": "1042", "days": 4}
    assert json.loads(list_out) == [0, "vip"]


def test_call_converts_scalar_result_to_str(sample_schemas):
    box = ToolBox()
    box.register(lambda order_id: 42, sample_schemas["lookup"])
    assert box.call("lookup_order", {"order_id": "1042"}) == "42"


def test_call_unknown_tool_returns_error_message(sample_schemas):
    box = ToolBox()
    box.register(lambda order_id: order_id, sample_schemas["lookup"])
    assert box.call("drop_orders", {"order_id": "1042"}) == "error: unknown tool drop_orders"


def test_call_missing_required_reports_first_in_schema_order(sample_schemas):
    box = ToolBox()
    box.register(lambda days_late, tier: tier, sample_schemas["policy"])
    assert box.call("check_policy", {}) == "error: missing days_late"
    res = box.call("check_policy", {"days_late": None, "tier": "std"})
    assert res == "error: missing days_late"
    assert box.call("check_policy", {"days_late": 3, "tier": ""}) == "error: missing tier"


def test_call_drops_unknown_args_without_mutating_caller_dict(sample_schemas):
    received = {}

    def record(order_id: str, verbose: bool = False) -> str:
        received["kwargs"] = {"order_id": order_id, "verbose": verbose}
        return "ok"

    box = ToolBox()
    box.register(record, sample_schemas["lookup"])
    caller_args = {"order_id": "1042", "confirmed": True, "role": "admin"}
    snapshot = dict(caller_args)
    assert box.call("lookup_order", caller_args) == "ok"
    assert received["kwargs"] == {"order_id": "1042", "verbose": False}
    assert caller_args == snapshot


def test_call_catches_tool_exception_as_error_string(sample_schemas):
    def strict_refund(order_id: str, amount: float) -> str:
        if amount <= 0:
            raise ValueError("amount must be positive")
        return f"refunded {order_id}"

    box = ToolBox()
    box.register(strict_refund, sample_schemas["refund"], side_effect=True)
    res = box.call("issue_refund", {"order_id": "1042", "amount": -5})
    assert res == "error: amount must be positive"
