Cài đặt hàm tạo key tất định `make_key(model, messages, **params)` và lớp `TTLCache` trong `starter.py`. Viết code của bạn bên trong hàm và các phương thức của lớp rồi dùng `return` để trả về kết quả.

**Ví dụ**

```python
msgs = [{"role": "system", "content": "Be concise."}, {"role": "user", "content": "  Hi   there "}]
k1 = make_key("mini", msgs, temperature=0.0, max_tokens=50)
k2 = make_key("mini", msgs, max_tokens=50, temperature=0.0)
k1 == k2  # True (chuỗi hex SHA-256 dài 64 ký tự)

cache = TTLCache(ttl=30.0)
cache.set(k1, "Hello!", now=10.0)
cache.get(k1, now=39.9)  # "Hello!" (trúng cache)
cache.get(k1, now=40.0)  # None (hết hạn và bị xóa)
cache.hit_rate()         # 0.5
```

**Quy tắc**
- `make_key(model, messages, **params)` cắt khoảng trắng hai đầu và gộp nhiều khoảng trắng liên tiếp trong `content` dạng chuỗi của mỗi message mà không làm biến đổi `messages` gốc, chuyển dữ liệu sang JSON với `sort_keys=True`, rồi trả về chuỗi SHA-256 `hexdigest()` dài 64 ký tự.
- Đổi thứ tự các tham số từ khóa trong `**params` phải cho cùng một key; đổi `model`, `system` prompt hoặc `temperature` phải cho key khác.
- `TTLCache(ttl)` nhận `now: float` ở `set(key, value, now)` và `get(key, now)`: `get` trả về `None` khi thiếu key hoặc đã hết hạn (`now >= expires_at`), xóa entry đã hết hạn khỏi bộ lưu trữ và cập nhật `self.hits`, `self.misses`.
- `hit_rate()` trả về `hits / (hits + misses)` kiểu `float`, hoặc `0.0` nếu chưa có lượt tra cứu nào; `__len__()` trả về số entry đang lưu trong cache.
