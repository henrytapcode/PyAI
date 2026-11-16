# Metrics dashboard and alerts

**What it shows:** How `/ask` records deterministic simulated latency (`0.2 + 0.002 * completion_tokens`), token cost, and cache hits, and how `GET /metrics` summarizes `p50_ms`, `p95_ms`, `total_cost`, and threshold alerts.

**Step by step**
1. Lines 28–38 define `SlowClient`, which advances `FakeClock` inside `chat()` using a fixed formula so misses take over 200 ms while cache hits stay at `0.0` ms.
2. Lines 56–112 wrap `/ask` with `t0 = clock()` and `clock() - t0`, storing one flat metric record per accepted request.
3. Lines 114–153 simulate 12 requests (including one `422` invalid payload rejected by Pydantic before `/ask` runs) and print the `/metrics` summary table and fired alerts.

**Notice:** `requests` is `11` instead of `12` because Pydantic blocks the empty-question payload at the door (`422`) before the `/ask` handler runs.

**Try it yourself:** Raise `max_p95_ms` to `250.0` and `max_cost` to `0.0005` in `create_app` and check that `alerts` becomes empty `[]`.
