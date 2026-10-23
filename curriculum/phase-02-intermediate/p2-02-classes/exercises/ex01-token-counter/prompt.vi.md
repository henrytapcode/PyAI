Viết class `TokenCounter` để theo dõi một tính năng LLM đã dùng bao nhiêu token. Hãy điền bốn method. Đặt code bên trong các method và `return` kết quả (đừng print).

**Ví dụ**

```python
counter = TokenCounter()
counter.add(10)
counter.add(20)
print(counter.total)       # 30
print(counter.calls)       # 2
print(counter.average())   # 15.0
print(counter)             # TokenCounter(total=30, calls=2)
```

**Quy tắc**
- Một `TokenCounter()` mới có hai attribute `total` và `calls`, cả hai bằng `0`.
- `add(n)` cộng `n` vào `total` và cộng `1` vào `calls`. Nó không trả về gì.
- `average()` trả về `total / calls`. Nếu `add` chưa từng được gọi thì trả về `0`.
- `__repr__` trả về chuỗi `TokenCounter(total=30, calls=2)` (với số thật) để `print(counter)` hiển thị đúng như vậy.
- Mỗi counter giữ số liệu riêng: cộng vào counter này không được làm đổi counter khác.
