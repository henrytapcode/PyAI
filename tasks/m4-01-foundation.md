# M4 bước 1: nền móng phase 6–8

## Mục tiêu
Chuẩn bị mọi thứ để viết bài phase 6–8. Bước này **chưa** viết bài học nào. Gồm 5 phần:
- **A.** Syllabus chi tiết cho p6, p7, p8.
- **B.** Chuyển `runner: local` từ mức phase xuống mức bài.
- **C.** Thêm thư viện deep learning và production cho môi trường local.
- **D.** Kiểm xem Pyodide 0.29.5 có những gói nào.
- **E.** Ghi quy tắc nội dung mới vào tài liệu.

Bối cảnh: `tasks/M4-PLAN.md`, mục "Quyết định kiến trúc", đã được user chốt.

## File được phép sửa/tạo
- `curriculum/syllabus.yaml`: chỉ ba phase p6, p7, p8.
- `tools/build_content.py`: chỉ phần dựng `summary` của bài và phần dựng phase.
- `tools/validate.py`: chỉ phần kiểm syllabus, nếu cần cho trường `runner` của bài.
- `apps/web/src/lib/types.ts`: chỉ `LessonSummary` và `Phase`.
- `apps/web/src/app/(main)/learn/page.tsx`: chỉ điều kiện hiện badge runner cục bộ (dòng khoảng 90).
- `pyproject.toml`, `uv.lock`.
- `docs/CONTENT_GUIDE.md`: thêm một mục.
- `docs/DESIGN.md`: chỉ §5, dòng "Chạy nặng".
- `tasks/m4-01-foundation.report.md`: báo cáo.

## Không được đụng
- Phase 0–5 trong syllabus, mọi bài trong `curriculum/phase-*`, `tools/pyrunner/`, `apps/web/public/`, mọi file khác.
- Không xóa file, không `git commit`, **không chạy `pnpm --filter web build`**, không chạy dev server.

## A. Syllabus p6–p8 (`curriculum/syllabus.yaml`)
Theo đúng dạng của p4/p5 (`id`, `title`, `prerequisites`, `outcomes` en/vi với 2–4 ý ngắn; bài project có `kind: project`). Giữ nguyên id và thứ tự bài đang có. Thay đổi:
- **p6.** Mọi bài thêm `runner: local`. `p6-04-fine-tune` thành `kind: project`, title "Mini-project: a small fine-tune" / "Mini-project: fine-tune nhỏ".
- **p7.** Không bài nào có `runner` (chạy trong trình duyệt bằng fake LLM client). Sửa prerequisites:
  - `p7-01-llm-api`: `[p2-05-typing, p3-01-pytest]`. Nếu id p3 khác thì dùng id bài pytest thật trong syllabus.
  - `p7-03-embeddings`: `[p7-01-llm-api, p5-01-math-bridge]`
  - `p7-04-vector-db`: `[p7-03-embeddings, p4-01-numpy]`
  - `p7-08-evals`: `[p7-05-rag, p5-04-evaluation]`
- **p8.**
  - `p8-01-fastapi` thêm `runner: local`.
  - Thêm bài cuối `p8-05-mini-project`, `kind: project`, `runner: local`, title "Mini-project: ship a RAG service" / "Mini-project: đưa dịch vụ RAG lên production", prerequisites `[p8-04-monitoring, p7-09-mini-project-rag]`. Đây là bài gói RAG của p7 thành API FastAPI có cache và đo latency/cost.
- **Phase.** Bỏ `runner: local` ở mức phase cho cả p6, p7, p8. Sửa `summary` của p7 để nói rõ phần LLM dùng fake client, không cần API key.
- **Outcomes.**
  - Viết cho người mới, dạng "làm được gì", tiếng Việt tự nhiên, thuật ngữ giữ tiếng Anh.
  - Phải khớp với giới hạn kỹ thuật: p6 chạy CPU, dữ liệu nhỏ; p6-03 và p6-04 dùng model nhỏ có sẵn trong cache; p7 dùng fake client; p8-02 Docker chỉ đọc và viết Dockerfile, không chạy Docker.
- Comment đầu file (dòng 4): sửa thành "Phases 0-5 detailed; phases 6-8 detailed in M4 (lessons written later)". Thêm một dòng giải thích `runner: local` ở mức bài.

