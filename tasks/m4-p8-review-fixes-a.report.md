# Báo cáo M4 bước 25b (đợt a): sửa p8-01..p8-03 theo review

## 1. Đã làm gì

### B1 — p8-03 "Lỗi thường gặp" 2 (`temperature > 0`)
- Viết lại khối code ở mục 8.2 (`lesson.en.md` và `lesson.vi.md`) để chứng minh bằng số lần gọi model thật thông qua hàm `call_model` và hai biến đếm `bad_calls`, `good_calls`:
  - `ask_bad("hello", 0.8)` gọi 2 lần → `bad_calls == 1`, `same reply: True` (đóng băng mẫu ngẫu nhiên đầu tiên).
  - `ask_good("hello", 0.8)` gọi 2 lần → `good_calls == 2` (lần nào cũng gọi model).
- Cập nhật đoạn văn trước và sau khối ở cả EN và VI khớp đúng điều khối chứng minh; bỏ comment in chuỗi ngẫu nhiên gây lệch.

### M1 — p8-02 `.dockerignore` khớp từ gốc context
- Cập nhật §5 (`lesson.en.md` / `lesson.vi.md`) và `examples/03_dockerignore_check.py`:
  - Dùng đúng logic khớp từ gốc (`_match_from`, `is_ignored` với `fnmatchcase` và `split("/")`), bỏ `PurePosixPath`.
  - Giải thích `fnmatchcase`, `split("/")`, khác biệt so với `.gitignore` (pattern không có `/` trong `.dockerignore` chỉ khớp ở gốc, không khớp thư mục con), và ghi chú mô phỏng bỏ qua luật `!`.
  - Trong §5, chạy trực tiếp `old_patterns` (`__pycache__/`, `*.pyc`) để thấy `rag/__pycache__/retriever.cpython-313.pyc` bị lọt vào context, rồi chạy `good_patterns` (`.venv/`, `.git/`, `**/__pycache__`, `**/*.pyc`, `.env`, `data/raw/`) để loại sạch.
  - Cập nhật danh sách khuyên dùng ở §5, `examples/03_dockerignore_check.py`, `.en.md`/`.vi.md`, và `quiz.yaml` (`p8-02-f05`). Chạy lại `03_dockerignore_check.py` và ghi output thật vào `.out` (kết quả trùng khớp nên file `.out` giữ nguyên nội dung).

### M2 — p8-03 TTL dùng đồng hồ callable & `__call__`
- Áp dụng quy ước đồng hồ chung ở `p8-03-caching/lesson.{en,vi}.md` (§6) và `examples/03_ttl_lru_timeline.py`:
  - `FakeClock` lưu `self.t`, định nghĩa `__call__(self) -> float` trả về `self.t`, và `advance(self, seconds: float)`.
  - `TTLCache.__init__(self, ttl: float, clock)` và `TTLLRUCache.__init__(self, maxsize: int, ttl: float, clock)` bỏ type hint `clock` (vì `Callable` chưa được dạy trong chương trình) và gọi `self.clock()` thay cho `self.clock.now`.
  - Giải thích `__call__` trong 2 câu ngay chỗ `FakeClock` xuất hiện lần đầu ở §6 (EN & VI), và thêm term `__call__` vào `curriculum/glossary.yaml` (chỉ thêm mới ở cuối file).
  - Bỏ `"hay đổi múi giờ"` ở `lesson.vi.md` (§6, đổi thành `"khi đồng bộ giờ"`). Chạy lại `03_ttl_lru_timeline.py` để cập nhật `03_ttl_lru_timeline.out` và sửa `03_ttl_lru_timeline.{en,vi}.md`.

