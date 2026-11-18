import re
from collections import deque

from pyai_llm import cosine, count_tokens

REFUSAL = "I don't know based on the provided context."
DEFAULT_SYSTEM = "Answer only from the shop FAQ context and cite sources as [n]."

_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")
_CITATION_RE = re.compile(r"\[(\d+)\]")


def build_index(docs: list[dict], client) -> dict:
    """Split FAQ docs into sentences and store plain Python embedding lists."""
    chunks: list[dict] = []
    for doc in docs:
        body = doc["text"].strip()
        if not body:
            continue
        for idx, part in enumerate(_SENTENCE_SPLIT_RE.split(body)):
            sentence = part.strip()
            if sentence:
                chunks.append(
                    {
                        "id": f"{doc['source']}#{idx}",
                        "source": doc["source"],
                        "text": sentence,
                    }
                )
    vectors = client.embed([c["text"] for c in chunks]) if chunks else []
    return {"chunks": chunks, "vectors": vectors}


def retrieve(
    index: dict,
    question: str,
    client,
    k: int = 2,
    min_score: float = 0.2,
) -> list[dict]:
    """Rank chunks with pure Python ``cosine()`` and ``sorted()`` without NumPy."""
    chunks = index["chunks"]
    if not chunks or k <= 0:
        return []
    q_vec = client.embed([question])[0]
    scored = [(cosine(vec, q_vec), idx) for idx, vec in enumerate(index["vectors"])]
    scored.sort(key=lambda pair: (-pair[0], pair[1]))
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


def rewrite_followup(question: str, history: list[dict]) -> str:
    """Pure helper that rewrites short or prefix-matching follow-ups from prior user text."""
    prev_user = ""
    for turn in reversed(history):
        if turn["role"] == "user":
            prev_user = turn["content"]
            break
    if not prev_user:
        return question
    words = question.split()
    low = question.lower()
    if (
        len(words) <= 4
        or words[0].lower() == "and"
        or low.startswith(("what about ", "how about "))
    ):
        return f"{prev_user} {question}"
    return question


def extract_citations(answer: str, hits: list[dict]) -> list[str]:
    """Pure helper returning deduplicated valid ``[n]`` sources in order of appearance."""
    seen: set[str] = set()
    sources: list[str] = []
    for raw in _CITATION_RE.findall(answer):
        num = int(raw)
        if 1 <= num <= len(hits):
            src = hits[num - 1]["source"]
            if src not in seen:
                seen.add(src)
                sources.append(src)
    return sources


def trim_history_deque(
    history: list[dict],
    system_prompt: str,
    max_history_tokens: int,
) -> list[dict]:
    """Pure helper using ``collections.deque`` to evict oldest turns in O(1)."""
    window = deque(history)
    budget_used = count_tokens(system_prompt) + sum(count_tokens(m["content"]) for m in window)
    while len(window) > 2 and budget_used > max_history_tokens:
        oldest = window.popleft()
        budget_used -= count_tokens(oldest["content"])
    return list(window)


class ChatBot:
    """Thin stateful shell delegating rewriting, citations, and trimming to pure helpers."""

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

    def ask(self, question: str) -> dict:
        cleaned = question.strip()
        if not cleaned:
            raise ValueError("question must not be empty")

        rewritten = rewrite_followup(cleaned, self.history)
        hits = retrieve(self.index, rewritten, self.client, self.k, self.min_score)

        if not hits:
            answer = REFUSAL
            sources: list[str] = []
        else:
            ctx = "\n".join(f"[{n}] {hit['text']}" for n, hit in enumerate(hits, 1))
            messages = [
                {"role": "system", "content": f"{self.system_prompt}\n\nContext:\n{ctx}"},
                *self.history,
                {"role": "user", "content": rewritten},
            ]
            answer = self.client.chat(messages, temperature=0.0).content or ""
            sources = extract_citations(answer, hits)

        updated = [
            *self.history,
            {"role": "user", "content": cleaned},
            {"role": "assistant", "content": answer},
        ]
        self.history = trim_history_deque(updated, self.system_prompt, self.max_history_tokens)
        return {"answer": answer, "sources": sources, "rewritten": rewritten}
