Hoàn thiện hàm `top_models(conn, min_runs)` bằng cách điền vào các chỗ trống `___` trong câu SQL truy vấn bảng `runs(model TEXT, score REAL)`. Hàm trả về danh sách tuple `(model, avg_score)` cho các model có ít nhất `min_runs` lượt chạy, làm tròn 2 chữ số thập phân và sắp xếp theo `avg_score` giảm dần (hòa thì xếp theo tên `model` tăng dần). Hãy viết code trong hàm và `return` danh sách tuple kết quả.

**Ví dụ**

```python
# Bảng runs chứa:
# ("gpt-4o", 0.92), ("gpt-4o", 0.88), ("claude", 0.88), ("claude", 0.88), ("mini", 0.95)
top_models(conn, 2)
# [("gpt-4o", 0.9), ("claude", 0.88)]
```

**Quy tắc**

- Chỉ giữ lại các model có `COUNT(*) >= min_runs`, dùng placeholder `?` cho `min_runs`.
- Làm tròn điểm trung bình tới 2 chữ số thập phân bằng hàm `ROUND` trong SQL.
- Sắp xếp theo `avg_score` giảm dần, nếu hòa thì theo `model` tăng dần.
