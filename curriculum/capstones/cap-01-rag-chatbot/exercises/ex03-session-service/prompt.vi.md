Xây dựng app factory `create_app(make_bot, clock, session_ttl=600.0, max_sessions=100) -> FastAPI` cho dịch vụ chat có quản lý session. Khác với đoạn code §6 trong bài học chỉ giữ dict lịch sử thuần Python, bài tập này yêu cầu bạn bổ sung đủ các route và mã trạng thái HTTP bằng FastAPI, bot riêng cho từng session, dọn phiên hết hạn ở đầu mọi request, mã `404` cho phiên thiếu hoặc đã hết hạn, mã `422` cho câu hỏi rỗng, và đếm số thứ tự lượt. Hãy viết code bên trong `create_app` (cùng model Pydantic hoặc hàm phụ nếu cần) và trả về đối tượng `FastAPI` đã cấu hình. Khi chạy thật cùng lời giải `ex01`, bạn nối bằng cách truyền `lambda: ChatBot(DOCS, client)` cho tham số `make_bot`.

**Ví dụ**

```python
from fastapi.testclient import TestClient

client = TestClient(create_app(make_bot, clock, session_ttl=60.0, max_sessions=2))

client.get("/health").json()
# -> {"status": "ok", "active_sessions": 0}

s1 = client.post("/sessions")
# status_code == 201, s1.json() -> {"session_id": "s1"}

r1 = client.post("/sessions/s1/messages", json={"question": "How much does shipping cost?"})
# status_code == 200, r1.json() -> {"answer": "...", "sources": [...], "rewritten": "...", "turn": 1}

client.get("/sessions/s1").json()
# -> {"session_id": "s1", "turns": [{"question": "How much does shipping cost?", "answer": "..."}]}

clock.advance(60.0)
client.get("/sessions/s1").status_code
# -> 404
```

**Quy tắc**

- Đúng chữ ký `create_app(make_bot, clock, session_ttl: float = 600.0, max_sessions: int = 100) -> FastAPI`. Ném `ValueError` ngay khi gọi `create_app` nếu `max_sessions < 1` hoặc `session_ttl <= 0`.
- Giữ toàn bộ trạng thái phiên bên trong closure của `create_app` để các app tạo ra luôn độc lập (không dùng biến trạng thái cấp module).
- Lưu mỗi session dưới dạng `{"bot": ..., "turns": list[{"question", "answer"}], "last_seen": float, "created": int}` với mã tất định `"s1"`, `"s2"`, … theo bộ đếm của app.
- **Hết hạn:** ở đầu **mỗi** request, xóa mọi session có `clock() - last_seen >= session_ttl`.
- `GET /health` trả về mã `200` với `{"status": "ok", "active_sessions": n}`.
- `POST /sessions` trả về mã `201` với `{"session_id": "sN"}` và gọi `make_bot()` **đúng một lần** cho session mới. Nếu sau khi dọn vẫn còn đủ `max_sessions`, xóa session có `last_seen` nhỏ nhất (hòa thì bỏ session được tạo trước).
- `POST /sessions/{sid}/messages` kiểm tra body `{"question": str}` bằng Pydantic (`min_length=1` sau khi strip khoảng trắng, nên câu rỗng hoặc chỉ có khoảng trắng trả `422`), gọi `bot.ask(question)` (trả `{"answer", "sources", "rewritten"}`), lưu `{"question", "answer"}` vào `turns`, cập nhật `last_seen`, rồi trả về mã `200` với `{"answer", "sources", "rewritten", "turn": n}` (`n` đếm từ `1`).
- `GET /sessions/{sid}` cập nhật `last_seen` và trả về mã `200` với `{"session_id": sid, "turns": [...]}`.
- Cả hai route chứa `{sid}` trả mã `404` với `{"detail": "session not found"}` khi session không tồn tại hoặc đã hết hạn.
