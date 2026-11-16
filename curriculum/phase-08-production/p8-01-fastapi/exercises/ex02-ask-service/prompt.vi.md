Xây dựng một dịch vụ FastAPI tra cứu tài liệu nhỏ từ bộ khung `app`, từ điển `DOCS` và `AskRequest` có sẵn. Viết code của bạn trong `AskRequest`, `health()` và `ask()`, dùng `return` để trả về dictionary kết quả từ các hàm route.

**Ví dụ**

```text
GET  /health                                       -> 200 {"status": "ok"}
POST /ask {"question": "FastAPI tests"}            -> 200 {"question": "FastAPI tests", "sources": [3, 4]}
POST /ask {"question": "FastAPI tests", "top_k": 5}-> 200 {"question": "FastAPI tests", "sources": [3, 4, 1]}
POST /ask {"question": "unknown topic"}            -> 404 {"detail": "no matching documents"}
POST /ask {"question": ""}                         -> 422
```

**Quy tắc**
- Ràng buộc `AskRequest` bằng `Field(...)`: `question` dài `1..200` ký tự, `top_k` nguyên trong `1..5` với mặc định `2`.
- `GET /health` phải trả về `{"status": "ok"}`.
- Trong `POST /ask`, so từ bằng cách đổi chữ thường và tách theo khoảng trắng (`text.lower().split()`), giữ các `doc_id` có số từ chung `> 0`, sắp xếp theo số từ chung giảm dần rồi `doc_id` tăng dần, lấy tối đa `top_k` ID.
- Nếu không có tài liệu nào khớp, raise `HTTPException(status_code=404, detail="no matching documents")`.
