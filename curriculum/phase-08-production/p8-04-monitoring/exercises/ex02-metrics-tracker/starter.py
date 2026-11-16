class MetricsTracker:
    """Track LLM request latency, token costs, error rate, and threshold alerts.

    Example:
        tracker = MetricsTracker(0.001, 0.002)
        tracker.record(250.0, 1000, 500)  # -> 0.002
        tracker.summary()
        # -> {"count": 1, "error_rate": 0.0, "p95_ms": 250.0, "total_cost": 0.002}
    """

    def __init__(self, price_in_per_1k: float, price_out_per_1k: float) -> None:
        # TODO: store token prices and initialize storage for recorded requests
        pass

    def record(
        self,
        latency_ms: float,
        prompt_tokens: int,
        completion_tokens: int,
        ok: bool = True,
    ) -> float | None:
        """Record one request (including failures) and return its cost in USD."""
        # TODO: compute request cost, save record, and return the cost
        return None

    def summary(self) -> dict[str, float | int] | None:
        """Return count, error_rate, nearest-rank p95_ms, and total_cost (6 decimals)."""
        # TODO: return zeroed summary when empty, otherwise aggregate stored records
        return None

    def alerts(
        self,
        max_p95_ms: float,
        budget: float,
        warn_ratio: float = 0.8,
    ) -> list[str] | None:
        """Return triggered alert codes in fixed order, or [] when healthy."""
        # TODO: check p95-latency, budget-exceeded / budget-warning, and error-rate
        return None
