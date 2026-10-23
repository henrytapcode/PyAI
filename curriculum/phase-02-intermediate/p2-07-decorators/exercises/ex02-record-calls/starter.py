"""A decorator that records every call. It has bugs: find and fix them.

Run the tests, read each failure, and fix the decorator.
"""

CALL_LOG = []


def record_calls(func):
    """Record each call as (function name, positional arguments) in CALL_LOG, then run func.

    Example: after add(2, 3) the log is [("add", (2, 3))] and add(2, 3) still returns 5.
    """

    def wrapper(*args, **kwargs):
        CALL_LOG.append((func.__name__, args))
        func(*args)

    return wrapper