## B. `runner` ở mức bài
- Nguồn duy nhất là trường `runner` của bài trong syllabus (giá trị hợp lệ duy nhất: `local`). **Không** thêm vào `meta.yaml`.
- `validate.py`: báo lỗi nếu `runner` của bài hoặc của phase có giá trị khác `local`. Báo lỗi nếu phase còn khóa `runner` (đã chuyển xuống bài).
- `build_content.py`: `summary` của bài có `runner` khi syllabus có. Thêm `runner` vào `meta` của file JSON bài (`lessons/<id>.json`) để step 3 dùng.
- `types.ts`:
  - thêm `runner?: "local"` vào `LessonSummary` và `LessonMeta`;
  - bỏ `runner` khỏi `Phase`.
- `learn/page.tsx`: badge hiện khi `phase.lessons.some((l) => l.runner === "local")`. Giữ nguyên chữ và kiểu badge.

## C. Thư viện (`pyproject.toml`)
- Thêm, ghim `==` đúng phiên bản (bản ổn định mới nhất có wheel cho **Python 3.13, Windows amd64**):
  - `torch`, bản **CPU** lấy từ index của PyTorch. Khai báo `[[tool.uv.index]]` tên `pytorch-cpu`, url `https://download.pytorch.org/whl/cpu`, `explicit = true`, và `[tool.uv.sources] torch = { index = "pytorch-cpu" }`;
  - `transformers`;
  - `fastapi`, `uvicorn`, `httpx` (cho `TestClient`).
  - `pydantic` không cần khai báo riêng vì đi kèm fastapi; ghi phiên bản thực tế vào report.
- `uv sync`, rồi xác nhận:
  `uv run python -c "import torch, transformers, fastapi, httpx, pydantic; print(torch.__version__, torch.cuda.is_available(), transformers.__version__, fastapi.__version__, pydantic.__version__)"`
  → `cuda.is_available()` phải là `False` (bản CPU).
- Đo thời gian `uv run python tools/validate.py` trước và sau khi thêm thư viện, ghi vào report (boss đo trước đây khoảng 165 s).

## D. Gói trong Pyodide 0.29.5
Tải `https://cdn.jsdelivr.net/pyodide/v0.29.5/full/pyodide-lock.json` rồi ghi vào report bảng `gói | có không | phiên bản` cho: `pydantic`, `pydantic_core`, `httpx`, `fastapi`, `starlette`, `anyio`, `tiktoken`, `regex`, `jsonschema`. Không sửa code gì dựa trên kết quả này; boss dùng nó cho các bước p7.

