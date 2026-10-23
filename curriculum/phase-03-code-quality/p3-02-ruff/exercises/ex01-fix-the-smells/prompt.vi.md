Ruff sẽ báo nhiều vấn đề trong file này, và ba trong số đó là lỗi thật. Bạn không chạy được ruff trong app, nên hãy đọc code như một linter. Sửa file để mọi test đều qua: bỏ phần không dùng, cho `collect` một list mới ở mỗi lần gọi, chỉ bắt đúng lỗi mà `parse_count` mong đợi, và sửa lỗi gõ sai trong `total_length`. Hãy sửa trực tiếp trong code.

**Ví dụ**

| lời gọi | kết quả |
|---|---|
| `collect("a")` rồi `collect("b")` | `["a"]` rồi `["b"]` |
| `parse_count("abc")` | `-1` |
| `parse_count(None)` | raise `TypeError` |
| `total_length(["ab", "c"])` | `3` |

**Quy tắc**
- Xóa import không dùng.
- `collect` không được dùng chung một list mặc định giữa các lần gọi. Dùng mẫu `None` trong bài.
- `parse_count` chỉ được bắt `ValueError`, để các lỗi khác vẫn hiện rõ.
- `total_length` phải cộng độ dài của mọi chuỗi vào `total`.
