Hoàn thiện lớp `MetricsTracker` trong `starter.py` để ghi nhận độ trễ, chi phí token và trạng thái từng request, tổng hợp trong `summary()`, và kiểm tra ngưỡng trong `alerts()`. Viết code bên trong các phương thức của class và `return` đúng giá trị yêu cầu.

**Ví dụ**

```python
tracker = MetricsTracker(price_in_per_1k=0.001, price_out_per_1k=0.002)
cost = tracker.record(latency_ms=250.0, prompt_tokens=1000, completion_tokens=500)
# cost == 0.002
tracker.summary()
# {"count": 1, "error_rate": 0.0, "p95_ms": 250.0, "total_cost": 0.002}
tracker.alerts(max_p95_ms=200.0, budget=0.0025)
# ["p95-latency", "budget-warning"]
```

**Quy tắc**
- `record(latency_ms, prompt_tokens, completion_tokens, ok=True)` lưu lại request (kể cả khi `ok=False`) và trả về chi phí của request đó dạng `float`.
- `summary()` trả về `{"count": ..., "error_rate": ..., "p95_ms": ..., "total_cost": ...}` với `p95_ms` tính theo nearest-rank và `total_cost` làm tròn 6 chữ số thập phân. Khi chưa có bản ghi nào, `count` là `0` và các giá trị còn lại là `0.0`.
- `alerts(max_p95_ms, budget, warn_ratio=0.8)` trả về danh sách mã cảnh báo theo đúng thứ tự cố định:
  1. `"p95-latency"` khi `p95_ms > max_p95_ms`
  2. `"budget-exceeded"` khi `total_cost > budget`, ngược lại `"budget-warning"` khi `total_cost >= warn_ratio * budget`
  3. `"error-rate"` khi `error_rate > 0.05`
