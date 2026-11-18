# Latency percentile report

**What it shows:** Computing `min`, `mean`, `p50`, `p90`, `p95`, and `max` over 20 request latencies using nearest-rank percentiles, then listing the 3 slowest `request_id`s.

**Step by step**
1. Lines 7–10 implement `percentile(values, p)` by sorting `values` and indexing `math.ceil(p / 100 * len(ordered)) - 1`.
2. Lines 14–35 define 20 `(request_id, latency_ms)` samples where 16 requests finish in 180–250 ms and 4 tail requests take 880–2,650 ms.
3. Lines 37–50 compute the 6 summary metrics and print them in a `metric | value` table.
4. Lines 52–55 sort `samples` by latency descending and print the 3 slowest requests (`req-14`, `req-05`, `req-19`).

**Notice:** Half of all requests finish at or below `215` ms (`p50`), yet `mean` is `462.5` ms and `p95` jumps to `1420` ms—showing why averages hide tail spikes while `p95` exposes them.

**Try it yourself:** Replace `req-14`'s `2650` ms with `260` ms and see how `mean` and `max` drop while `p50` stays unchanged.
