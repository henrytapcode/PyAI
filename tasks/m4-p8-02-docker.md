# M4 bước 23: bài p8-02 Docker basics

## Mục tiêu
Viết bài `p8-02-docker` trong `curriculum/phase-08-production/`, đúng `docs/CONTENT_GUIDE.md` (gồm mục "phase 6+"), song ngữ EN/VI.
- Bài **không** có `runner: local`: mọi khối `python`, example, exercise và quiz chạy trong Pyodide, nên chỉ được dùng Python thuần cùng thư viện chuẩn có trong Pyodide (`re`, `fnmatch`, `pathlib.PurePosixPath`…).
- Máy học viên có thể **không có Docker**. Bài dạy đọc và viết Dockerfile; lệnh `docker` chỉ nằm trong fence `bash`, không chạy, không chấm.
- Phần chấm điểm là code Python xử lý **văn bản** Dockerfile: tách lệnh, kiểm thứ tự layer, kiểm `.dockerignore`.
- Người học vừa xong p8-01: một app FastAPI `main.py` chạy bằng `uvicorn main:app`. Bài này đóng gói chính app đó.
- Bài mẫu về giọng văn và hình dạng: `curriculum/phase-08-production/p8-01-fastapi/` (commit `85b81fc`).

## File được phép sửa/tạo
- Thư mục mới `curriculum/phase-08-production/p8-02-docker/` và mọi file bên trong.
- `curriculum/glossary.yaml`: chỉ **thêm** thuật ngữ mới (Docker, image, container, Dockerfile, base image, layer, build cache, `.dockerignore`, port mapping). Thuật ngữ nào đã có thì bỏ qua. `git diff --numstat curriculum/glossary.yaml` phải có 0 dòng xóa.
- `tasks/m4-p8-02-docker.report.md`

## Không được đụng
- Mọi file khác, gồm `apps/`, `tools/`, `packages/`, `curriculum/syllabus.yaml`, `curriculum/topics.yaml`, phase 0–7, `p8-01-fastapi`, `exams/`, `pyproject.toml`, `uv.lock`.
- Tag dùng tag có sẵn trong `topics.yaml`: `production` (chính), có thể thêm `packaging`.
- Không xóa file, không `git commit`, **không chạy `pnpm --filter web build`**, không chạy server hay dev server, **không chạy `docker`**.
- `meta.yaml` **không** có trường `runner`.

## Quy tắc code (bắt buộc)
- Dockerfile đặt trong fence ```` ```dockerfile ````; lệnh terminal trong ```` ```bash ````.
- Validator so fence `dockerfile`, `bash` và `text` **giống hệt từng ký tự** giữa EN và VI, kể cả comment. Vì vậy comment trong các fence này viết bằng tiếng Anh, ngắn, hoặc bỏ hẳn; phần giải thích để ở đoạn văn bên ngoài.
- **Dockerfile mẫu chuẩn** dùng xuyên suốt bài, worker giữ đúng ý (được chỉnh nhỏ nếu có lý do, ghi vào report):
  ```dockerfile
  FROM python:3.13-slim
  WORKDIR /app
  COPY requirements.txt .
  RUN pip install --no-cache-dir -r requirements.txt
  COPY . .
  EXPOSE 8000
  CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
  ```
  Callout `[!TIP]` nói rằng repo của khóa học dùng `uv`, và có thể dùng uv trong Docker. Bài dùng `pip` cho dễ hiểu; trỏ tới tài liệu "uv in Docker".
- Khối `python` chạy được trong Pyodide và in output thật (chạy rồi chép).
  - Dockerfile trong code Python là chuỗi nhiều dòng (`"""..."""`).
  - Không đọc hay ghi file thật, không `subprocess`, không mạng.
  - Sạch với `uv run python -W error`, stderr rỗng.
- Thông báo lỗi hay output của `docker` **không chạy được ở đây**, nên không bịa thông báo dài.
  - Ở mục lỗi thường gặp, mô tả triệu chứng bằng lời: build chậm, image nặng, không truy cập được từ máy host, lộ key.
  - Phát hiện các lỗi đó bằng mini-linter Python của bài; output của linter là output thật.
  - Nếu trích một dòng của Docker hay `curl`, chỉ dùng dòng ngắn, phổ biến, và ghi vào report "chưa kiểm được trên máy".
