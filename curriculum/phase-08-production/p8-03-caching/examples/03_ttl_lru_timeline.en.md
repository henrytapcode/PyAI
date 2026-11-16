# Combined TTL and LRU cache timeline

**What it shows:** Tracing `maxsize=3` LRU eviction and `ttl=30.0` expiration together over 9 operations using an injected `FakeClock`.

**Step by step**
1. Lines 6–11 define `FakeClock` with deterministic `advance(seconds)` so no real wall clock or `sleep` is needed.
2. Lines 14–36 implement `TTLLRUCache` on top of `OrderedDict`, updating recency on hits (`move_to_end`), dropping the oldest entry when exceeding `maxsize` (`popitem(last=False)`), and deleting entries when `clock.now >= expires_at`.
3. Lines 39–66 replay 9 operations from `t=0` to `t=42` and print the resulting status and key order at each step.

**Notice:** At `t=12`, `get k1` moves `k1` to the back so `k2` is the item evicted by LRU when `k4` arrives at `t=15`; later at `t=40`, `k1` still expires by TTL (`t=0 + 30 = 30`) and is deleted on lookup.

**Try it yourself:** Change `ttl=30.0` to `ttl=50.0` and check which `EXPIRED` row turns into a `HIT`.
