import re

import numpy as np
from pyai_llm import count_tokens

REFUSAL = "I don't know based on the provided context."
DEFAULT_SYSTEM = "Answer only from the shop FAQ context and cite sources as [n]."

_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")
_CITATION_RE = re.compile(r"\[(\d+)\]")


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
        self.client = client
        self.system_prompt = system_prompt
        self.k = k
        self.min_score = min_score
        self.max_history_tokens = max_history_tokens
        self.index = build_index(docs, client)
        self.history: list[dict] = []

    def _rewrite(self, question: str) -> str:
        prev_user = next(
            (turn["content"] for turn in reversed(self.history) if turn["role"] == "user"),
            "",
        )
        if not prev_user:
            return question
        words = question.split()
        lowered = question.lower()
        is_followup = (
            len(words) <= 4
            or words[0].lower() == "and"
            or lowered.startswith(("what about ", "how about "))
        )
        return f"{prev_user} {question}" if is_followup else question

    def _extract_sources(self, answer: str, hits: list[dict]) -> list[str]:
        sources: list[str] = []
        for raw_num in _CITATION_RE.findall(answer):
            idx = int(raw_num) - 1
            if 0 <= idx < len(hits):
                src = hits[idx]["source"]
                if src not in sources:
                    sources.append(src)
        return sources

    def _record_and_trim(self, question: str, answer: str) -> None:
        self.history.append({"role": "user", "content": question})
        self.history.append({"role": "assistant", "content": answer})
        sys_tokens = count_tokens(self.system_prompt)
        total_tokens = sys_tokens + sum(count_tokens(turn["content"]) for turn in self.history)
        while total_tokens > self.max_history_tokens and len(self.history) > 2:
            dropped = self.history.pop(0)
            total_tokens -= count_tokens(dropped["content"])

    def ask(self, question: str) -> dict:
        """Process one user turn and return answer, valid sources, and rewritten query."""
        cleaned = question.strip()
        if not cleaned:
            raise ValueError("question must not be empty")

        rewritten = self._rewrite(cleaned)
        hits = retrieve(self.index, rewritten, self.client, self.k, self.min_score)

        if not hits:
            answer = REFUSAL
            sources: list[str] = []
        else:
            context_block = "\n".join(
                f"[{num}] {hit['text']}" for num, hit in enumerate(hits, 1)
            )
            messages = [
                {"role": "system", "content": f"{self.system_prompt}\n\nContext:\n{context_block}"},
                *self.history,
                {"role": "user", "content": rewritten},
            ]
            reply = self.client.chat(messages, temperature=0.0)
            answer = reply.content or ""
            sources = self._extract_sources(answer, hits)

        self._record_and_trim(cleaned, answer)
        return {"answer": answer, "sources": sources, "rewritten": rewritten}