### M3, M4, M5 — Bổ sung test & chạy mutant
- **M3 (`p8-01` `ex02-ask-service/test_exercise.py`)**: thêm kiểm tra `top_k=0` → `422`, `"a" * 201` → `422`, `"a" * 200` → `404` (không bị `422`), query `"FASTAPI Tests"` khớp `"fastapi tests"`, và `"test"` → `404` (không khớp chuỗi con với `"tests"`/`"TestClient"`/`"Pytest"`).
- **M4 (`p8-02` `ex02-dockerfile-linter/test_exercise.py`, `prompt.{en,vi}.md`)**: thêm 6 case vào `parametrize` (`ENV HF_TOKEN=abc`, `ENV DB_SECRET=x`, `ADD .env /app/.env`, `FROM python:LATEST`, `RUN apt-get update` trước `COPY . .` rồi `RUN pip install`, `ENV MODE=prod API_KEY=abc`). Ghi rõ cú pháp `ENV` nhiều cặp trong `prompt.{en,vi}.md` (`solution.py` và `alternatives/01_regex_rule_table.py` đã hỗ trợ sẵn).
- **M5 (`p8-03` `ex02-llm-cache/test_exercise.py`)**: assert `cache.hits == 1`, `cache.misses == 1`, `cache.hit_rate() == pytest.approx(0.5)` sau khi entry hết hạn bị `get`; thêm `test_make_key_changes_when_max_tokens_or_message_role_changes` kiểm tra cả `max_tokens` và đổi `role`.

### M6 — Hint 3 tầng, starter không lộ, đổi đề p8-03 ex01
- `p8-01` `ex01-notes-routes`: sửa `starter.py` (bỏ nhắc `404` trong comment), viết lại 3 hint (hint 1 không liệt kê blank; hint 2 các bước bằng lời; hint 3 mẫu tổng quát `/items/{item_id}` không chép starter).
- `p8-01` `ex02-ask-service`: sửa `# TODO` trong `starter.py` (không lộ biểu thức code), viết lại hint 2 (chỉ bằng lời, không biểu thức Python) và hint 3 (chừa trống `overlap`, `key=`, `sources`) để ghép hint 2 + 3 không ra lời giải.
- `p8-02` `ex01-fix-dockerfile`: sửa `starter.py` và `prompt.{en,vi}.md` chỉ nêu số lỗi (4) và triệu chứng từng test fail, bỏ mẫu Dockerfile đã sửa khỏi Example; viết lại hint 1 (chỉ mục bài), hint 2 (nhóm lỗi bằng lời), hint 3 (chỉ 1 lỗi khó nhất về thứ tự cache layer).
- `p8-02` `ex02-dockerfile-linter`: bỏ biểu thức Python trong hint 2 (`text.splitlines()`, `(inst.upper(), args.strip())`, `parse_dockerfile(text)`).
- `p8-03` `ex01-lru-cache`: đổi yêu cầu thêm `self.evictions` và `peek(key)` (không đổi thứ tự, không đổi `hits`/`misses`); đặt blank vào `peek`, `evictions` và phần thứ tự (`move_to_end`, `last=False`); thêm 2 test mới + assert `evictions == 0` khi update key; viết lại 3 tầng hint đúng luật.
- `p8-03` `ex02-llm-cache`: viết lại hint 2 không dùng code Python, bỏ `{**m, ...}` trong hint 3 thay bằng `dict(msg)`.

### M7 — Tiêu đề tiếng Việt trong `examples/*.vi.md`
- Chuẩn hóa toàn bộ 9 file `examples/*.vi.md` của p8-01, p8-02, p8-03 về mẫu `p1-01`: `**Ví dụ này cho thấy:**`, `**Từng bước**`, `**Để ý:**`, `**Tự thử:**`.

### Minor m1–m5
- **m1**: đối chiếu và sửa toàn bộ số dòng trong `examples/*.en.md` / `*.vi.md` của cả 3 bài theo đúng file `.py` sau khi sửa.
- **m2 (`p8-01`)**: sửa `02_validation_report.vi.md` (`"bốn payload không hợp lệ"`); đổi `/docs/{doc_id}` → `/documents/{doc_id}` trong `lesson.{en,vi}.md` và `quiz.yaml` (`q01`, `f02`), giữ nguyên mô tả trang tài liệu `/docs` tự sinh ở §2; thêm `test_get_existing_note_returns_200_with_int_id` kiểm tra `type(body["id"]) is int` trong `ex01`.
- **m3 (`p8-02`)**: cập nhật `ex01-fix-dockerfile/test_exercise.py` yêu cầu tag có chữ số (chặn `python:slim`) và chấp nhận cả `--host 0.0.0.0` lẫn `--host=0.0.0.0`; sửa `lesson.{en,vi}.md` về layer filesystem (`RUN`, `COPY`, `ADD`) vs metadata, thời điểm gửi build context (khi bắt đầu `docker build`), ghim digest `@sha256:...`, và giải thích `split(None, 1)` tại lần xuất hiện đầu.
- **m4 (`p8-03`)**: giải thích `sha256` ở §3; sửa JSON ở text picture §3 thành `'{"max_tokens": 128, "messages": [...], "model": "fake-mini", "temperature": 0.0}'`; sửa tham chiếu `p2-07-decorators` ở §2 thành `@cache_results`; sửa lý do xóa cache khi đổi embedding model ở §4 thành để giải phóng RAM; gloss `"hàm thuần (pure function)"` lần đầu ở §2 và đổi `"tiêm"` → `"truyền vào (inject)"` trong bài, example 03 và flashcard `f06`; sửa Try-it của `examples/01_faq_cache.en.md` sang thêm biến thể lặp của `"What is tool calling?"`.
- **m5 (quiz)**: viết lại distractor vô lý thành hiểu nhầm thực tế ở `p8-01-q03`, `p8-02-q01`, `p8-03-q13`, `p8-03-q16`; bỏ dòng lọc `.env` vô nghĩa ở `p8-02-q10` (dùng `fnmatchcase`, 4 dòng); đổi `p8-02-q04` sang `fnmatchcase` và thêm `".env*"` vào đáp án chấp nhận `[[".env", ".env*"]]`.

