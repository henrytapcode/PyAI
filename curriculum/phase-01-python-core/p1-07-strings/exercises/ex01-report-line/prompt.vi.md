Viết hàm `report_line(model, tokens, cost)` trả về một dòng của bảng usage. Tên model căn trái trong 12 ký tự, số token căn phải trong 10 ký tự và có dấu phẩy ngăn cách hàng nghìn, còn chi phí căn phải trong 8 ký tự với 2 chữ số thập phân.

**Ví dụ**

| lời gọi | trả về |
|---|---|
| `report_line("small", 12345, 3.5)` | `"small           12,345    3.50"` |
| `report_line("big", 987, 0.126)` | `"big                987    0.13"` |

**Quy tắc**
- Viết code bên trong hàm và `return` chuỗi (đừng `print`).
- Dùng một f-string với format spec. Bấm **Kiểm tra** để chạy test.
