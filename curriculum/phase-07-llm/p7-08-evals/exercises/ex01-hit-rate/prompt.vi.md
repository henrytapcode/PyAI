Điền vào các chỗ trống `___` trong hàm `hit_rates(results, ks)` ở `starter.py` để tính tỉ lệ truy xuất trúng `hit@k` qua nhiều mức cắt `ks`.

Viết code bên trong hàm và `return` một `dict[int, float]` ánh xạ từng `k` trong `ks` sang điểm số làm tròn đến 3 chữ số thập phân.

## Ví dụ

```python
results = [
    {"expected_source": "refunds.md", "retrieved": ["refunds.md", "shipping.md"]},
    {"expected_source": "shipping.md", "retrieved": ["loyalty.md", "shipping.md"]},
    {"expected_source": None, "retrieved": ["pickup.md", "payment.md"]},
]
hit_rates(results, ks=[1, 2])  # -> {1: 0.5, 2: 1.0}
```

## Quy tắc

- Mỗi phần tử trong `results` có dạng `{"expected_source": str | None, "retrieved": list[str]}` đã sắp xếp từ điểm cao nhất xuống thấp nhất.
- Raise `ValueError` nếu có bất kỳ `k` nào trong `ks` nhỏ hơn hoặc bằng `0`.
- Bỏ qua các dòng có `expected_source` là `None` để câu không trả lời được không lọt vào mẫu số; trả về `{}` khi `ks` rỗng.
- Tính là trúng khi `expected_source` nằm trong `retrieved[:k]`, và lưu `round(hits / total, 3)` (hoặc `0.0` nếu không có dòng nào có nguồn kỳ vọng).
