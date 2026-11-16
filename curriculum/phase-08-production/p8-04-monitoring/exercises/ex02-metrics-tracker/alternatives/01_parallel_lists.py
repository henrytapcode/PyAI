import math


class MetricsTracker:
    """Track LLM metrics using parallel lists and a running total instead of record objects."""

    def __init__(self, price_in_per_1k: float, price_out_per_1k: float) -> None:
        self.price_in_per_1k = price_in_per_1k
        self.price_out_per_1k = price_out_per_1k
        self._latencies: list[float] = []
        self._total_cost = 0.0
        self._error_count = 0

    def record(
        self,
        latency_ms: float,
        prompt_tokens: int,
        completion_tokens: int,
        ok: bool = True,
    ) -> float:
        cost = (
            (prompt_tokens / 1000) * self.price_in_per_1k
            + (completion_tokens / 1000) * self.price_out_per_1k
        )
        self._latencies.append(float(latency_ms))
        self._total_cost += cost
        if not ok:
            self._error_count += 1
        return cost

    def summary(self) -> dict[str, float | int]:
        count = len(self._latencies)
        if count == 0:
            return {"count": 0, "error_rate": 0.0, "p95_ms": 0.0, "total_cost": 0.0}
        ordered = sorted(self._latencies)
        p95_ms = ordered[math.ceil(0.95 * count) - 1]
        return {
            "count": count,
            "error_rate": self._error_count / count,
            "p95_ms": p95_ms,
            "total_cost": round(self._total_cost, 6),
        }

    def alerts(
        self,
        max_p95_ms: float,
        budget: float,
        warn_ratio: float = 0.8,
    ) -> list[str]:
        stats = self.summary()
        codes: list[str] = []
        checks = (
            (stats["p95_ms"] > max_p95_ms, "p95-latency"),
            (
                stats["total_cost"] > budget,
                "budget-exceeded",
            ),
            (
                stats["total_cost"] <= budget and stats["total_cost"] >= warn_ratio * budget,
                "budget-warning",
            ),
            (stats["error_rate"] > 0.05, "error-rate"),
        )
        for fired, code in checks:
            if fired:
                codes.append(code)
        return codes
