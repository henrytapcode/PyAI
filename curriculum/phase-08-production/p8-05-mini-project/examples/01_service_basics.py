# RAG FastAPI service basics: one-time doc indexing, /health, citations, and refusal.
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pyai_llm import FakeLLM, cosine
from pydantic import BaseModel, Field

DOCS = [
    {"id": "refunds", "text": "Refunds take 5 business days after approval. Keep your receipt."},
    {"id": "shipping", "text": "Express shipping costs 12 dollars and arrives next day. Free shipping starts at 50 dollars."},
    {"id": "warranty", "text": "Hardware warranty covers factory defects for 12 months. Water damage is excluded."},
    {"id": "support", "text": "Support agents work Monday to Friday from 9 AM to 6 PM. Urgent tickets get priority."},
    {"id": "security", "text": "Two-factor login protects your account. Password resets arrive by email."},
    {"id": "billing", "text": "Invoices are emailed right after checkout. Accepted cards include Visa."},
]


class SpyClient:
    def __init__(self, inner: FakeLLM) -> None:
        self.inner = inner
        self.embed_sizes: list[int] = []
        self.chat_calls = 0

    def embed(self, texts: list[str]) -> list[list[float]]:
        self.embed_sizes.append(len(texts))
        return self.inner.embed(texts)

    def chat(self, messages: list[dict]) -> object:
        self.chat_calls += 1
        return self.inner.chat(messages)


class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=300)
    top_k: int = Field(default=2, ge=1, le=5)


def create_app(docs: list[dict], client: SpyClient, min_score: float = 0.2) -> FastAPI:
    app = FastAPI()
    doc_vecs = client.embed([d["text"] for d in docs])

    @app.get("/health")
    def health() -> dict[str, object]:
        return {"status": "ok", "docs": len(docs)}

    @app.post("/ask")
    def ask(body: AskRequest) -> dict[str, object]:
        q_vec = client.embed([body.question])[0]
        scored = sorted(
            [
                (cosine(q_vec, dv), idx, d)
                for idx, (d, dv) in enumerate(zip(docs, doc_vecs, strict=True))
            ],
            key=lambda item: (-item[0], item[1]),
        )
        hits = [d for score, _, d in scored[: body.top_k] if score >= min_score]
        if not hits:
            return {
                "answer": "I don't know based on the provided context.",
                "sources": [],
                "usage": {"prompt_tokens": 0, "completion_tokens": 0},
            }
        ctx = "\n".join(f"[{n}] {d['text']}" for n, d in enumerate(hits, 1))
        resp = client.chat([
            {"role": "system", "content": "Answer from context only.\n\nContext:\n" + ctx},
            {"role": "user", "content": body.question},
        ])
        return {
            "answer": resp.content or "",
            "sources": [d["id"] for d in hits],
            "usage": {
                "prompt_tokens": resp.usage.prompt_tokens,
                "completion_tokens": resp.usage.completion_tokens,
            },
        }

    return app


spy = SpyClient(FakeLLM(embed_dim=256))
http = TestClient(create_app(DOCS, spy))
print("health:", http.get("/health").json())

questions = [
    "How many days do refunds take?",
    "How much does express shipping cost?",
    "Can I pay with crypto?",
]
for idx, q in enumerate(questions, 1):
    r = http.post("/ask", json={"question": q})
    data = r.json()
    print(f"q{idx}: status={r.status_code} sources={data['sources']}")
    print(f"    ans={data['answer']}")

index_embeds = sum(1 for size in spy.embed_sizes if size == len(DOCS))
print(f"calls: index_embed={index_embeds} total_embed={len(spy.embed_sizes)} chat={spy.chat_calls}")
