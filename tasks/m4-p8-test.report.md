# Báo cáo M4 bước 26: Phase test 8 (`p8-phase-test`)

## 1. Đã làm gì
- Đọc spec `tasks/m4-p8-test.md`, mẫu `curriculum/phase-07-llm/phase-test.yaml`, schema `tools/schema/exam.schema.json`, `curriculum/topics.yaml`, `docs/CONTENT_GUIDE.md`, cả 5 `quiz.yaml` và 5 `lesson.en.md` (cùng `p8-05-mini-project/exercises/ex02-cache-metrics/solution.py`) của Phase 8.
- Tạo mới `curriculum/phase-08-production/phase-test.yaml` với `id: p8-phase-test`, `kind: phase_test`, `phase: p8`, `duration_min: 25`, `pass_score: 0.7`, gồm 16 câu hỏi hoàn toàn mới (`p8-test-q01` → `p8-test-q16`), song ngữ EN/VI đầy đủ và có `explanation` giải thích lý do.
- Toàn bộ code chạy được (`output`, `fill`, `parsons`) không gọi mạng, không dùng API key, không dùng `time.time` / `time.sleep` / `perf_counter`, dùng `FakeClock` đúng dạng trong spec, chỉ dùng tối đa 2 câu có `FastAPI` (`TestClient` ở `q02` và `q03`), và chạy sạch dưới `python -W error`.

### Bảng đếm thực tế theo blueprint

**Theo chủ đề & loại câu:**
| Chủ đề | Tổng câu | `mcq` | `output` | `fill` | `parsons` | Độ khó (1 / 2 / 3) |
|---|---:|---:|---:|---:|---:|---|
| FastAPI (`p8-01`) | 3 | 1 | 1 | 1 | 0 | 1 / 2 / 0 |
| Docker (`p8-02`) | 3 | 2 | 0 | 1 | 0 | 1 / 1 / 1 |
| Caching (`p8-03`) | 4 | 1 | 1 | 1 | 1 | 0 / 3 / 1 |
| Monitoring (`p8-04`) | 3 | 1 | 1 | 0 | 1 | 1 / 1 / 1 |
| Mini-project RAG (`p8-05`) | 3 | 2 | 1 | 0 | 0 | 0 / 2 / 1 |
| **Tổng** | **16** | **7** | **4** | **3** | **2** | **3 / 9 / 4** |

- **Phân bổ `answer` của 7 câu `mcq`:** `{0: 2, 1: 2, 2: 2, 3: 1}` (`q06=0`, `q10=0`, `q01=1`, `q05=1`, `q13=2`, `q14=2`, `q16=3`).
- **Tags sử dụng:** chỉ nằm trong `[production, apis, performance, testing, logging, packaging, rag, llm]`.

### Liệt kê ý chính từng câu kiểm tra
- `p8-test-q01` (`mcq`, mức 1): `TestClient(app)` chạy test in-process không cần mở cổng hay khởi động `uvicorn`.
- `p8-test-q02` (`output`, mức 2): path param `doc_id: int` trả `422` trước khi vào hàm (`seen` không đổi), `HTTPException(404)` trả `404`, hợp lệ trả `200`.
- `p8-test-q03` (`fill`, mức 2): Pydantic `Field(min_length=..., le=...)` từ chối request sai bằng `422` trước khi chạy route handler.
- `p8-test-q04` (`fill`, mức 2): `.dockerignore` so khớp từ gốc build context (`**/__pycache__` khớp thư mục lồng sâu, còn `__pycache__/` bỏ sót).
- `p8-test-q05` (`mcq`, mức 1): ghép chuẩn `FROM python:3.13-slim`, `--host 0.0.0.0`, và truyền secret bằng `--env-file .env` (tránh `:latest`, `127.0.0.1`, `COPY .env`, `ENV SECRET=...`).
- `p8-test-q06` (`mcq`, mức 3): bẫy `COPY . .` đặt trước `RUN pip install` làm sửa `main.py` mất cache layer và buộc `pip install` chạy lại.
- `p8-test-q07` (`parsons`, mức 2): dựng cache key gồm `model`, `messages` (có `role`), `temperature`, `max_tokens` qua `json.dumps(sort_keys=True)` và `sha256[:8]`.
- `p8-test-q08` (`fill`, mức 2): `FakeClock` callable (`__call__`, `advance`) và biên TTL `clock() >= expires_at` tính là miss.
- `p8-test-q09` (`output`, mức 2): LRU bằng `OrderedDict` (`move_to_end`, `popitem(last=False)`) kết hợp quy tắc chỉ cache khi `temperature == 0.0`.
- `p8-test-q10` (`mcq`, mức 3): bẫy cache key thiếu `max_tokens` khiến request `max_tokens=500` nhận lại câu trả lời bị cắt ở `max_tokens=16`.
- `p8-test-q11` (`parsons`, mức 1): tính cost theo công thức `(in/1000)*price_in + (out/1000)*price_out` và kiểm tra ngưỡng chặt `>` để phân biệt `budget-warning` với `budget-exceeded`.
- `p8-test-q12` (`output`, mức 2): `percentile` nearest-rank (`ceil(95/100 * n)`), trung bình che phần đuôi chậm, `p95` khác `max`, và ngưỡng cảnh báo dùng `>` (bằng ngưỡng `200 > 200` là `False`).
- `p8-test-q13` (`mcq`, mức 3): bẫy khởi tạo `status = "ok"` trước `try` khiến ngoại lệ không khớp `except RateLimitError` (như `ValueError`) bị `finally` ghi nhận là `"ok"`.
- `p8-test-q14` (`mcq`, mức 2): app factory `create_app(docs, client, clock)` yêu cầu `clock` là callable (`time.monotonic`, không phải `time.monotonic()`).
- `p8-test-q15` (`output`, mức 2): tích hợp pipeline `/ask`: `RateLimitError` ghi `status="error"` và không cache, retry sau đó thành công, refusal (`score < 0.2`) không gọi LLM, cache hit không gọi LLM với cost `0.0`, mọi request được chấp nhận đều vào `metrics`.
- `p8-test-q16` (`mcq`, mức 3): bẫy lưu phản hồi lỗi `RateLimitError` vào `cache[key]` làm các lượt retry sau khi LLM hồi phục vẫn nhận lỗi cũ.

