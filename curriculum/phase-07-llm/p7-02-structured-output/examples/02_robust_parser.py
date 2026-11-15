# Robustly parse JSON objects from noisy LLM replies (fences, prose, truncated text).
import json

from pyai_llm import FakeLLM


def extract_json(text: str) -> dict:
    """Extract and parse a JSON object from text, raising ValueError on failure."""
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end < start:
        raise ValueError("no JSON object found in reply")
    snippet = text[start : end + 1]
    try:
        data = json.loads(snippet)
    except json.JSONDecodeError as err:
        raise ValueError(f"invalid JSON: {err.msg}") from err
    if not isinstance(data, dict):
        raise ValueError("parsed JSON is not an object")
    return data


scripted_replies = [
    '{"name": "Lan", "order_id": 1042}',
    '```json\n{"name": "Minh", "order_id": 2088}\n```',
    'Sure! Here is the JSON: {"name": "An", "order_id": 3100}',
    '{"name": "Lan", "order_id": }',
    "Sorry, I do not have that information.",
]

client = FakeLLM(script=scripted_replies)
for idx in range(1, len(scripted_replies) + 1):
    raw = client.chat([{"role": "user", "content": "extract ticket"}]).content or ""
    try:
        parsed = extract_json(raw)
        print(f"Reply {idx}: ok -> {parsed}")
    except ValueError as err:
        print(f"Reply {idx}: error -> {err}")
