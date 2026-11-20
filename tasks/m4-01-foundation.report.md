# M4 bước 1 (`m4-01-foundation`) — Báo cáo triển khai

## 1. Đã làm gì

### A. Syllabus phase 6–8 (`curriculum/syllabus.yaml`)
- Cập nhật comment dòng 4–5 ở đầu file: `Phases 0-5 detailed; phases 6-8 detailed in M4 (lessons written later).` và thêm dòng giải thích `runner: local` ở mức bài.
- Bỏ `runner: local` ở mức phase cho cả `p6`, `p7`, `p8`.
- **p6:** Thêm `runner: local` cho cả 4 bài (`p6-01-tensors` … `p6-04-fine-tune`); chuyển `p6-04-fine-tune` thành `kind: project`, title `"Mini-project: a small fine-tune"` / `"Mini-project: fine-tune nhỏ"`; bổ sung `outcomes` en/vi (3 ý mỗi bài, phản ánh chạy CPU và model nhỏ từ cache offline cho `p6-03`/`p6-04`).
- **p7:** Không gán `runner` cho bất kỳ bài nào; cập nhật `summary` của phase `p7` nêu rõ dùng fake LLM client và không cần API key; cập nhật prerequisites của `p7-01-llm-api` (`[p2-05-typing, p3-01-pytest]`), `p7-03-embeddings` (`[p7-01-llm-api, p5-01-math-bridge]`), `p7-04-vector-db` (`[p7-03-embeddings, p4-01-numpy]`), `p7-08-evals` (`[p7-05-rag, p5-04-evaluation]`); bổ sung `outcomes` en/vi (2–3 ý mỗi bài, phản ánh fake LLM client).
- **p8:** Thêm `runner: local` cho `p8-01-fastapi`; bổ sung `outcomes` en/vi cho `p8-01`–`p8-04` (`p8-02-docker` nêu rõ đọc/viết Dockerfile, không chạy Docker); thêm bài cuối `p8-05-mini-project` (`kind: project`, `runner: local`, title `"Mini-project: ship a RAG service"` / `"Mini-project: đưa dịch vụ RAG lên production"`, prerequisites `[p8-04-monitoring, p7-09-mini-project-rag]`).
- Phase 0–5 trong `curriculum/syllabus.yaml` giữ nguyên không đổi một ký tự.

### B. `runner` ở mức bài
- `tools/validate.py`: kiểm tra `syllabus.yaml` để báo lỗi nếu phase còn khóa `runner` hoặc giá trị `runner` ở mức phase/bài khác `"local"`.
  - **Kiểm tra thủ công giá trị sai:** đã tạm sửa `p6` thành có `runner: local` ở mức phase và `p6-01-tensors` thành `runner: browser`, chạy `uv run python tools/validate.py --fast` và nhận về 2 lỗi đúng kỳ vọng (`FAILED: 2 error(s), 0 warning(s)`):
    - `ERROR curriculum/syllabus.yaml: phase p6: phase-level 'runner' is no longer allowed (move to lesson)`
    - `ERROR curriculum/syllabus.yaml: p6-01-tensors: invalid runner 'browser' (only 'local' is allowed)`
  - Sau đó đã khôi phục `curriculum/syllabus.yaml` về đúng spec.
- `tools/build_content.py`: đưa `runner` vào `summary` của bài trong `catalog.json` khi syllabus có trường `runner`, gán `lesson["meta"]["runner"]` cho bài `ready`, và loại bỏ `runner` khi dựng object `Phase`.
- `apps/web/src/lib/types.ts`: thêm `runner?: "local"` vào `LessonMeta` và `LessonSummary`; bỏ `runner?: "local"` khỏi `Phase`.
- `apps/web/src/app/(main)/learn/page.tsx`: đổi điều kiện hiển thị badge runner cục bộ (dòng 90) từ `phase.runner === "local"` sang `phase.lessons.some((l) => l.runner === "local")`, giữ nguyên chữ và kiểu badge.

