# Time an embedding step with a decorator and keep the timings in a dict.
import time
from functools import wraps

timings = {}


def timed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        timings[func.__name__] = elapsed
        return result
    return wrapper


@timed
def embed(texts):
    """Turn each text into a tiny fake vector: [length, number of words]."""
    return [[len(text), len(text.split())] for text in texts]


vectors = embed(["hello world", "ai"])
print(vectors)
print(embed.__name__)
print(list(timings))
print("non-negative time:", timings["embed"] >= 0)
