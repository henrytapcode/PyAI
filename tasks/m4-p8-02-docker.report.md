# Báo cáo M4 bước 23: bài `p8-02-docker` (Docker basics)

## 1. Đã làm gì

- **Meta (`meta.yaml`):**
  - Tạo `id: p8-02-docker`, `phase: p8`, `order: 2`, `kind: lesson`, `level: beginner`, `tags: [production, packaging]`, `prerequisites: [p8-01-fastapi]`, `duration_min: 14`, `review_by: "2027-05-01"`. Không có trường `runner` (chạy hoàn toàn trong Pyodide).
  - `outcomes` khớp `curriculum/syllabus.yaml` và thêm 1 mục về phát hiện lỗi Dockerfile thường gặp.
  - `further_reading` gồm 3 link tài liệu chính thức đã kiểm tra HTTP `200` bằng `urllib.request`:
    - Docker Docs: Dockerfile reference — `https://docs.docker.com/reference/dockerfile/` (`200 OK`)
    - Docker Docs: Build cache — `https://docs.docker.com/build/cache/` (`200 OK`)
    - uv Docs: Using uv in Docker — `https://docs.astral.sh/uv/guides/integration/docker/` (`200 OK`)

- **Bài học (`lesson.en.md` và `lesson.vi.md`):**
  - Mở đầu không heading về bài toán "chạy được trên máy tôi" với dịch vụ FastAPI `main.py` (`uvicorn main:app`) từ `p8-01-fastapi`.
  - 7 mục nội dung + `Recap`/`Tóm tắt`:
    1. **Image và container:** ví von OOP (`class` vs instance), picture in text (`text` fence giống hệt EN/VI), so sánh ngắn với máy ảo (dùng chung nhân OS).
    2. **Đọc một Dockerfile:** Dockerfile mẫu chuẩn đúng theo spec (`FROM python:3.13-slim`, `WORKDIR /app`, `COPY requirements.txt .`, `RUN pip install --no-cache-dir -r requirements.txt`, `COPY . .`, `EXPOSE 8000`, `CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]`), giải thích thêm `ENV`, callout `[!TIP]` về `uv` trỏ sang `further_reading`, bảng so sánh `RUN` (lúc build) vs `CMD` (lúc start), khối Python `parse_dockerfile(text)` kèm output thật.
    3. **Build và run:** khối `bash` (`docker build`, `docker run -p 8000:8000`, `curl http://127.0.0.1:8000/health`), giải thích `-p host:container` và vì sao dùng `--host 0.0.0.0` thay `127.0.0.1`, biểu đồ Mermaid `flowchart LR` (6 node, số dòng bằng nhau EN/VI).
    4. **Layer và build cache:** trace table khi chỉ sửa `main.py`, khối Python `first_rebuild_layer` mô phỏng cache invalidation và lời mời bấm **Visualize** theo dõi `rebuild_from`.
       - Kết quả `tools/pyrunner/tracer.py` trên khối Visualize: `len(steps) = 52`, `truncated = False`, `error = None`.
    5. **`.dockerignore`:** liệt kê `.venv/`, `.git/`, `__pycache__/`, `*.pyc`, `.env`, `data/raw/`; khối Python dùng `fnmatch` và `PurePosixPath` (ghi rõ chỉ là bản đơn giản, luật thật có thêm `**` và `!`); callout `[!WARNING]` về lộ secret qua `.env` và khối `bash` `docker run --env-file .env -p 8000:8000 rag-api`.
    6. **Image gọn và lặp lại được:** ghim tag `python:3.13-slim`, `--no-cache-dir`, `requirements.txt` ghim phiên bản, và bảng so sánh lựa chọn.
    7. **Lỗi thường gặp:** trình bày 5 lỗi (thứ tự `COPY . .` trước `pip install`, `FROM python:latest`/thiếu tag, `--host 127.0.0.1`, `COPY .env` / `ENV OPENAI_API_KEY=...`, shell form `CMD`) bằng triệu chứng bằng lời + khối Python `lint_dockerfile` in cảnh báo thật.
    8. **Tóm tắt:** 5 gạch đầu dòng.

