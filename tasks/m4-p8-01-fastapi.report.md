# Báo cáo M4 bước 22: `p8-01-fastapi`

## 1. Đã làm gì
- Tạo bài học mới `curriculum/phase-08-production/p8-01-fastapi/` (không tạo `phase-test.yaml`), song ngữ EN/VI theo `docs/CONTENT_GUIDE.md`:
  - `meta.yaml`: `phase: p8`, `order: 1`, `kind: lesson`, `level: beginner`, `tags: [production, apis, testing, typing]`, `prerequisites: [p2-05-typing]`, `duration_min: 16`, `review_by: "2027-05-01"`, không có trường `runner`, 3 link `further_reading` chính thức.
  - `lesson.en.md` và `lesson.vi.md`: mở đầu nối từ `p7-09-mini-project-rag`, 9 mục theo đúng dàn ý:
    1. HTTP trong 5 phút (kèm picture-in-text `text` fence và ví von quầy giao dịch).
    2. App đầu tiên `GET /health` (gọi qua `TestClient` và gọi trực tiếp `health()`, kèm khối `bash` chạy `uv run uvicorn main:app --reload`, `curl`, và giải thích `/docs`).
    3. Path và query parameter (`GET /docs/{doc_id}` với `doc_id: int`, `limit: int = 3`, `HTTPException(404)` và trace table 4 request).
    4. `POST` với Pydantic (`AskRequest` dùng `BaseModel` + `Field`, in gọn `(loc, type)`, đối chiếu `p7-02-structured-output`, sơ đồ Mermaid `flowchart TD` 8 node, callout `[!NOTE]`).
    5. Chọn status code có chủ ý (`201`, `400`, `404`, bảng so sánh 6 mã `200/201/400/404/422/500`, callout `[!WARNING]` không trả lỗi kèm `200`).
    6. Kiểm thử bằng `TestClient` và `pytest` (`make_client` + `@pytest.fixture def client()`, 3 hàm test `ok`, `422`, `404`, tự chạy và in `all tests passed`; có lời mời **Visualize**).
    7. Đặt LLM sau endpoint `POST /chat` dùng `FakeLLM(seed=0)` ở mức module, trả `answer` và `tokens`, nối sang `p8-04-monitoring` và `p8-05-mini-project`.
    8. Lỗi thường gặp (`data=` thay cho `json=`, khai báo body là `dict`, trả dict lỗi kèm `200`, quên `status_code=201`).
    9. Tóm tắt (5 gạch đầu dòng).
- Tạo 3 ví dụ chạy được kèm `.out` và giải thích EN/VI:
  - `examples/01_notes_api.py`: `GET /notes`, `GET /notes/{note_id}` (404), `POST /notes` (201).
  - `examples/02_validation_report.py`: gửi 5 payload tới `POST /ask`, in bảng status và lỗi đầu tiên.
  - `examples/03_chat_endpoint.py`: `POST /chat` với `FakeLLM(seed=0)` cho 3 câu hỏi + 1 request `temperature=2` (422).
- Tạo 2 bài tập kèm hint 3 tầng EN/VI:
  - `exercises/ex01-notes-routes` (`kind: fill`): 5 ô `___` (`text`, `get`, `201`, `int`, `404`), fixture reset `exercise.notes.clear()`, 5 test.
  - `exercises/ex02-ask-service` (`kind: code`): `DOCS`, `GET /health`, `POST /ask` với `AskRequest`, xếp hạng theo số từ chung giảm dần rồi `doc_id` tăng dần, 404 `"no matching documents"`, 6 hàm test (7 test case với `parametrize`), kèm `alternatives/01_annotated_sorted.py` (+ `.en.md`/`.vi.md`).