- Khối mời **Visualize** phải dưới 600 step. Kiểm bằng `tools/pyrunner/tracer.py`, ghi `len(steps)`, `truncated` vào report.

## Nội dung bài (boss chốt dàn ý, worker viết)
Opening (không heading): "chạy được trên máy tôi" là vấn đề kinh điển. Service FastAPI ở p8-01 cần đúng phiên bản Python, đúng thư viện, đúng lệnh khởi động. Docker gói tất cả vào một **image**, để máy bạn, máy đồng đội và server chạy giống hệt nhau.

1. **Image và container.**
   - Ví von bằng OOP ở phase 2: image giống class, container giống instance. Một image chạy được nhiều container.
   - **Picture in text** (fence `text`): `Dockerfile --build--> image --run--> container(s)`.
   - Một câu: container khác máy ảo ở chỗ dùng chung nhân hệ điều hành nên nhẹ hơn; chi tiết để "Đọc thêm".
2. **Đọc một Dockerfile.**
   - Dockerfile mẫu chuẩn ở trên, giải thích từng lệnh: `FROM`, `WORKDIR`, `COPY`, `RUN`, `EXPOSE`, `CMD`, có thể thêm `ENV`.
   - **Bảng so sánh** `| instruction | what it does | runs when |`: build hay lúc khởi động container. Nhấn mạnh `RUN` chạy lúc build, `CMD` chạy lúc start.
   - Khối `python`: hàm `parse_dockerfile(text)` nhỏ tách thành list `(instruction, args)`, bỏ dòng trống và comment, in ra. Hàm này dùng lại ở các mục sau và trong exercise.
3. **Build và run** (fence `bash`, không chạy):
   - `docker build -t rag-api .`, `docker run -p 8000:8000 rag-api`, `curl http://127.0.0.1:8000/health`.
   - Giải thích port mapping `-p host:container`.
   - Vì sao `--host 0.0.0.0` trong container, khác `127.0.0.1` ở p8-01: `127.0.0.1` trong container chỉ là chính container.
   - **Mermaid** `flowchart LR` (≤ 7 node): source + Dockerfile → `docker build` → image → `docker run -p` → container → request từ máy host.
4. **Layer và build cache: thứ tự quan trọng.**
   - Mỗi lệnh tạo một layer. Khi một layer thay đổi, mọi layer phía sau phải build lại.
   - So sánh thứ tự tốt (copy `requirements.txt` → install → `COPY . .`) với thứ tự xấu (`COPY . .` trước `pip install`).
   - **Trace table** `| step | instruction | good order: cached? | bad order: cached? |` cho tình huống "chỉ sửa `main.py`".
   - Khối `python` mô phỏng: cho list lệnh và tập file đã đổi, hàm trả về vị trí layer đầu tiên phải build lại. In kết quả cho hai thứ tự. Đây là section mời bấm **Visualize** (xem biến `rebuild_from` đổi theo từng bước).
5. **`.dockerignore`: những gì không được vào image.**
   - Liệt kê `.venv/`, `.git/`, `__pycache__/`, `*.pyc`, `.env`, `data/raw/` hoặc tương tự. Lý do: image nhỏ hơn, build nhanh hơn, và **không lộ secret**.
   - Khối `python` dùng `fnmatch` mô phỏng xem file nào bị loại, trên một list đường dẫn giả. Ghi rõ đây là bản đơn giản: luật thật của Docker có thêm `**` và `!`.
   - Callout `[!WARNING]`: `.env` mà lọt vào image thì ai có image cũng đọc được key. Truyền biến lúc chạy bằng `docker run --env-file .env` (fence `bash`), không dùng `ENV API_KEY=...` trong Dockerfile.
6. **Image gọn và lặp lại được.**
   - Ghim base image (`python:3.13-slim`, không dùng `latest`).
   - Dùng `--no-cache-dir` khi `pip install`.
   - Dùng `requirements.txt` có phiên bản ghim, nối với ý ghim phiên bản trong phase 3.
   - **Bảng** `| choice | smaller/faster | why |`.
