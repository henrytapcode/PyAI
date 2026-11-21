Implement structured trace recording (`TraceRecorder`), trace aggregation (`summarize_traces`), and compact terminal reporting (`format_report`) in `starter.py`. Your implementation must record deterministic timing spans in JSONL format, compute exact summary metrics across edge cases (empty spans, failing steps, `None` or non-positive budgets), and format every report line strictly under 60 characters.

**Example**

```python
recorder = TraceRecorder(clock)
res, span = recorder.record_step(
    "req-1", 1, "tool", "lookup_order", lambda: {"id": "ord-1"}
)
jsonl = recorder.to_jsonl()
summary = summarize_traces(recorder.spans, budget_usd=0.05)
report = format_report(summary)
```

**Rules**

- **`TraceRecorder(clock)`:**
  - Store `self.spans: list[dict] = []`.
  - `record_step(request_id: str, step: int, kind: str, name: str, fn: Callable, tokens: int = 0, cost_usd: float = 0.0, retries: int = 0) -> tuple[Any, dict]`:
    - Capture `started_at = clock()`, invoke `fn()`, and compute `duration_ms = round((clock() - started_at) * 1000.0, 3)`.
    - If `fn()` succeeds, set `status = "ok"` and `error = None`, returning `(result, span)`.
    - If `fn()` raises `Exception`, catch it, set `status = "error"`, `error = str(exc)`, and return `(None, span)`.
    - Append the span dict with exact keys `{"request_id", "step", "kind", "name", "status", "started_at", "duration_ms", "tokens", "cost_usd", "retries", "error"}` to `self.spans`.
  - `to_jsonl() -> str`: return newline-joined `json.dumps(span, sort_keys=True)` for all recorded spans (or `""` when empty).
- **`summarize_traces(spans: list[dict], budget_usd: float | None = None) -> dict`:**
  - Return a dictionary with keys:
    - `"total_requests"`: count of unique `request_id` values (`int`).
    - `"total_steps"`: total number of spans (`int`).
    - `"tool_counts"`: `dict[str, int]` counting **only** spans where `span["kind"] == "tool"`, keyed by `span["name"]`.
    - `"status_counts"`: `dict[str, int]` counting spans by `span["status"]`.
    - `"total_retries"`: sum of `retries` across all spans (`int`).
    - `"total_tokens"`: sum of `tokens` across all spans (`int`).
    - `"total_cost_usd"`: `round(sum(s["cost_usd"] for s in spans), 6)`.
    - `"p95_step_ms"`: `0.0` when `spans` is empty; otherwise sort durations ascending and pick `durs[max(0, math.ceil(0.95 * len(durs)) - 1)]`.
    - `"budget_utilization"`: `round(total_cost_usd / budget_usd, 6)` when `budget_usd is not None and budget_usd > 0`, else `None`.
    - `"failed_requests"`: `sorted({s["request_id"] for s in spans if s["status"] == "error"})`.
- **`format_report(summary: dict) -> str`:**
  - Return a deterministic, human-readable multi-line string summarizing the metrics in `summary`.
  - Every line in the returned string must satisfy `len(line) < 60`.
