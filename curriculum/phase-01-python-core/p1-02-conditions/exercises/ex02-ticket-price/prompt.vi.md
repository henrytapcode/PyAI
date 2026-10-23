Hàm `ticket_price(age, is_student)` phải theo các quy tắc sau:

- dưới 5 tuổi: miễn phí (`0`)
- dưới 12 tuổi, **hoặc** từ 65 tuổi trở lên: `6`
- sinh viên từ 25 tuổi trở xuống: `9`
- những người còn lại: `12`

Code bên dưới có **3 lỗi**. Hãy chạy test, tìm và sửa chúng. Sửa **bên trong hàm**; hàm dùng `return` để trả về giá vé (bạn sẽ học hàm bài bản ở bài 5).

**Ví dụ**

| Gọi hàm | Trả về |
|---|---|
| `ticket_price(3, False)` | `0` |
| `ticket_price(8, False)` | `6` |
| `ticket_price(20, True)` | `9` |
| `ticket_price(30, True)` | `12` |

**Quy tắc**
- Trả về một số: `0`, `6`, `9` hoặc `12`.
- Giữ nguyên cấu trúc (`if` / `elif` / `else`); chỉ sửa các điều kiện.