- Tạo `quiz.yaml`: 16 câu hỏi (`7 mcq`, `3 output`, `3 fill`, `3 parsons`; `5` dễ, `8` vừa, `3` khó) và 6 flashcard.
- Bổ sung 7 thuật ngữ mới vào cuối `curriculum/glossary.yaml`: `route`, `HTTP method`, `request body`, `path parameter`, `query parameter`, `Pydantic`, `TestClient` (bỏ qua `endpoint` vì đã có sẵn và `status code` vì đã có mục `HTTP status code`).

## 2. File đã sửa / tạo
- Sửa:
  - `curriculum/glossary.yaml`
- Tạo mới:
  - `curriculum/phase-08-production/p8-01-fastapi/meta.yaml`
  - `curriculum/phase-08-production/p8-01-fastapi/lesson.en.md`
  - `curriculum/phase-08-production/p8-01-fastapi/lesson.vi.md`
  - `curriculum/phase-08-production/p8-01-fastapi/quiz.yaml`
  - `curriculum/phase-08-production/p8-01-fastapi/examples/01_notes_api.py` (+ `.out`, `.en.md`, `.vi.md`)
  - `curriculum/phase-08-production/p8-01-fastapi/examples/02_validation_report.py` (+ `.out`, `.en.md`, `.vi.md`)
  - `curriculum/phase-08-production/p8-01-fastapi/examples/03_chat_endpoint.py` (+ `.out`, `.en.md`, `.vi.md`)
  - `curriculum/phase-08-production/p8-01-fastapi/exercises/ex01-notes-routes/{exercise.yaml,prompt.en.md,prompt.vi.md,starter.py,solution.py,test_exercise.py}`
  - `curriculum/phase-08-production/p8-01-fastapi/exercises/ex02-ask-service/{exercise.yaml,prompt.en.md,prompt.vi.md,starter.py,solution.py,test_exercise.py}`
  - `curriculum/phase-08-production/p8-01-fastapi/exercises/ex02-ask-service/alternatives/01_annotated_sorted.{py,en.md,vi.md}`
  - `tasks/m4-p8-01-fastapi.report.md`

## 3. Kết quả lệnh kiểm tra

| Kiểm tra | Kết quả | Thời gian |
|---|---|---|
| `uv run python tools/validate.py --path curriculum/phase-08-production/p8-01-fastapi` | `OK: 0 error(s), 0 warning(s). Checked 1 lessons, 7 markdown pairs, 3 examples, 2 exercises, 1 alternatives, 16 questions.` | 10.474 s |
| `uv run python tools/validate.py --fast` | `OK: 0 error(s), 0 warning(s). Checked 50 lessons, 380 markdown pairs, 148 examples, 100 exercises, 82 alternatives, 977 questions, 10 exams, 1 portfolio, 1 glossary, 1 interview.` | 295.98 s |
| `uv run python -m pytest curriculum/phase-08-production -p no:warnings --color=no` | `12 passed in 0.37s` | 1.219 s |
| `uv run ruff check curriculum/phase-08-production` | `All checks passed!` | — |
| Kiểm mẫu cấm (`uvicorn.run`, `.run(app`, `requests.`, `api_key`, `OPENAI`, `time.sleep`, `open(`) trên `.py`, `.yaml` | 0 kết quả (`grep hits: 0`) | — |
| `git diff --numstat curriculum/glossary.yaml` | `78  0  curriculum/glossary.yaml` (0 dòng xóa) | — |
| `uv run python tools/build_content.py` | `Built 50 lessons, 10 exams, 300 flashcards, 802 questions -> apps\web\src\generated` (tăng từ 49 lên 50 bài) | — |
| `git status --short` | Chỉ gồm `M curriculum/glossary.yaml`, `?? curriculum/phase-08-production/`, `?? tasks/` (và `.hallmark/` đã có từ trước) | — |

### Chi tiết bài tập (`runner.run_tests` và thứ tự test)
- `ex01-notes-routes`:
  - `starter.py`: `ok=False`, `passed=0/0`, `0.43 s` (crash ở mức module khi Pydantic gặp tên field `___`: `NameError: Fields must not use names with leading underscores`).
  - `solution.py`: `ok=True`, `passed=5/5`, `0.187 s`.
