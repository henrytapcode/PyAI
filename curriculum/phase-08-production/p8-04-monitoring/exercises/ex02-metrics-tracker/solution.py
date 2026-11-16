import math
from dataclasses import dataclass


@dataclass
class _RequestMetric:
    latency_ms: float
    cost_usd: float
    ok: bool


class MetricsTracker:
    """Track LLM request latency, token costs, error rate, and threshold alerts.

    Example:
        tracker = MetricsTracker(0.001, 0.002)
        tracker.record(250.0, 1000, 500)  # -> 0.002
        tracker.summary()
        # -> {"count": 1, "error_rate": 0.0, "p95_ms": 250.0, "total_cost": 0.002}
    """

    def __init__(self, price_in_per_1k: float, price_out_per_1k: float) -> None:
        self.price_in_per_1k = price_in_per_1k
        self.price_out_per_1k = price_out_per_1k
        self._records: list[_RequestMetric] = []

    def record(
        self,
        latency_ms: float,
        prompt_tokens: int,
        completion_tokens: int,
        ok: bool = True,
    ) -> float:
        """Record one request (including failures) and return its cost in USD."""
        cost = (
            (prompt_tokens / 1000) * self.price_in_per_1k
            + (completion_tokens / 1000) * self.price_out_per_1k
        )
        self._records.append(_RequestMetric(latency_ms=float(latency_ms), cost_usd=cost, ok=ok))
        return cost

    def summary(self) -> dict[str, float | int]:
        """Return count, error_rate, nearest-rank p95_ms, and total_cost (6 decimals)."""
        if not self._records:
            return {"count": 0, "error_rate": 0.0, "p95_ms": 0.0, "total_cost": 0.0}
        count = len(self._records)
        ordered = sorted(r.latency_ms for r in self._records)
        rank = math.ceil(0.95 * count)
        errors = sum(1 for r in self._records if not r.ok)
        total_cost = sum(r.cost_usd for r in self._records)
        return {
            "count": count,
            "error_rate": errors / count,
            "p95_ms": ordered[rank - 1],
            "total_cost": round(total_cost, 6),
        }

    def alerts(
        self,
        max_p95_ms: float,
        budget: float,
        warn_ratio: float = 0.8,
    ) -> list[str]:
        """Return triggered alert codes in fixed order, or [] when healthy."""
        stats = self.summary()
        triggered: list[str] = []
        if stats["p95_ms"] > max_p95_ms:
            triggered.append("p95-latency")
        if stats["total_cost"] > budget:
            triggered.append("budget-exceeded")
        elif stats["total_cost"] >= warn_ratio * budget:
            triggered.append("budget-warning")
        if stats["error_rate"] > 0.05:
            triggered.append("error-rate")
        return triggered
