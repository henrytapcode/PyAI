import hashlib
import json
import math
from fastapi import FastAPI
from pyai_llm import cosine
from pydantic import BaseModel, Field

REFUSAL = "I don't know based on the provided context."
MIN_SCORE = 0.2


class AskRequest(BaseModel):
    """Validated JSON body for POST /ask."""

    question: str = Field(min_length=1, max_length=300)
    top_k: int = Field(default=2, ge=1, le=5)


def _make_cache_key(question: str, top_k: int) -> str:
    clean = " ".join(question.strip().split())
    raw = json.dumps({"question": clean, "top_k": top_k}, sort_keys=True)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _nearest_rank(values: list[float], p: float) -> float:
    ordered = sorted(values)
    rank = math.ceil(p / 100 * len(ordered))
    return ordered[rank - 1]


def create_app(
    docs: list[dict],
    client,
    clock,
    cache_ttl: float = 300.0,
    price_in_per_1k: float = 0.0005,
    price_out_per_1k: float = 0.0015,
) -> FastAPI:
    """Build a RAG FastAPI service with TTL caching and /metrics tracking."""
    app = FastAPI()
    doc_vecs = client.embed([d["text"] for d in docs])
    cache: dict[str, tuple[dict, float]] = {}
    records: list[dict] = []

    @app.get("/health")
    def health() -> dict[str, object]:
        return {"status": "ok", "docs": len(docs)}

    @app.post("/ask")
    def ask(body: AskRequest) -> dict[str, object]:
        t0 = clock()
        key = _make_cache_key(body.question, body.top_k)
        entry = cache.get(key)

        if entry is not None and t0 < entry[1]:
            payload = {"answer": entry[0]["answer"], "sources": list(entry[0]["sources"])}
            cached = True
            prompt_tokens = 0
            completion_tokens = 0
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
            hits = [doc for score, _, doc in scored[: body.top_k] if score >= MIN_SCORE]
            if not hits:
                payload = {"answer": REFUSAL, "sources": []}
                prompt_tokens = 0
                completion_tokens = 0
            else:
                ctx = "\n".join(f"[{n}] {doc['text']}" for n, doc in enumerate(hits, 1))
                resp = client.chat([
                    {"role": "system", "content": f"Answer from context only.\n\nContext:\n{ctx}"},
                    {"role": "user", "content": body.question},
                ])
                payload = {"answer": resp.content or "", "sources": [doc["id"] for doc in hits]}
                prompt_tokens = resp.usage.prompt_tokens
                completion_tokens = resp.usage.completion_tokens
            cache[key] = (payload, clock() + cache_ttl)

        latency_ms = (clock() - t0) * 1000.0
        cost = (
            (prompt_tokens / 1000.0) * price_in_per_1k
            + (completion_tokens / 1000.0) * price_out_per_1k
        )
        records.append({"latency_ms": latency_ms, "cost": cost, "cached": cached})
        return {
            **payload,
            "usage": {"prompt_tokens": prompt_tokens, "completion_tokens": completion_tokens},
            "cached": cached,
        }

    @app.get("/metrics")
    def metrics() -> dict[str, object]:
        total = len(records)
        if total == 0:
            return {"requests": 0, "cache_hit_rate": 0.0, "p95_ms": 0.0, "total_cost": 0.0}
        hits = sum(1 for rec in records if rec["cached"])
        p95_ms = _nearest_rank([rec["latency_ms"] for rec in records], 95)
        total_cost = round(sum(rec["cost"] for rec in records), 6)
        return {
            "requests": total,
            "cache_hit_rate": hits / total,
            "p95_ms": p95_ms,
            "total_cost": total_cost,
        }

    return app
