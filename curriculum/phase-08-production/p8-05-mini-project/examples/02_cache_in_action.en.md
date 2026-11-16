# TTL cache in action

**What it shows:** How a deterministic TTL cache inside `create_app` handles whitespace normalization, separates different `top_k` values, caches refusals, and expires entries when the injected `FakeClock` reaches `ttl`.

**Step by step**
1. Lines 17–25 implement `FakeClock` with `__call__()` and `advance(seconds)` so the app checks time without reading the system clock.
2. Lines 46–49 build `make_key` by stripping and collapsing whitespace before hashing `{"question": clean, "top_k": top_k}` with `sort_keys=True`.
3. Lines 87–102 replay 6 timed requests (`t=0` to `t=50`), then advance the clock by `350` seconds (`t=400 >= 300`) to trigger a fresh cache miss.

**Notice:** At `t=10` extra spaces still hit the cache (`chat` stays `1`), at `t=20` changing `top_k=1` misses (`chat` becomes `2`), and at `t=50` the refusal is stored so future repeats skip `embed` too.

**Try it yourself:** Repeat `"Can I pay with crypto?"` at `t=60` and check that `cached` becomes `True` while `chat` remains `3`.