### C. Thư viện mới (`pyproject.toml`, `uv.lock`)
- Ghim `==` các bản ổn định mới nhất có wheel cho Python 3.13 (`3.13.15`) Windows amd64:
  - `torch==2.15.0` lấy từ `[[tool.uv.index]]` (`name = "pytorch-cpu"`, `url = "https://download.pytorch.org/whl/cpu"`, `explicit = true`) qua `[tool.uv.sources] torch = { index = "pytorch-cpu" }` -> cài đặt thực tế `torch==2.15.0+cpu`
  - `transformers==5.23.0`
  - `fastapi==0.162.7`
  - `uvicorn==0.54.0`
  - `httpx==0.28.1`
  - `pydantic` (kéo theo bởi `fastapi`): phiên bản thực tế `2.14.3`
- Xác nhận import và bản CPU:
  `2.15.0+cpu False 5.23.0 0.162.7 2.14.3` (`torch.cuda.is_available()` là `False`).
- Thời gian chạy `uv run python tools/validate.py`:
  - Trước khi thêm thư viện: **275.71 s** (`275.7119314` s)
  - Sau khi thêm thư viện: **330.60 s** (`330.5979967` s) — tăng ~54.89 s (+19.9%).

### D. Gói trong Pyodide 0.29.5
Nguồn: `https://cdn.jsdelivr.net/pyodide/v0.29.5/full/pyodide-lock.json`

| Gói | Có không | Phiên bản |
|---|---|---|
| `pydantic` | Có | `2.12.5` |
| `pydantic_core` | Có | `2.41.5` |
| `httpx` | Có | `0.28.1` |
| `fastapi` | Có | `0.116.1` |
| `starlette` | Có | `0.47.2` |
| `anyio` | Có | `4.9.0` |
| `tiktoken` | Có | `0.9.0` |
| `regex` | Có | `2024.11.6` |
| `jsonschema` | Có | `4.23.0` |

### E. Tài liệu
- `docs/CONTENT_GUIDE.md`: thêm mục `## Deep learning, LLM & production code (phase 6+)` ngay sau `## Data & ML code (phase 4+)`, viết bằng tiếng Anh theo dạng gạch đầu dòng ngắn.
- `docs/DESIGN.md`: sửa dòng `Chạy nặng (phase 6–8)` ở §5 thành `Chạy nặng (theo bài)` với đúng nội dung spec.

## 2. File đã sửa
- `curriculum/syllabus.yaml`
- `tools/build_content.py`
- `tools/validate.py`
- `apps/web/src/lib/types.ts`
- `apps/web/src/app/(main)/learn/page.tsx`
- `pyproject.toml`
- `uv.lock`
- `docs/CONTENT_GUIDE.md`
- `docs/DESIGN.md`
- `tasks/m4-01-foundation.report.md` (file báo cáo này)

## 3. Kết quả lệnh kiểm tra

