import re

import numpy as np


def _retrieve(question: str, chunks: list[dict], client, k: int) -> tuple[list[dict], float]:
    all_vecs = np.array(client.embed([c["text"] for c in chunks] + [question]), dtype=float)
    doc_matrix, q_vec = all_vecs[:-1], all_vecs[-1]
    scores = doc_matrix @ q_vec
    order = np.argsort(-scores, kind="stable")[:k]
    hits = [chunks[int(i)] for i in order]
    return hits, float(scores[int(order[0])])


def _build_messages(question: str, hits: list[dict]) -> list[dict]:
    context = "\n".join(f"[{n}] {h['text']}" for n, h in enumerate(hits, 1))
    system = (
        "Answer using only the provided context.\n"
        "If the context lacks the answer, say \"I don't know.\"\n"
        "Cite sources with [n].\n\n"
        f"Context:\n{context}"
    )
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": question},
    ]


def answer_with_sources(
    question: str,
    chunks: list[dict],
    client,
    k: int = 2,
    min_score: float = 0.2,
) -> dict:
    """Retrieve top-k chunks, build a grounded prompt, and return answer + unique sources."""
    if not chunks or k <= 0:
        return {"answer": "I don't know.", "sources": []}
    hits, best_score = _retrieve(question, chunks, client, k)
    if best_score < min_score:
        return {"answer": "I don't know.", "sources": []}
    answer = client.chat(_build_messages(question, hits)).content or ""
    ordered = [
        hits[int(n) - 1]["source"]
        for n in re.findall(r"\[(\d+)\]", answer)
        if 1 <= int(n) <= len(hits)
    ]
    return {"answer": answer, "sources": list(dict.fromkeys(ordered))}
