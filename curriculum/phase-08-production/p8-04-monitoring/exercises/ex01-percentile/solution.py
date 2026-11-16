import math


def percentile(values: list[float], p: float) -> float:
    """Compute the nearest-rank p-th percentile of values (0 < p <= 100).

    Example:
        percentile([10, 20, 30, 40], 50) -> 20.0
    """
    ordered = sorted(values)
    if not values or p <= 0 or p > 100:
        raise ValueError("values must be non-empty and p must be in (0, 100]")
    rank = math.ceil(p / 100 * len(ordered))
    return float(ordered[rank - 1])


def latency_report(values: list[float]) -> dict[str, float]:
    """Return p50, p95, and max latency for a non-empty list of values.

    Example:
        latency_report([100, 200, 300]) -> {"p50": 200.0, "p95": 300.0, "max": 300.0}
    """
    return {
        "p50": percentile(values, 50),
        "p95": percentile(values, 95),
        "max": float(max(values)),
    }
