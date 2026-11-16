# Kiểm tra build context và lộ secret với .dockerignore

**What it shows:** Lọc cây thư mục của một dự án RAG bằng `fnmatch` và `PurePosixPath` để thu gọn build context và kiểm tra xem `.env` có bị lọt vào image hay không.

**Step by step**
1. Dòng 6–27 liệt kê 11 đường dẫn mẫu của dự án (`PROJECT_FILES`) và danh sách quy tắc `.dockerignore` chuẩn (`SAFE_DOCKERIGNORE`).
2. Dòng 30–43 định nghĩa `is_ignored(rel_path, patterns)`, kiểm tra quy tắc thư mục kết thúc bằng `/` theo tiền tố hoặc thành phần đường dẫn, còn mẫu file dùng `fnmatch`.
3. Dòng 46–54 tách file thành hai danh sách `included` và `excluded` qua `audit_context`.
4. Dòng 57–72 in các file được gửi vào build context, các file bị loại, rồi chạy bước kiểm tra an toàn so sánh `SAFE_DOCKERIGNORE` với danh sách bị thiếu `.env`.

**Notice:** File `.env.example` vẫn được giữ lại trong build context trong khi `.env` bị chặn đứng, cho thấy quy tắc `.dockerignore` chặn đúng file chứa bí mật mà không ẩn file mẫu.

**Try it yourself:** Thử bỏ `"data/raw/"` khỏi `SAFE_DOCKERIGNORE` và quan sát `data/raw/handbook.pdf` lập tức lọt vào build context làm phình dung lượng image.