7. **Lỗi thường gặp** (VI: `## 7. Lỗi thường gặp`). Mỗi lỗi gồm Dockerfile sai, triệu chứng (bằng lời) và cách sửa. Có một khối `python` chạy mini-linter trên Dockerfile sai, in cảnh báo thật:
   - `COPY . .` trước `pip install`, nên build lại chậm mỗi lần sửa code;
   - `FROM python:latest` hoặc `FROM python` không có tag;
   - `CMD` dùng `--host 127.0.0.1`, nên host không truy cập được;
   - `COPY .env` hoặc `ENV OPENAI_API_KEY=...`, nên lộ secret;
   - shell form `CMD uvicorn main:app` thay cho exec form (nêu ngắn: nên dùng exec form JSON).
8. **Recap / Tóm tắt**: 4–6 gạch đầu dòng.

meta: `phase: p8`, `order: 2`, `kind: lesson`, `tags: [production]` (có thể thêm `packaging`), `prerequisites: [p8-01-fastapi]`, `duration_min` 12–16, `outcomes` khớp syllabus (có thể thêm 1 dòng), `review_by: "2027-05-01"`. `further_reading`: Docker docs "Dockerfile reference", Docker docs "Build cache", uv docs "Using uv in Docker". Dùng URL chính thức, mở thử từng link, ghi vào report.

