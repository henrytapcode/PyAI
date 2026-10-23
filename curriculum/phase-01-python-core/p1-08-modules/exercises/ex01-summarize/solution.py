import math
import statistics


def summarize(values):
    """Return a dict with count, mean, median and stdev (rounded to 2 decimals)."""
    return {
        "count": len(values),
        "mean": statistics.mean(values),
        "median": statistics.median(values),
        "stdev": round(statistics.stdev(values), 2),
    }


def same_average(a, b):
    """Return True if the averages of lists a and b are (practically) equal."""
    return math.isclose(statistics.mean(a), statistics.mean(b))
