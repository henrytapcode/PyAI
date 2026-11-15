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
    if not docs or k <= 0:
        return []

    doc_matrix = np.array(client.embed(docs), dtype=float)
    query_vec = np.array(client.embed([query])[0], dtype=float)
    scores = doc_matrix @ query_vec
    order = np.argsort(-scores, kind="stable")

    results: list[tuple[int, float]] = []
    for idx in order[:k]:
        score = round(float(scores[int(idx)]), 3)
        if score >= min_score:
            results.append((int(idx), score))
    return results
