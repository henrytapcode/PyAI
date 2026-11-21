import re

import numpy as np


def _split_words(cleaned: str, size: int, overlap: int) -> list[str]:
    if size <= 0 or overlap < 0 or overlap >= size:
        raise ValueError("need size > 0 and 0 <= overlap < size")
    words = cleaned.split()
    step = size - overlap
    pieces: list[str] = []
    pos = 0
    while pos < len(words):
        pieces.append(" ".join(words[pos : pos + size]))
        if pos + size >= len(words):
            break
        pos += step
    return pieces


def _split_doc(text: str, mode: str, size: int, overlap: int) -> list[str]:
    if not (cleaned := text.strip()):
        return []
    if mode == "sentence":
        parts = re.split(r"(?<=[.!?])\s+", cleaned)
        return [s.strip() for s in parts if s.strip()]
    return _split_words(cleaned, size, overlap)


def build_index(
    docs: list[dict],
    client,
    mode: str = "sentence",
    size: int = 8,
    overlap: int = 2,
) -> dict:
    """Chunk docs by sentence or word window and embed all chunks once."""
    if mode not in ("sentence", "words"):
        raise ValueError(f"unsupported mode: {mode}")
    chunks: list[dict] = []
    for doc in docs:
        pieces = _split_doc(doc["text"], mode, size, overlap)
        for idx, text in enumerate(pieces):
            chunks.append({"id": f"{doc['source']}#{idx}", "source": doc["source"], "text": text})
    vectors = (
        np.array(client.embed([c["text"] for c in chunks]), dtype=float)
        if chunks
        else np.empty((0, 0), dtype=float)
    )
    return {"chunks": chunks, "vectors": vectors}


def retrieve(
    index: dict,
    question: str,
    client,
    k: int = 2,
    min_score: float = 0.2,
) -> list[dict]:
    """Embed question, rank index chunks stably, and filter by min_score."""
    if not index["chunks"] or k <= 0:
        return []
    q_vec = np.array(client.embed([question])[0], dtype=float)
    scores = index["vectors"] @ q_vec
    order = np.argsort(-scores, kind="stable")[:k]
    hits: list[dict] = []
    for idx in order:
        score = float(scores[int(idx)])
        if score >= min_score:
            chunk = index["chunks"][int(idx)]
            hits.append(
                {
                    "id": chunk["id"],
                    "source": chunk["source"],
                    "text": chunk["text"],
                    "score": round(score, 3),
                }
            )
    return hits
