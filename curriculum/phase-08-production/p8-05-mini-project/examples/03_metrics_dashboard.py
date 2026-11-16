# Full RAG service metrics dashboard: simulated day, p50/p95 latency, cost, and alerts.
import hashlib
import json
import math
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
        self.now = start

    def __call__(self) -> float:
        return self.now

    def advance(self, seconds: float) -> None:
        self.now += seconds


class SlowClient:
    def __init__(self, inner: FakeLLM, clock: FakeClock) -> None:
        self.inner = inner
        self.clock = clock

    def embed(self, texts: list[str]) -> list[list[float]]:
        return self.inner.embed(texts)

    def chat(self, messages: list[dict]) -> object:
        resp = self.inner.chat(messages)
        # Deterministic latency model: 0.2s base + 0.002s per completion token
        self.clock.advance(0.2 + 0.002 * resp.usage.completion_tokens)
        return resp


class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=300)
    top_k: int = Field(default=2, ge=1, le=5)


def percentile(values: list[float], p: float) -> float:
    ordered = sorted(values)
    rank = math.ceil(p / 100 * len(ordered))
    return ordered[rank - 1]


def create_app(
    docs: list[dict],
    client: SlowClient,
    clock: FakeClock,
    ttl: float = 300.0,
    max_p95_ms: float = 200.0,
    max_cost: float = 0.0001,
) -> FastAPI:
    app = FastAPI()
    doc_vecs = client.embed([d["text"] for d in docs])
    cache: dict[str, tuple[dict, float]] = {}
    records: list[dict] = []

    @app.post("/ask")
    def ask(body: AskRequest) -> dict[str, object]:
        t0 = clock()
        clean = " ".join(body.question.strip().split())
        key = hashlib.sha256(json.dumps({"question": clean, "top_k": body.top_k}, sort_keys=True).encode("utf-8")).hexdigest()
        entry = cache.get(key)
        if entry is not None and t0 < entry[1]:
            payload = dict(entry[0])
            cached = True
            p_tok, c_tok = 0, 0
        else:
            cached = False
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
                p_tok, c_tok = 0, 0
            else:
                ctx = "\n".join(f"[{n}] {d['text']}" for n, d in enumerate(hits, 1))
                resp = client.chat([
                    {"role": "system", "content": "Answer from context only.\n\nContext:\n" + ctx},
                    {"role": "user", "content": body.question},
                ])
                payload = {"answer": resp.content or "", "sources": [d["id"] for d in hits]}
                p_tok, c_tok = resp.usage.prompt_tokens, resp.usage.completion_tokens
            cache[key] = (payload, clock() + ttl)

        latency_ms = round((clock() - t0) * 1000.0, 2)
        cost = (p_tok / 1000.0) * 0.0005 + (c_tok / 1000.0) * 0.0015
        records.append({"latency_ms": latency_ms, "cost": cost, "cached": cached})
        return {**payload, "usage": {"prompt_tokens": p_tok, "completion_tokens": c_tok}, "cached": cached}

    @app.get("/metrics")
    def metrics() -> dict[str, object]:
        total = len(records)
        if total == 0:
            return {"requests": 0, "cache_hit_rate": 0.0, "p50_ms": 0.0, "p95_ms": 0.0, "total_cost": 0.0, "alerts": []}
        lats = [r["latency_ms"] for r in records]
        hits = sum(1 for r in records if r["cached"])
        p50 = round(percentile(lats, 50), 2)
        p95 = round(percentile(lats, 95), 2)
        cost = round(sum(r["cost"] for r in records), 6)
        alerts: list[str] = []
        if p95 > max_p95_ms:
            alerts.append(f"p95 latency {p95}ms > {max_p95_ms}ms")
        if cost > max_cost:
            alerts.append(f"daily cost ${cost:.6f} > ${max_cost:.6f}")
        return {
            "requests": total,
            "cache_hit_rate": round(hits / total, 4),
            "p50_ms": p50,
            "p95_ms": p95,
            "total_cost": cost,
            "alerts": alerts,
        }

    return app


clock = FakeClock()
http = TestClient(create_app(DOCS, SlowClient(FakeLLM(embed_dim=256), clock), clock))

day_traffic = [
    {"question": "How many days do refunds take?"},
    {"question": "How much does express shipping cost?"},
    {"question": "How many days do refunds take?"},
    {"question": "How long is hardware warranty?"},
    {"question": "How many days do refunds take?"},
    {"question": ""},  # invalid 422 payload: blocked by Pydantic before /ask handler
    {"question": "When do support agents work?"},
    {"question": "How much does express shipping cost?"},
    {"question": "How are invoices emailed?"},
    {"question": "Can I pay with crypto?"},
    {"question": "Can I pay with crypto?"},
    {"question": "How long is hardware warranty?"},
]

statuses: list[int] = []
for payload in day_traffic:
    statuses.append(http.post("/ask", json=payload).status_code)
print("statuses:", statuses)

summary = http.get("/metrics").json()
print("metric         | value")
for k in ("requests", "cache_hit_rate", "p50_ms", "p95_ms", "total_cost"):
    val = f"${summary[k]:.6f}" if k == "total_cost" else str(summary[k])
    print(f"{k:<14} | {val}")
print("alerts:", summary["alerts"])
