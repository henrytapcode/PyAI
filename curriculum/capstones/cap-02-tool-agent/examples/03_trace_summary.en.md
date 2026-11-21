# JSONL trace recording and SRE summary reporting

**What it shows:** Capturing per-step `"llm"` and `"tool"` spans with `TraceRecorder`, aggregating metrics with `summarize_traces()`, and rendering a compact `< 60`-character terminal report.

**Step by step**
1. Lines 8–59 define `FakeClock` and `TraceRecorder`, whose `record_step()` times each call, catches exceptions into `status="error"`, and exports sorted JSONL via `to_jsonl()`.
2. Lines 62–81 implement `summarize_traces()` to count only `kind == "tool"` spans in `tool_counts`, compute nearest-rank `p95_step_ms`, and calculate `budget_utilization`.
3. Lines 84–93 implement `format_report()` to format key SRE metrics into lines shorter than 60 characters.
4. Lines 96–107 record four steps across `req-1` and `req-2` (including one failing `issue_refund` call), then print the JSONL spans and the summary report.

**Notice:** `tool_counts` contains only `lookup_order` and `issue_refund` (excluding `"fake-llm"`), `p95_step_ms` is `45.0` ms, and `req-2` appears in `failed_requests`.

**Try it yourself:** Pass `budget_usd=None` to `summarize_traces()` and confirm `budget_utilization` displays as `n/a` in the report.
