Hoàn thiện lớp `LRUCache` trong `starter.py` bằng cách thay thế tất cả các ô `___` để cache lưu tối đa `maxsize` phần tử, loại bỏ key lâu chưa dùng nhất khi đầy, hỗ trợ `peek(key)` không làm đổi trạng thái và đếm `hits`, `misses`, `evictions`. Điền vào các ô trống bên trong phương thức và giữ nguyên chữ ký hàm sẵn có.

**Ví dụ**

```python
cache = LRUCache(maxsize=2)
cache.set("a", 1)
cache.set("b", 2)
cache.peek("a")  # 1 (KHÔNG đổi thứ tự và KHÔNG đổi hits/misses)
cache.set("c", 3)  # loại bỏ "a" (evictions == 1)
cache.get("a")   # None (cache miss)
cache.get("b")   # 2 (cache hit, đẩy "b" thành mới dùng nhất)
```

**Quy tắc**
- `peek(key)` trả về giá trị đang lưu hoặc `None` mà không làm thay đổi thứ tự key và không thay đổi `self.hits` hay `self.misses`.
- `get(key)` trả về `None` và tăng `self.misses` khi không có `key`; khi trúng cache, nó đánh dấu `key` là mới dùng nhất, tăng `self.hits` và trả về giá trị đã lưu.
- `set(key, value)` lưu hoặc cập nhật `key` ở vị trí mới dùng nhất; nếu kích thước vượt quá `self.maxsize`, nó xóa phần tử lâu chưa dùng nhất và tăng `self.evictions` thêm `1`.
- Gọi `set(key, new_value)` cho một key đã tồn tại phải cập nhật giá trị mới mà không làm tăng kích thước, không đẩy nhầm key khác và không tăng `self.evictions`.
