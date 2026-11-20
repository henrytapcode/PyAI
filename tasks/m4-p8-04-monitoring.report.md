# Báo cáo M4 bước 25: `p8-04-monitoring`

## 1. Đã làm gì

- Tạo bài học mới `curriculum/phase-08-production/p8-04-monitoring/` (không có `runner: local`, chạy hoàn toàn trong Pyodide với stdlib + `pyai_llm`, không dùng đồng hồ thật):
  - `meta.yaml`: `id: p8-04-monitoring`, `phase: p8`, `order: 4`, `kind: lesson`, `tags: [production, performance, logging, llm]`, `prerequisites: [p8-03-caching]`, `duration_min: 16`, `review_by: "2027-05-01"`, cùng 3 link `further_reading`.
  - `lesson.en.md` & `lesson.vi.md`: mở đầu bằng tình huống bot RAG tăng chi phí và chậm dần; 7 mục nội dung + Tóm tắt đúng dàn ý; có bảng so sánh `log chữ tự do` vs `log có cấu trúc (JSON)`, callout `[!WARNING]` (không log dữ liệu nhạy cảm), picture-in-text `text` giống hệt EN/VI ở §3, bảng trace nearest-rank (`p=50`, `p=95`, `n=10`), lời mời bấm **Visualize** ở §3, sơ đồ Mermaid `flowchart LR` (7 node) ở §5, callout `[!TIP]` ở §6, 4 lỗi thường gặp có output thật ở §7.
  - Khối **Visualize** (§3): kiểm bằng `tools/pyrunner/tracer.py` đạt **`steps=18`**, **`truncated=False`**, `error=None`.
- Tạo 3 ví dụ trong `examples/` kèm `.out`, `.en.md`, `.vi.md`, chạy sạch với `uv run python -I -W error` và `stderr=''`:
  - `01_request_log.py`: 8 request qua `FakeLLM(fail_times=1)` + `FakeClock` (1 lỗi `RateLimitError`, 2 cache hit, 5 cache miss), ghi JSON qua `logging` ra `sys.stdout`, cuối cùng in `logged_lines: 8`.
  - `02_latency_report.py`: 20 latency cố định, in bảng `metric | value` (`min`, `mean`, `p50`, `p90`, `p95`, `max`) và top 3 request chậm nhất.
  - `03_daily_budget.py`: 3 ngày dữ liệu cố định, ngày 3 bật cảnh báo sớm `budget warning: 85% of budget used ($17.00/$20.00)`.
- Tạo 2 bài tập trong `exercises/`:
  - `ex01-percentile` (`kind: fill`): gồm `percentile(values, p)` và `latency_report(values)`. Khác code bài học ở chỗ kiểm tra đầu vào (`raise ValueError` khi list rỗng hoặc `p` ngoài `(0, 100]`), ép `float`, và bổ sung `latency_report`. Starter import sạch (các ô `___` nằm trong thân hàm) và fail **0/5 test**: `ordered = ___(values)` nằm trước câu lệnh `if not values or p <= 0 or p > 100: raise ValueError(...)` nên ngay cả test `pytest.raises(ValueError)` cũng fail vì `NameError` thay vì `ValueError`.
  - `ex02-metrics-tracker` (`kind: code`): lớp `MetricsTracker` dùng `@dataclass _RequestMetric`, có `record()`, `summary()`, `alerts()` với mã ngắn (`"p95-latency"`, `"budget-exceeded"`, `"budget-warning"`, `"error-rate"`), tách biệt với hàm `summarize`/`check_alerts` trong bài học. Starter import sạch và fail **0/15 test** (trả `None`). Alternative `alternatives/01_parallel_lists.py` (+ `.en.md`, `.vi.md`) dùng list `_latencies` song song với biến cộng dồn `_total_cost`, `_error_count` thay cho list dataclass.
