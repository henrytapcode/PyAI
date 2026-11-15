import re

import numpy as np


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
    context = "\n".join(f"[{n}] {h['text']}" for n, h in enumerate(hits, 1))
    messages = [
        {
            "role": "system",
            "content": (
                "Answer using only the provided context. "
                "If the answer is not there, say \"I don't know.\" "
                "Cite sources with [n].\n\n"
                f"Context:\n{context}"
            ),
        },
        {"role": "user", "content": question},
    ]
    answer = client.chat(messages).content or ""

    sources: list[str] = []
    for raw in re.findall(r"\[(\d+)\]", answer):
        idx = int(raw) - 1
        if 0 <= idx < len(hits):
            src = hits[idx]["source"]
            if src not in sources:
                sources.append(src)
    return {"answer": answer, "sources": sources}
