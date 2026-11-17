# Kiểm tra build context và lộ secret với .dockerignore

**Ví dụ này cho thấy:** Lọc cây thư mục dự án RAG tính từ gốc build context bằng `fnmatchcase` và `split("/")` để chặn cả thư mục con như `rag/__pycache__` và kiểm tra `.env` không lọt vào image.

**Từng bước**
1. Dòng 5–26 liệt kê 11 đường dẫn mẫu của dự án (`PROJECT_FILES`) và danh sách quy tắc `.dockerignore` tính từ gốc (`SAFE_DOCKERIGNORE`) dùng `**/__pycache__` và `**/*.pyc`.
2. Dòng 29–50 định nghĩa `_match_from` và `is_ignored(rel_path, patterns)`, so khớp từng đoạn pattern từ gốc context (hoặc ở mọi cấp khi pattern bắt đầu bằng `**`), bỏ qua luật `!`.
3. Dòng 53–61 tách file thành hai danh sách `included` và `excluded` qua `audit_context`.
4. Dòng 64–79 in các file được gửi vào build context, các file bị loại, rồi chạy bước kiểm tra an toàn so sánh `SAFE_DOCKERIGNORE` với danh sách bị thiếu `.env`.

**Để ý:** File `.env.example` vẫn ở lại build context trong khi `.env` bị chặn đứng, đồng thời `**/__pycache__` và `**/*.pyc` bắt được cả `rag/__pycache__/retriever.cpython-313.pyc` mà mẫu `__pycache__/` hay `*.pyc` không có `**` sẽ bỏ sót.

**Tự thử:** Thử bỏ `"data/raw/"` khỏi `SAFE_DOCKERIGNORE` và quan sát `data/raw/handbook.pdf` lập tức lọt vào build context làm phình dung lượng image.
