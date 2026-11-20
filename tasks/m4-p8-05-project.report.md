# Báo cáo: M4 bước 25a — Mini-project `p8-05-mini-project` (Ship a RAG service)

## 1. Đã làm gì

1. **Meta & bài học song ngữ (`meta.yaml`, `lesson.en.md`, `lesson.vi.md`)**
   - Tạo `meta.yaml` (`kind: project`, `phase: p8`, `order: 5`, `duration_min: 45`, `review_by: "2027-05-01"`, không có trường `runner`, tag hợp lệ `[production, rag, apis, testing]`).
   - Viết bài học song ngữ EN/VI theo đúng dàn ý: Opening → `## 1. The plan` (`flowchart TD` 8 node, bảng nối các Part với `p7-09`/`p8-01`/`p8-02`/`p8-03`/`p8-04`, hợp đồng 3 API) → `## 2. Part 1: app factory and index` (kèm khối Visualize thuần Python dùng `dot_cosine` trên 4 vector viết tay + trace table) → `## 3. Part 2: POST /ask` (trích nguồn `[n]`, lọc `min_score`, từ chối không gọi LLM, in lỗi `422` gọn) → `## 4. Part 3: response caching` (TTL cache chuẩn hóa khoảng trắng + `top_k`, ghi chú `index_version`, picture in text `ttl = 300s`) → `## 5. Part 4: metrics and GET /metrics` (`SlowClient` với công thức `0.2 + 0.002 * completion_tokens`, `p50_ms`/`p95_ms` nearest-rank, `total_cost`, `alerts`, callout `[!WARNING]`) → `## 6. Part 5: testing the service` (5 hàm test mẫu + bảng bảo vệ + callout `[!TIP]`) → `## 7. Part 6: packaging and running for real` (fence `bash` với `main.py` một dòng `app = create_app(DOCS, real_client, time.monotonic)`, `uvicorn`, `curl` và fence `dockerfile`) → `## 8. Common mistakes` (4 lỗi thực tế kèm output thật) → `## Recap` & `## Take it further`.
   - Toàn bộ 10 khối Python trong bài đã chạy kiểm với `uv run python -W error`, stderr rỗng, mọi dòng output `< 80` ký tự.

2. **3 Examples (`examples/`)**
   - `01_service_basics`: `create_app` với 6 doc, gọi `/health`, 2 câu hỏi trả lời được, 1 câu từ chối; in `status`, `sources`, `answer`, `index_embed=1`, `total_embed=4`, `chat=2`.
   - `02_cache_in_action`: 6 request có lặp, thừa khoảng trắng, đổi `top_k`, câu từ chối (cũng được cache), rồi `clock.advance(350)` vượt TTL để kiểm tra miss ở `t=400`.
   - `03_metrics_dashboard`: mô phỏng 12 request (gồm 1 payload `422` bị Pydantic chặn trước handler nên `requests = 11`), in bảng `metric | value` và `alerts`.
   - Đã sinh `.out` từ stdout thật và viết `.en.md` / `.vi.md` đầy đủ cho cả 3 example.

3. **2 Exercises (`exercises/`, đều `kind: project`)**
   - `ex01-rag-service`: `create_app(docs, client, min_score=0.2) -> FastAPI` với `/health` (`{"status": "ok", "docs": len(docs)}`), `/ask` (`AskRequest` `question` `1..300`, `top_k` `1..5` mặc định `2`, tie-break giữ thứ tự gốc, từ chối không gọi `client.chat`). 10 test (gồm parametrize `422`, cô lập 2 app, tie-break). Alternative `01_class_numpy.py` dùng lớp `RagService` + ma trận NumPy & `np.argsort(..., kind="stable")`.
   - `ex02-cache-metrics`: `create_app(docs, client, clock, cache_ttl=300.0, price_in_per_1k=0.0005, price_out_per_1k=0.0015) -> FastAPI` trên starter RAG có sẵn; thêm TTL cache (chuẩn hóa khoảng trắng + `top_k`, hit khi `clock() < expires_at`, cache cả câu từ chối), ghi metric mọi `/ask` hợp lệ và `GET /metrics`. 9 test với `FakeClock` và `SlowClient`. Alternative `01_class_cache_metrics.py` tách thành 2 lớp `TTLCache` và `MetricsTracker`.
   - **Điểm khác với code trong bài:**
     - `ex01` nhận thêm tham số `min_score: float = 0.2`, trả `{"status": "ok", "docs": len(docs)}` ở `/health`, không có cache/clock/metrics.
     - `ex02` nhận tham số cấu hình `cache_ttl`, `price_in_per_1k`, `price_out_per_1k` và `GET /metrics` chỉ trả 4 trường (`requests`, `cache_hit_rate`, `p95_ms`, `total_cost` làm tròn 6 chữ số), không kèm `p50_ms` hay `alerts` như bản đầy đủ trong bài học.

