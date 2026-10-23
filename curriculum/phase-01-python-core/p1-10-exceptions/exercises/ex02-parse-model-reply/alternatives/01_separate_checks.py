import json

UNKNOWN = {"label": "unknown", "score": 0.0}


def parse_reply(text):
    try:
        data = json.loads(text)
        label = data["label"]
        score = data["score"]
        if score < 0 or score > 1:
            return dict(UNKNOWN)
    except json.JSONDecodeError:
        return dict(UNKNOWN)
    except (KeyError, TypeError):
        return dict(UNKNOWN)
    return {"label": label, "score": score}


def count_unknown(replies):
    return sum(1 for reply in replies if parse_reply(reply)["label"] == "unknown")
