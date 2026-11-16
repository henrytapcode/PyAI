Hoàn thiện lớp `LRUCache` trong `starter.py` bằng cách thay thế tất cả các ô `___` để cache lưu tối đa `maxsize` phần tử, loại bỏ key lâu chưa dùng nhất khi đầy và đếm `hits` cùng `misses`. Điền vào các ô trống bên trong phương thức và giữ nguyên chữ ký hàm sẵn có.

**Ví dụ**

```python
cache = LRUCache(maxsize=2)
cache.set("a", 1)
cache.set("b", 2)
cache.get("a")   # 1 (đẩy "a" thành mới dùng nhất)
cache.set("c", 3)  # loại bỏ "b"
cache.get("b")   # None (cache miss)
```

**Quy tắc**
- `get(key)` trả về `None` và tăng `self.misses` khi không có `key`; khi trúng cache, nó đánh dấu `key` là mới dùng nhất, tăng `self.hits` và trả về giá trị đã lưu.
- `set(key, value)` lưu hoặc cập nhật `key` ở vị trí mới dùng nhất; nếu kích thước vượt quá `self.maxsize`, nó xóa phần tử lâu chưa dùng nhất (`last=False`).
- Gọi `set(key, new_value)` cho một key đã tồn tại phải cập nhật giá trị mới mà không làm tăng kích thước hay đẩy nhầm key khác.