4. **Quiz (`quiz.yaml`) & Glossary (`curriculum/glossary.yaml`)**
   - 16 câu hỏi (`p8-05-q01`..`p8-05-q16`): 8 `mcq`, 3 `output`, 3 `fill`, 2 `parsons`; phân bố độ khó 5 mức `1`, 7 mức `2`, 4 mức `3`; 6 flashcards (`p8-05-f01`..`p8-05-f06`).
   - Thêm 3 thuật ngữ mới vào cuối `curriculum/glossary.yaml`: `app factory`, `dependency injection`, `health check` (0 dòng xóa).

## 2. File đã tạo / sửa

- Sửa: `curriculum/glossary.yaml` (`+33/-0` dòng)
- Tạo mới: `tasks/m4-p8-05-project.report.md`
- Tạo mới thư mục `curriculum/phase-08-production/p8-05-mini-project/` gồm 35 file:
  - `meta.yaml`, `lesson.en.md`, `lesson.vi.md`, `quiz.yaml`
  - `examples/01_service_basics.{py,out,en.md,vi.md}`
  - `examples/02_cache_in_action.{py,out,en.md,vi.md}`
  - `examples/03_metrics_dashboard.{py,out,en.md,vi.md}`
  - `exercises/ex01-rag-service/{exercise.yaml,prompt.en.md,prompt.vi.md,starter.py,solution.py,test_exercise.py}`
  - `exercises/ex01-rag-service/alternatives/01_class_numpy.{py,en.md,vi.md}`
  - `exercises/ex02-cache-metrics/{exercise.yaml,prompt.en.md,prompt.vi.md,starter.py,solution.py,test_exercise.py}`
  - `exercises/ex02-cache-metrics/alternatives/01_class_cache_metrics.{py,en.md,vi.md}`

## 3. Kết quả kiểm tra

### Lệnh trong spec
| Lệnh | Kết quả | Thời gian / Ghi chú |
|---|---|---|
| `uv run python tools/validate.py --path curriculum/phase-08-production/p8-05-mini-project` | `OK: 0 error(s), 0 warning(s). Checked 1 lessons, 8 markdown pairs, 3 examples, 2 alternatives, 2 exercises, 16 questions.` | `8.4s` |
| `uv run python tools/validate.py --fast` | `OK: 0 error(s), 0 warning(s). Checked 54 lessons, 409 markdown pairs, 160 examples, 108 exercises, 87 alternatives, 1041 questions, 10 exams, 1 portfolio, 1 glossary, 1 interview.` | Hoàn tất sạch |
| `uv run python -m pytest curriculum/phase-08-production -p no:warnings --color=no` | `83 passed in 0.58s` | Exit 0 |
| `uv run ruff check curriculum/phase-08-production` | `All checks passed!` | Exit 0 |
| Kiểm tra regex cấm trên `.py` và `.yaml` (`git grep -nE ...` & script Python) | `0` dòng khớp (`git grep` exit 1, `matches: 0`) | Sạch |
| `git diff --numstat curriculum/glossary.yaml` | `33 0 curriculum/glossary.yaml` | 0 dòng xóa |
| `uv run python tools/build_content.py` | `Built 54 lessons, 10 exams, 324 flashcards, 866 questions -> apps\web\src\generated` | 53 → 54 lesson |
| `git status --short` | `M curriculum/glossary.yaml`, `?? curriculum/phase-08-production/p8-05-mini-project/`, `?? tasks/`, `?? .hallmark/` | Đúng phạm vi cho phép |

### Số step `tools/pyrunner/tracer.py` (Visualize & Examples)
| Đoạn code | `len(steps)` | `truncated` | `error` |
|---|---|---|---|
| Khối Visualize trong bài (Part 1, không FastAPI/FakeLLM) | `149` | `False` | `None` |
| `examples/01_service_basics.py` | `78` | `False` | `None` |
| `examples/02_cache_in_action.py` | `130` | `False` | `None` |
| `examples/03_metrics_dashboard.py` | `139` | `False` | `None` |

