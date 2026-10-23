from functools import wraps


def retry(times):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts_left = times
            while True:
                attempts_left -= 1
                try:
                    return func(*args, **kwargs)
                except Exception as error:
                    if attempts_left == 0:
                        raise error

        return wrapper

    return decorator
