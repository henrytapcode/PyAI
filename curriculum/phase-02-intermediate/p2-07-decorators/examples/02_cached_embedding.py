# A cache decorator: remember results so a repeated (slow) call is skipped.
from functools import wraps


def cache_results(func):
    saved = {}

    @wraps(func)
    def wrapper(*args):
        if args not in saved:
            saved[args] = func(*args)
        return saved[args]
    return wrapper


calls = []


@cache_results
def embed_text(text):
    calls.append(text)
    return [len(text), text.count("a")]


print(embed_text("banana"))
print(embed_text("banana"))
print(embed_text("kiwi"))
print("real calls:", len(calls))
print(calls)
