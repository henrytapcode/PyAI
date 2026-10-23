import json

UNKNOWN = {"label": "unknown", "score": 0.0}


def parse_reply(text):
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return dict(UNKNOWN)

    if not isinstance(data, dict) or "label" not in data or "score" not in data:
        return dict(UNKNOWN)

    score = data["score"]
    if not isinstance(score, (int, float)) or score < 0 or score > 1:
        return dict(UNKNOWN)
    return {"label": data["label"], "score": score}


def count_unknown(replies):
    count = 0
    for reply in replies:
        if parse_reply(reply)["label"] == "unknown":
            count += 1
    return count
