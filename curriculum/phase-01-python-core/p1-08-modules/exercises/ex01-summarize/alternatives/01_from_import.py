from math import isclose
from statistics import mean, median, stdev


def summarize(values):
    return {
        "count": len(values),
        "mean": mean(values),
        "median": median(values),
        "stdev": round(stdev(values), 2),
    }


def same_average(a, b):
    return isclose(mean(a), mean(b))
