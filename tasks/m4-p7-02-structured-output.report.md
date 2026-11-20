# Báo cáo hoàn thành: `m4-p7-02-structured-output`

## 1. Đã làm gì

- Tạo hoàn chỉnh bài học `curriculum/phase-07-llm/p7-02-structured-output/` (chạy Pyodide, không có `runner: local`, mọi lời gọi LLM đi qua `pyai_llm`) gồm:
  - `meta.yaml`: `phase: p7`, `order: 2`, `tags: [llm]`, `prerequisites: [p7-01-llm-api]`, `duration_min: 14`, `outcomes` khớp `curriculum/syllabus.yaml`, `review_by: "2027-05-01"`, không có `runner`, kèm 2 link `further_reading`.
  - `lesson.en.md` và `lesson.vi.md`: mở đầu bằng bài toán đọc email khách hàng tạo ticket (`name`, `order_id`, `urgent`), đầy đủ 8 phần theo dàn ý:
    1. Văn xuôi không phải dữ liệu (`split()` mong manh vs `response_format={"type": "json", "schema": ...}` + `json.loads`).
    2. Schema (`type`, `properties`, `required`), bảng `| JSON type | Python type |`, callout `[!NOTE]`.
    3. Parse & validate (`bool` kiểm trước `int`), sơ đồ Mermaid `flowchart LR` (6 node), khối mẫu lỗi từ `FakeLLM(script=...)` kèm lời mời **Visualize**.
    4. `@dataclass class Ticket` và bẫy "giá trị rỗng giả" (`""`, `0`, `False`) với `__post_init__`.
    5. Pydantic `BaseModel` (`model_validate_json`, `.model_dump()`, `ValidationError` chỉ in `len(e.errors())`, `loc`, `type`), bảng so sánh `| approach | good for |`.
    6. Retry kèm phản hồi lỗi (nhắc lại `p7-01-llm-api` về lịch sử message) rồi fallback, trace table `| attempt | reply | errors | action |`, callout `[!WARNING]` không dùng `eval()`.
    7. Lỗi thường gặp (chạy thật lấy thông báo `JSONDecodeError`, `isinstance(True, int)`, `KeyError`, giá trị rỗng giả).
    8. Recap / Tóm tắt.
  - `examples/` (3 ví dụ kèm `.out`, `.en.md`, `.vi.md`):
    - `01_ticket_extractor.py`: trích xuất 3 email, email thiếu thông tin bị `__post_init__` loại.
    - `02_robust_parser.py`: `extract_json(text)` xử lý fence markdown, câu dẫn, JSON lỗi và không có JSON trên 5 reply từ `FakeLLM(script=...)`.
    - `03_retry_then_fallback.py`: `get_structured()` thử lại kèm phản hồi lỗi (hồi phục ở lượt 2) và rơi về fallback `needs_review=True` khi hỏng cả 3 lượt.
  - `exercises/` (2 bài tập):
    - `ex01-check-reply` (`kind: fill`): `check_reply(data, schema) -> list[str]` với format `"missing: <key>"` / `"wrong type: <key>"`, 6 test parametrize (starter: `0/6` pass, solution: `6/6` pass).
    - `ex02-structured-call` (`kind: code`): `parse_reply(text)` và `get_ticket(client, messages, schema, max_attempts=3)` (tự định nghĩa `_check_reply` nội bộ, không import từ `ex01`), 8 test gồm spy client kiểm tra nội dung retry và kiểm tra không mutate `messages` gốc (starter: `0/8` pass, solution: `8/8` pass), kèm `alternatives/01_raw_decode.py` dùng `json.JSONDecoder().raw_decode` (+ `.en.md`/`.vi.md`).
  - `quiz.yaml`: 16 câu hỏi (`6 mcq`, `4 output`, `4 fill`, `2 parsons`; độ khó 5 dễ / 8 vừa / 3 khó), 6 flashcard, tag `llm`, không dùng `pydantic` trong `output`/`fill`.
- Cập nhật `curriculum/glossary.yaml`: chỉ thêm 2 thuật ngữ chưa có là `parse` và `fallback` (3 thuật ngữ `structured output`, `JSON schema`, `validation` đã tồn tại sẵn trong glossary nên giữ nguyên).

## 2. File đã sửa / tạo

- Sửa:
  - `curriculum/glossary.yaml` (thêm `parse`, `fallback`)
- Tạo mới:
  - `curriculum/phase-07-llm/p7-02-structured-output/meta.yaml`
  - `curriculum/phase-07-llm/p7-02-structured-output/lesson.en.md`
  - `curriculum/phase-07-llm/p7-02-structured-output/lesson.vi.md`
  - `curriculum/phase-07-llm/p7-02-structured-output/quiz.yaml`
  - `curriculum/phase-07-llm/p7-02-structured-output/examples/01_ticket_extractor.{py,out,en.md,vi.md}`
  - `curriculum/phase-07-llm/p7-02-structured-output/examples/02_robust_parser.{py,out,en.md,vi.md}`
  - `curriculum/phase-07-llm/p7-02-structured-output/examples/03_retry_then_fallback.{py,out,en.md,vi.md}`
  - `curriculum/phase-07-llm/p7-02-structured-output/exercises/ex01-check-reply/{exercise.yaml,prompt.en.md,prompt.vi.md,starter.py,solution.py,test_exercise.py}`
  - `curriculum/phase-07-llm/p7-02-structured-output/exercises/ex02-structured-call/{exercise.yaml,prompt.en.md,prompt.vi.md,starter.py,solution.py,test_exercise.py}`
  - `curriculum/phase-07-llm/p7-02-structured-output/exercises/ex02-structured-call/alternatives/01_raw_decode.{py,en.md,vi.md}`
  - `tasks/m4-p7-02-structured-output.report.md`

