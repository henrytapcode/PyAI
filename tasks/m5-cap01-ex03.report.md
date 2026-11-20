# Báo cáo M5 bước 2d: `cap-01-ex03` (`ex03-session-service`)

## 1. Đã làm gì
- Tạo bài tập `cap-01-ex03` (`runner: local`, `kind: project`, `difficulty: 3`, `tags: [production, apis, testing]`) trong `curriculum/capstones/cap-01-rag-chatbot/exercises/ex03-session-service/`:
  - `exercise.yaml`: khai báo metadata, `runner: local`, 3 gợi ý leo thang song ngữ EN/VI theo `CONTENT_GUIDE.md` (hint 1 trỏ §6 và app factory `p8-05` kèm ví dụ, hint 2 kế hoạch từng bước, hint 3 khung code có chỗ trống `...`).
  - `prompt.en.md` và `prompt.vi.md`: mô tả nhiệm vụ, ví dụ dùng `TestClient`, đầy đủ hợp đồng `create_app(make_bot, clock, session_ttl=600.0, max_sessions=100) -> FastAPI`, nêu rõ phần bài học §6 chưa làm và cách nối `lambda: ChatBot(DOCS, client)` từ `ex01`.
  - `starter.py`: giữ import `fastapi`/`pydantic`, `MessageRequest` (`ConfigDict(str_strip_whitespace=True)`, `question: str = Field(min_length=1)`), hàm `create_app` kèm docstring + ví dụ + `# TODO`, trả về `FastAPI()` rỗng để import sạch và fail toàn bộ test.
  - `solution.py`: cài đặt hợp đồng đầy đủ trong closure của `create_app` (kiểm tra `max_sessions < 1` hoặc `session_ttl <= 0`, dọn hết hạn `clock() - last_seen >= session_ttl` ở đầu mỗi route, loại LRU theo `(last_seen, created)`, `POST /sessions` trả 201 với `"s1"`, `"s2"`, …, gọi `make_bot()` đúng một lần mỗi session, `POST /sessions/{sid}/messages` đếm lượt từ 1 và trả 422 cho câu rỗng/khoảng trắng, `GET /sessions/{sid}` cập nhật `last_seen`, 404 `{"detail": "session not found"}`), không chép từ bài học.
  - `alternatives/01_session_store_depends.py` (+ `.en.md` / `.vi.md`): tách lớp `SessionStore` dùng `collections.OrderedDict` + `move_to_end` cho LRU O(1) kết hợp `Depends` của FastAPI (dùng `typing.Annotated` để đạt chuẩn ruff `B008`).
  - `test_exercise.py`: 12 hàm test (16 test case sau parametrize) dùng `TestClient`, `FakeClock`, `EchoBot`, `BotFactory` kiểm tra đầy đủ `/health`, `POST /sessions` 201, cô lập bot giữa các session, tăng `turn` và `GET /sessions/{sid}`, ranh giới hết hạn `>= session_ttl`, dọn hết hạn ở cả `/health` và `POST .../messages`, làm mới `last_seen` khi `GET`/`POST`, loại LRU khi đầy và hòa theo thứ tự tạo, 404 cho session thiếu/hết hạn, 422 cho câu rỗng/chỉ khoảng trắng, cô lập trạng thái giữa hai app, và `ValueError` khi cấu hình sai.
- Cập nhật đúng dòng `ex03` trong bảng §7 của `curriculum/capstones/cap-01-rag-chatbot/lesson.en.md` và `lesson.vi.md` từ `create_app(docs, client, clock, session_ttl, max_sessions)` thành `create_app(make_bot, clock, session_ttl, max_sessions)` (giữ nguyên số dòng bảng và parity EN/VI).

## 2. File đã sửa / tạo
- Sửa:
  - `curriculum/capstones/cap-01-rag-chatbot/lesson.en.md`
  - `curriculum/capstones/cap-01-rag-chatbot/lesson.vi.md`
- Tạo mới:
  - `curriculum/capstones/cap-01-rag-chatbot/exercises/ex03-session-service/exercise.yaml`
  - `curriculum/capstones/cap-01-rag-chatbot/exercises/ex03-session-service/prompt.en.md`
  - `curriculum/capstones/cap-01-rag-chatbot/exercises/ex03-session-service/prompt.vi.md`
  - `curriculum/capstones/cap-01-rag-chatbot/exercises/ex03-session-service/starter.py`
  - `curriculum/capstones/cap-01-rag-chatbot/exercises/ex03-session-service/solution.py`
  - `curriculum/capstones/cap-01-rag-chatbot/exercises/ex03-session-service/test_exercise.py`
  - `curriculum/capstones/cap-01-rag-chatbot/exercises/ex03-session-service/alternatives/01_session_store_depends.py`
  - `curriculum/capstones/cap-01-rag-chatbot/exercises/ex03-session-service/alternatives/01_session_store_depends.en.md`
  - `curriculum/capstones/cap-01-rag-chatbot/exercises/ex03-session-service/alternatives/01_session_store_depends.vi.md`
  - `tasks/m5-cap01-ex03.report.md`

