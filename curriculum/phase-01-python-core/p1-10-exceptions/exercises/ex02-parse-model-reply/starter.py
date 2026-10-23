import json  # noqa: F401


def parse_reply(text):
    """Turn a model reply (JSON text) into {"label": ..., "score": ...}.

    If the reply cannot be used, return {"label": "unknown", "score": 0.0}.
    Example: parse_reply('{"label": "spam", "score": 0.9}') returns {"label": "spam", "score": 0.9}
    """
    # TODO 1: inside try, use json.loads(text) and read data["label"] and data["score"]
    # TODO 2: still inside try, raise ValueError if the score is below 0 or above 1
    # TODO 3: except (ValueError, KeyError, TypeError): return the unknown dict
    # TODO 4: after the try block, return the good dict
    return None


def count_unknown(replies):
    """Return how many replies give the unknown result.

    Example: count_unknown(['{"label": "ham", "score": 0.5}', "hello"]) returns 1
    """
    # TODO: loop over replies, call parse_reply, count labels equal to "unknown"
    return None
