import pytest
from exercise import check_reply

TICKET_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "order_id": {"type": "integer"},
        "score": {"type": "number"},
        "urgent": {"type": "boolean"},
        "note": {"type": "string"},
    },
    "required": ["name", "order_id", "urgent"],
}


@pytest.mark.parametrize(
    ("data", "schema", "expected"),
    [
        (
            {"name": "Lan", "order_id": 1042, "urgent": True, "score": 4.5},
            TICKET_SCHEMA,
            [],
        ),
        (
            {"name": "Lan", "urgent": False},
            TICKET_SCHEMA,
            ["missing: order_id"],
        ),
        (
            {"name": "Lan", "order_id": "1042", "urgent": True},
            TICKET_SCHEMA,
            ["wrong type: order_id"],
        ),
        (
            {"name": "Lan", "order_id": True, "urgent": True},
            TICKET_SCHEMA,
            ["wrong type: order_id"],
        ),
        (
            {"score": 3},
            {"properties": {"score": {"type": "number"}}, "required": ["score"]},
            [],
        ),
        (
            {"name": "Lan", "order_id": 1042, "urgent": False},
            TICKET_SCHEMA,
            [],
        ),
    ],
    ids=[
        "valid_payload",
        "missing_required_key",
        "wrong_type_string_for_integer",
        "bool_rejected_for_integer",
        "int_accepted_for_number",
        "optional_key_omitted",
    ],
)
def test_check_reply(data: dict, schema: dict, expected: list[str]):
    errors = check_reply(data, schema)
    assert errors == expected, f"expected {expected!r}, got {errors!r}"
