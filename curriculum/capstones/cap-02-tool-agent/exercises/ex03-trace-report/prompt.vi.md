Hãy cài đặt bộ ghi trace có cấu trúc (`TraceRecorder`), hàm tổng hợp trace (`summarize_traces`), và hàm định dạng báo cáo ngắn gọn (`format_report`) trong `starter.py`. Code của bạn phải ghi được các span thời gian xác định theo định dạng JSONL, tính đúng các chỉ số tóm tắt qua mọi trường hợp biên (danh sách span rỗng, bước bị lỗi, ngân sách `None` hoặc không dương), và đảm bảo mọi dòng báo cáo có độ dài nhỏ hơn 60 ký tự.

**Ví dụ**

```python
recorder = TraceRecorder(clock)
res, span = recorder.record_step(
    "req-1", 1, "tool", "lookup_order", lambda: {"id": "ord-1"}
)
jsonl = recorder.to_jsonl()
summary = summarize_traces(recorder.spans, budget_usd=0.05)
report = format_report(summary)
```

**Quy tắc**

- **`TraceRecorder(clock)`:**
  - Khởi tạo `self.spans: list[dict] = []`.
  - `record_step(request_id: str, step: int, kind: str, name: str, fn: Callable, tokens: int = 0, cost_usd: float = 0.0, retries: int = 0) -> tuple[Any, dict]`:
    - Ghi lại `started_at = clock()`, gọi `fn()`, và tính `duration_ms = round((clock() - started_at) * 1000.0, 3)`.
    - Nếu `fn()` thành công, đặt `status = "ok"` và `error = None`, trả về `(result, span)`.
    - Nếu `fn()` raise `Exception`, bắt ngoại lệ, đặt `status = "error"`, `error = str(exc)`, và trả về `(None, span)`.
    - Thêm dict span với đúng các khóa `{"request_id", "step", "kind", "name", "status", "started_at", "duration_ms", "tokens", "cost_usd", "retries", "error"}` vào `self.spans`.
  - `to_jsonl() -> str`: trả về các dòng `json.dumps(span, sort_keys=True)` nối nhau bằng `"\n"` cho toàn bộ span đã ghi (hoặc `""` nếu rỗng).
- **`summarize_traces(spans: list[dict], budget_usd: float | None = None) -> dict`:**
  - Trả về dict gồm các khóa:
    - `"total_requests"`: số lượng `request_id` duy nhất (`int`).
    - `"total_steps"`: tổng số span (`int`).
    - `"tool_counts"`: `dict[str, int]` **chỉ** đếm các span có `span["kind"] == "tool"`, theo khóa `span["name"]`.
    - `"status_counts"`: `dict[str, int]` đếm span theo `span["status"]`.
    - `"total_retries"`: tổng `retries` trên mọi span (`int`).
    - `"total_tokens"`: tổng `tokens` trên mọi span (`int`).
    - `"total_cost_usd"`: `round(sum(s["cost_usd"] for s in spans), 6)`.
    - `"p95_step_ms"`: `0.0` khi `spans` rỗng; ngược lại sắp xếp thời lượng tăng dần và lấy `durs[max(0, math.ceil(0.95 * len(durs)) - 1)]`.
    - `"budget_utilization"`: `round(total_cost_usd / budget_usd, 6)` khi `budget_usd is not None and budget_usd > 0`, ngược lại là `None`.
    - `"failed_requests"`: `sorted({s["request_id"] for s in spans if s["status"] == "error"})`.
- **`format_report(summary: dict) -> str`:**
  - Trả về chuỗi nhiều dòng xác định, dễ đọc, tóm tắt các chỉ số trong `summary`.
  - Mọi dòng trong chuỗi trả về phải thỏa mãn `len(line) < 60`.
