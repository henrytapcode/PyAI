# M5 bước 2d: capstone 1, exercise 3 "dịch vụ chat có session"

## Mục tiêu
Viết exercise `cap-01-ex03` trong `curriculum/capstones/cap-01-rag-chatbot/exercises/ex03-session-service/`, chạy trên **runner cục bộ** (`runner: local` trong `exercise.yaml`, vì cần FastAPI `TestClient`). Đây là mốc 3 trong bảng §7 của lesson (đọc lesson §6, §7 trước). Học viên gói session store (lesson §6) sau các route FastAPI, mỗi session một bot riêng.

**Quyết định thiết kế:** `create_app` nhận `make_bot` (hàm không tham số trả về object có `ask(question) -> {"answer", "sources", "rewritten"}`), không nhận `docs, client`. Lý do: exercise không phụ thuộc lời giải ex01, test dùng bot giả. Khi dùng thật, học viên truyền `lambda: ChatBot(DOCS, client)` từ ex01 (nói rõ trong prompt). Phải sửa dòng ex03 trong bảng §7 của lesson (EN + VI) cho khớp chữ ký mới.

## File được phép sửa/tạo
- `curriculum/capstones/cap-01-rag-chatbot/exercises/ex03-session-service/`: `exercise.yaml`, `prompt.en.md`, `prompt.vi.md`, `starter.py`, `solution.py`, `test_exercise.py`, `alternatives/01_*.py|.en.md|.vi.md`
- `curriculum/capstones/cap-01-rag-chatbot/lesson.en.md` và `lesson.vi.md`: **chỉ** dòng `ex03` trong bảng §7 (và câu trong §2 hoặc §6 nếu có nhắc đúng chữ ký `create_app(docs, client, ...)`)
- `tasks/m5-cap01-ex03.report.md`

## Không được đụng
- Mọi file khác (ex01, ex02, examples, meta, syllabus, tools, apps, packages, phase khác). Không tạo `quiz.yaml`.

## Hợp đồng (viết đúng vào prompt Rules)
```python
from fastapi import FastAPI

def create_app(make_bot, clock, session_ttl: float = 600.0, max_sessions: int = 100) -> FastAPI: ...
```
- Mọi trạng thái nằm trong closure của `create_app` (mỗi app độc lập; không biến cấp module).
- Session: `{"bot", "turns": list[{"question", "answer"}], "last_seen": float, "created": int}`. Mã session tất định: `"s1"`, `"s2"`, … theo bộ đếm của app.
- **Hết hạn:** đầu **mỗi** request, xóa mọi session có `clock() - last_seen >= session_ttl`.
- Route:
  - `GET /health` → 200 `{"status": "ok", "active_sessions": n}`.
  - `POST /sessions` → **201** `{"session_id": "sN"}`. Gọi `make_bot()` đúng một lần cho session mới. Nếu sau khi dọn vẫn đủ `max_sessions` thì bỏ session có `last_seen` nhỏ nhất (hòa thì bỏ session tạo trước).
  - `POST /sessions/{sid}/messages`, body `{"question": str}` (Pydantic, `min_length=1` sau khi strip: câu chỉ có khoảng trắng → 422) → 200 `{"answer", "sources", "rewritten", "turn": n}` với `n` là số thứ tự lượt trong session (đếm từ 1). Lưu lượt vào `turns`, cập nhật `last_seen`.
  - `GET /sessions/{sid}` → 200 `{"session_id": sid, "turns": [...]}` và cập nhật `last_seen`.
  - Session không có hoặc đã hết hạn → 404 `{"detail": "session not found"}` cho cả hai route có `{sid}`.
- `max_sessions < 1` hoặc `session_ttl <= 0` → `ValueError` khi gọi `create_app`.

Phần lesson **chưa** làm (ghi rõ trong prompt): các route và mã trạng thái HTTP, bot riêng cho từng session, dọn hết hạn ở mọi request, 404 cho session hết hạn, 422 cho câu rỗng, đếm lượt.

