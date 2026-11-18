import re

import numpy as np
from pyai_llm import count_tokens

REFUSAL = "I don't know based on the provided context."
DEFAULT_SYSTEM = "Answer only from the shop FAQ context and cite sources as [n]."

_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")


def build_index(docs: list[dict], client) -> dict:
    """Split FAQ docs into sentences and embed every non-empty chunk once."""
    chunks: list[dict] = []
    for doc in docs:
        body = doc["text"].strip()
        if not body:
            continue
        sentences = [part.strip() for part in _SENTENCE_SPLIT_RE.split(body) if part.strip()]
        for idx, sentence in enumerate(sentences):
            chunks.append(
                {
                    "id": f"{doc['source']}#{idx}",
                    "source": doc["source"],
                    "text": sentence,
                }
            )
    if chunks:
        vectors = np.array(client.embed([item["text"] for item in chunks]), dtype=float)
    else:
        vectors = np.empty((0, 0), dtype=float)
    return {"chunks": chunks, "vectors": vectors}


def retrieve(
    index: dict,
    question: str,
    client,
    k: int = 2,
    min_score: float = 0.2,
) -> list[dict]:
    """Embed ``question``, rank chunks stably, and keep top-k hits >= ``min_score``."""
    if not index["chunks"] or k <= 0:
        return []
    query_vec = np.array(client.embed([question])[0], dtype=float)
    scores = index["vectors"] @ query_vec
    ranked = np.argsort(-scores, kind="stable")[:k]
    results: list[dict] = []
    for pos in ranked:
        score = float(scores[int(pos)])
        if score < min_score:
            continue
        chunk = index["chunks"][int(pos)]
        results.append(
            {
                "id": chunk["id"],
                "source": chunk["source"],
                "text": chunk["text"],
                "score": round(score, 3),
            }
        )
    return results


class ChatBot:
    """Stateful multi-turn RAG chatbot with query rewriting and token-budgeted history."""

    def __init__(
        self,
        docs: list[dict],
        client,
        system_prompt: str = DEFAULT_SYSTEM,
        k: int = 2,
        min_score: float = 0.2,
        max_history_tokens: int = 60,
    ) -> None:
        """Index ``docs`` once and initialize a per-instance ``history`` list.

        Example:
            bot = ChatBot(docs, client)
            bot.history  # -> []
        """
        # TODO: save configuration attributes, call build_index(docs, client) once,
        # and initialize an empty self.history list unique to this instance.
        pass

    def ask(self, question: str) -> dict:
        """Answer one user turn with rewriting, RAG citations, refusal, and trimming.

        Example:
            bot.ask("How long are store pickup orders held?")
            # -> {
            #     "answer": "Unclaimed orders are held at the counter for 7 days. [2]",
            #     "sources": ["pickup.md"],
            #     "rewritten": "How long are store pickup orders held?",
            # }
        """
        # TODO:
        # 1. Strip question and raise ValueError if blank.
        # 2. Rewrite short (<= 4 words) or follow-up ("and", "what about ", "how about ")
        #    questions using the latest original user turn in self.history.
        # 3. Call retrieve(...); if empty, refuse with REFUSAL and sources=[] (no client.chat).
        # 4. Otherwise call client.chat(..., temperature=0.0) with system+Context and history.
        # 5. Extract unique valid [n] sources (1 <= n <= len(hits)) in appearance order.
        # 6. Append original question and answer to self.history, then pop(0) while
        #    count_tokens(system_prompt) + history tokens > max_history_tokens and len(history) > 2.
        return None