- Tạo `quiz.yaml`: 16 câu hỏi (7 `mcq`, 4 `output`, 3 `fill`, 2 `parsons`; độ khó: 5 dễ, 8 vừa, 3 khó) + 6 flashcard (`p8-04-f01`..`p8-04-f06`).
- Cập nhật `curriculum/glossary.yaml`: bỏ qua `latency` (đã có sẵn) và thêm 9 thuật ngữ mới (`metric`, `percentile`, `p50`, `p95`, `structured logging`, `alert`, `threshold`, `budget`, `observability`), 0 dòng xóa.

## 2. File đã sửa / tạo

- Sửa:
  - `curriculum/glossary.yaml`
- Tạo mới:
  - `curriculum/phase-08-production/p8-04-monitoring/meta.yaml`
  - `curriculum/phase-08-production/p8-04-monitoring/lesson.en.md`
  - `curriculum/phase-08-production/p8-04-monitoring/lesson.vi.md`
  - `curriculum/phase-08-production/p8-04-monitoring/examples/01_request_log.py`
  - `curriculum/phase-08-production/p8-04-monitoring/examples/01_request_log.out`
  - `curriculum/phase-08-production/p8-04-monitoring/examples/01_request_log.en.md`
  - `curriculum/phase-08-production/p8-04-monitoring/examples/01_request_log.vi.md`
  - `curriculum/phase-08-production/p8-04-monitoring/examples/02_latency_report.py`
  - `curriculum/phase-08-production/p8-04-monitoring/examples/02_latency_report.out`
  - `curriculum/phase-08-production/p8-04-monitoring/examples/02_latency_report.en.md`
  - `curriculum/phase-08-production/p8-04-monitoring/examples/02_latency_report.vi.md`
  - `curriculum/phase-08-production/p8-04-monitoring/examples/03_daily_budget.py`
  - `curriculum/phase-08-production/p8-04-monitoring/examples/03_daily_budget.out`
  - `curriculum/phase-08-production/p8-04-monitoring/examples/03_daily_budget.en.md`
  - `curriculum/phase-08-production/p8-04-monitoring/examples/03_daily_budget.vi.md`
  - `curriculum/phase-08-production/p8-04-monitoring/exercises/ex01-percentile/exercise.yaml`
  - `curriculum/phase-08-production/p8-04-monitoring/exercises/ex01-percentile/prompt.en.md`
  - `curriculum/phase-08-production/p8-04-monitoring/exercises/ex01-percentile/prompt.vi.md`
  - `curriculum/phase-08-production/p8-04-monitoring/exercises/ex01-percentile/starter.py`
  - `curriculum/phase-08-production/p8-04-monitoring/exercises/ex01-percentile/solution.py`
  - `curriculum/phase-08-production/p8-04-monitoring/exercises/ex01-percentile/test_exercise.py`
  - `curriculum/phase-08-production/p8-04-monitoring/exercises/ex02-metrics-tracker/exercise.yaml`
  - `curriculum/phase-08-production/p8-04-monitoring/exercises/ex02-metrics-tracker/prompt.en.md`
  - `curriculum/phase-08-production/p8-04-monitoring/exercises/ex02-metrics-tracker/prompt.vi.md`
  - `curriculum/phase-08-production/p8-04-monitoring/exercises/ex02-metrics-tracker/starter.py`
  - `curriculum/phase-08-production/p8-04-monitoring/exercises/ex02-metrics-tracker/solution.py`
  - `curriculum/phase-08-production/p8-04-monitoring/exercises/ex02-metrics-tracker/test_exercise.py`
  - `curriculum/phase-08-production/p8-04-monitoring/exercises/ex02-metrics-tracker/alternatives/01_parallel_lists.py`
  - `curriculum/phase-08-production/p8-04-monitoring/exercises/ex02-metrics-tracker/alternatives/01_parallel_lists.en.md`
  - `curriculum/phase-08-production/p8-04-monitoring/exercises/ex02-metrics-tracker/alternatives/01_parallel_lists.vi.md`
  - `curriculum/phase-08-production/p8-04-monitoring/quiz.yaml`
  - `tasks/m4-p8-04-monitoring.report.md`

