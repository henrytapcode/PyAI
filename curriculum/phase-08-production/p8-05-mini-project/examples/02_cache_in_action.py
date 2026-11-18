# TTL response cache in the RAG service: hits, whitespace norm, top_k, and expiry.
import hashlib
import json
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


class FakeClock:
    def __init__(self, start: float = 0.0) -> None:
        self.t = start

    def __call__(self) -> float:
        return self.t

    def advance(self, seconds: float) -> None:
        self.t += seconds


class SpyClient:
    def __init__(self, inner: FakeLLM) -> None:
        self.inner = inner
        self.embed_calls = 0
        self.chat_calls = 0

    def embed(self, texts: list[str]) -> list[list[float]]:
        self.embed_calls += 1
        return self.inner.embed(texts)

    def chat(self, messages: list[dict]) -> object:
        self.chat_calls += 1
        return self.inner.chat(messages)


class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=300)
    top_k: int = Field(default=2, ge=1, le=5)


def make_key(question: str, top_k: int) -> str:
    clean = " ".join(question.strip().split())
    raw = json.dumps({"question": clean, "top_k": top_k}, sort_keys=True)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def create_app(docs: list[dict], client: SpyClient, clock: FakeClock, ttl: float = 300.0) -> FastAPI:
    app = FastAPI()
    doc_vecs = client.embed([d["text"] for d in docs])
    cache: dict[str, tuple[dict, float]] = {}

    @app.post("/ask")
    def ask(body: AskRequest) -> dict[str, object]:
        now = clock()
        key = make_key(body.question, body.top_k)
        entry = cache.get(key)
        if entry is not None and now < entry[1]:
            payload = dict(entry[0])
            return {**payload, "usage": {"prompt_tokens": 0, "completion_tokens": 0}, "cached": True}

        q_vec = client.embed([body.question])[0]
        scored = sorted(
            [
                (cosine(q_vec, dv), idx, d)
                for idx, (d, dv) in enumerate(zip(docs, doc_vecs, strict=True))
            ],
            key=lambda item: (-item[0], item[1]),
        )
        hits = [d for score, _, d in scored[: body.top_k] if score >= 0.2]
        if not hits:
            payload = {"answer": "I don't know based on the provided context.", "sources": []}
            usage = {"prompt_tokens": 0, "completion_tokens": 0}
        else:
            ctx = "\n".join(f"[{n}] {d['text']}" for n, d in enumerate(hits, 1))
            resp = client.chat([
                {"role": "system", "content": "Answer from context only.\n\nContext:\n" + ctx},
                {"role": "user", "content": body.question},
            ])
            payload = {"answer": resp.content or "", "sources": [d["id"] for d in hits]}
            usage = {"prompt_tokens": resp.usage.prompt_tokens, "completion_tokens": resp.usage.completion_tokens}
        cache[key] = (payload, clock() + ttl)
        return {**payload, "usage": usage, "cached": False}

    return app


clock = FakeClock()
spy = SpyClient(FakeLLM(embed_dim=256))
http = TestClient(create_app(DOCS, spy, clock, ttl=300.0))

batch = [
    (0, "How many days do refunds take?", 2),
    (10, "  How many days   do refunds take? ", 2),
    (20, "How many days do refunds take?", 1),
    (30, "How long is hardware warranty?", 2),
    (40, "How long is hardware warranty?", 2),
    (50, "Can I pay with crypto?", 2),
]

print("t    | question                         | k | cached | chat")
for target_t, q, k in batch:
    clock.advance(target_t - clock())
    data = http.post("/ask", json={"question": q, "top_k": k}).json()
    print(f"{int(clock()):<4} | {q.strip()[:32]:<32} | {k} | {str(data['cached']):<6} | {spy.chat_calls}")

clock.advance(350)
data = http.post("/ask", json={"question": "How many days do refunds take?", "top_k": 2}).json()
print(f"{int(clock()):<4} | {'How many days do refunds take?':<32} | 2 | {str(data['cached']):<6} | {spy.chat_calls}")