- `ex02-ask-service`:
  - `starter.py`: `ok=False`, `passed=0/7`, `0.02 s` (0 test pass).
  - `solution.py`: `ok=True`, `passed=7/7`, `0.016 s`.
  - `alternatives/01_annotated_sorted.py`: `ok=True`, `passed=7/7`, `0.017 s`.
- Chứng minh độc lập thứ tự chạy: chạy riêng từng hàm test theo thứ tự ngược lại bằng `uv run python -m pytest <test_exercise.py> -k <tên_hàm>` cho cả 5 hàm của `ex01-notes-routes` và 6 hàm của `ex02-ask-service` (tổng 12 case), tất cả đều pass.

### Khối code trong lesson & khối Visualize
- Tất cả 10 khối `python` trong cả `lesson.en.md` và `lesson.vi.md` đều chạy sạch với `uv run python -W error`, `stderr` rỗng, mọi dòng in ra dưới 80 ký tự, mỗi khối chạy dưới `0.62 s`.
- Khối mời **Visualize** (§6, khối `python` #5) đo bằng `tools/pyrunner/tracer.py`:
  - `len(steps) = 50`, `truncated = False`, `time = 0.652 s`, `error = None`.
  - Tracer lọc `frame.f_code.co_filename == "<main>"` nên **không** bước vào code thư viện (FastAPI/Starlette/Pydantic/httpx), chỉ bước qua các hàm trong bài (`make_client`, `test_create_note_ok`, `test_empty_text_returns_422`, `test_missing_note_returns_404`) và hiển thị rõ biến toàn cục `notes` tăng lên `{1: 'ship v1'}` rồi được `notes.clear()` xóa sạch trước test tiếp theo.

### Kiểm tra độ dài MCQ (`quiz.yaml`)
- Kết quả chạy script kiểm tra độ dài MCQ: `mcqs: 7 violations: 0 longest-unique: 1` (chỉ `p8-01-q06` có đáp án đúng là phương án dài nhất duy nhất: EN `[111, 92, 93, 94]` ratio `1.19`; VI `[108, 96, 87, 89]` ratio `1.19`, nằm dưới ngưỡng `1.2` và `<= 1/3` tổng số MCQ).

### Link `further_reading` đã mở kiểm tra
- `https://fastapi.tiangolo.com/tutorial/first-steps/` -> HTTP `200`
- `https://fastapi.tiangolo.com/tutorial/testing/` -> HTTP `200`
- `https://docs.pydantic.dev/latest/concepts/models/` -> HTTP `200` (redirect sang `https://pydantic.dev/docs/validation/latest/concepts/models/`).

## 4. Điều còn chưa chắc / ghi chú API
- Ghi nhận thực tế trên `fastapi==0.162.7` và `pydantic==2.12.5`:
  - Gửi `data=` thay cho `json=` trong `TestClient.post` trả về `422` với `loc: ['body']`, `type: 'model_attributes_type'`.
  - Khi điền khuyết `___` làm tên field trong `BaseModel` (`ex01-notes-routes/starter.py`), Pydantic v2 ném `NameError` ngay lúc định nghĩa class vì cấm tên field bắt đầu bằng dấu gạch dưới; điều này vẫn khớp yêu cầu bài `fill` được phép lỗi khi import.
- Chưa chạy `pnpm --filter web build` và chưa khởi chạy dev server (theo đúng giới hạn task), nên chưa kiểm tra trực quan trên giao diện trình duyệt; toàn bộ nội dung và test đã được xác minh qua `validate.py`, `build_content.py`, `runner.run_tests`, `tracer.py`, `pytest`, và `python -W error`.
- Trong `curriculum/glossary.yaml`, giữ nguyên mục `HTTP status code` đã có sẵn thay vì thêm mục `status code` trùng nghĩa.
