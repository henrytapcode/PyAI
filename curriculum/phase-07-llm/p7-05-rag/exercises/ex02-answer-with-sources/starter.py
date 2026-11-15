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
    # TODO: handle empty chunks / k <= 0
    # TODO: batch-embed chunks and question, rank with np.argsort(-scores, kind="stable")[:k]
    # TODO: return {"answer": "I don't know.", "sources": []} if best score < min_score
    # TODO: build [system, user] messages with Context: and [1]..[k], call client.chat
    # TODO: parse valid [n] citations in order without duplicates
    return None
