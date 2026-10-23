Hãy xây nửa đầu của bộ công cụ làm sạch văn bản: một `CleanConfig` frozen, hai hàm nhỏ `normalize_spaces` và `remove_urls`, và `clean_text`, hàm dùng chúng theo config. Trình soạn thảo có sẵn một khung với các bước `# TODO`. Hãy viết code bên trong class và các hàm. Các phần 2 đến 4 của bài học cho thấy từng phần.

**Ví dụ**

```python
normalize_spaces("  a   b \n")                          # "a b"
remove_urls("see https://example.com now")              # "see now"
clean_text("  Read https://x.io  TODAY ")               # "read today"
clean_text("Hello  WORLD", CleanConfig(lowercase=False))  # "Hello WORLD"
clean_text("hello brave new world", CleanConfig(max_chars=11))  # "hello brave"
```

**Quy tắc**
- `CleanConfig` là một frozen dataclass với `lowercase=True`, `drop_urls=True` và `max_chars=None`.
- `normalize_spaces` biến mọi chuỗi khoảng trắng, tab và xuống dòng thành một khoảng trắng và cắt hai đầu.
- `remove_urls` bỏ các từ bắt đầu bằng `http://` hoặc `https://` và nối các từ còn lại bằng một khoảng trắng. `www.example.com` không phải là link trong bài này.
- `clean_text` chạy các bước theo thứ tự: bỏ URL (nếu `drop_urls`), sửa khoảng trắng, chữ thường (nếu `lowercase`), cắt còn `max_chars` và bỏ khoảng trắng bên phải (nếu `max_chars` không phải `None`). `max_chars=0` cho chuỗi rỗng.
- `clean_text(text)` không có config thì dùng `CleanConfig()`.
- Nếu `text` không phải string, `raise TypeError("text must be a string")`.
