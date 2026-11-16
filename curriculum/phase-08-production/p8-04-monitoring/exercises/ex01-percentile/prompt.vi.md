Hoàn thiện `percentile` và `latency_report` trong `starter.py` bằng cách điền vào từng ô `___` để tính phân vị theo phương pháp nearest-rank và trả về dictionary tổng hợp. Giữ nguyên chữ ký hàm và phần kiểm tra lỗi có sẵn.

**Ví dụ**

```python
percentile([10, 20, 30, 40], 50)   # 20.0
latency_report([100, 200, 300])    # {"p50": 200.0, "p95": 300.0, "max": 300.0}
```

**Quy tắc**
- `percentile(values, p)` sắp xếp `values` không làm đổi list đầu vào, tính `rank = math.ceil(p / 100 * len(ordered))`, rồi trả về `float(ordered[rank - 1])`.
- `percentile` ném `ValueError` khi `values` rỗng hoặc `p` nằm ngoài `(0, 100]`.
- `latency_report(values)` trả về `{"p50": ..., "p95": ..., "max": ...}` với các giá trị kiểu `float`.