- **Examples (3):**
  - `01_parse_dockerfile`: tách Dockerfile mẫu có comment `#`, dòng trống và dòng nối `\`; in bảng `INSTRUCTION | ARGS` và đếm số layer `RUN`/`COPY`/`ADD` (`3`).
  - `02_cache_simulator`: mô phỏng Build 1 (cold) và Build 2 (sửa `main.py`) cho thứ tự tốt (`2/6` layer rebuild) và thứ tự xấu (`3/5` layer rebuild).
  - `03_dockerignore_check`: lọc 11 đường dẫn của dự án RAG bằng `fnmatch` + `PurePosixPath`, in danh sách vào context vs bị loại, và cảnh báo khi thiếu quy tắc `.env`.

- **Exercises (2):**
  - `ex01-fix-dockerfile` (`kind: debug`): starter có `DOCKERFILE` mắc 4 lỗi (`python:latest`, `COPY . .` trước `pip install`, thiếu `--no-cache-dir`, `--host 127.0.0.1`). File `test_exercise.py` có sẵn `_parse()` và 4 test đọc như câu. Starter fail **4/4** test (`0 passed`), solution pass **4/4**.
  - `ex02-dockerfile-linter` (`kind: code`): `parse_dockerfile(text)` + `lint(text)` với 4 mã cảnh báo theo thứ tự cố định (`unpinned-base`, `copy-before-install`, `secret-in-image`, `localhost-cmd`). File `test_exercise.py` có 7 hàm test (13 test item qua `parametrize`), kiểm cả `\`, comment/dòng trống, chữ thường `from`, Dockerfile sạch `[]`, và Dockerfile dính cả 4 lỗi. Starter import được và fail **13/13** test (`0 passed`), solution và `alternatives/01_regex_rule_table.py` pass **13/13** trên cả pytest lẫn browser runner.

- **Quiz (`quiz.yaml`):**
  - 16 câu hỏi (`7 mcq`, `3 output`, `3 fill`, `3 parsons`; độ khó: 5 mức 1, 8 mức 2, 3 mức 3) + 6 flashcards (`p8-02-f01` .. `p8-02-f06`).
  - Bao phủ đầy đủ image vs container, `RUN` vs `CMD`, layer & build cache, `.dockerignore` & `.env`, `-p host:container`, `0.0.0.0` vs `127.0.0.1`, ghim base image.
  - Mỗi câu `parsons` là Python thuần có phụ thuộc tuyến tính giữa các dòng, đã qua kiểm tra không có hoán vị khác hợp lệ trong `validate.py`.

- **Glossary (`curriculum/glossary.yaml`):**
  - `Docker image` và `container` đã có sẵn trong `glossary.yaml` nên bỏ qua `image` và `container`.
  - Chỉ thêm mới 7 thuật ngữ vào cuối file: `Docker`, `Dockerfile`, `base image`, `layer`, `build cache`, `.dockerignore`, `port mapping`.

## 2. File đã tạo / sửa

- Tạo mới thư mục `curriculum/phase-08-production/p8-02-docker/`:
  - `meta.yaml`
  - `lesson.en.md`, `lesson.vi.md`
  - `quiz.yaml`
  - `examples/01_parse_dockerfile.{py,out,en.md,vi.md}`
  - `examples/02_cache_simulator.{py,out,en.md,vi.md}`
  - `examples/03_dockerignore_check.{py,out,en.md,vi.md}`
  - `exercises/ex01-fix-dockerfile/{exercise.yaml,prompt.en.md,prompt.vi.md,starter.py,solution.py,test_exercise.py}`
  - `exercises/ex02-dockerfile-linter/{exercise.yaml,prompt.en.md,prompt.vi.md,starter.py,solution.py,test_exercise.py}`
  - `exercises/ex02-dockerfile-linter/alternatives/01_regex_rule_table.{py,en.md,vi.md}`
- Sửa (chỉ thêm dòng): `curriculum/glossary.yaml`
- Tạo mới báo cáo: `tasks/m4-p8-02-docker.report.md`

## 3. Kết quả lệnh kiểm tra

- `uv run python tools/validate.py --path curriculum/phase-08-production/p8-02-docker`:
  - `OK: 0 error(s), 0 warning(s). Checked 1 lessons, 7 markdown pairs, 3 examples, 2 exercises, 1 alternatives, 16 questions.`
  - Thời gian chạy: `3.17s` (exit `0`).
- `uv run python tools/validate.py --fast`:
  - `OK: 0 error(s), 0 warning(s). Checked 51 lessons, 387 markdown pairs, 151 examples, 102 exercises, 83 alternatives, 993 questions, 10 exams, 1 portfolio, 1 glossary, 1 interview.` (exit `0`).
- `uv run python -m pytest curriculum/phase-08-production -p no:warnings --color=no`:
  - `29 passed in 0.39s` (exit `0`).
- Kiểm tra riêng starter của hai bài tập (`EXERCISE_TARGET=starter`):
  - `ex01-fix-dockerfile`: `4 failed` (`0 passed`).
  - `ex02-dockerfile-linter`: `13 failed` (`0 passed`).
- `uv run ruff check curriculum/phase-08-production`:
  - `All checks passed!` (exit `0`).
- Kiểm tra regex `subprocess|open\(|requests\.|httpx|import docker|os\.system` trên `curriculum/phase-08-production/p8-02-docker` (`.py` và `.yaml`):
  - `0` kết quả khớp (rỗng).
- `git diff --numstat curriculum/glossary.yaml`:
  - `78  0  curriculum/glossary.yaml` (78 dòng thêm, 0 dòng xóa).
- `uv run python tools/build_content.py`:
  - `Built 51 lessons, 10 exams, 306 flashcards, 818 questions -> apps\web\src\generated` (tăng từ 50 lên 51 lessons).
- Kiểm tra `-W error` (CPython 3.13, stderr rỗng):
  - Toàn bộ 8 file `.py` (3 example, 2 starter, 2 solution, 1 alternative), 4 khối Python trong lesson và 9 câu code (`output`/`fill`/`parsons`) trong `quiz.yaml` đều exit `0`, stderr rỗng.
- Script kiểm tra độ dài MCQ trên `curriculum/phase-08-production/p8-02-docker/quiz.yaml`:
  - `total mcq: 7`, `violations: 0`, `longest-unique: 2` (`<= 7/3`).
  - Chi tiết từng câu MCQ:
    - `p8-02-q01` (ans=1): EN `[67, 71, 72, 68]` (`1.03`), VI `[70, 70, 73, 69]` (`0.99`)
    - `p8-02-q03` (ans=2): EN `[57, 59, 61, 68]` (`0.99`), VI `[60, 61, 62, 67]` (`0.99`)
    - `p8-02-q06` (ans=0): EN `[51, 53, 48, 53]` (`0.99`), VI `[49, 52, 51, 56]` (`0.92`)
    - `p8-02-q08` (ans=3): EN `[63, 64, 64, 64]` (`1.01`), VI `[62, 64, 66, 64]` (`1.00`)
    - `p8-02-q11` (ans=2): EN `[44, 50, 56, 52]` (`1.15`), VI `[53, 56, 57, 54]` (`1.05`)
    - `p8-02-q13` (ans=1): EN `[57, 61, 59, 58]` (`1.05`), VI `[48, 57, 53, 54]` (`1.10`)
    - `p8-02-q16` (ans=0): EN `[58, 59, 57, 60]` (`0.99`), VI `[55, 60, 61, 61]` (`0.91`)
- `git status --short`:
  - Chỉ có `M curriculum/glossary.yaml` và `?? curriculum/phase-08-production/p8-02-docker/` (cùng `.hallmark/` và `tasks/` đã untracked từ trước).

## 4. Điều còn chưa chắc / chưa kiểm trên máy

- **Các lệnh Docker và `curl` trong `bash`:** chưa chạy thực tế trên máy theo quy tắc không chạy Docker/server của spec (`docker build -t rag-api .`, `docker run -p 8000:8000 rag-api`, `docker run --env-file .env -p 8000:8000 rag-api`, `curl http://127.0.0.1:8000/health`). Trong bài không bịa output dài của Docker/curl.
- **Trình duyệt / Pyodide thật:** mọi code Python đều là Python thuần + thư viện chuẩn (`re`, `fnmatch`, `pathlib.PurePosixPath`, `json`) và đã qua `tools/pyrunner/runner.py` + `tools/pyrunner/tracer.py` trên CPython; chưa mở app web để chạy thử trực tiếp trên Pyodide wasm32.
- **Web build:** chưa chạy `pnpm --filter web build` theo yêu cầu cấm của spec.

## Vòng 2

### Đã sửa theo feedback
1. **Trace table §4 (`lesson.en.md`, `lesson.vi.md`):**
   - Đổi sang bảng 5 cột `| step | good order | cached? | bad order | cached? |` (VI: `| bước | thứ tự tốt | dùng cache? | thứ tự xấu | dùng cache? |`), liệt kê đúng 6 lệnh của `good_layers` và 5 lệnh của `bad_layers` (hàng 6 cột thứ tự xấu dùng `—`).
   - Thêm câu ghi chú bảng đánh số từ 1 còn danh sách Python đếm chỉ số layer từ 0 (bước 5 ứng chỉ số `4`, bước 3 ứng chỉ số `2`), và đồng bộ lại câu giải thích sau khối code (good build lại 2 layer từ chỉ số `4`, bad build lại 3 layer từ chỉ số `2`).
2. **Code sai & sửa ở §7 (`lesson.en.md`, `lesson.vi.md`):**
   - Bổ sung mỗi lỗi 1–5 một khối `dockerfile` ngắn chứa `# wrong` và `# fixed` bằng tiếng Anh, giống hệt nhau giữa bản EN và VI.
3. **Thu gọn linter ở §7 và cập nhật Hint 1 của `ex02` (`lesson.en.md`, `lesson.vi.md`, `exercises/ex02-dockerfile-linter/exercise.yaml`):**
   - Thay `lint_dockerfile` bằng `check_style` chỉ kiểm tra hai luật không chấm trong `ex02` (`pip-cache` và `shell-cmd`), dùng lại `parse_dockerfile` từ §2 (định nghĩa lại trong khối để tự chạy được), kèm output thật (`WARN: pip-cache...`, `WARN: shell-cmd...`).
   - Thêm câu sau khối code báo rằng 4 lỗi còn lại (`unpinned-base`, `copy-before-install`, `secret-in-image`, `localhost-cmd`) sẽ tự viết trong bài tập `ex02`.
   - Cập nhật Hint 1 (EN và VI) trong `exercises/ex02-dockerfile-linter/exercise.yaml` để phản ánh đúng nội dung §7.
4. **Sửa §6 về `uv.lock` và phiên bản FastAPI (`lesson.en.md`, `lesson.vi.md`):**
   - Bỏ nhận định sai rằng các phase trước đã dạy `uv.lock`; viết lại thành ghim phiên bản trong `requirements.txt` giúp mọi lần build cài đúng cùng bộ thư viện và giới thiệu một câu rằng `uv` làm việc này tự động bằng file khóa `uv.lock`.
   - Đổi ví dụ `fastapi==0.115.0` thành `fastapi==0.162.7` khớp với `pyproject.toml`.

### File đã sửa ở vòng 2
- `curriculum/phase-08-production/p8-02-docker/lesson.en.md`
- `curriculum/phase-08-production/p8-02-docker/lesson.vi.md`
- `curriculum/phase-08-production/p8-02-docker/exercises/ex02-dockerfile-linter/exercise.yaml`
- `tasks/m4-p8-02-docker.report.md`

### Kết quả lệnh kiểm tra (vòng 2)
- `uv run python tools/validate.py --path curriculum/phase-08-production/p8-02-docker`:
  - `OK: 0 error(s), 0 warning(s). Checked 1 lessons, 7 markdown pairs, 3 examples, 2 exercises, 1 alternatives, 16 questions.` (thời gian đo bằng `Measure-Command`: `3.56s`, exit `0`).
- `uv run python tools/validate.py --fast`:
  - `OK: 0 error(s), 0 warning(s). Checked 51 lessons, 387 markdown pairs, 151 examples, 102 exercises, 83 alternatives, 993 questions, 10 exams, 1 portfolio, 1 glossary, 1 interview.` (exit `0`).
- `uv run python -m pytest curriculum/phase-08-production -p no:warnings --color=no`:
  - `29 passed in 0.43s` (exit `0`).
- `uv run ruff check curriculum/phase-08-production`:
  - `All checks passed!` (exit `0`).
- Kiểm tra `-W error` trên toàn bộ 4 khối Python trong `lesson.en.md` và `lesson.vi.md`:
  - Tất cả 4/4 khối mỗi bản đều exit `0`, stderr rỗng, stdout khớp chính xác comment kết quả trong bài.
- Kiểm tra regex `subprocess|open\(|requests\.|httpx|import docker|os\.system` trên `curriculum/phase-08-production/p8-02-docker` (`.py`, `.yaml`): `0` kết quả khớp.
- `uv run python tools/build_content.py`:
  - `Built 51 lessons, 10 exams, 306 flashcards, 818 questions -> apps\web\src\generated` (exit `0`).
- `git diff --numstat curriculum/glossary.yaml`: `78  0  curriculum/glossary.yaml` (không đổi so với vòng 1).
- `git status --short`: chỉ có `M curriculum/glossary.yaml`, `?? curriculum/phase-08-production/p8-02-docker/`, `?? tasks/`, `?? .hallmark/`.
