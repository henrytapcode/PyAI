import hashlib  # noqa: F401
import json  # noqa: F401
import math  # noqa: F401
from fastapi import FastAPI, HTTPException, Query  # noqa: F401
from pyai_llm import RateLimitError, cosine  # noqa: F401
from pydantic import BaseModel, Field

REFUSAL = "I don't know based on the provided context."
MIN_SCORE = 0.2


class AskRequest(BaseModel):
    """Validated JSON body for POST /ask."""

    question: str = Field(min_length=1, max_length=300)
    top_k: int = Field(default=2, ge=1, le=5)


def create_app(
    docs: list[dict],
    client,
    clock,
    cache_ttl: float = 300.0,
    price_in_per_1k: float = 0.0005,
    price_out_per_1k: float = 0.0015,
) -> FastAPI:
    """Build a RAG FastAPI service with TTL caching, error handling, and /metrics.

    Example:
        app = create_app(docs, client, clock, cache_ttl=300.0)
        POST /ask -> {"answer": ..., "sources": [...], "usage": {...}, "cached": False}
        GET /metrics?last=10
            -> {"requests": ..., "cache_hit_rate": ..., "error_rate": ..., "p95_ms": ..., ...}
    """
    app = FastAPI()
    doc_vecs = client.embed([d["text"] for d in docs])
    # TODO: initialize in-memory TTL cache and metric records list

    @app.get("/health")
    def health() -> dict[str, object]:
        return {"status": "ok", "docs": len(docs)}

    @app.post("/ask")
    def ask(body: AskRequest) -> dict[str, object]:
        # TODO: record start time with clock(), check TTL cache (normalized question + top_k)
        # TODO: catch RateLimitError on embed/chat -> record status="error", cost=0.0, raise 503
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
            return {
                "answer": REFUSAL,
                "sources": [],
                "usage": {"prompt_tokens": 0, "completion_tokens": 0},
            }

        ctx = "\n".join(f"[{n}] {doc['text']}" for n, doc in enumerate(hits, 1))
        resp = client.chat([
            {"role": "system", "content": f"Answer from context only.\n\nContext:\n{ctx}"},
            {"role": "user", "content": body.question},
        ])
        # TODO: store result (including refusals) in cache with expires_at = clock() + cache_ttl
        # TODO: record latency_ms, cost, cached, and status; include "cached": bool in response
        return {
            "answer": resp.content or "",
            "sources": [doc["id"] for doc in hits],
            "usage": {
                "prompt_tokens": resp.usage.prompt_tokens,
                "completion_tokens": resp.usage.completion_tokens,
            },
        }

    # TODO: add GET /metrics (with optional last: int >= 1) returning
    #       requests, cache_hit_rate, error_rate, p95_ms, total_cost
    return app
