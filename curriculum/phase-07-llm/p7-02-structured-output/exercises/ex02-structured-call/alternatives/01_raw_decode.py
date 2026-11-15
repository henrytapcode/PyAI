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
    """Decode the first JSON object starting at '{' using JSONDecoder.raw_decode."""
    start = text.find("{")
    if start == -1:
        raise ValueError("no JSON object found in reply")
    decoder = json.JSONDecoder()
    data, _ = decoder.raw_decode(text, start)
    return data


def get_ticket(
    client: FakeLLM,
    messages: list[dict[str, str]],
    schema: dict,
    max_attempts: int = 3,
) -> tuple[dict | None, int]:
    """Retry structured JSON calls with error feedback without mutating messages."""
    history = list(messages)
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
        history = [
            *history,
            {"role": "assistant", "content": raw},
            {
                "role": "user",
                "content": f"Your JSON was invalid: {'; '.join(errors)}. Return only JSON.",
            },
        ]
    return None, max_attempts
