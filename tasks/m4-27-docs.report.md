# Báo cáo: M4 bước 27 — Cập nhật tài liệu sau M4 (`m4-27-docs`)

## 1. Đã làm gì

1. **[`CLAUDE.md`](file:///D:/Proj/python-ai-platform/CLAUDE.md)** (36 dòng, giữ ngắn dưới 100 dòng):
   - Cập nhật dòng "Hiện tại" ở mục **Quy trình**: ghi M4 đã xong (phase 6 có 4 bài, phase 7 có 10 bài, phase 8 có 5 bài; mỗi phase có phase test và đã qua reviewer), nêu rõ 6 bài `runner: local` (`p6-01`–`p6-04`, `p8-01`, `p8-05`) chạy trên runner cục bộ và phần còn lại chạy trên Pyodide, bỏ trạng thái M3 cũ, giữ nguyên `"Theme Dose đã merge"`, và ghi kế tiếp là M5 (capstone, portfolio, xuất PDF, đánh bóng).
   - Bổ sung vào mục **Lệnh**: lệnh chạy runner cục bộ (`uv run python tools/localrunner/serve.py`), lệnh tải và kiểm cache model Hugging Face (`uv run python tools/localrunner/fetch_models.py`, `--check`), lệnh kiểm starter fail (`EXERCISE_TARGET=starter uv run python -m pytest <dir>`), và thống nhất lệnh test nội dung dùng `uv run python -m pytest curriculum`.
   - Thêm 1 dòng vào mục **Quy tắc** về `pyai_llm` (`packages/pyai_llm`): mọi lời gọi LLM trong nội dung đi qua fake client `pyai_llm`, không cần API key.

2. **[`docs/DESIGN.md`](file:///D:/Proj/python-ai-platform/docs/DESIGN.md)**:
   - §5 bảng kiến trúc, dòng **Chạy nặng (theo bài)**: cập nhật mô tả chính xác theo `tools/localrunner/serve.py`, `server.py` và `README.md` — runner FastAPI nghe tại `http://127.0.0.1:8765`, khởi động bằng `uv run python tools/localrunner/serve.py`, chạy code tuần tự trong subprocess `python -I` tách biệt (thư mục tạm, chế độ offline HF), áp dụng cho các bài `runner: local` (`p6-01`–`p6-04`, `p8-01`, `p8-05`); trên app hiện chip `"Local runner"`.
   - §10 bảng lộ trình, dòng **M4**: thêm `— M4 xong (2026-11-18)` theo đúng định dạng dòng M3.
   - Không chỉnh sửa các mục khác.

3. **[`docs/CONTENT_GUIDE.md`](file:///D:/Proj/python-ai-platform/docs/CONTENT_GUIDE.md)** (mục `## Deep learning, LLM & production code (phase 6+)`):
   - Thêm 4 quy ước mới từ phase 8:
     - **Fake clock (`Đồng hồ giả`):** zero-argument callable trả về số giây; chép nguyên khối `class FakeClock` (`self.t`, `__call__`, `advance(seconds)`) từ `curriculum/phase-08-production/p8-03-caching/lesson.en.md` (nằm ở §6 của bài học); production truyền `time.monotonic` hoặc `time.perf_counter` không có ngoặc.
     - **Exercises must not copy the lesson:** solution không chép nguyên khối code từ lesson, phải có thêm ít nhất một yêu cầu/tính năng bài học chưa làm.
     - **Output comments:** `# ...` ngay sau `print(...)` là output kỳ vọng và phải khớp output chạy thật; comment giải thích đặt trước `print` hoặc cách 1 dòng trống.
     - **`.dockerignore`:** pattern khớp từ gốc build context; dùng `**/` để khớp mọi cấp (ví dụ `**/__pycache__`, `**/*.pyc`).

4. **[`curriculum/portfolio.yaml`](file:///D:/Proj/python-ai-platform/curriculum/portfolio.yaml)**:
   - Thêm mục **`rag-service`** cho `p8-05-mini-project` (`phase: p8`, `difficulty: 5`, tags `[rag, production, apis, testing]` đều có trong `curriculum/topics.yaml`), đặt sau `tool-agent` và trước 2 capstone (`cap-rag-chatbot`, `cap-tool-agent`). Nội dung bám sát `lesson.en.md` và `ex01-rag-service`, `ex02-cache-metrics`: app factory `create_app`, `/ask` có citation `[n]` và từ chối khi điểm thấp, TTL cache trong RAM, xử lý `RateLimitError` → `503`, `/metrics` (`requests`, `cache_hit_rate`, `error_rate`, `p95_ms`, `total_cost`), test bằng `TestClient` + `FakeClock`, và `Dockerfile`.
   - Soát và sửa **`rag-qa`** (`p7-09-mini-project-rag`):
     - Lý do sửa: bài `p7-09` dùng bộ FAQ cửa hàng (không phải "technical documentation") và dùng chỉ mục vector NumPy trong RAM (`vectors @ q_vec`), **không** dùng vector database; bài cũng có bước từ chối khi thiếu căn cứ và đánh giá trên cả tập `dev_set` và `test_set` tách biệt. Do đó sửa `pitch`, `cv_bullet` (nêu rõ tài liệu FAQ, NumPy vector search, citation `[n]`, refusal và eval dev/held-out test) và đổi skill `"vector database"` → `"NumPy vector search"`.
   - Soát và sửa **`tool-agent`** (`p7-10-mini-project-agent`):
     - Lý do sửa: `pitch` cũ nói agent tự gọi `"calculator, search function, file reader"` — không đúng với bài `p7-10` thật (bài xây order-support agent với `lookup_order`, `track_shipment`, `check_refund_policy`, `issue_refund`). Đồng thời bổ sung đúng các cơ chế bài có: allowlisted toolbox, giới hạn bước/chống lặp/ngân sách token, cổng duyệt side-effect kèm audit log, và scenario tests tất định; cập nhật `skills` tương ứng.
   - Giữ nguyên `cap-rag-chatbot` và `cap-tool-agent`.

## 2. File đã sửa

- `CLAUDE.md` (gitignored)
- `docs/DESIGN.md` (gitignored)
- `docs/CONTENT_GUIDE.md` (gitignored)
- `curriculum/portfolio.yaml` (tracked trong git)
- `tasks/m4-27-docs.report.md` (báo cáo này)

## 3. Kết quả lệnh kiểm tra

- `uv run python tools/validate.py --fast` → **exit code 0**:
  `OK: 0 error(s), 0 warning(s). Checked 54 lessons, 409 markdown pairs, 160 examples, 108 exercises, 87 alternatives, 1057 questions, 11 exams, 1 portfolio, 1 glossary, 1 interview.`
- `uv run python tools/build_content.py` → **exit code 0**:
  `Built 54 lessons, 11 exams, 324 flashcards, 866 questions -> apps\web\src\generated`
- `git status --short`:
  ```text
   M curriculum/portfolio.yaml
  ?? .hallmark/
  ?? tasks/
  ```
  (Ghi chú: `CLAUDE.md`, `docs/DESIGN.md`, `docs/CONTENT_GUIDE.md` nằm trong `.gitignore` nên không hiện trong `git status --short` hay `git diff --stat`.)
- `git diff --stat`:
  ```text
   curriculum/portfolio.yaml | 43 +++++++++++++++++++++++++++++++++----------
   1 file changed, 33 insertions(+), 10 deletions(-)
  ```

## 4. Điều còn chưa chắc

- Đã chạy `tools/validate.py --fast` theo spec (bỏ qua pytest subprocess và ruff); chưa chạy `tools/validate.py` bản đầy đủ và chưa chạy `uv run python -m pytest` hay `pnpm --filter web build` (không chạy server/build web theo ràng buộc spec).
- Trong spec mục 3 có ghi chép `FakeClock` từ `p8-03-caching/lesson.en.md` §4; thực tế trong file đó `FakeClock` nằm ở **§6 (`## 6. TTL: expiring stale data`)** (và cũng xuất hiện ở `p8-05-mini-project/lesson.en.md` §2). Đã chép đúng nguyên khối `class FakeClock` vào `docs/CONTENT_GUIDE.md`.
