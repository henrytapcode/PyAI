`passed(scores, threshold)` nhận một dict `tên -> điểm` và trả về **list tên đã sắp xếp** của những người có điểm **từ `threshold` trở lên**.

Đoạn code trong editor chạy được nhưng có lỗi. Hãy tìm và sửa. Viết code bên trong hàm và dùng `return` để trả kết quả.

**Ví dụ**

| Lời gọi | Kết quả |
|---|---|
| `passed({"Minh": 8, "Lan": 5, "Hoa": 3}, 5)` | `['Lan', 'Minh']` |
| `passed({"Lan": 1}, 5)` | `[]` |

**Quy tắc**

- Chỉ trả về tên, không trả về điểm.
- Điểm bằng `threshold` vẫn được tính là đậu.
- Các tên được trả về theo thứ tự bảng chữ cái.

Bấm **Kiểm tra** để chạy test.
