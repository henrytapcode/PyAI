Hàm `check_reply` quyết định câu trả lời của mô hình có dùng được không và ghi lại chuyện đã xảy ra vào log. Các thông báo đã được viết sẵn, nhưng mỗi `logger.___(...)` còn một chỗ trống ở vị trí của level. Hãy thay mỗi `___` bằng method logging đúng: `debug`, `info`, `warning`, `error` hoặc `critical`. Chọn từng cái dựa vào comment bên cạnh và bảng các level ở §2.

**Ví dụ**

| lời gọi | trả về | log |
|---|---|---|
| `check_reply("hello", 1)` | `True` | một record `DEBUG`: `reply has 5 characters` |
| `check_reply("", 1)` | `False` | một record `WARNING`: `empty reply, retrying (attempt 1)` |
| `check_reply("", 3)` | `False` | một record `ERROR`: `giving up after 3 attempts` |

**Quy tắc**
- Chỉ đổi ba chỗ trống. Các thông báo và dòng `return` đã đúng sẵn.
- Các test đọc log bằng `caplog`, nên level của từng record sẽ được kiểm tra.