### Bảng độ dài 4 phương án (EN) của từng câu MCQ
| Câu | Index đúng | Độ dài 4 phương án EN (ký tự) | Trung bình distractor | Tỉ lệ `đúng / TB` | Dài nhất duy nhất? |
|---|---:|---|---:|---:|---|
| `p8-test-q01` | 1 | `[59, 58, 58, 57]` | 58.00 | 1.000 | Không |
| `p8-test-q05` | 1 | `[65, 70, 69, 64]` | 66.00 | 1.061 | Có |
| `p8-test-q06` | 0 | `[61, 61, 63, 63]` | 62.33 | 0.979 | Không |
| `p8-test-q10` | 0 | `[60, 57, 62, 63]` | 60.67 | 0.989 | Không |
| `p8-test-q13` | 2 | `[58, 60, 56, 55]` | 57.67 | 0.971 | Không |
| `p8-test-q14` | 2 | `[52, 52, 57, 57]` | 53.67 | 1.062 | Không |
| `p8-test-q16` | 3 | `[58, 58, 57, 57]` | 57.67 | 0.988 | Không |

## 2. File đã sửa / tạo
- Tạo mới: `curriculum/phase-08-production/phase-test.yaml`
- Tạo mới: `tasks/m4-p8-test.report.md`

## 3. Kết quả lệnh kiểm tra
- `uv run python tools/validate.py --path curriculum/phase-08-production` → **PASS**: `OK: 0 error(s), 0 warning(s). Checked 5 lessons, 36 markdown pairs, 15 examples, 10 exercises, 6 alternatives, 96 questions, 1 exams.`
- `uv run python tools/build_content.py` → **PASS**: `Built 54 lessons, 11 exams, 324 flashcards, 866 questions -> apps\web\src\generated` (số exams tăng lên 11).
- Kiểm tra pattern cấm (`api_key=|OPENAI|httpx|requests\.|time\.sleep|time\.time|perf_counter\(\)|độ chính xác`) trên `curriculum/phase-08-production/phase-test.yaml` bằng `Select-String` → **0 dòng khớp**.
- Script kiểm độ dài MCQ → `violations: 0 longest-unique: 1`.
- Script chạy toàn bộ 9 câu có code (`output`, `fill`, `parsons`) với `python -W error` → **PASS** cả 9/9 câu, `returncode=0`, `stderr=''`.
- `git status --short` → chỉ có `?? curriculum/phase-08-production/phase-test.yaml` (cùng `?? .hallmark/` và `?? tasks/`).

## 4. Điều còn chưa chắc
- Chỉ chạy `tools/validate.py --path curriculum/phase-08-production` (theo spec) chứ chưa chạy `tools/validate.py` toàn repo hay `uv run python -m pytest`, và không chạy `pnpm --filter web build` theo yêu cầu spec.
- `uv run python tools/build_content.py` cập nhật output trong `apps/web/src/generated` (đã gitignore nên không hiện trong `git status --short`).

## Vòng 2
- **Đã sửa theo feedback vòng 1** (chỉ sửa duy nhất `p8-test-q02` trong `curriculum/phase-08-production/phase-test.yaml`):
  - Đổi route trong code từ `@app.get("/docs/{doc_id}")` thành `@app.get("/documents/{doc_id}")` và 3 URL test thành `("/documents/x", "/documents/5", "/documents/20")`; output giữ nguyên `[422, 404, 200] [5, 20]`.
  - Cập nhật `explanation` EN và VI của `p8-test-q02` cho khớp với `/documents/x`, `/documents/5`, `/documents/20`.
- **Kết quả kiểm tra lại:**
  - `uv run python tools/validate.py --path curriculum/phase-08-production` → **PASS**: `OK: 0 error(s), 0 warning(s). Checked 5 lessons, 36 markdown pairs, 15 examples, 10 exercises, 6 alternatives, 96 questions, 1 exams.`
  - `uv run python tools/build_content.py` → **PASS**: `Built 54 lessons, 11 exams, 324 flashcards, 866 questions -> apps\web\src\generated`
  - Chạy lại snippet `p8-test-q02` với `-W error` → `returncode=0`, stdout `'[422, 404, 200] [5, 20]'`, `stderr=''`.
  - Kiểm tra pattern cấm (`Select-String`) → 0 dòng khớp; kiểm tra độ dài MCQ → `violations: 0 longest-unique: 1`; `git status --short` → chỉ có `?? curriculum/phase-08-production/phase-test.yaml`, `?? .hallmark/`, `?? tasks/`.
