Starting from the working RAG service in `starter.py`, add an in-memory TTL response cache, `RateLimitError` (`503`) handling, and per-request latency/cost/error monitoring exposed via `GET /metrics`. Write your code inside `create_app` (and any helper functions or classes you need) and return the `FastAPI` instance.

**Example**

```text
GET  /metrics (before any /ask)                        -> 200 {"requests": 0, "cache_hit_rate": 0.0, "error_rate": 0.0, "p95_ms": 0.0, "total_cost": 0.0}
POST /ask (when model raises RateLimitError)           -> 503 {"detail": "model busy, retry later"}
POST /ask {"question": "How long do refunds take?"}    -> 200 {"answer": "...", "sources": ["refunds"], "usage": {...}, "cached": false}
POST /ask {"question": "  How long   do refunds take?"}-> 200 {"answer": "...", "sources": ["refunds"], "usage": {"prompt_tokens": 0, "completion_tokens": 0}, "cached": true}
GET  /metrics?last=2                                   -> 200 {"requests": 2, "cache_hit_rate": 0.5, "error_rate": 0.0, "p95_ms": ..., "total_cost": ...}
```

**Rules**
- Signature: `create_app(docs, client, clock, cache_ttl=300.0, price_in_per_1k=0.0005, price_out_per_1k=0.0015) -> FastAPI`, where `clock` is a zero-argument callable returning seconds (never call real-time `time.*` functions).
- Add `"cached": bool` to every successful `POST /ask` response.
- Cache key must depend on the normalized question (strip outer spaces and collapse internal whitespace runs) **and** `top_k`.
- A cache entry is valid strictly while `clock() < expires_at` (so once `clock() >= expires_at`, it is a miss). On a cache hit, do not call `client.embed` or `client.chat`, and return `usage: {"prompt_tokens": 0, "completion_tokens": 0}`.
- **Refusals are cached too**: if retrieval finds no documents above `min_score`, cache the refusal response so repeating that question within `cache_ttl` returns `cached: true`.
- **Handle `RateLimitError`**: if `client.embed` (during `/ask`) or `client.chat` raises `RateLimitError` (`from pyai_llm import RateLimitError`), do **not** cache the result, still record the request with `status="error"`, `cost=0.0`, and measured `latency_ms`, and raise `HTTPException(status_code=503, detail="model busy, retry later")`. All other accepted `/ask` calls record `status="ok"`.
- For every accepted `POST /ask` call (hit, miss, refusal, or error), record `latency_ms = (clock_after - clock_before) * 1000`, `cost` using `price_in_per_1k` and `price_out_per_1k` (`0.0` on cache hits, refusals, and errors), `cached`, and `status`.
- `GET /metrics` accepts optional query parameter `last: int | None` (`>= 1`, returning `422` when `last=0`). Use `Query` from `fastapi` for query parameters just like `Field` is used for request bodies—for example `last: int | None = Query(default=None, ge=1)`—and FastAPI automatically returns `422` when the constraint is violated. When `last=N` is given, compute metrics over only the last `N` records; otherwise use all records. Return keys in this exact order: `requests`, `cache_hit_rate`, `error_rate`, `p95_ms`, `total_cost` (`p95_ms` by nearest-rank, `total_cost` rounded to 6 decimal places, all `0` / `0.0` when empty).
