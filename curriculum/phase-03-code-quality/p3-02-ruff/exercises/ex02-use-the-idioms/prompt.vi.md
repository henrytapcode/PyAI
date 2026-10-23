Ruff thích một số dạng viết hơn những dạng khác: `is None` thay cho `== None` (`E711`), `not in` thay cho `not ... in` (`E713`), và `if flag:` thay cho `if flag == True:` (`E712`). Mỗi hàm bên dưới có một `___` ở chỗ cần dùng cách viết đó. Hãy thay mỗi `___` bằng dạng mà ruff muốn, dựa vào §7 của bài. Các test cũng kiểm tra đáp án của bạn chạy đúng, chứ không chỉ trông đúng.

**Ví dụ**

| lời gọi | kết quả |
|---|---|
| `describe(None)` | `"no data"` |
| `describe([1, 2])` | `"got 2 rows"` |
| `is_unknown("eggs", {"spam", "ham"})` | `True` |
| `switch_state("yes")` | `"on"` |

**Quy tắc**
- Chỉ đổi ba chỗ trống `___`.
- Ở mỗi chỗ trống hãy viết một điều kiện hoặc một biểu thức, không phải cả một câu lệnh.
