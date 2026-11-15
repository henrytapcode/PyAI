# Extract structured Ticket dataclasses from customer emails using FakeLLM.
from dataclasses import dataclass
import json

from pyai_llm import FakeLLM

TICKET_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "order_id": {"type": "integer"},
        "urgent": {"type": "boolean"},
    },
    "required": ["name", "order_id", "urgent"],
}


@dataclass
class Ticket:
    name: str
    order_id: int
    urgent: bool

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("missing customer name")
        if self.order_id <= 0:
            raise ValueError("order_id must be positive")


def validate_ticket_dict(data: dict, schema: dict) -> list[str]:
    type_map = {"string": str, "integer": int, "number": (int, float), "boolean": bool}
    errors: list[str] = []
    for key in schema.get("required", []):
        if key not in data:
            errors.append(f"missing: {key}")
    for key, spec in schema.get("properties", {}).items():
        if key not in data:
            continue
        expected_type = spec.get("type", "")
        value = data[key]
        if expected_type in ("integer", "number") and isinstance(value, bool):
            errors.append(f"wrong type: {key}")
            continue
        expected = type_map.get(expected_type)
        if expected is not None and not isinstance(value, expected):
            errors.append(f"wrong type: {key}")
    return errors


emails = [
    "name: Lan, order_id: 1042, urgent: yes. Package arrived damaged.",
    "Hi team, my package is late. Please check soon.",
    "name is Minh, order_id is 2088, urgent: no. Need a PDF invoice.",
]

client = FakeLLM()
for idx, email in enumerate(emails, start=1):
    resp = client.chat(
        [{"role": "user", "content": email}],
        response_format={"type": "json", "schema": TICKET_SCHEMA},
    )
    raw = resp.content or ""
    data = json.loads(raw)
    schema_errors = validate_ticket_dict(data, TICKET_SCHEMA)
    if schema_errors:
        print(f"Email {idx}: rejected ({'; '.join(schema_errors)})")
        continue
    try:
        ticket = Ticket(**data)
        print(f"Email {idx}: {ticket}")
    except ValueError as err:
        print(f"Email {idx}: rejected ({err})")
