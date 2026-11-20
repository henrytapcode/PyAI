# M4 bước 27: cập nhật tài liệu sau M4

## Mục tiêu
M4 đã xong: phase 6, 7, 8 có đủ bài, phase test và review, runner cục bộ chạy được. Cập nhật tài liệu để phiên sau đọc là biết trạng thái và quy ước mới. Thêm mini-project p8-05 vào portfolio.

Lịch sử commit M4 (để ghi đúng): xem `git log --oneline` từ commit `f15a3a3` trở về trước và `tasks/M4-PLAN.md`. Commit mới nhất là `e4b7dba` (phase test 8).

## File được phép sửa
- `CLAUDE.md`
- `docs/DESIGN.md`
- `docs/CONTENT_GUIDE.md`
- `curriculum/portfolio.yaml`
- `tasks/m4-27-docs.report.md`

## Không được đụng
- Mọi file khác: `curriculum/**` (trừ `portfolio.yaml`), `tools/**`, `apps/**`, `packages/**`, `tasks/*` khác.
- Không chạy `pnpm --filter web build`, không chạy server.

## Việc cần làm

### 1. `CLAUDE.md` (giữ ngắn, dưới khoảng 100 dòng)
- Dòng "Hiện tại" ở mục Quy trình:
  - ghi M4 đã xong, kèm số bài thật (đếm từ `curriculum/syllabus.yaml`): phase 6 có 4 bài, phase 7 có 10 bài, phase 8 có 5 bài; mỗi phase có phase test và đã qua reviewer;
  - ghi rõ bài nào chạy runner cục bộ;
  - kế tiếp là M5 (capstone, portfolio, xuất PDF, đánh bóng).
  Bỏ nội dung cũ về M3 khỏi dòng này, nhưng vẫn giữ câu "Theme Dose đã merge".
- Mục Lệnh, thêm:
  - chạy runner cục bộ: `uv run python tools/localrunner/serve.py`. Bài `runner: local` cần runner này trong app;
  - tải model Hugging Face cho runner: `uv run python tools/localrunner/fetch_models.py`. Đọc `tools/localrunner/README.md` để ghi đúng;
  - chạy starter: `EXERCISE_TARGET=starter uv run python -m pytest <dir>` (mọi test phải fail).
- Mục Quy tắc: thêm 1 dòng về `pyai_llm`. Mọi lời gọi LLM trong nội dung đi qua fake client `pyai_llm` (`packages/pyai_llm`), không cần API key.

### 2. `docs/DESIGN.md`
- §5, bảng kiến trúc, dòng "Chạy nặng (theo bài)":
  - nêu bài nào chạy runner cục bộ (p6-01..p6-04, p8-01, p8-05) và lệnh khởi động;
  - nêu rằng app hiện chip "Local runner" khi bài cần runner.
  Đọc `tools/localrunner/README.md` và `serve.py`/`server.py` để mô tả đúng: runner nghe ở đâu, chạy code thế nào. Mô tả ngắn, 1–3 câu, không đoán.
- §10, bảng lộ trình, dòng M4: thêm "— M4 xong (2026-11-18)" theo đúng kiểu dòng M3.
- Không đổi các mục khác.

### 3. `docs/CONTENT_GUIDE.md`, mục "Deep learning, LLM & production code (phase 6+)"
Thêm các quy ước đã chốt trong phase 8, mỗi ý 1 bullet ngắn:
- **Đồng hồ giả:** đồng hồ là hàm không tham số trả về số giây. Trong bài và test, dùng `FakeClock` dạng chuẩn (`self.t`, `__call__`, `advance(seconds)`); production truyền `time.monotonic` hoặc `time.perf_counter`, không có ngoặc. Không dùng thời gian thật trong code chạy. Chép nguyên khối class từ `curriculum/phase-08-production/p8-03-caching/lesson.en.md` §4 vào guide.
- **Bài tập không chép bài học:** solution của exercise (nhất là mini-project) không được chép nguyên khối code từ lesson. Bài tập phải yêu cầu thêm ít nhất một phần lesson không có.
- **Comment output:** mọi dòng `# ...` ngay sau `print(...)` là output kỳ vọng và phải khớp output chạy thật. Comment giải thích đặt trước `print` hoặc cách một dòng trống.
- **`.dockerignore`:** pattern khớp từ gốc build context; muốn khớp mọi cấp phải dùng `**/` (`**/__pycache__`, `**/*.pyc`).

### 4. `curriculum/portfolio.yaml`
- Thêm một project cho `p8-05-mini-project`, theo đúng khuôn các mục có sẵn: `id`, `lesson`, `phase: p8`, `difficulty`, `tags` có trong `curriculum/topics.yaml`, `title`, `pitch`, `cv_bullet`, `skills`, `stretch` (en + vi).
  - Đọc `curriculum/phase-08-production/p8-05-mini-project/lesson.en.md` và 2 exercise để viết đúng những gì người học thật sự làm: app factory, `/ask` có citation và từ chối, TTL cache, `/metrics` (latency p95, cost, hit rate, error rate), xử lý `RateLimitError` → 503, test bằng `TestClient` + `FakeClock`, Dockerfile.
  - Chọn `id` ngắn, ví dụ `rag-service`.
  - Đặt đúng chỗ theo độ khó tăng dần (validator kiểm thứ tự), trước 2 capstone.
- Soát lại pitch và cv_bullet của `rag-qa` (p7-09) và `tool-agent` (p7-10) so với lesson thật. Câu nào nói điều bài không làm thì sửa cho đúng, ví dụ tool "file reader", "search function", "vector database". Có sửa thì ghi lý do vào report.
- Pitch của 2 capstone `cap-rag-chatbot` và `cap-tool-agent` giữ nguyên, vì M5 mới làm.
- Bản VI tự nhiên, dùng "bạn", thuật ngữ giữ tiếng Anh.

## Tiêu chí hoàn thành (checklist)
- [ ] CLAUDE.md: trạng thái M4 xong, lệnh runner, `EXERCISE_TARGET=starter`, dòng `pyai_llm`; tổng dưới khoảng 100 dòng
- [ ] DESIGN.md §5 và §10 cập nhật, mô tả runner đúng với code
- [ ] CONTENT_GUIDE có 4 quy ước mới
- [ ] portfolio.yaml có mục p8-05, đúng thứ tự; mục p7-09, p7-10 khớp bài
- [ ] Lệnh kiểm tra xanh

## Lệnh kiểm tra
Chạy từ gốc repo `D:\Proj\python-ai-platform`:
```
uv run python tools/validate.py --fast
uv run python tools/build_content.py
git status --short
git diff --stat
```
Kết quả mong đợi: validate 0 lỗi; build_content in "1 portfolio" hoặc số project không lỗi; diff chỉ chạm 4 file trong phạm vi.
Nếu `--fast` không tồn tại thì chạy `uv run python tools/validate.py` (mất khoảng 6 phút).

## Ghi chú cho worker
- Không chạy server hay dev server.
- Đọc `tools/schema/portfolio.schema.json` trước khi thêm mục portfolio.

## Trạng thái
- Bước hiện tại: 2
- Vòng: 1/3
- Số lần swap: 0
- Fallback: không
- Model: Gemini 4 Hydrogen (High)
