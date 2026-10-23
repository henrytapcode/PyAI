import json


def parse_reply(text):
    """Turn a model reply (JSON text) into {"label": ..., "score": ...}.

    If the reply cannot be used, return {"label": "unknown", "score": 0.0}.
    Example: parse_reply('{"label": "spam", "score": 0.9}') returns {"label": "spam", "score": 0.9}
    """
    try:
        data = json.loads(text)
        label = data["label"]
        score = data["score"]
        if score < 0 or score > 1:
            raise ValueError("score out of range")
    except (ValueError, KeyError, TypeError):
        return {"label": "unknown", "score": 0.0}
    return {"label": label, "score": score}


def count_unknown(replies):
    """Return how many replies give the unknown result.

    Example: count_unknown(['{"label": "ham", "score": 0.5}', "hello"]) returns 1
    """
    count = 0
    for reply in replies:
        if parse_reply(reply)["label"] == "unknown":
            count += 1
    return count
