def hit_rate(results: list[dict], k: int) -> float:
    """Compute retrieval hit@k across answerable eval rows.

    Example: hit_rate([{"expected_source": "a.md", "retrieved": ["a.md"]}], 1) -> 1.0
    """
    # TODO: replace each ___ blank to skip None targets, check top-k, and divide safely
    if k <= 0:
        return 0.0
    hits = 0
    total = 0
    for row in results:
        expected = row["expected_source"]
        if ___:
            continue
        total += 1
        if expected in ___:
            hits += 1
    return ___
