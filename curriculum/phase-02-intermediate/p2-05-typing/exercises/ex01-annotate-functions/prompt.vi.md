Bốn hàm dưới đây đã được viết sẵn, nhưng thiếu type hint. Hãy thay mỗi `___` bằng hint đúng, để mỗi hint nói thật về những gì hàm nhận vào và trả về. Đừng sửa code bên trong các hàm.

**Ví dụ**

| hàm | cái gì vào | cái gì ra |
|---|---|---|
| `count_tokens(["Hello", "world"])` | một list các văn bản | `2` |
| `build_prompt("Hi")` | một câu hỏi, không có system prompt | `"Hi"` |
| `build_prompt("Hi", "Be brief.")` | một câu hỏi và một system prompt | `"Be brief.\nHi"` |
| `word_lengths(["hi", "hello"])` | một list các từ | `{"hi": 2, "hello": 5}` |
| `first_and_count(["a", "b"])` | một list các token | `("a", 2)` |

**Quy tắc**
- Thay cả 5 chỗ trống bằng hint. Dùng các dạng có sẵn như `list[str]` và `str | None`.
- `build_prompt` phải vẫn chạy được khi không có system prompt, nên hint của `system` phải cho phép `None`.
- Giữ nguyên tên hàm, tên tham số và giá trị mặc định.
- Python không kiểm tra hint, nên các test đọc các hint được lưu trong `__annotations__` (giống cách một type checker làm) và cũng gọi từng hàm.
