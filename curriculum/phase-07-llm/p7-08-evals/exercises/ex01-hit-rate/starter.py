def hit_rates(results: list[dict], ks: list[int]) -> dict[int, float]:
    """Compute retrieval hit@k rounded to 3 decimals for each k in ks.

    Example:
        hit_rates([{"expected_source": "a.md", "retrieved": ["b.md", "a.md"]}], [1, 2])
        -> {1: 0.0, 2: 1.0}
    """
    # TODO: replace each ___ blank to validate each k, collect rates, and round to 3 decimals
    rates: dict[int, float] = ___
    for k in ks:
        if ___:
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
        rates[k] = ___
    return rates
