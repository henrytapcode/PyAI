import re

import numpy as np


def _build_messages(question: str, hits: list[dict]) -> list[dict[str, str]]:
    context = "\n".join(f"[{n}] {hit['text']}" for n, hit in enumerate(hits, 1))
    system_prompt = (
        'Answer using only the provided context. If the answer is not there, say "I don\'t know." '
        f"Cite sources with [n].\n\nContext:\n{context}"
    )
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question},
    ]


def _extract_sources(answer: str, hits: list[dict]) -> list[str]:
    sources: list[str] = []
    for raw in re.findall(r"\[(\d+)\]", answer):
        idx = int(raw) - 1
        if 0 <= idx < len(hits):
            src = hits[idx]["source"]
            if src not in sources:
                sources.append(src)
    return sources


def answer_with_sources(
    question: str,
    chunks: list[dict],
    client,
    k: int = 2,
    min_score: float = 0.2,
) -> dict:
    """Retrieve top-k chunks, ask client with Context:, and return answer + valid sources.

    Example:
        answer_with_sources("How many days do refunds take?", chunks, client)
        -> {"answer": "Refunds are issued within 30 days. [1]", "sources": ["refunds.md"]}
    """
    if not chunks or k <= 0:
        return {"answer": "I don't know.", "sources": []}

    doc_vecs = np.array(client.embed([c["text"] for c in chunks]), dtype=float)
    q_vec = np.array(client.embed([question])[0], dtype=float)
    scores = doc_vecs @ q_vec
    order = np.argsort(-scores, kind="stable")[:k]
    if float(scores[int(order[0])]) < min_score:
        return {"answer": "I don't know.", "sources": []}

    hits = [chunks[int(i)] for i in order]
    answer = client.chat(_build_messages(question, hits)).content or ""
    return {"answer": answer, "sources": _extract_sources(answer, hits)}
