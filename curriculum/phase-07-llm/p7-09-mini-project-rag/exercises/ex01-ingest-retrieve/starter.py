def build_index(
    docs: list[dict],
    client,
    mode: str = "sentence",
    size: int = 8,
    overlap: int = 2,
) -> dict:
    """Chunk docs by sentence or word window and embed all chunks once.

    Example:
        build_index([{"source": "a.md", "text": "One. Two."}], client)
        -> {"chunks": [{"id": "a.md#0", ...}, {"id": "a.md#1", ...}], "vectors": ...}
    """
    # TODO: validate mode (and size/overlap for "words"), build non-empty chunks,
    # and embed all chunk texts in a single client.embed call.
    return None


def retrieve(
    index: dict,
    question: str,
    client,
    k: int = 2,
    min_score: float = 0.2,
) -> list[dict]:
    """Embed question, rank index chunks stably, and filter by min_score.

    Example:
        retrieve(index, "How many days?", client, k=2, min_score=0.2)
        -> [{"id": "a.md#0", "source": "a.md", "text": "...", "score": 0.45}]
    """
    # TODO: embed [question], compute scores, sort stably descending,
    # take top-k with score >= min_score, and round scores to 3 decimals.
    return None