## 2. File đã sửa / tạo

- Sửa `curriculum/glossary.yaml` (chỉ thêm term `__call__`)
- `curriculum/phase-08-production/p8-01-fastapi/`:
  - `lesson.en.md`, `lesson.vi.md`, `quiz.yaml`
  - `examples/01_notes_api.en.md`, `examples/01_notes_api.vi.md`
  - `examples/02_validation_report.en.md`, `examples/02_validation_report.vi.md`
  - `examples/03_chat_endpoint.en.md`, `examples/03_chat_endpoint.vi.md`
  - `exercises/ex01-notes-routes/exercise.yaml`, `starter.py`, `test_exercise.py`
  - `exercises/ex02-ask-service/exercise.yaml`, `starter.py`, `test_exercise.py`
- `curriculum/phase-08-production/p8-02-docker/`:
  - `lesson.en.md`, `lesson.vi.md`, `quiz.yaml`
  - `examples/01_parse_dockerfile.en.md`, `examples/01_parse_dockerfile.vi.md`
  - `examples/02_cache_simulator.en.md`, `examples/02_cache_simulator.vi.md`
  - `examples/03_dockerignore_check.py`, `examples/03_dockerignore_check.en.md`, `examples/03_dockerignore_check.vi.md`
  - `exercises/ex01-fix-dockerfile/exercise.yaml`, `prompt.en.md`, `prompt.vi.md`, `starter.py`, `test_exercise.py`
  - `exercises/ex02-dockerfile-linter/exercise.yaml`, `prompt.en.md`, `prompt.vi.md`, `test_exercise.py`
- `curriculum/phase-08-production/p8-03-caching/`:
  - `lesson.en.md`, `lesson.vi.md`, `quiz.yaml`
  - `examples/01_faq_cache.en.md`, `examples/01_faq_cache.vi.md`
  - `examples/02_embedding_cache.en.md`, `examples/02_embedding_cache.vi.md`
  - `examples/03_ttl_lru_timeline.py`, `examples/03_ttl_lru_timeline.out`, `examples/03_ttl_lru_timeline.en.md`, `examples/03_ttl_lru_timeline.vi.md`
  - `exercises/ex01-lru-cache/exercise.yaml`, `prompt.en.md`, `prompt.vi.md`, `solution.py`, `starter.py`, `test_exercise.py`
  - `exercises/ex02-llm-cache/exercise.yaml`, `test_exercise.py`
- Tạo mới: `tasks/m4-p8-review-fixes-a.report.md`

## 3. Kết quả lệnh kiểm tra

