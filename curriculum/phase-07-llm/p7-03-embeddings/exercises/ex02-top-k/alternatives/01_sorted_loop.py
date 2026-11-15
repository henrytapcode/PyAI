from pyai_llm import cosine


def top_k(
    query: str,
    docs: list[str],
    client,
    k: int = 2,
    min_score: float = 0.0,
) -> list[tuple[int, float]]:
    """Rank docs using pyai_llm.cosine in a Python loop and sorted()."""
    if not docs or k <= 0:
        return []

    doc_vecs = client.embed(docs)
    query_vec = client.embed([query])[0]

    scored: list[tuple[int, float]] = []
    for idx, vec in enumerate(doc_vecs):
        score = round(float(cosine(vec, query_vec)), 3)
        if score >= min_score:
            scored.append((idx, score))

    scored.sort(key=lambda pair: (-pair[1], pair[0]))
    return scored[:k]