## 3. Kết quả lệnh kiểm tra

- `uv run python tools/validate.py --path curriculum/phase-08-production/p8-04-monitoring` (chạy sau lần sửa cuối):
  - `OK: 0 error(s), 0 warning(s). Checked 1 lessons, 7 markdown pairs, 3 examples, 2 exercises, 1 alternatives, 16 questions.`
  - Thời gian chạy: `5.43s` (exit code 0).
- `uv run python tools/validate.py --fast`:
  - `OK: 0 error(s), 0 warning(s). Checked 53 lessons, 401 markdown pairs, 157 examples, 106 exercises, 85 alternatives, 1025 questions, 10 exams, 1 portfolio, 1 glossary, 1 interview.` (exit code 0).
- `uv run python -m pytest curriculum/phase-08-production -p no:warnings --color=no` (sau lần sửa cuối):
  - `64 passed in 0.43s` (exit code 0).
- `uv run ruff check curriculum/phase-08-production` (sau lần sửa cuối):
  - `All checks passed!` (exit code 0).
- Kiểm tra browser runner (`tools/pyrunner/runner.py`):
  - `ex01-percentile`: starter `ok=False passed=0/5`; solution `ok=True passed=5/5`.
  - `ex02-metrics-tracker`: starter `ok=False passed=0/15`; solution `ok=True passed=15/15`; `alternatives/01_parallel_lists.py` `ok=True passed=15/15`.
- Kiểm tra khối Visualize & toàn bộ Python block trong `lesson.en.md` và `examples/*.py` và `quiz.yaml`:
  - Khối Visualize (§3): `steps=18, truncated=False, error=None`.
  - Tất cả 10 khối Python trong lesson, 3 file example và các câu `output`/`fill`/`parsons` trong `quiz.yaml` chạy sạch với `-W error`, `stderr` rỗng.
- Kiểm tra độ dài MCQ (`quiz.yaml`):
  - `mcqs: 7 violations: 0 longest-unique: 0`.
- Kiểm tra từ khóa cấm trong `.py` và `.yaml` thuộc `p8-04-monitoring`:
  - Regex `time\.time|time\.sleep|perf_counter\(\)|monotonic\(\)|datetime\.now|_chat_calls|open\(|subprocess|requests\.|httpx`: `grep hits: 0` (rỗng).
- `git diff --numstat curriculum/glossary.yaml`:
  - `100	0	curriculum/glossary.yaml` (0 dòng xóa).
- `uv run python tools/build_content.py`:
  - `Built 53 lessons, 10 exams, 318 flashcards, 850 questions -> apps\web\src\generated` (số lesson tăng từ 52 lên 53).
- `git status --short`:
  - Chỉ có `M curriculum/glossary.yaml`, `?? curriculum/phase-08-production/p8-04-monitoring/`, ngoài `?? .hallmark/` và `?? tasks/` vốn có.
- Kiểm tra link `further_reading` (HTTP HEAD):
  - `https://docs.python.org/3/howto/logging.html` -> HTTP `200`
  - `https://docs.python.org/3/library/statistics.html#statistics.quantiles` -> HTTP `200`
  - `https://opentelemetry.io/docs/what-is-opentelemetry/` -> HTTP `200`

## 4. Điều còn chưa chắc

- Chưa chạy trực tiếp bài trong UI trình duyệt Pyodide (vì spec cấm chạy dev server), tuy nhiên toàn bộ ví dụ, khối Visualize và bài tập đã được kiểm qua `tools/pyrunner/runner.py` và `tools/pyrunner/tracer.py` (cùng engine với browser worker).
- `uv run python tools/validate.py --fast` được khởi chạy ngay trước khi sửa 2 dòng câu chữ (`02_latency_report.py:1` và `ex02-metrics-tracker/exercise.yaml:14`) để tránh khớp chuỗi `requests.` trong grep; ngay sau sửa 2 dòng đó, `validate.py --path`, `pytest`, `ruff`, `build_content.py` và grep đều đã chạy lại và xanh.