## 3. Kết quả lệnh kiểm tra
1. `uv run python tools/validate.py --path curriculum/capstones/cap-01-rag-chatbot`
   - Kết quả: `FAILED: 1 error(s), 0 warning(s).` — lỗi duy nhất là `ERROR curriculum/capstones/cap-01-rag-chatbot: missing quiz.yaml` (đúng kỳ vọng vì không tạo `quiz.yaml` ở bước này). Đã kiểm: 1 lesson, 10 cặp markdown, 3 example, 20 output block, 3 alternative, 3 exercise (gồm cả browser runner + pytest cho `starter`, `solution` và `alternatives`).
2. `uv run python -m pytest curriculum/capstones/cap-01-rag-chatbot -q`
   - Kết quả: exit code `0`, `42 passed` (`. * 42`).
3. `$env:EXERCISE_TARGET = "starter"; uv run python -m pytest curriculum/capstones/cap-01-rag-chatbot/exercises/ex03-session-service -q`
   - Kết quả: exit code `1`, `16 failed` (`FFFFFFFFFFFFFFFF`), `0 passed`.
4. `uv run ruff check curriculum/capstones/cap-01-rag-chatbot`
   - Kết quả: exit code `0`, `All checks passed!`.
5. `git status --short`
   - Chỉ có các file được phép trong `curriculum/capstones/cap-01-rag-chatbot/` (`lesson.en.md`, `lesson.vi.md`, `exercises/ex03-session-service/`) và `tasks/` (cùng `.hallmark/` có sẵn từ trước trong working tree).
6. Kiểm tra 5 mutant trong thư mục tạm bằng `pytest`:
   - `1_gt_instead_of_ge` (`>` thay `>=` khi hết hạn): **FAIL** 2/16 test (`test_session_expires_at_exact_ttl_boundary_across_routes`, `test_health_and_post_messages_purge_expired_sessions`).
   - `2_purge_only_post_sessions` (chỉ dọn ở `POST /sessions`): **FAIL** 2/16 test (`test_session_expires_at_exact_ttl_boundary_across_routes`, `test_health_and_post_messages_purge_expired_sessions`).
   - `3_no_refresh_on_get` (không cập nhật `last_seen` khi `GET /sessions/{sid}`): **FAIL** 2/16 test (`test_get_and_post_refresh_last_seen_before_expiry`, `test_evicts_least_recently_used_session_at_capacity`).
   - `4_shared_bot` (dùng chung một bot cho mọi session): **FAIL** 2/16 test (`test_health_and_create_sessions_return_201_with_sequential_ids`, `test_each_session_gets_isolated_bot_instance`).
   - `5_evict_newest` (loại session mới nhất thay vì cũ nhất): **FAIL** 2/16 test (`test_evicts_least_recently_used_session_at_capacity`, `test_eviction_tie_breaks_by_creation_order`).

## 4. Điều còn chưa chắc
- **Nối trực tiếp với `ChatBot` của `ex01`:** Bộ test của `ex03` dùng `EchoBot` giả theo thiết kế tách rời khỏi lời giải `ex01`, nên chưa chạy một test tích hợp nối thẳng `lambda: ChatBot(DOCS, FakeLLM())` vào `create_app` (dựa vào hợp đồng trả về `{"answer", "sources", "rewritten"}` khớp nhau giữa `ex01` và `ex03`).
- **Hòa `last_seen` sau `GET`/`POST` trong cùng một mốc `clock()` ở `alternatives/01_session_store_depends.py`:** `OrderedDict.move_to_end` xem lần truy cập gần nhất trong cùng tick là "mới hơn", nên nếu tạo `s1` và `s2` ở `t=0`, truy cập `s1` ở `t=0` rồi tạo `s3` ở `t=0`, `solution.py` sẽ loại `s1` (do `created` nhỏ hơn khi `last_seen` hòa) còn alternative sẽ loại `s2` (do `s1` vừa được chạm gần nhất). Khi đồng hồ có tiến (`clock.advance(...)`) giữa các thao tác hoặc khi không truy cập lại trong cùng tick thì cả hai hành xử giống hệt nhau.
