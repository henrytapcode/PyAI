Xây dựng app factory `create_app(docs, client, min_score=0.2) -> FastAPI` cho dịch vụ RAG. Viết code bên trong `create_app` (cùng model Pydantic hoặc hàm phụ nếu cần) và trả về đối tượng `FastAPI` đã cấu hình.

**Ví dụ**

```text
GET  /health                                           -> 200 {"status": "ok", "docs": 6}
GET  /documents/refunds                                -> 200 {"id": "refunds", "text": "Refunds take 5..."}
GET  /documents/missing                                -> 404 {"detail": "document not found"}
POST /ask {"question": "How long do refunds take?"}    -> 200 {"answer": "...", "sources": ["refunds", ...], "scores": [0.712, ...], "usage": {"prompt_tokens": ..., "completion_tokens": ...}}
POST /ask {"question": "Can I pay with crypto?"}       -> 200 {"answer": "I don't know based on the provided context.", "sources": [], "scores": [], "usage": {"prompt_tokens": 0, "completion_tokens": 0}}
POST /ask {"question": ""}                             -> 422
```

**Quy tắc**
- Mỗi phần tử trong `docs` có dạng `{"id": str, "text": str}`. Gọi `client.embed([d["text"] for d in docs])` **đúng một lần** trong `create_app` lúc tạo app.
- `GET /health` trả về `{"status": "ok", "docs": len(docs)}`.
- `GET /documents/{doc_id}` trả về `{"id": ..., "text": ...}` cho tài liệu khớp `doc_id`, hoặc ném `HTTPException(status_code=404, detail="document not found")` nếu không có.
- `POST /ask` nhận JSON kiểm tra bằng Pydantic: `question` dài `1..300`, `top_k` là số nguyên `1..5` mặc định `2`.
- Xếp hạng toàn bộ `docs` theo `cosine(q_vec, doc_vec)` giảm dần (hòa thì giữ thứ tự gốc), lấy `top_k` phần tử đầu, rồi bỏ các mục có `score < min_score`.
- Nếu không còn mục nào, trả về `answer="I don't know based on the provided context."`, `sources=[]`, `scores=[]` và `usage={"prompt_tokens": 0, "completion_tokens": 0}` **mà không gọi `client.chat`**.
- Ngược lại, gọi `client.chat` đúng một lần với message chứa `Context:` và các dòng `[1] <text>`, `[2] <text>`... theo đúng thứ tự `sources`. Nếu model trả về đúng câu từ chối `"I don't know based on the provided context."`, đặt `sources=[]` và `scores=[]`; ngược lại trả về `[doc["id"] for doc in hits]` và `scores=[round(score, 3) ...]` cùng thứ tự, kèm `usage` (`prompt_tokens`, `completion_tokens`).
- Giữ toàn bộ trạng thái index bên trong `create_app` (không dùng biến trạng thái ở cấp module).
