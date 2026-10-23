Hai hàm đã gần xong, nhưng còn thiếu ba từ. Thay mỗi `___` bằng từ đúng (một loại lỗi hoặc một giá trị) để tuổi không hợp lệ gây ra lỗi rõ ràng và `age_or_none` biến dữ liệu xấu thành `None`.

**Ví dụ**

| lời gọi | kết quả |
|---|---|
| `validate_age(30)` | `30` |
| `validate_age(200)` | raise một lỗi với thông báo `age must be between 0 and 120, got 200` |
| `age_or_none("25")` | `25` |
| `age_or_none("x")` | `None` |
| `age_or_none("200")` | `None` |

**Quy tắc**
- Chỉ điền ba chỗ trống; cấu trúc `try`, `except` và `else` đã đúng sẵn.
- Tuổi từ `0` đến `120` (gồm cả hai đầu) là hợp lệ.
- `age_or_none` không được sập với bất kỳ văn bản nào: cả văn bản xấu lẫn tuổi ngoài khoảng đều gây cùng một loại lỗi.
- Bấm **Check** để chạy test.
