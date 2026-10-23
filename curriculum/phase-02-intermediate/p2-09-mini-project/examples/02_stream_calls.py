# Stage 2: stream expensive calls lazily with a generator; a decorator logs every parse.
from functools import wraps


def logged(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print("  parsed", args[0], "->", result)
        return result

    return wrapper


@logged
def parse_line(line):
    model, cost = line.split(",")
    return (model, float(cost))


def expensive_calls(lines, limit):
    for line in lines:
        model, cost = parse_line(line)
        if cost >= limit:
            yield model, cost


lines = ["small,0.01", "large,0.40", "small,0.02", "large,0.55", "small,0.03"]

stream = expensive_calls(lines, 0.30)
print("nothing parsed yet")
print("first:", next(stream))
print("second:", next(stream))
print("name kept by wraps:", parse_line.__name__)
