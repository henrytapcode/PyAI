# Retry invalid structured replies with error feedback, then fall back safely.
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


def validate_reply(data: dict, schema: dict) -> list[str]:
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


def get_structured(
    client: FakeLLM,
    messages: list[dict[str, str]],
    schema: dict,
    max_attempts: int = 3,
) -> dict:
    history = [dict(m) for m in messages]
    for attempt in range(1, max_attempts + 1):
        reply = client.chat(
            history,
            response_format={"type": "json", "schema": schema},
        ).content or ""
        try:
            start = reply.index("{")
            end = reply.rindex("}")
            data = json.loads(reply[start : end + 1])
            errors = validate_reply(data, schema) if isinstance(data, dict) else ["expected JSON object"]
        except (ValueError, json.JSONDecodeError) as err:
            errors = [f"parse error: {err}"]
            data = {}
        if not errors:
            print(f"Attempt {attempt}: valid")
            return data
        print(f"Attempt {attempt}: invalid ({'; '.join(errors)})")
        history.append({"role": "assistant", "content": reply})
        history.append({
            "role": "user",
            "content": f"Your JSON was invalid: {'; '.join(errors)}. Return only JSON.",
        })
    print(f"Falling back after {max_attempts} failed attempts")
    return {"name": "unknown", "order_id": 0, "urgent": False, "needs_review": True}


prompt = [{"role": "user", "content": "name: Lan, order_id: 1042, urgent: yes"}]

print("--- Run 1: recovers on attempt 2 ---")
recover_client = FakeLLM(script=[
    '{"name": "Lan", "order_id": "bad", "urgent": true}',
    '{"name": "Lan", "order_id": 1042, "urgent": true}',
])
print("Result:", get_structured(recover_client, prompt, TICKET_SCHEMA, max_attempts=3))

print("--- Run 2: falls back after 3 failures ---")
failing_client = FakeLLM(script=[
    "Sure, here you go!",
    '{"name": "Lan"}',
    '{"name": "Lan", "order_id": true, "urgent": false}',
])
print("Result:", get_structured(failing_client, prompt, TICKET_SCHEMA, max_attempts=3))
