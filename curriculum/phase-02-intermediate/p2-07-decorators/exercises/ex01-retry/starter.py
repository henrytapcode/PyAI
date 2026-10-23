from functools import wraps


def retry(times):
    """Return a decorator that calls the function up to `times` times until it works.

    Example:
        @retry(3)
        def ask_llm(prompt): ...

    If the first two calls raise an error and the third returns "ok", ask_llm(...) returns "ok".
    If all 3 calls raise an error, the error of the last call is raised.
    """
    # TODO 1: define decorator(func) inside retry
    # TODO 2: inside it, define wrapper(*args, **kwargs) with @wraps(func) above it
    # TODO 3: in wrapper, try the call up to `times` times; return the first result that works
    # TODO 4: if every attempt raised an error, raise the last one
    # TODO 5: return wrapper from decorator, and decorator from retry
    return None
