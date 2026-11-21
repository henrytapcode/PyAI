def _hit_rate_at_k(results: list[dict], k: int) -> float:
    scored = [row for row in results if row["expected_source"] is not None]
    if not scored:
        return 0.0
    hits = sum(1 for row in scored if row["expected_source"] in row["retrieved"][:k])
    return round(hits / len(scored), 3)


def hit_rates(results: list[dict], ks: list[int]) -> dict[int, float]:
    """Compute retrieval hit@k rounded to 3 decimals for each k in ks.

    Example:
        hit_rates([{"expected_source": "a.md", "retrieved": ["b.md", "a.md"]}], [1, 2])
        -> {1: 0.0, 2: 1.0}
    """
    rates: dict[int, float] = {}
    for k in ks:
        if k <= 0:
            raise ValueError(f"k must be positive, got {k}")
        rates[k] = _hit_rate_at_k(results, k)
    return rates