### Thời gian & kết quả từng exercise (`runner.run_tests` và `pytest`)
| Exercise | Target | `runner.run_tests` | `pytest` |
|---|---|---|---|
| `ex01-rag-service` | `starter.py` | `ok=False`, `0/10` (`0.40s`) | `rc=1`, `FFFFFFFFFF` 10/10 fail (`0.93s`) |
| `ex01-rag-service` | `solution.py` | `ok=True`, `10/10` (`0.08s`) | `rc=0`, 10 passed (`1.06s`) |
| `ex01-rag-service` | `alternatives/01_class_numpy.py` | `ok=True`, `10/10` (`0.12s`) | Kiểm qua `validate.py` (`0` lỗi) |
| `ex02-cache-metrics` | `starter.py` | `ok=False`, `0/9` (`0.07s`) | `rc=1`, `FFFFFFFFF` 9/9 fail (`0.99s`) |
| `ex02-cache-metrics` | `solution.py` | `ok=True`, `9/9` (`0.08s`) | `rc=0`, 9 passed (`0.92s`) |
| `ex02-cache-metrics` | `alternatives/01_class_cache_metrics.py` | `ok=True`, `9/9` (`0.08s`) | Kiểm qua `validate.py` (`0` lỗi) |

### Kết quả script độ dài MCQ (`quiz.yaml`)
Chạy script kiểm tra trên 8 câu MCQ (`en` và `vi`): `violations: 0 longest-unique: 0`.

| ID | EN `ans` | EN lens | EN ratio | VI lens | VI ratio |
|---|---|---|---|---|---|
| `p8-05-q01` | 0 | `[55, 50, 53, 61]` | 1.01 | `[50, 49, 55, 51]` | 0.97 |
| `p8-05-q02` | 1 | `[49, 46, 47, 44]` | 0.99 | `[54, 47, 52, 45]` | 0.93 |
| `p8-05-q04` | 2 | `[51, 44, 50, 50]` | 1.03 | `[54, 52, 55, 57]` | 1.01 |
| `p8-05-q07` | 3 | `[48, 45, 49, 43]` | 0.91 | `[46, 52, 50, 54]` | 1.09 |
| `p8-05-q08` | 0 | `[26, 24, 25, 30]` | 0.99 | `[26, 28, 28, 27]` | 0.94 |
| `p8-05-q12` | 1 | `[54, 47, 53, 53]` | 0.88 | `[51, 51, 53, 57]` | 0.95 |
| `p8-05-q15` | 2 | `[58, 52, 57, 57]` | 1.02 | `[51, 54, 56, 52]` | 1.07 |
| `p8-05-q16` | 3 | `[51, 50, 52, 47]` | 0.92 | `[53, 48, 49, 51]` | 1.02 |

### Link `further_reading` đã kiểm tra
- `https://fastapi.tiangolo.com/tutorial/testing/` (kiểm tra nội dung `TestClient`, `def` test functions với `pytest` qua `search_web`).
- `https://fastapi.tiangolo.com/advanced/settings/` (kiểm tra `pydantic-settings`, `BaseSettings`, `.env` qua `search_web`).
- `https://fastapi.tiangolo.com/deployment/docker/` (kiểm tra trang "FastAPI in Containers - Docker" qua `search_web`).
- Đã kiểm tra phiên bản runtime thực tế trong `.venv`: `fastapi==0.162.7`, `pydantic==2.12.5`, `httpx==0.28.1`.

## 4. Điều còn chưa chắc / Lưu ý

- **Số lần gọi `embed` ở `01_service_basics` và `ex01`**: Khi tạo app, `client.embed([d["text"] for d in docs])` được gọi **1 lần** cho toàn bộ kho tài liệu (`index_embed=1`), và mỗi lần `POST /ask` (trượt cache) cần gọi `client.embed([body.question])` để embed câu hỏi thành vector. Vì vậy tổng số lần gọi `client.embed` sau 3 câu hỏi là `4` (`1` cho corpus + `3` cho câu hỏi), trong khi số lần embed kho tài liệu vẫn giữ là `1`. Trong `01_service_basics.py` và `test_exercise.py` của `ex01`, điều này được kiểm rõ qua kích thước lô (`index_embed=1`, `total_embed=4`) để vừa chính xác tuyệt đối vừa bắt được lỗi re-embed tài liệu mỗi request.
- **Kiểm tra link ngoài**: Môi trường không có công cụ mở trình duyệt trực tiếp nên 3 URL `further_reading` được xác minh tiêu đề và đường dẫn qua `search_web` trên domain `fastapi.tiangolo.com`.
- **Phần chạy thật (`uvicorn` / `Dockerfile`)**: Theo quy tắc không chạy server hay Docker, các lệnh trong Part 6 nằm ở fence `bash` và `dockerfile`, chỉ kiểm tra bằng đọc soát cú pháp chứ không khởi chạy container.
