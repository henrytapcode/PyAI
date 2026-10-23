Điền vào ba chỗ trống (`___`) để cả hai dict comprehension hoạt động. `lengths` ánh xạ mỗi từ sang số ký tự của nó. `long_lengths` chỉ giữ những mục của `lengths` mà từ có ít nhất 5 ký tự.

**Ví dụ**

Với `words = ["token", "prompt", "model", "ai"]`:

| tên | giá trị |
|---|---|
| `lengths` | `{"token": 5, "prompt": 6, "model": 5, "ai": 2}` |
| `long_lengths` | `{"token": 5, "prompt": 6, "model": 5}` |

**Quy tắc**
- Thay mọi `___` và giữ nguyên phần code còn lại.
- Cả hai kết quả phải được tạo bằng dict comprehension, không dùng vòng lặp.
- Bấm **Kiểm tra** để chạy test.
