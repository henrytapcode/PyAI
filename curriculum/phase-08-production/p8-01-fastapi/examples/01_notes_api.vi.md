# API ghi chú trong bộ nhớ

**Ví dụ này cho thấy:** Kết hợp `GET`, `POST` (`201 Created`), path parameter và `HTTPException` (`404`) trong một dịch vụ ghi chú nhỏ chạy qua `TestClient`.

**Từng bước**
1. Dòng 7–12 tạo app `FastAPI`, dict `notes` rỗng và Pydantic model `NoteCreate` bắt buộc chuỗi `text` không rỗng.
2. Dòng 15–24 định nghĩa `GET /notes` để liệt kê ghi chú theo thứ tự ID và `GET /notes/{note_id}` để lấy một ghi chú hoặc raise `HTTPException` `404`.
3. Dòng 27–31 định nghĩa `POST /notes` với `status_code=201` để cấp ID tiếp theo, lưu ghi chú và trả về bản ghi vừa tạo.
4. Dòng 34–49 gửi lần lượt sáu request qua `TestClient(app)` và in mỗi request trên một dòng gọn.

**Để ý:** Gọi `POST /notes` cập nhật ngay dict `notes` trong RAM, nên lần gọi `GET /notes` thứ hai thấy đủ cả hai bản ghi mới mà không cần database.

**Tự thử:** Thêm một bước `("POST", "/notes", {"text": ""})` vào cuối `steps` và xem FastAPI trả về `422` mà không thêm ghi chú thứ ba.