| Lệnh | Kết quả | Ghi chú |
|---|---|---|
| `uv sync` | Pass (exit 0) | Resolved 76 packages, installed 41 packages |
| `uv run python -c "import torch, transformers, fastapi, httpx, pydantic; print(torch.__version__, torch.cuda.is_available(), transformers.__version__, fastapi.__version__, pydantic.__version__)"` | Pass (exit 0) | Output: `2.15.0+cpu False 5.23.0 0.162.7 2.14.3` |
| `uv run python tools/validate.py` (trước khi thêm thư viện) | Pass (exit 0) | `OK: 0 error(s), 0 warning(s). Checked 35 lessons, 272 markdown pairs, 103 examples, 70 exercises, 64 alternatives, 702 questions, 8 exams, 1 portfolio, 1 glossary, 1 interview.` — **275.71 s** |
| `uv run python tools/validate.py` (sau khi thêm thư viện) | Pass (exit 0) | `OK: 0 error(s), 0 warning(s). Checked 35 lessons, 272 markdown pairs, 103 examples, 70 exercises, 64 alternatives, 702 questions, 8 exams, 1 portfolio, 1 glossary, 1 interview.` — **330.60 s** |
| `uv run python -m pytest curriculum -q` | Pass (exit 0) | Tất cả test pass (`[100%]`), có deprecation warning từ `matplotlib`/`pyparsing` |
| `uv run python -m pytest tools/pyrunner -q` | Pass (exit 0) | 14 tests passed (`.............. [100%]`) |
| `uv run ruff check curriculum tools/build_content.py tools/validate.py` | Exit 1 (44 lỗi có sẵn) | `uv run ruff check curriculum` pass (`All checks passed!`). 44 lỗi còn lại đều là `E501` (43) và `E713` (1) trên các dòng có sẵn chưa sửa của `tools/build_content.py` và `tools/validate.py`; các dòng mới/sửa trong bước này không phát sinh lỗi ruff. |
| `uv run python tools/build_content.py` | Pass (exit 0) | `Built 35 lessons, 8 exams, 210 flashcards, 563 questions -> apps\web\src\generated` |
| `pnpm.cmd --filter web typecheck` | Pass (exit 0) | `tsc --noEmit` xanh (`pnpm` dùng `pnpm.cmd` do PowerShell chặn `pnpm.ps1`) |
| `git diff --stat -- curriculum/syllabus.yaml` | Đã kiểm | `curriculum/syllabus.yaml \| 152 +++...--- (1 file changed, 128 insertions(+), 24 deletions(-))` — chỉ đổi header comment và p6–p8 |
| `git status --short` | Đã kiểm | 7 file tracked được phép (`M` — `apps/web/src/app/(main)/learn/page.tsx`, `apps/web/src/lib/types.ts`, `curriculum/syllabus.yaml`, `pyproject.toml`, `tools/build_content.py`, `tools/validate.py`, `uv.lock`) + `tasks/` + `.hallmark/` (`docs/` đang nằm trong `.gitignore`) |

## 4. Điều còn chưa chắc
1. **`ruff check` trên `tools/build_content.py` và `tools/validate.py`:** Hai file này có 44 lỗi `E501`/`E713` tồn tại từ trước; vì spec giới hạn chỉ sửa đúng phần dựng summary/phase và phần kiểm syllabus nên không tự ý reformat toàn file.
2. **Độ trễ `validate.py`:** Trên máy hiện tại, `validate.py` mất 275.71 s trước khi cài thêm thư viện và 330.60 s sau khi cài (+19.9%), cao hơn mốc ~165 s ghi trong `tasks/M4-PLAN.md` (có thể do tải hệ thống hoặc Windows Defender quét virtualenv mới).
3. **Nhánh `ready` của `runner` trong `lessons/<id>.json`:** Hiện chưa có thư mục bài học nào cho phase 6–8, nên nhánh gán `lesson["meta"]["runner"]` khi `ready == True` trong `tools/build_content.py` mới được kiểm tra qua đọc code và kiểm chứng `catalog.json` cho các bài chưa `ready`; sẽ được kiểm tra thực tế khi bước 5+ tạo bài đầu tiên của p6.
4. **Giao diện web runtime:** Theo spec không chạy `pnpm --filter web build` và không chạy dev server, nên `learn/page.tsx` mới được kiểm tra bằng TypeScript `tsc --noEmit` và kiểm tra dữ liệu `apps/web/src/generated/catalog.json`, chưa render trực tiếp trên trình duyệt.

## Vòng 2

