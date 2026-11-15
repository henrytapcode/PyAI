Điền vào các chỗ trống `___` trong hàm `hit_rate(results, k)` ở `starter.py` để tính tỉ lệ truy xuất trúng `hit@k` trên các câu hỏi có nguồn kỳ vọng.

Viết code bên trong hàm và `return` một số thực `float` trong đoạn `0.0` đến `1.0`.

## Ví dụ

```python
results = [
    {"expected_source": "refunds.md", "retrieved": ["refunds.md", "shipping.md"]},
    {"expected_source": "shipping.md", "retrieved": ["loyalty.md", "shipping.md"]},
    {"expected_source": None, "retrieved": ["pickup.md", "payment.md"]},
]
hit_rate(results, k=1)  # -> 0.5
hit_rate(results, k=2)  # -> 1.0
```

## Quy tắc

- Mỗi phần tử trong `results` có dạng `{"expected_source": str | None, "retrieved": list[str]}` đã sắp xếp từ điểm cao nhất xuống thấp nhất.
- Bỏ qua các dòng có `expected_source` là `None` để câu không trả lời được không lọt vào mẫu số.
- Tính là trúng khi `expected_source` nằm trong `retrieved[:k]`.
- Trả về `0.0` nếu `results` không có dòng nào có `expected_source` khác `None` (hoặc khi `k <= 0`).