## Việc cần làm
1. `exercise.yaml`: `id: cap-01-ex03`, `kind: project`, `difficulty: 3`, `tags: [production, apis, testing]`, `runner: local`, title en/vi, 3 hint mỗi ngôn ngữ theo CONTENT_GUIDE (hint 1 trỏ lesson §6 và p8-05 app factory + ví dụ; hint 2 kế hoạch; hint 3 khung code 1–2 chỗ `...`).
2. `starter.py`: import (`fastapi`, `pydantic`), model body, `create_app` với docstring + ví dụ + `# TODO`, trả về một `FastAPI()` rỗng chưa có route (để test import được và fail từng cái). Không dùng `FakeClock` trong starter (test tự định nghĩa đúng class chuẩn của CONTENT_GUIDE).
3. `solution.py` theo hợp đồng; không chép ≥ 5 dòng liền từ lesson §6. `alternatives/01_*.py`: cách khác thật (ví dụ class `SessionStore` riêng + `OrderedDict` với `move_to_end` cho LRU, hoặc `Depends` để lấy session), kèm `.en.md`/`.vi.md`.
4. `test_exercise.py` (8–12 test, chỉ tập con pytest được phép + `fastapi.testclient.TestClient`; `FakeClock` chuẩn; bot giả `EchoBot` ghi lại câu hỏi và trả `{"answer": f"echo: {q}", "sources": [], "rewritten": q}`, có biến đếm số bot được tạo). Bắt buộc có test cho:
   - `/health` và `POST /sessions` trả 201 với `s1`, `s2`;
   - mỗi session có bot riêng (`make_bot` gọi đúng một lần mỗi session; lịch sử không lẫn);
   - `turn` tăng 1, 2 và `GET /sessions/{sid}` trả đúng `turns`;
   - hết hạn: sau `advance(session_ttl)` thì 404 (biên `>=`), còn `advance(session_ttl - 1)` thì vẫn 200; truy cập làm mới `last_seen`;
   - giới hạn: `max_sessions=2`, tạo 3 session → session ít dùng gần nhất bị bỏ (404), trong đó có ca session cũ được truy cập lại nên session khác bị bỏ;
   - 404 cho session không tồn tại; 422 cho `question` rỗng và chỉ khoảng trắng;
   - hai app tạo từ `create_app` không dùng chung session;
   - `ValueError` cho tham số sai.
5. `prompt.en.md` / `prompt.vi.md`: task 2–4 câu, **Example** (chuỗi request/response bằng `TestClient`), **Rules** đủ hợp đồng, một câu nói cách nối với `ChatBot` của ex01. VI tự nhiên, "bạn", không "ta"/"chúng ta".
6. Lesson §7 (EN + VI): dòng ex03 đổi thành `create_app(make_bot, clock, session_ttl, max_sessions)`, giữ nghĩa các cột khác. Cùng số dòng bảng, parity EN/VI giữ nguyên.

## Tiêu chí hoàn thành (checklist)
- [ ] Starter: mọi test fail; solution + alternative: mọi test pass (validate kiểm cả pytest lẫn runner)
- [ ] Validate capstone chỉ còn `missing quiz.yaml`, 0 cảnh báo
- [ ] Mutant (ở thư mục tạm): `>` thay `>=` khi hết hạn; dọn hết hạn chỉ ở `POST /sessions`; không cập nhật `last_seen` khi GET; dùng chung một bot cho mọi session; bỏ session mới nhất thay vì cũ nhất → mỗi cái làm ít nhất một test fail. Ghi vào report.

## Lệnh kiểm tra
Chạy từ gốc repo `D:\Proj\python-ai-platform`:
```bash
D=curriculum/capstones/cap-01-rag-chatbot
uv run python tools/validate.py --path $D
uv run python -m pytest $D -q
EXERCISE_TARGET=starter uv run python -m pytest $D/exercises/ex03-session-service -q
uv run ruff check $D
git status --short
```
Mong đợi: validate chỉ báo `missing quiz.yaml`; pytest xanh; lệnh starter 0 passed.

## Ghi chú cho worker
- Không chạy server hay dev server (TestClient chạy trong tiến trình, không cần server).
- Khuôn file và cách test FastAPI: `curriculum/phase-08-production/p8-05-mini-project/exercises/ex01-rag-service/`; quy ước `FakeClock` trong `docs/CONTENT_GUIDE.md`.

## Trạng thái
- Bước hiện tại: 5 (đạt vòng 1; boss kiểm: validate chỉ `missing quiz.yaml`, 42 test capstone pass, starter 0 pass, thêm 6 mutant của boss đều bị bắt; trong app qua runner cục bộ 16/16; chờ duyệt commit)
- Vòng: 1/3
- Số lần swap: 0
- Fallback: không
- Model: Gemini 4 Hydrogen (High)
