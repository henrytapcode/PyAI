import math


def summarize(values):
    n = len(values)
    mean_value = sum(values) / n
    ordered = sorted(values)
    middle = n // 2
    if n % 2 == 1:
        median_value = ordered[middle]
    else:
        median_value = (ordered[middle - 1] + ordered[middle]) / 2
    squares = 0
    for v in values:
        squares += (v - mean_value) ** 2
    stdev_value = math.sqrt(squares / (n - 1))
    return {
        "count": n,
        "mean": mean_value,
        "median": median_value,
        "stdev": round(stdev_value, 2),
    }


def same_average(a, b):
    return math.isclose(sum(a) / len(a), sum(b) / len(b))
