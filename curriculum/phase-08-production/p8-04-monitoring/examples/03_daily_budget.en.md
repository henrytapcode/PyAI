# Daily budget and latency alerts

**What it shows:** Summarizing three days of request records (`day_1` to `day_3`) and running latency, early-budget, and error-rate threshold checks on each day.

**Step by step**
1. Lines 12–24 define `summarize(records)` to compute `count`, `error_rate`, nearest-rank `p95_ms`, `total_cost`, and `cache_hit_rate`.
2. Lines 27–45 define `check_alerts(...)`, emitting a hard `"budget exceeded"` alert when cost passes `budget` or an early `"budget warning"` once spend reaches `warn_ratio` (default `0.8`, i.e., 80%) of `budget`.
3. Lines 49–68 supply fixed records for three days (with `0.0` cost on cache hits and errors): `day_1` is healthy, `day_2` spikes in latency, cost, and errors, and `day_3` stays fast and error-free at `$17.00` (`85%` of the `$20.00` budget).
4. Lines 70–77 print each day's summary and active alerts.

**Notice:** On `day_3`, latency and error rate are normal and total spend is still below `$20.00`, yet the early 80% threshold fires `"budget warning: 85% of budget used"` before the account hits its hard cap.

**Try it yourself:** Lower `warn_ratio` in `check_alerts` from `0.8` to `0.5` and check which earlier day now receives a budget warning.
