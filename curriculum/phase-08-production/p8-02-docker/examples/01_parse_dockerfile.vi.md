# Tách Dockerfile thành các lệnh và đếm layer

**Ví dụ này cho thấy:** Tách chuỗi `Dockerfile` thực tế thành danh sách tuple `(INSTRUCTION, args)` chuẩn hóa—bỏ qua comment, dòng trống và nối các dòng có `\`—rồi đếm số layer hệ thống file.

**Từng bước**
1. Dòng 3–14 khai báo `DOCKERFILE` gồm một dòng comment `#`, một dòng trống và lệnh `RUN pip install ...` chia hai dòng bằng `\`.
2. Dòng 17–34 viết hàm `parse_dockerfile(text)`: cắt khoảng trắng đầu cuối mỗi dòng, bỏ qua dòng rỗng hoặc bắt đầu bằng `#`, nối các dòng kết thúc bằng `\` vào `pending`, rồi tách phần tên lệnh viết hoa và đối số.
3. Dòng 37–46 in bảng `INSTRUCTION | ARGS` và đếm số lệnh tạo layer dữ liệu (`RUN`, `COPY`, `ADD`).

**Để ý:** `parse_dockerfile` gộp `RUN pip install --no-cache-dir \` và `-r requirements.txt` thành một mục `RUN` duy nhất, giúp các bước kiểm tra phía sau không đọc nhầm thành hai dòng rời.

**Tự thử:** Thêm dòng `ENV PYTHONUNBUFFERED=1` ngay sau `WORKDIR /app` và kiểm tra xem tổng số lệnh tăng từ `7` lên `8` trong khi số layer (`RUN`/`COPY`/`ADD`) vẫn là `3`.