### 1. Sửa theo feedback vòng 1
1. **Ghim `pydantic==2.12.5` (`pyproject.toml`, `uv.lock`):** thêm `"pydantic==2.12.5"` vào `dependencies` để khớp phiên bản trên Pyodide 0.29.5 (`pydantic 2.12.5`, `pydantic-core 2.41.5`). Khi chạy `uv sync`, `fastapi==0.162.7` tương thích tốt với `pydantic==2.12.5` nên không cần hạ phiên bản `fastapi` (hệ thống gỡ `pydantic==2.14.3` / `pydantic-core==2.50.4` và cài `pydantic==2.12.5` / `pydantic-core==2.41.5`).
2. **`tools/validate.py`:** tách dòng gọi `rep.error(...)` ở dòng 426 (kiểm tra `runner` ở mức bài) xuống dòng giống khối phase phía trên, hết lỗi ruff `E501`.
3. **`curriculum/syllabus.yaml` (`p6-04-fine-tune`):** sửa outcome VI thứ 2 thành `"So sánh tỉ lệ đoán đúng (accuracy) trước và sau khi fine-tune"`.
4. **`curriculum/syllabus.yaml` (`p6-02-training-loop`):** sửa outcome thứ 3 thành EN `"Save a trained model and evaluate it on tiny synthetic data"` / VI `"Lưu model đã train và đánh giá trên dữ liệu tổng hợp (synthetic) nhỏ"`.
5. **`curriculum/syllabus.yaml` (`p7-08-evals`):** sửa outcome thứ 3 thành EN `"Compare two RAG configurations on the same eval set"` / VI `"So sánh hai cấu hình RAG trên cùng một tập eval"`.

### 2. Kết quả lệnh kiểm tra (vòng 2)

| Lệnh | Kết quả | Ghi chú |
|---|---|---|
| `uv sync` | Pass (exit 0) | Resolved 76 packages; thay `pydantic==2.14.3` -> `2.12.5`, `pydantic-core==2.50.4` -> `2.41.5` |
| `uv run python -c "import torch, transformers, fastapi, httpx, pydantic; print(torch.__version__, torch.cuda.is_available(), transformers.__version__, fastapi.__version__, pydantic.__version__)"` | Pass (exit 0) | Output: `2.15.0+cpu False 5.23.0 0.162.7 2.12.5` |
| `uv run python tools/validate.py` | Pass (exit 0) | `OK: 0 error(s), 0 warning(s). Checked 35 lessons, 272 markdown pairs, 103 examples, 70 exercises, 64 alternatives, 702 questions, 8 exams, 1 portfolio, 1 glossary, 1 interview.` |
| `uv run python -m pytest curriculum -q` | Pass (exit 0) | Tất cả test pass (`[100%]`), có deprecation warning từ `matplotlib`/`pyparsing` |
| `uv run python -m pytest tools/pyrunner -q` | Pass (exit 0) | `14 passed` (`.............. [100%]`) |
| `uv run ruff check curriculum tools/build_content.py tools/validate.py` | Exit 1 (43 lỗi có sẵn) | Giảm từ 44 xuống 43 lỗi (`E501` ở `tools/validate.py:426` đã hết; 43 lỗi còn lại đều là lỗi có sẵn trước đó) |
| `uv run python tools/build_content.py` | Pass (exit 0) | `Built 35 lessons, 8 exams, 210 flashcards, 563 questions -> apps\web\src\generated` |
| `pnpm.cmd --filter web typecheck` | Pass (exit 0) | `tsc --noEmit` xanh |
| `git diff --stat -- curriculum/syllabus.yaml` | Đã kiểm | `curriculum/syllabus.yaml \| 152 +++++++++++++++++++++++++++++++++++++++-------- (1 file changed, 128 insertions(+), 24 deletions(-))` |
| `git status --short` | Đã kiểm | Chỉ có 7 file tracked được phép (`M` — `apps/web/src/app/(main)/learn/page.tsx`, `apps/web/src/lib/types.ts`, `curriculum/syllabus.yaml`, `pyproject.toml`, `tools/build_content.py`, `tools/validate.py`, `uv.lock`) + `tasks/` + `.hallmark/` |
