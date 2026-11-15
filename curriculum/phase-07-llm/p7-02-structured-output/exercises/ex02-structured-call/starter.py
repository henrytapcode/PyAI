import json

from pyai_llm import FakeLLM


def _check_reply(data: dict, schema: dict) -> list[str]:
    """Validate required keys and primitive types against schema."""
    type_map = {
        "string": str,
        "integer": int,
        "number": (int, float),
        "boolean": bool,
    }
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


def parse_reply(text: str) -> dict:
    """Extract JSON from the first '{' to the last '}' and parse it as a dict.

    Example: parse_reply('```json\\n{"name": "Lan"}\\n```') -> {"name": "Lan"}
    """
    # TODO: slice between '{' and '}', json.loads, and raise ValueError on failure or non-dict
    return None


def get_ticket(
    client: FakeLLM,
    messages: list[dict[str, str]],
    schema: dict,
    max_attempts: int = 3,
) -> tuple[dict | None, int]:
    """Call client with JSON response_format, retrying with error feedback up to max_attempts.

    Example: get_ticket(FakeLLM(), [{"role": "user", "content": "name: Lan"}], schema) -> (..., 1)
    """
    # TODO: copy messages, loop up to max_attempts, parse + validate, append feedback on error
    return None
