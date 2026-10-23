from functools import wraps


def retry(times):
    """Return a decorator that calls the function up to `times` times until it works.

    Example:
        @retry(3)
        def ask_llm(prompt): ...

    If the first two calls raise an error and the third returns "ok", ask_llm(...) returns "ok".
    If all 3 calls raise an error, the error of the last call is raised.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _attempt in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception as error:
                    last_error = error
            raise last_error

        return wrapper

    return decorator
