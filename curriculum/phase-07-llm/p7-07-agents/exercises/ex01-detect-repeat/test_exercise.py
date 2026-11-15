import pytest
from exercise import is_repeat


@pytest.mark.parametrize(
    ("history", "name", "args", "expected"),
    [
        ([], "lookup_order", {"order_id": "1042"}, False),
        (
            [("lookup_order", {"order_id": "1042"})],
            "estimate_delivery",
            {"order_id": "1042"},
            False,
        ),
        (
            [("lookup_order", {"order_id": "1042"})],
            "lookup_order",
            {"order_id": "1043"},
            False,
        ),
        (
            [("lookup_order", {"order_id": "1042"})],
            "lookup_order",
            {"order_id": "1042"},
            True,
        ),
        (
            [
                ("lookup_order", {"order_id": "1042"}),
                ("estimate_delivery", {"carrier": "FastPost"}),
            ],
            "lookup_order",
            {"order_id": "1042"},
            False,
        ),
        (
            [("issue_refund", {"order_id": "1042", "amount": 45.0})],
            "issue_refund",
            {"amount": 45.0, "order_id": "1042"},
            True,
        ),
    ],
    ids=[
        "empty_history",
        "different_tool_name",
        "same_tool_different_args",
        "identical_to_last_step",
        "matches_older_step_not_last",
        "dict_key_order_ignored",
    ],
)
def test_is_repeat_cases(history, name, args, expected):
    assert is_repeat(history, name, args) is expected