| Kiểm tra | Kết quả |
|---|---|
| `uv run python tools/validate.py --path .../p8-01-fastapi` | `OK: 0 error(s), 0 warning(s)` (1 lesson, 7 md pairs, 3 examples, 2 exercises, 1 alternative, 16 questions) |
| `uv run python tools/validate.py --path .../p8-02-docker` | `OK: 0 error(s), 0 warning(s)` (1 lesson, 7 md pairs, 3 examples, 2 exercises, 1 alternative, 16 questions) |
| `uv run python tools/validate.py --path .../p8-03-caching` | `OK: 0 error(s), 0 warning(s)` (1 lesson, 7 md pairs, 3 examples, 2 exercises, 1 alternative, 16 questions) |
| `uv run python -m pytest curriculum/phase-08-production -q -p no:warnings` | `98 passed` (toàn bộ phase 8) |
| `EXERCISE_TARGET=starter ... pytest ... --continue-on-collection-errors` | `53 failed, 1 error` (`ex01-notes-routes` lỗi ngay lúc import do `___` trong decorator), `0 passed` |
| `uv run ruff check curriculum/phase-08-production` | `All checks passed!` |
| `check_lesson_comments.py` (`p8-01..03`) | `comment mismatches: 0` |
| `git diff --numstat curriculum/glossary.yaml` | `12  0  curriculum/glossary.yaml` (0 dòng xóa) |
| Script kiểm tra độ dài MCQ (`p8-0[1-3]*/quiz.yaml`) | `p8-01`: 7 MCQ, `longest-unique 1`; `p8-02`: 7 MCQ, `longest-unique 2`; `p8-03`: 7 MCQ, `longest-unique 1`; `violations: 0` |

### Kết quả kiểm tra mutant (chạy trong thư mục tạm ngoài repo)

| Nhóm | Mutant | Kết quả pytest |
|---|---|---|
| m2 (`p8-01` ex01) | `note_id: float` thay cho `int` | `1 failed, 5 passed` |
| M3 (`p8-01` ex02) | Bỏ `.lower()` | `1 failed, 11 passed` |
| M3 (`p8-01` ex02) | Bỏ `ge=1` | `1 failed, 11 passed` |
| M3 (`p8-01` ex02) | Bỏ `max_length=200` | `1 failed, 11 passed` |
| M3 (`p8-01` ex02) | So chuỗi con (`w in text.lower()`) thay cho so từ | `1 failed, 11 passed` |
| M4 (`p8-02` ex02) | `ENV` chỉ kiểm `KEY` (bỏ `TOKEN`, `SECRET`) | `2 failed, 17 passed` |
| M4 (`p8-02` ex02) | Chỉ kiểm `COPY`, bỏ qua `ADD` | `1 failed, 18 passed` |
| M4 (`p8-02` ex02) | So `:latest` phân biệt hoa thường | `1 failed, 18 passed` |
| M4 (`p8-02` ex02) | `copy-before-install` tính mọi `RUN` thay vì `RUN` có `pip install` | `1 failed, 18 passed` |
| M4 (`p8-02` ex02) | `ENV` chỉ xét token đầu tiên | `1 failed, 18 passed` |
| M5 (`p8-03` ex02) | Entry hết hạn không tăng `self.misses` | `1 failed, 10 passed` |
| M5 (`p8-03` ex02) | `make_key` bỏ qua `**params` | `2 failed, 9 passed` |
| M5 (`p8-03` ex02) | `make_key` bỏ `role` khỏi message | `1 failed, 10 passed` |
| m3 (`p8-02` ex01) | `FROM python:slim` (không có số phiên bản) | `1 failed, 3 passed` |
| m3 (`p8-02` ex01) | `CMD` dùng `--host=0.0.0.0` (kiểm tra chấp nhận cả hai dạng) | `4 passed` |

## 4. Điều còn chưa chắc

- Khi `validate.py` chạy `tools/pyrunner/tracer.py` cho `p8-02-docker/examples/03_dockerignore_check.py`, tracer chạm giới hạn `MAX_STEPS = 600` và cắt trace (là cơ chế bình thường của `Visualize`), đồng thời Python in ra stderr `Exception ignored in: <generator object _match_from.<locals>.<genexpr> ...> tracer._TooManySteps` khi generator bị thu gom rác; `validate.py` vẫn thoát mã `0` (`OK: 0 error(s), 0 warning(s)`).
- Khi chạy `EXERCISE_TARGET=starter` không có `--continue-on-collection-errors`, `pytest` dừng ngay ở lỗi import của bài fill `p8-01/ex01-notes-routes` (`@app.___("/notes")`) nên không chạy tiếp các bài sau; khi chạy thêm `--continue-on-collection-errors`, cả 53 test thu thập được đều `FAILED` và 1 module lỗi lúc import (`0 passed`).
- Hai bài `p8-04-monitoring` và `p8-05-mini-project` chưa được sửa vì nằm ngoài phạm vi đợt A, nên quy ước đồng hồ callable (`FakeClock.__call__`) cho hai bài đó vẫn chờ đợt B.
