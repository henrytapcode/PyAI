Prompt do người dùng gõ thường rất lộn xộn: thừa dấu cách, chữ hoa chữ thường lung tung, và có những dòng rỗng. Hãy viết `clean_prompts(prompts)`. Hãy thử dùng một list comprehension. Hàm trả về một list mới gồm các prompt đã được làm sạch, và bỏ các prompt rỗng. Đặt code bên trong hàm và `return` kết quả.

**Ví dụ**

| đầu vào | đầu ra |
|---|---|
| `["  Hello   WORLD ", "", "   ", "What IS AI?"]` | `["hello world", "what is ai?"]` |

**Quy tắc**
- Đổi mỗi prompt sang chữ thường.
- Bỏ dấu cách ở hai đầu, và thu mọi dãy dấu cách, tab hoặc xuống dòng bên trong văn bản thành đúng một dấu cách.
- Bỏ các prompt rỗng hoặc chỉ gồm khoảng trắng.
- Giữ nguyên thứ tự ban đầu, và giữ các prompt trùng nhau.
- Không thay đổi list được truyền vào. Hãy trả về một list mới.
