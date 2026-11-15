Hoàn thành hàm `cosine_sim(a, b)` trong `starter.py` bằng cách thay thế các chỗ trống `___` để tính cosine similarity giữa hai danh sách số bằng NumPy.

Viết code của bạn bên trong thân hàm và `return` kết quả kiểu `float` đã làm tròn.

## Ví dụ

```python
cosine_sim([3.0, 4.0], [6.0, 8.0])   # -> 1.0
cosine_sim([1.0, 0.0], [0.0, 1.0])   # -> 0.0
cosine_sim([0.0, 0.0], [1.0, 2.0])   # -> 0.0
```

## Quy tắc

- Ném `ValueError` nếu `a` và `b` không cùng độ dài.
- Trả về `0.0` nếu một trong hai vector toàn số 0 (hoặc rỗng).
- Dùng NumPy để tính độ dài vector và tích vô hướng.
- Trả về `float` chuẩn của Python đã làm tròn đến 3 chữ số thập phân.