## E. Tài liệu
- `docs/CONTENT_GUIDE.md`: thêm mục `## Deep learning, LLM & production code (phase 6+)` ngay sau mục "Data & ML code (phase 4+)", tiếng Anh, mỗi ý một gạch đầu dòng ngắn:
  - Mọi quy tắc phase 4+ vẫn áp dụng.
  - Bài có `runner: local` trong `syllabus.yaml` chạy trên runner cục bộ. Các bài khác phải chạy được trong Pyodide.
  - torch:
    - `torch.manual_seed(0)` ở đầu mọi khối có ngẫu nhiên;
    - không in tensor thô (repr có `tensor(...)`, dtype, device), mà in `round(t.item(), 3)` hoặc list đã làm tròn;
    - chỉ dùng CPU, không dùng `.cuda()`;
    - mỗi khối chạy dưới 10 giây.
  - Không gọi mạng. Model Hugging Face chỉ nạp với `local_files_only=True`, lấy từ cache do `tools/localrunner/fetch_models.py` tải sẵn. LLM chỉ gọi qua fake client `pyai_llm`. Cách gọi API thật chỉ đưa vào khối `bash`, đọc key từ `.env`, không bao giờ in key.
  - Docker: Dockerfile đưa vào khối ```` ```dockerfile ````. Không chạy Docker trong bài hay trong test.
  - Mỗi bài p7 có `review_by` trong `meta.yaml` không quá 6 tháng.
- `docs/DESIGN.md` §5, dòng "Chạy nặng (phase 6–8)": sửa thành "Chạy nặng (theo bài)", nội dung: "**Runner cục bộ** (FastAPI trên `127.0.0.1`) cho các bài có `runner: local` trong syllabus (torch, transformers, FastAPI). Phase 7 chạy trong trình duyệt với fake LLM client".

## Tiêu chí hoàn thành (checklist)
1. [ ] Syllabus p6–p8 đủ outcomes en/vi, prerequisites đúng như mục A, `runner` ở mức bài, phase không còn `runner`; phase 0–5 không đổi một ký tự.
2. [ ] validate/build/types/learn page hiểu `runner` mức bài; validate bắt được giá trị sai (thử bằng tay, ghi vào report, rồi trả lại như cũ).
3. [ ] Thư viện cài được, torch bản CPU, phiên bản ghi trong report; thời gian validate trước/sau.
4. [ ] Bảng gói Pyodide trong report.
5. [ ] CONTENT_GUIDE và DESIGN sửa đúng phạm vi.
6. [ ] Lệnh kiểm tra xanh; `git status` chỉ có file được phép (ngoài `tasks/`, `.hallmark/`).

## Lệnh kiểm tra
Từ gốc repo `D:\Proj\python-ai-platform`:
```
uv sync
uv run python -c "import torch, transformers, fastapi, httpx, pydantic; print(torch.__version__, torch.cuda.is_available(), transformers.__version__, fastapi.__version__, pydantic.__version__)"
uv run python tools/validate.py
uv run python -m pytest curriculum -q
uv run python -m pytest tools/pyrunner -q
uv run ruff check curriculum tools/build_content.py tools/validate.py
uv run python tools/build_content.py
pnpm --filter web typecheck
git diff --stat -- curriculum/syllabus.yaml
git status --short
```
Mong đợi: tất cả xanh; `torch.cuda.is_available()` là `False`.

## Ghi chú cho worker
- Dùng `uv run python -m pytest`, không dùng `uv run pytest`.
- Nếu uv không tìm được wheel torch CPU cho Python 3.13 trên Windows, dừng lại và ghi rõ lỗi vào report. Không đổi phiên bản Python.

## Trạng thái
- Bước hiện tại: 5 (đạt vòng 2; boss chạy lại cổng, kiểm bảng Pyodide, validate 308–331 s trên máy hôm nay, worker đo cùng phiên 275→330 s; đã commit `a94c693`)
- Vòng: 2/3
- Số lần swap: 0
- Fallback: không
- Model: Gemini 4 Hydrogen (High)

## Feedback vòng 1
Phần lớn đã đúng (code runner, syllabus, docs, bảng Pyodide boss đã kiểm lại khớp). Sửa 5 điểm:
1. **Ghim pydantic khớp app.** Pyodide 0.29.5 có `pydantic 2.12.5` (`pydantic-core 2.41.5`), còn local đang `2.14.3`. Bài p7-02 chạy trong trình duyệt nên thông báo lỗi validation phải giống nhau. Thêm `"pydantic==2.12.5"` vào `pyproject.toml` (cùng lý do với `scipy==1.14.1`) rồi `uv sync`. Nếu `fastapi==0.162.7` không chịu pydantic 2.12.5, hạ fastapi xuống bản mới nhất chịu được và ghi lý do vào report.
2. `tools/validate.py:426`: E501 (106 > 100) ở dòng mới thêm. Xuống dòng như khối phase ngay trên.
3. `syllabus.yaml` p6-04, outcome VI thứ 2: "độ chính xác" sai quy ước (accuracy = "tỉ lệ đoán đúng"). Sửa thành "So sánh tỉ lệ đoán đúng (accuracy) trước và sau khi fine-tune".
4. p6-02 outcome 3: EN "Save and evaluate on tiny synthetic data" mơ hồ, VI thiếu "synthetic". Sửa: EN "Save a trained model and evaluate it on tiny synthetic data" / VI "Lưu model đã train và đánh giá trên dữ liệu tổng hợp (synthetic) nhỏ".
5. p7-08 outcome 3: EN "Compare two RAG configs before changing prompts" không rõ ý. Sửa: EN "Compare two RAG configurations on the same eval set" / VI "So sánh hai cấu hình RAG trên cùng một tập eval".

Chạy lại toàn bộ lệnh kiểm tra (validate không cần đo giờ lại), cập nhật report (thêm mục "Vòng 2").
