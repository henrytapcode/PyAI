import hashlib
import json
import math
from fastapi import FastAPI, HTTPException, Query
from pyai_llm import RateLimitError, cosine
from pydantic import BaseModel, Field

REFUSAL = "I don't know based on the provided context."
MIN_SCORE = 0.2


class AskRequest(BaseModel):
    """Validated JSON body for POST /ask."""

    question: str = Field(min_length=1, max_length=300)
    top_k: int = Field(default=2, ge=1, le=5)


class TTLCache:
    """In-memory TTL cache driven by an injected clock callable."""

    def __init__(self, ttl: float, clock) -> None:
        self.ttl = ttl
        self.clock = clock
        self._store: dict[str, tuple[dict, float]] = {}

    @staticmethod
    def make_key(question: str, top_k: int) -> str:
        clean = " ".join(question.strip().split())
        raw = json.dumps({"question": clean, "top_k": top_k}, sort_keys=True)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def get(self, key: str) -> dict | None:
        item = self._store.get(key)
        if item is None:
            return None
        payload, expires_at = item
        if self.clock() >= expires_at:
            del self._store[key]
            return None
        return {"answer": payload["answer"], "sources": list(payload["sources"])}

    def set(self, key: str, payload: dict) -> None:
        stored = {"answer": payload["answer"], "sources": list(payload["sources"])}
        self._store[key] = (stored, self.clock() + self.ttl)


class MetricsTracker:
    """Collects per-request latency, cost, cache hit status, and ok/error status."""

    def __init__(self, price_in_per_1k: float, price_out_per_1k: float) -> None:
        self.price_in_per_1k = price_in_per_1k
        self.price_out_per_1k = price_out_per_1k
        self._records: list[dict] = []

    def record(
        self,
        latency_ms: float,
        prompt_tokens: int,
        completion_tokens: int,
        cached: bool,
        status: str = "ok",
    ) -> None:
        cost = (
            0.0
            if status != "ok"
            else (prompt_tokens / 1000.0) * self.price_in_per_1k
            + (completion_tokens / 1000.0) * self.price_out_per_1k
        )
        self._records.append(
            {
                "latency_ms": latency_ms,
                "cost": cost,
                "cached": cached,
                "status": status,
            }
        )

    def summary(self, last: int | None = None) -> dict[str, object]:
        window = self._records if last is None else self._records[-last:]
        total = len(window)
        if total == 0:
            return {
                "requests": 0,
                "cache_hit_rate": 0.0,
                "error_rate": 0.0,
                "p95_ms": 0.0,
                "total_cost": 0.0,
            }
        ordered = sorted(r["latency_ms"] for r in window)
        rank = math.ceil(0.95 * total)
        hits = sum(1 for r in window if r["cached"])
        errors = sum(1 for r in window if r["status"] != "ok")
        return {
            "requests": total,
            "cache_hit_rate": hits / total,
            "error_rate": errors / total,
            "p95_ms": ordered[rank - 1],
            "total_cost": round(sum(r["cost"] for r in window), 6),
        }


def create_app(
    docs: list[dict],
    client,
    clock,
    cache_ttl: float = 300.0,
    price_in_per_1k: float = 0.0005,
    price_out_per_1k: float = 0.0015,
) -> FastAPI:
    """Build a RAG service using dedicated TTLCache and MetricsTracker objects."""
    app = FastAPI()
    doc_vecs = client.embed([d["text"] for d in docs])
    cache = TTLCache(cache_ttl, clock)
    tracker = MetricsTracker(price_in_per_1k, price_out_per_1k)

    @app.get("/health")
    def health() -> dict[str, object]:
        return {"status": "ok", "docs": len(docs)}

    @app.post("/ask")
    def ask(body: AskRequest) -> dict[str, object]:
        t0 = clock()
        key = cache.make_key(body.question, body.top_k)
        status = "error"
        cached = False
        p_tok, c_tok = 0, 0
        payload: dict[str, object] = {}

        try:
            hit = cache.get(key)
            if hit is not None:
                payload, cached = hit, True
            else:
                q_vec = client.embed([body.question])[0]
                scored = sorted(
                    [
                        (cosine(q_vec, dv), idx, d)
                        for idx, (d, dv) in enumerate(zip(docs, doc_vecs, strict=True))
                    ],
                    key=lambda item: (-item[0], item[1]),
                )
                hits = [doc for score, _, doc in scored[: body.top_k] if score >= MIN_SCORE]
                if not hits:
                    payload = {"answer": REFUSAL, "sources": []}
                else:
                    ctx = "\n".join(f"[{n}] {doc['text']}" for n, doc in enumerate(hits, 1))
                    sys_prompt = f"Answer from context only.\n\nContext:\n{ctx}"
                    resp = client.chat([
                        {"role": "system", "content": sys_prompt},
                        {"role": "user", "content": body.question},
                    ])
                    payload = {"answer": resp.content or "", "sources": [doc["id"] for doc in hits]}
                    p_tok, c_tok = resp.usage.prompt_tokens, resp.usage.completion_tokens
                cache.set(key, payload)
            status = "ok"
        except RateLimitError as exc:
            raise HTTPException(status_code=503, detail="model busy, retry later") from exc
        finally:
            tracker.record((clock() - t0) * 1000.0, p_tok, c_tok, cached, status=status)

        return {
            **payload,
            "usage": {"prompt_tokens": p_tok, "completion_tokens": c_tok},
            "cached": cached,
        }

    @app.get("/metrics")
    def metrics(last: int | None = Query(default=None, ge=1)) -> dict[str, object]:
        return tracker.summary(last=last)

    return app
