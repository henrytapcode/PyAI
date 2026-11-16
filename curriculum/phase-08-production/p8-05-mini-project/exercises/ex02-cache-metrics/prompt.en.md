Starting from the working RAG service in `starter.py`, add an in-memory TTL response cache and per-request latency/cost monitoring exposed via `GET /metrics`. Write your code inside `create_app` (and any helper functions or classes you need) and return the `FastAPI` instance.

**Example**

```text
GET  /metrics (before any /ask)                        -> 200 {"requests": 0, "cache_hit_rate": 0.0, "p95_ms": 0.0, "total_cost": 0.0}
POST /ask {"question": "How long do refunds take?"}    -> 200 {"answer": "...", "sources": ["refunds"], "usage": {...}, "cached": false}
POST /ask {"question": "  How long   do refunds take?"}-> 200 {"answer": "...", "sources": ["refunds"], "usage": {"prompt_tokens": 0, "completion_tokens": 0}, "cached": true}
GET  /metrics                                          -> 200 {"requests": 2, "cache_hit_rate": 0.5, "p95_ms": ..., "total_cost": ...}
```

**Rules**
- Signature: `create_app(docs, client, clock, cache_ttl=300.0, price_in_per_1k=0.0005, price_out_per_1k=0.0015) -> FastAPI`, where `clock` is a zero-argument callable returning seconds (never call real-time `time.*` functions).
- Add `"cached": bool` to every `POST /ask` response.
- Cache key must depend on the normalized question (strip outer spaces and collapse internal whitespace runs) **and** `top_k`.
- A cache entry is valid strictly while `clock() < expires_at` (so once `clock() >= expires_at`, it is a miss). On a cache hit, do not call `client.embed` or `client.chat`, and return `usage: {"prompt_tokens": 0, "completion_tokens": 0}`.
- **Refusals are cached too**: if retrieval finds no documents above `min_score`, cache the refusal response so repeating that question within `cache_ttl` returns `cached: true`.
- For every accepted `POST /ask` call (hit, miss, or refusal), record `latency_ms = (clock_after - clock_before) * 1000`, `cost` using `price_in_per_1k` and `price_out_per_1k` (`0.0` on cache hits), and `cached`.
- `GET /metrics` returns `{"requests": int, "cache_hit_rate": float, "p95_ms": float, "total_cost": float}`, with `p95_ms` computed by nearest-rank and `total_cost` rounded to 6 decimal places (all `0` / `0.0` when no requests have been recorded yet).
