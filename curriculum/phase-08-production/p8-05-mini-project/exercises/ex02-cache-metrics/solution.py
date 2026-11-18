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


def _digest_cache_key(question: str, top_k: int) -> str:
    normalized = " ".join(question.strip().split())
    serialized = json.dumps({"question": normalized, "top_k": top_k}, sort_keys=True)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def _percentile_nearest_rank(values: list[float], p: float) -> float:
    sorted_vals = sorted(values)
    idx = math.ceil((p / 100.0) * len(sorted_vals)) - 1
    return sorted_vals[idx]


def _retrieve_hits(
    docs: list[dict],
    doc_vecs: list[list[float]],
    query_vec: list[float],
    top_k: int,
) -> list[dict]:
    candidates: list[tuple[float, int, dict]] = []
    for idx, doc in enumerate(docs):
        score = cosine(query_vec, doc_vecs[idx])
        candidates.append((score, idx, doc))
    candidates.sort(key=lambda row: (-row[0], row[1]))
    return [doc for score, _, doc in candidates[:top_k] if score >= MIN_SCORE]


def _summarize_window(records: list[dict]) -> dict[str, object]:
    count = len(records)
    if count == 0:
        return {
            "requests": 0,
            "cache_hit_rate": 0.0,
            "error_rate": 0.0,
            "p95_ms": 0.0,
            "total_cost": 0.0,
        }
    hit_count = sum(1 for item in records if item["cached"])
    err_count = sum(1 for item in records if item["status"] != "ok")
    p95 = _percentile_nearest_rank([item["latency_ms"] for item in records], 95)
    cost_sum = round(sum(item["cost"] for item in records), 6)
    return {
        "requests": count,
        "cache_hit_rate": hit_count / count,
        "error_rate": err_count / count,
        "p95_ms": p95,
        "total_cost": cost_sum,
    }


def create_app(
    docs: list[dict],
    client,
    clock,
    cache_ttl: float = 300.0,
    price_in_per_1k: float = 0.0005,
    price_out_per_1k: float = 0.0015,
) -> FastAPI:
    """Build a RAG FastAPI service with TTL caching, 503 error handling, and /metrics."""
    app = FastAPI()
    corpus_vecs = client.embed([item["text"] for item in docs])
    ttl_store: dict[str, tuple[dict, float]] = {}
    metric_log: list[dict] = []

    @app.get("/health")
    def health() -> dict[str, object]:
        return {"status": "ok", "docs": len(corpus_vecs)}

    @app.post("/ask")
    def ask(req: AskRequest) -> dict[str, object]:
        started = clock()
        cache_key = _digest_cache_key(req.question, req.top_k)
        cached_item = ttl_store.get(cache_key)

        status = "error"
        cost = 0.0
        cached = False
        prompt_tokens = 0
        completion_tokens = 0
        payload: dict[str, object] = {}

        try:
            if cached_item is not None and started < cached_item[1]:
                stored_payload = cached_item[0]
                payload = {
                    "answer": stored_payload["answer"],
                    "sources": list(stored_payload["sources"]),
                }
                cached = True
            else:
                query_vec = client.embed([req.question])[0]
                hits = _retrieve_hits(docs, corpus_vecs, query_vec, req.top_k)
                if not hits:
                    payload = {"answer": REFUSAL, "sources": []}
                else:
                    context_block = "\n".join(
                        f"[{rank}] {doc['text']}" for rank, doc in enumerate(hits, 1)
                    )
                    reply = client.chat([
                        {
                            "role": "system",
                            "content": f"Answer from context only.\n\nContext:\n{context_block}",
                        },
                        {"role": "user", "content": req.question},
                    ])
                    payload = {
                        "answer": reply.content or "",
                        "sources": [doc["id"] for doc in hits],
                    }
                    prompt_tokens = reply.usage.prompt_tokens
                    completion_tokens = reply.usage.completion_tokens
                ttl_store[cache_key] = (payload, clock() + cache_ttl)

            cost = (
                (prompt_tokens / 1000.0) * price_in_per_1k
                + (completion_tokens / 1000.0) * price_out_per_1k
            )
            status = "ok"
        except RateLimitError as exc:
            raise HTTPException(status_code=503, detail="model busy, retry later") from exc
        finally:
            elapsed_ms = (clock() - started) * 1000.0
            metric_log.append(
                {
                    "latency_ms": elapsed_ms,
                    "cost": cost,
                    "cached": cached,
                    "status": status,
                }
            )

        return {
            **payload,
            "usage": {
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
            },
            "cached": cached,
        }

    @app.get("/metrics")
    def metrics(last: int | None = Query(default=None, ge=1)) -> dict[str, object]:
        window = metric_log if last is None else metric_log[-last:]
        return _summarize_window(window)

    return app
