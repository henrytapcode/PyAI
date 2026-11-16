Hoàn thành ứng dụng FastAPI quản lý ghi chú trong bộ nhớ bằng cách thay từng ô `___` bằng tên field, method decorator, type hint hoặc mã trạng thái HTTP đúng.

**Ví dụ**

```text
GET  /notes       -> 200 []
POST /notes       -> 201 {"id": 1, "text": "ship v1"}   (body: {"text": "ship v1"})
GET  /notes/999   -> 404 {"detail": "note not found"}
GET  /notes/abc   -> 422
POST /notes       -> 422                                (body: {})
```

**Quy tắc**
- Thay mọi ô `___` trong `NoteCreate`, các decorator route và `get_note`.
- Giữ nguyên tên `app` và `notes`; bộ test sẽ dọn sạch `notes` qua fixture.
- Không đổi cấu trúc dictionary trả về.
