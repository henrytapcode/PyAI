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
        hits = 0
        total = 0
        for row in results:
            expected = row["expected_source"]
            if expected is None:
                continue
            total += 1
            if expected in row["retrieved"][:k]:
                hits += 1
        rates[k] = round(hits / total, 3) if total else 0.0
    return rates
