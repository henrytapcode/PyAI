import json

from pyai_llm import FakeLLM


_TYPE_MAP: dict[str, type | tuple[type, ...]] = {
    "string": str,
    "integer": int,
    "number": (int, float),
    "boolean": bool,
}


def _field_error(key: str, value: object, spec: dict) -> str | None:
    expected_type = spec.get("type", "")
    if expected_type in ("integer", "number") and isinstance(value, bool):
        return f"wrong type: {key}"
    expected = _TYPE_MAP.get(expected_type)
    if expected is not None and not isinstance(value, expected):
        return f"wrong type: {key}"
    return None


def _check_reply(data: dict, schema: dict) -> list[str]:
    """Validate required keys and primitive types against schema."""
    errors = [f"missing: {key}" for key in schema.get("required", []) if key not in data]
    for key, spec in schema.get("properties", {}).items():
        if key in data:
            err = _field_error(key, data[key], spec)
            if err is not None:
                errors.append(err)
    return errors


def parse_reply(text: str) -> dict:
    """Extract JSON from the first '{' to the last '}' and parse it as a dict.

    Example: parse_reply('```json\\n{"name": "Lan"}\\n```') -> {"name": "Lan"}
    """
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end < start:
        raise ValueError("no JSON object found in reply")
    return json.loads(text[start : end + 1])


def get_ticket(
    client: FakeLLM,
    messages: list[dict[str, str]],
    schema: dict,
    max_attempts: int = 3,
) -> tuple[dict | None, int]:
    """Call client with JSON response_format, retrying with error feedback up to max_attempts.

    Example: get_ticket(FakeLLM(), [{"role": "user", "content": "name: Lan"}], schema) -> (..., 1)
    """
    history = [dict(m) for m in messages]
    for attempt in range(1, max_attempts + 1):
        raw = (
            client.chat(
                history,
                response_format={"type": "json", "schema": schema},
            ).content
            or ""
        )
        try:
            data = parse_reply(raw)
            errors = _check_reply(data, schema)
        except ValueError as err:
            errors = [str(err)]
            data = {}
        if not errors:
            return data, attempt
        history.append({"role": "assistant", "content": raw})
        history.append({
            "role": "user",
            "content": f"Your JSON was invalid: {'; '.join(errors)}. Return only JSON.",
        })
    return None, max_attempts
