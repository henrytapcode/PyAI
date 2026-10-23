from functools import wraps

CALL_LOG = []


def record_calls(func):
    """Record each call as (function name, positional arguments) in CALL_LOG, then run func.

    Example: after add(2, 3) the log is [("add", (2, 3))] and add(2, 3) still returns 5.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        CALL_LOG.append((func.__name__, args))
        return func(*args, **kwargs)

    return wrapper
