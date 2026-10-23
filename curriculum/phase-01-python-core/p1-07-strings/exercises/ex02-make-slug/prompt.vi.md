`make_slug(title)` phải biến một tiêu đề thành slug cho URL: toàn chữ thường, bỏ khoảng trắng thừa, các từ nối với nhau bằng đúng một dấu gạch ngang. Code chạy được nhưng cho kết quả sai. Hãy tìm lỗi và sửa.

**Ví dụ**

| lời gọi | trả về |
|---|---|
| `make_slug("Hello World")` | `"hello-world"` |
| `make_slug("  Python   For AI  ")` | `"python-for-ai"` |

**Quy tắc**
- Sửa code bên trong hàm và `return` slug (đừng `print`).
- Có nhiều hơn một lỗi. Bấm **Kiểm tra** để xem test nào còn fail.
