# Parse model replies that should be JSON, and fall back when they are not.
import json


def parse_reply(text):
    try:
        data = json.loads(text)
        return {"label": data["label"], "score": data["score"]}
    except json.JSONDecodeError as err:
        print("  not valid JSON:", err.msg)
    except (KeyError, TypeError):
        print("  JSON is missing a field")
    return {"label": "unknown", "score": 0.0}


replies = [
    '{"label": "spam", "score": 0.97}',
    "Sure! Here is the JSON you asked for.",
    '{"label": "ham"}',
    '{"label": "ham", "score": 0.88}',
]

for reply in replies:
    print("reply:", reply[:30])
    result = parse_reply(reply)
    print("  ->", result)
