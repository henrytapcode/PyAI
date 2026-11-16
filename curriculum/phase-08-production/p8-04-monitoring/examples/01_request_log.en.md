# Structured request log with FakeLLM

**What it shows:** Logging 8 simulated LLM requests as one-line JSON records via `logging` to `sys.stdout`, covering cache hits, cache misses, and a `RateLimitError` failure.

**Step by step**
1. Lines 13–18 define `FakeClock` so latency advances deterministically (`2.0` ms on cache hits, `200 + 3 * completion_tokens` ms on model calls, and `150.0` ms on errors).
2. Lines 22–28 configure the `"app.metrics"` logger with `stream=sys.stdout` and `format="%(message)s"` so every log line is pure JSON.
3. Lines 46–82 process 8 requests: `req-01` hits `RateLimitError` (`fail_times=1`) and logs `status="error"` with zero tokens, `req-05` and `req-07` hit the cache with `0` tokens, and the remaining 5 call `FakeLLM` and compute `cost_usd`.
4. Line 84 prints `logged_lines: 8`, confirming that failed requests are recorded just like successful ones.

**Notice:** `req-01` failed before returning a model reply, yet its structured record is still logged with `status="error"` and `latency_ms=150.0` so downstream error-rate calculations stay accurate.

**Try it yourself:** Change `FakeLLM(fail_times=1)` to `FakeLLM(fail_times=2)` and observe how both `req-01` and `req-02` log `"status": "error"` instead of silently disappearing.
