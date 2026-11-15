# Policy bot: answer shop questions from docs and skip the LLM when off-topic.
import re

import numpy as np
from pyai_llm import FakeLLM

DOCS = [
    {"source": "refunds.md", "text": "Refunds are issued within 30 days of purchase. Keep your original receipt."},
    {"source": "shipping.md", "text": "Standard shipping delivers orders in three to five business days."},
    {"source": "warranty.md", "text": "Hardware warranty covers factory defects for 12 months from delivery."},
    {"source": "support.md", "text": "Support hours run Monday to Friday from 9am to 5pm."},
]


class CountingLLM(FakeLLM):
    def __init__(self, embed_dim: int = 256) -> None:
        super().__init__(embed_dim=embed_dim)
        self.chat_calls = 0

    def chat(self, messages, **kwargs):
        self.chat_calls += 1
        return super().chat(messages, **kwargs)


def ask_bot(
    question: str,
    docs: list[dict],
    matrix: np.ndarray,
    client: CountingLLM,
    k: int = 2,
    min_score: float = 0.2,
) -> tuple[str, list[str]]:
    q_vec = np.array(client.embed([question])[0], dtype=float)
    scores = matrix @ q_vec
    order = np.argsort(-scores, kind="stable")[:k]
    if float(scores[int(order[0])]) < min_score:
        return "I don't know.", []

    hits = [docs[int(i)] for i in order]
    context = "\n".join(f"[{n}] {h['text']}" for n, h in enumerate(hits, 1))
    messages = [
        {"role": "system", "content": "Answer using only the context. Cite [n].\n\nContext:\n" + context},
        {"role": "user", "content": question},
    ]
    answer = client.chat(messages).content or ""
    sources: list[str] = []
    for num in re.findall(r"\[(\d+)\]", answer):
        idx = int(num) - 1
        if 0 <= idx < len(hits) and hits[idx]["source"] not in sources:
            sources.append(hits[idx]["source"])
    return answer, sources


client = CountingLLM(embed_dim=256)
matrix = np.array(client.embed([d["text"] for d in DOCS]), dtype=float)
questions = [
    "How many days do refunds take?",
    "What does hardware warranty cover?",
    "Do you offer student discounts?",
]
for q in questions:
    before = client.chat_calls
    ans, srcs = ask_bot(q, DOCS, matrix, client)
    note = "LLM called" if client.chat_calls > before else "LLM not called"
    print(f"Q: {q}")
    print(f"A: {ans} | sources={srcs} | {note}")
print("Total chat calls:", client.chat_calls)
