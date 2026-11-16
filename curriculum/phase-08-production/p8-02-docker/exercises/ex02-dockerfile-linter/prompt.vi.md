Viết hàm tách Dockerfile `parse_dockerfile(text)` và hàm kiểm lỗi tĩnh `lint(text)` bằng Python thuần. Viết code của bạn bên trong hai hàm trong `starter.py` và dùng `return` để trả về kết quả.

**Ví dụ**

```python
parse_dockerfile("from python:3.13-slim\nRUN pip install \\\n  fastapi\n")
# [('FROM', 'python:3.13-slim'), ('RUN', 'pip install fastapi')]

lint("FROM python:latest\nCOPY . .\nRUN pip install -r requirements.txt\n")
# ['unpinned-base', 'copy-before-install']
```

**Quy tắc**
- `parse_dockerfile(text)` trả về `list[tuple[str, str]]`: tên lệnh viết hoa và phần đối số đã `strip`, bỏ qua dòng trống và comment `#`, nối các dòng kết thúc bằng `\` bằng một dấu cách.
- `lint(text)` trả về danh sách mã cảnh báo theo đúng thứ tự cố định sau (mỗi mã tối đa một lần, hoặc `[]` nếu sạch):
  1. `"unpinned-base"`: image trong `FROM` không có tag `:` hoặc dùng tag `:latest` (không phân biệt hoa/thường).
  2. `"copy-before-install"`: lệnh `COPY . .` đứng trước lệnh `RUN` đầu tiên có chứa `pip install`.
  3. `"secret-in-image"`: `COPY` hoặc `ADD` chép file `.env` (không tính `.env.example`), hoặc `ENV` khai báo biến có tên chứa `KEY`, `TOKEN` hoặc `SECRET`.
  4. `"localhost-cmd"`: `CMD` có chứa `127.0.0.1` hoặc `localhost`.