## 3. Kết quả lệnh kiểm tra

- `uv run python tools/validate.py --path curriculum/phase-07-llm/p7-02-structured-output`:
  - `OK: 0 error(s), 0 warning(s). Checked 1 lessons, 7 markdown pairs, 3 examples, 2 exercises, 1 alternatives, 16 questions.`
- Starter vs Solution (browser runner `tools/pyrunner/runner.py`):
  - `ex01-check-reply`: starter `0 / 6` (`ok=False`), solution `6 / 6` (`ok=True`).
  - `ex02-structured-call`: starter `0 / 8` (`ok=False`), solution `8 / 8` (`ok=True`).
- `uv run python -m pytest curriculum/phase-07-llm`:
  - `29 passed in 0.05s` (exit 0).
- `uv run ruff check curriculum/phase-07-llm`:
  - `All checks passed!` (exit 0).
- Quét pattern cấm (`input(|time\.sleep|requests\.|urllib|open\(|eval\(|pydantic`) trong `curriculum/phase-07-llm/p7-02-structured-output/**/*.py`:
  - `hits: 0`.
- Kiểm tra `-W error` cho 9 code block Python trong `lesson.en.md`, 3 file `examples/*.py`, và 10 câu quiz chạy code (`output`, `fill`, `parsons`):
  - Tất cả chạy exit 0, stderr rỗng, stdout khớp.
- Khối **Visualize** (§3, block #3 trong `lesson.en.md`/`lesson.vi.md`) kiểm bằng `tools/pyrunner/tracer.py`:
  - `102` steps (< 600), `truncated=False`, `error=None`.
- Kiểm tra độ dài MCQ (`quiz.yaml`):
  - `violations: 0`, `strictly_longest: 1 out_of: 12` (`p7-02-q08` bản EN `[47, 44, 47, 48]`, đáp án đúng dài hơn distractor dài nhất đúng 1 ký tự, đạt tỷ lệ `1/12 <= 1/3`).
- `uv run python -c "import pydantic; print(pydantic.VERSION)"`:
  - `2.12.5`.
- Kiểm tra schema `curriculum/glossary.yaml` bằng `tools/schema/glossary.schema.json`:
  - `glossary schema errors: 0`.
- `uv run python tools/build_content.py`:
  - `Built 41 lessons, 9 exams, 246 flashcards, 659 questions -> apps\web\src\generated` (exit 0).
- Mở thử 2 link `further_reading` (với `User-Agent: Mozilla/5.0` qua `urllib.request`):
  - `https://json-schema.org/learn/getting-started-step-by-step` -> HTTP `200`.
  - `https://docs.pydantic.dev/latest/concepts/models/` -> HTTP `200` (redirect tới `https://pydantic.dev/docs/validation/latest/concepts/models/`).
- `git status --short`:
  - `M curriculum/glossary.yaml`, `?? curriculum/phase-07-llm/p7-02-structured-output/`, `?? tasks/` (và `?? .hallmark/` có sẵn từ trước trong repo).

## 4. Hành vi của `pyai_llm` và điều còn chưa chắc

- Hành vi cần lưu ý của `packages/pyai_llm/pyai_llm.py` (`_extract_schema_values`):
  1. Giá trị kiểu `integer`/`number` được trích tuần tự theo `_NUMBER_RE = re.compile(r"-?\d+(?:\.\d+)?")` trên toàn bộ `last_user` chứ không gắn với `<key>: <val>`, nên nếu một trường chuỗi đứng trước có chứa dấu gạch nối kèm số (ví dụ `ORD-1042`) thì số `-1042` sẽ bị rút vào trường số. Bài học chọn giá trị số nguyên dương (`order_id: 1042`) để khớp tự nhiên.
  2. Mọi trường `boolean` trong cùng schema dùng chung một cờ `has_bool_true` (chỉ cần đâu đó trong `last_user` có `yes` hoặc `true`), và các kiểu JSON khác ngoài `string`/`integer`/`number`/`boolean` (như `array`/`object`) sẽ nhận `""`. Không sửa `pyai_llm.py` theo đúng rule của task; các bài ví dụ/bài tập giữ 1 trường boolean và dùng 4 kiểu cơ bản được hỗ trợ.
- Điều còn chưa chắc:
  - Các bài tập và ví dụ đã kiểm qua CPython (`pytest`, `-W error`, `tools/pyrunner/runner.py`, `tools/pyrunner/tracer.py`), nhưng chưa chạy trực tiếp trong runtime Pyodide thật trên trình duyệt (chỉ suy ra tương thích vì `pydantic 2.12.5` trùng bản ghim và bài tập/ví dụ dùng thuần thư viện chuẩn + `pyai_llm`).
  - `tools/validate.py` chạy với `--path curriculum/phase-07-llm/p7-02-structured-output` (toàn bộ bài mới pass 0 lỗi), chưa chạy `validate.py` toàn bộ repo không có `--path`; riêng `curriculum/glossary.yaml` đã kiểm riêng qua `glossary.schema.json` (0 lỗi).
