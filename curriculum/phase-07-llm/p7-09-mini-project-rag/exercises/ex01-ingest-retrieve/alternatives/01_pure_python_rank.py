import re

from pyai_llm import cosine


def build_index(
    docs: list[dict],
    client,
    mode: str = "sentence",
    size: int = 8,
    overlap: int = 2,
) -> dict:
    """Chunk docs and store plain Python embedding lists without NumPy."""
    if mode not in ("sentence", "words"):
        raise ValueError(f"unsupported mode: {mode}")
    if mode == "words" and (size <= 0 or overlap < 0 or overlap >= size):
        raise ValueError("need size > 0 and 0 <= overlap < size")
    chunks: list[dict] = []
    for doc in docs:
        cleaned = doc["text"].strip()
        if not cleaned:
            continue
        if mode == "sentence":
            pieces = [s.strip() for s in re.split(r"(?<=[.!?])\s+", cleaned) if s.strip()]
        else:
            words = cleaned.split()
            step = size - overlap
            pieces = [
                " ".join(words[i : i + size])
                for i in range(0, len(words), step)
                if i == 0 or i + size - step < len(words)
            ]
        for idx, text in enumerate(pieces):
            chunks.append({"id": f"{doc['source']}#{idx}", "source": doc["source"], "text": text})
    vectors = client.embed([c["text"] for c in chunks]) if chunks else []
    return {"chunks": chunks, "vectors": vectors}


def retrieve(
    index: dict,
    question: str,
    client,
    k: int = 2,
    min_score: float = 0.2,
) -> list[dict]:
    """Rank chunks using pure Python cosine() and sorted() without NumPy."""
    chunks = index["chunks"]
    if not chunks or k <= 0:
        return []
    q_vec = client.embed([question])[0]
    scored = [
        (cosine(vec, q_vec), idx)
        for idx, vec in enumerate(index["vectors"])
    ]
    scored.sort(key=lambda item: (-item[0], item[1]))
    hits: list[dict] = []
    for score, idx in scored[:k]:
        if score >= min_score:
            chunk = chunks[idx]
            hits.append(
                {
                    "id": chunk["id"],
                    "source": chunk["source"],
                    "text": chunk["text"],
                    "score": round(float(score), 3),
                }
            )
    return hits