## Examples (3)
- `01_parse_dockerfile`: tách Dockerfile mẫu, xử lý được comment, dòng trống và dòng nối bằng `\`. In bảng `instruction | args` và đếm số layer (`RUN`, `COPY`, `ADD`).
- `02_cache_simulator`: mô phỏng build hai lần, lần đầu không có cache, lần hai chỉ đổi `main.py`. Với thứ tự tốt và thứ tự xấu, in cho mỗi lệnh `CACHED` hay `REBUILD`, rồi in số layer phải build lại.
- `03_dockerignore_check`: list 10–12 đường dẫn của một dự án RAG (gồm `.env`, `.venv/...`, `data/raw/...`, `main.py`, `requirements.txt`). Áp luật `.dockerignore` bằng `fnmatch`. In file nào được gửi vào build context, file nào bị loại, và cảnh báo nếu `.env` lọt vào.

## Exercises (2)
Test import code người học như module `exercise`. Pyodide chạy được.
- `ex01-fix-dockerfile` (`kind: debug`):
  - Starter có `DOCKERFILE = """..."""` chứa 3–4 lỗi: `COPY . .` trước `pip install`, base `python:latest`, `--host 127.0.0.1`, thiếu `--no-cache-dir`.
  - Test tách chuỗi bằng một hàm parse **viết sẵn trong file test** (người học không phải viết parse), rồi kiểm:
    - base có tag cụ thể, không phải `latest`;
    - `COPY requirements.txt` đứng trước `RUN pip install`, và `RUN pip install` đứng trước `COPY . .`;
    - `CMD` là exec form và có `0.0.0.0`;
    - `pip install` có `--no-cache-dir`.
  - Từ 4 tới 5 test, tên test đọc như câu. Starter import được và fail mọi test.
- `ex02-dockerfile-linter` (`kind: code`):
  - `parse_dockerfile(text: str) -> list[tuple[str, str]]`: instruction viết hoa, args đã `strip`; bỏ dòng trống và comment `#`; nối dòng kết thúc bằng `\`.
  - `lint(text: str) -> list[str]` trả list mã cảnh báo, theo thứ tự cố định:
    - `"unpinned-base"`: `FROM` không có tag hoặc tag là `latest`;
    - `"copy-before-install"`: có `COPY . .` đứng trước lệnh `RUN` đầu tiên có `pip install`;
    - `"secret-in-image"`: `COPY` hay `ADD` có `.env`, hoặc `ENV` có tên chứa `KEY`, `TOKEN` hay `SECRET`;
    - `"localhost-cmd"`: `CMD` có `127.0.0.1` hoặc `localhost`.
    - Dockerfile sạch trả `[]`.
  - Starter có hai hàm, docstring kèm ví dụ, `# TODO`, `return None`. Starter import được và fail **mọi** test.
  - Từ 6 tới 7 test, có `parametrize` cho từng mã cảnh báo, gồm:
    - dòng nối `\`;
    - comment và dòng trống;
    - instruction viết thường (`from python:3.13-slim`);
    - Dockerfile sạch;
    - Dockerfile dính nhiều lỗi cùng lúc, đúng thứ tự mã.
  - `alternatives/01_*`: một cách khác thật sự, ví dụ dùng `re` để tách, hoặc một bảng luật gồm list `(code, check_fn)`. File `.md` nói khi nào nên dùng cách nào.
- Hint 3 tầng đúng CONTENT_GUIDE. Hint 3 chỉ cho **khung**, để trống ít nhất 2–3 dòng logic chính, không chép gần trọn lời giải.

## Quiz
- 15–18 câu, mỗi loại `mcq`, `output`, `fill`, `parsons` có ít nhất 2. Khoảng 5 dễ, 7 vừa, 3 khó. 6 flashcard.
- Code trong câu hỏi là Python thuần, chạy được trong Pyodide. Dockerfile chỉ xuất hiện dưới dạng chuỗi trong code, hoặc trong đề bài và phương án MCQ.
- `parsons` phải là code Python chạy được và chỉ có **một** thứ tự đúng, nhờ phụ thuộc giữa các dòng. Không dùng parsons chỉ để sắp xếp dòng Dockerfile, vì thứ tự đó không chạy được để chấm.
- Phải có câu về:
  - image và container;
  - `RUN` và `CMD`;
  - thứ tự layer và cache;
  - `.dockerignore` với `.env`;
  - `-p 8000:8000`;
  - `0.0.0.0` và `127.0.0.1`;
  - ghim base image.
- Luật MCQ:
  - đáp án đúng có `len <= 1.2 ×` trung bình độ dài distractor, ở cả en và vi;
  - đáp án đúng là phương án dài nhất duy nhất ở tối đa 1/3 số MCQ;
  - không giấu lý do trong đáp án đúng.
  - Chạy script độ dài trong `tasks/m4-p7-test.md`, đổi path sang `quiz.yaml` của bài này, ghi kết quả.

## Tiêu chí hoàn thành (checklist)
1. [ ] Đủ file theo layout CONTENT_GUIDE. `meta.yaml` đúng như mục meta, không có `runner`.
2. [ ] Lesson đúng dàn ý, có đủ: picture in text, trace table, mermaid, bảng so sánh, fence `dockerfile` và `bash`, một lời mời Visualize, callout.
3. [ ] Parity EN/VI: code Python chỉ khác comment; fence `dockerfile`, `bash` và `text` giống hệt; số dòng mermaid bằng nhau.
4. [ ] Tuân thủ Quy tắc code: chạy được trong Pyodide, `-W error` sạch, stderr rỗng, output là output thật, không bịa output Docker. Lệnh grep bên dưới rỗng.
5. [ ] Exercise: starter fail **mọi** test (ghi số test pass với starter, phải là 0); solution và alternative pass cả pytest lẫn browser runner trong validate.
6. [ ] Bản VI tự nhiên, xưng "bạn", thuật ngữ giữ tiếng Anh kèm giải nghĩa lần đầu, vd "image (bản đóng gói)", "container (phiên bản đang chạy của image)".
7. [ ] Report ghi: số step khối Visualize, thời gian `validate.py --path`, kết quả script MCQ, link đã mở, mọi dòng output Docker/curl chưa kiểm được.
8. [ ] Lệnh kiểm tra xanh, chạy đúng như ghi.

## Lệnh kiểm tra
Từ gốc repo `D:\Proj\python-ai-platform`:
```
uv run python tools/validate.py --path curriculum/phase-08-production/p8-02-docker
uv run python tools/validate.py --fast
uv run python -m pytest curriculum/phase-08-production -p no:warnings --color=no
uv run ruff check curriculum/phase-08-production
grep -rnE "subprocess|open\(|requests\.|httpx|import docker|os\.system" curriculum/phase-08-production/p8-02-docker --include=*.py --include=*.yaml
git diff --numstat curriculum/glossary.yaml
uv run python tools/build_content.py
git status --short
```
Mong đợi:
- validate 0 lỗi, pytest exit 0, ruff sạch;
- grep rỗng;
- glossary chỉ có dòng thêm;
- build_content in số lesson tăng 1 (50 → 51);
- thay đổi chỉ nằm trong các file được phép, ngoài `tasks/` và `.hallmark/` vốn đã untracked.

## Ghi chú cho worker
- Đọc trước:
  - `docs/CONTENT_GUIDE.md`;
  - bài `p8-01-fastapi`, cả lesson, exercise và quiz, làm mẫu hình dạng;
  - `curriculum/phase-03-code-quality/` để biết người học đã được dạy gì về ghim phiên bản và packaging.
- Dùng `uv run python -m pytest`, không dùng `uv run pytest`. Trên Windows có thể không có `grep` trong PATH; dùng Git Bash.
- Mọi lệnh phải tự kết thúc. Không chạy server, không chạy Docker.
- Kiểm cảnh báo bằng `uv run python -W error <file>`.

## Trạng thái
- Bước hiện tại: xong, đã commit `da2612a` (đạt vòng 2; boss kiểm: validate --path 0 lỗi, validate toàn bộ 0 lỗi (51 bài), pytest phase 8 29 passed, ruff sạch, glossary +78/-0, typecheck + build 75 trang; trong app (Pyodide) ex02 starter 0/13, solution qua hết)
- Vòng: 2/3
- Số lần swap: 0
- Fallback: không
- Model: Gemini 4 Hydrogen (High)

## Feedback vòng 2
Boss đã chạy lại: validate, pytest, ruff, grep đều xanh; quiz đúng phân bổ và luật độ dài MCQ. Còn 4 điểm trong lesson (sửa cả `lesson.en.md` và `lesson.vi.md`, giữ parity):
1. **Trace table §4 khó đọc.** Một hàng đang trộn lệnh của cả hai thứ tự (`COPY requirements.txt .` / `COPY . .`), và hai hàng cuối lệch nhau. Viết lại thành bảng `| step | good order | cached? | bad order | cached? |`:
   - mỗi cột thứ tự liệt kê đúng các lệnh của list tương ứng trong khối Python bên dưới: good 6 lệnh, bad 5 lệnh, ô trống dùng `—`;
   - kết quả khớp output thật: good build lại 2 layer từ chỉ số 4; bad build lại 3 layer từ chỉ số 2.
   - Một câu nhắc rằng bảng đánh số từ 1, còn code đếm chỉ số từ 0 (hoặc đổi cho thống nhất).
2. **§7 Lỗi thường gặp thiếu code sai.** Với mỗi lỗi 1–5, thêm một fence `dockerfile` ngắn (1–3 dòng) chứa dòng sai, rồi một fence `dockerfile` chứa dòng đã sửa, hoặc gộp cả hai vào một fence với comment `# wrong` / `# fixed` bằng tiếng Anh. Các fence này giống hệt nhau giữa EN và VI.
3. **Linter ở §7 gần như là lời giải của ex02**: tách lệnh, `unpinned-base`, `copy-before-install`, `secret-in-image`, `localhost-cmd`. Thu khối Python ở §7 lại:
   - chỉ kiểm hai luật **không** chấm trong ex02: `pip-cache` (thiếu `--no-cache-dir`) và `shell-cmd` (CMD không ở exec form);
   - dùng `parse_dockerfile` ở §2 (định nghĩa lại trong khối cho tự chạy được), không thêm luật nào khác;
   - một câu sau khối: bốn lỗi còn lại bạn sẽ tự viết luật phát hiện trong bài tập ex02;
   - output vẫn là output thật.
   Hint 1 của ex02 đang nói "mini-linter pattern from §7"; sửa cho khớp (en + vi).
4. **§6 nói sai về kiến thức trước:** câu "the same lock-file discipline you saw with `uv.lock` in earlier phases". Các phase trước không dạy `uv.lock` (p3-02 chỉ có `uv add --dev ruff` và `pyproject.toml`). Viết lại: ghim phiên bản giúp mọi lần build cài đúng cùng gói, và `uv` làm việc này tự động bằng `uv.lock` (giới thiệu một câu). Ví dụ phiên bản dùng `fastapi==0.162.7`, cho khớp `pyproject.toml` của repo.

Chạy lại:
- `validate.py --path curriculum/phase-08-production/p8-02-docker`;
- `pytest curriculum/phase-08-production`;
- `ruff`;
- `-W error` cho mọi khối lesson đã sửa.

Ghi kết quả vào cuối report, dưới mục "Vòng 2".
