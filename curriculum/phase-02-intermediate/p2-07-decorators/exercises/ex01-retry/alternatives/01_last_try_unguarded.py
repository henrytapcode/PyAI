from functools import wraps


def retry(times):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(times - 1):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    pass
            return func(*args, **kwargs)

        return wrapper

    return decorator
