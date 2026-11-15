import numpy as np


def top_k(
    query: str,
    docs: list[str],
    client,
    k: int = 2,
    min_score: float = 0.0,
) -> list[tuple[int, float]]:
    """Rank docs by cosine similarity to query and return top-k (index, score) pairs.

    Example: top_k("affordable automobile", ["cheap car"], client, k=1) -> [(0, 0.816)]
    """
    # TODO: return [] on empty docs, batch-embed docs, score with D @ q, sort & filter
    return None
