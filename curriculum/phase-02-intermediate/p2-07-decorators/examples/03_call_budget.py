# A decorator with an argument: stop an LLM stub after too many calls.
from functools import wraps


def limit_calls(max_calls):
    def decorator(func):
        used = []

        @wraps(func)
        def wrapper(*args, **kwargs):
            if len(used) >= max_calls:
                raise RuntimeError(f"{func.__name__} budget of {max_calls} calls is used up")
            used.append(1)
            return func(*args, **kwargs)
        return wrapper
    return decorator


@limit_calls(2)
def ask_llm(prompt):
    return "answer to: " + prompt


print(ask_llm("hi"))
print(ask_llm("again"))
try:
    ask_llm("third")
except RuntimeError as error:
    print("blocked:", error)
