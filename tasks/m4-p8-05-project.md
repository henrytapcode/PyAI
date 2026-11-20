# M4 bước 25a: mini-project p8-05 Ship a RAG service

## Mục tiêu
Viết bài `p8-05-mini-project` (`kind: project`) trong `curriculum/phase-08-production/`, đúng `docs/CONTENT_GUIDE.md` (gồm mục "phase 6+"), song ngữ EN/VI.
- Syllabus đã đặt `runner: local` cho bài này: code chạy qua runner cục bộ (CPython), vì `TestClient` cần thread mà Pyodide không có. `meta.yaml` **không** có trường `runner`.
- Đây là mini-project trọng yếu của phase 8 (vào portfolio ở bước docs sau). Người học ghép p7-09 (RAG), p8-01 (FastAPI + TestClient), p8-03 (cache, TTL, đồng hồ tiêm vào), p8-04 (metric, p95, chi phí, cảnh báo) thành **một dịch vụ RAG chạy được và kiểm thử được**.
- Outcomes trong syllabus: gói pipeline RAG thành dịch vụ FastAPI; thêm cache phản hồi và theo dõi độ trễ cùng chi phí; kiểm thử route và metric bằng TestClient.
- Mẫu cấu trúc và giọng văn: `curriculum/phase-07-llm/p7-09-mini-project-rag/` (các "Part", mục "Take it further"). Mẫu kỹ thuật: `p8-01-fastapi` (TestClient, Pydantic, in lỗi 422 gọn), `p8-03-caching`, `p8-04-monitoring`.

## Phiên bản (đã ghim trong `pyproject.toml`)
- `fastapi==0.162.7`, `pydantic==2.12.5`, `httpx==0.28.1`. API không chắc thì đọc source trong `.venv` và ghi vào report.
- Mỗi lần tạo `TestClient` và chạy một khối mất khoảng 2–3 s; giữ mỗi khối dưới 10 s.

## File được phép sửa/tạo
- Thư mục mới `curriculum/phase-08-production/p8-05-mini-project/` và mọi file bên trong. **Không** tạo `phase-test.yaml`.
- `curriculum/glossary.yaml`: chỉ **thêm** thuật ngữ mới nếu cần (vd app factory, dependency injection, health check). Thuật ngữ nào đã có thì bỏ qua. `git diff --numstat curriculum/glossary.yaml` phải có 0 dòng xóa.
- `tasks/m4-p8-05-project.report.md`

## Không được đụng
- Mọi file khác, gồm `apps/`, `tools/`, `packages/`, `curriculum/syllabus.yaml`, `curriculum/topics.yaml`, `curriculum/portfolio.yaml`, phase 0–7, `p8-01`…`p8-04`, `exams/`, `pyproject.toml`, `uv.lock`.
- Tag chỉ dùng tag có sẵn: `production` (chính), có thể thêm `rag`, `apis`, `testing`.
- Không xóa file, không `git commit`, **không chạy `pnpm --filter web build`**, không chạy server, `uvicorn` hay dev server, kể cả ở background.

## Quy tắc code (bắt buộc)
- Không mạng, không mở port: mọi request qua `TestClient(app)` trong cùng process. `uvicorn`, `curl`, `docker` chỉ nằm trong fence `bash` / `dockerfile`, không chạy, không chấm.
- **Không dùng thời gian thật**: không gọi `time.time()`, `time.perf_counter()`, `time.monotonic()`, `time.sleep`, `datetime.now()`. Dịch vụ nhận `clock` là một **callable trả về giây** (tiêm vào). Code trong bài và test luôn truyền một `FakeClock` (có `__call__` và `advance(seconds)`). Một câu trong bài: ở production bạn truyền `time.monotonic` (không gọi).
- Độ trễ "LLM" mô phỏng tất định: một wrapper client nhỏ (vd `SlowClient`) gọi `clock.advance(...)` theo công thức cố định trong `chat` (vd `0.2 + 0.002 × completion_tokens` giây). Ghi công thức trong code.
- LLM và embedding chỉ qua `from pyai_llm import FakeLLM, cosine` (đọc `packages/pyai_llm/README.md` và `pyai_llm.py`: RAG mode của `chat` cần dòng `Context:` rồi `[n] ...`, cần ≥ 2 từ thô chung; model trả câu đầu của chunk). Không đọc thuộc tính private của `FakeLLM`; đếm lời gọi bằng wrapper/spy của chính bạn.
- **App factory**: `create_app(...)` trả một `FastAPI` mới mỗi lần, mọi trạng thái (index, cache, metric) nằm trong closure hoặc object do factory tạo. Không có trạng thái ở mức module. Nhờ vậy test chạy theo mọi thứ tự.
- In lỗi 422 gọn như p8-01: `[(e["loc"], e["type"]) for e in r.json()["detail"]]`. Mỗi dòng in dưới 80 ký tự; tiền in `:.4f` hoặc `:.6f`.
- Mỗi khối `python` trong bài tự chạy được (tự định nghĩa dữ liệu, client, clock, app). Dữ liệu dùng chung giữ gọn: 6–8 tài liệu, mỗi tài liệu 1–3 câu ngắn, sự thật chính ở câu đầu. Mọi output in ra là output thật (chạy rồi chép).
- Không đọc hay ghi file, không `subprocess`, không `eval(`/`exec(`. Sạch với `uv run python -W error`, stderr rỗng.
- Khối mời **Visualize** dưới 600 step và **không** dùng FastAPI hay `FakeLLM`: vd xếp hạng top-k bằng cosine trên 3–4 vector viết tay. Kiểm bằng `tools/pyrunner/tracer.py`, ghi `len(steps)` và `truncated` vào report.

## Nội dung bài (boss chốt dàn ý, worker viết)
Opening (không heading): ở p7-09 bạn có một RAG bot chạy trong script. Trong phase này bạn đã học cách đặt code sau HTTP, cache, đo và cảnh báo. Giờ ghép lại thành một dịch vụ mà đồng đội gọi được, rẻ hơn nhờ cache, và tự báo khi chậm hay tốn tiền.

1. **The plan.**
   - **Mermaid** `flowchart TD` (≤ 10 node): request → validate (Pydantic) → cache hit? → (có) trả ngay → (không) retrieve → LLM có trích nguồn → lưu cache → ghi metric → response.
   - **Bảng** `| part | builds | from lesson |` nối mỗi Part với p7-09, p8-01, p8-03, p8-04.
   - Mô tả API cuối cùng: `GET /health`, `POST /ask`, `GET /metrics`.
2. **Part 1: app factory và index.**
   - Vì sao `create_app(docs, client, clock)` thay cho `app = FastAPI()` ở mức module: mỗi test có app mới, tiêm được client giả và đồng hồ giả. Đây là **dependency injection** ở dạng đơn giản nhất.
   - Embed toàn bộ tài liệu **một lần** khi tạo app (nối p7-09: index một lần). In số lần gọi `embed` sau 3 request: vẫn là 1.
   - Khối Visualize: top-k bằng cosine trên vài vector viết tay (không FastAPI). **Trace table** `| doc | score | rank |`.
3. **Part 2: `POST /ask` có trích nguồn và từ chối.**
   - `AskRequest(question: 1–300 ký tự, top_k: 1–5, mặc định 2)`.
   - Retrieve top_k, bỏ doc có score < `min_score`. Không còn doc nào thì trả câu từ chối, `sources: []`, **không gọi LLM**.
   - Prompt RAG dạng `Context:` + `[n] ...`. Response: `answer`, `sources` (id theo thứ tự retrieve), `usage`.
   - Chạy 3 request: trả lời được, không có trong tài liệu, và payload sai (422 gọn).
4. **Part 3: cache phản hồi.**
   - TTL cache trong factory, key = sha256 của JSON `sort_keys` gồm câu hỏi đã chuẩn hóa (strip, gộp khoảng trắng) và `top_k` (nối p8-03). Response thêm `cached: bool`.
   - Một câu: có thể thêm `index_version` vào key để làm cache hết hiệu lực khi tài liệu đổi.
   - **Picture in text** (fence `text`): timeline `t=0 ask → MISS`, `t=10 ask → HIT`, `t=400 ask → MISS (expired)` với ttl=300. Giống hệt EN/VI.
5. **Part 4: metric và `GET /metrics`.**
   - Mỗi request `/ask` ghi một record: latency (ms, từ `clock` trước/sau), token, cost, `cached`, `status`.
   - `/metrics` trả `requests`, `cache_hit_rate`, `p50_ms`, `p95_ms` (nearest-rank như p8-04), `total_cost`, `alerts`.
   - Chạy 10 request có lặp, in `/metrics`. Cho thấy cache hit có latency gần 0 và cost 0.
   - Callout `[!WARNING]`: không đưa câu hỏi gốc của người dùng vào metric hay log.
6. **Part 5: kiểm thử dịch vụ.**
   - Viết 4–5 test pytest mẫu (trong khối `python` gọi hàm test trực tiếp và in `"ok"`, hoặc chỉ hiển thị ý tưởng trong bảng). **Bảng** `| test | what it protects |`: health; 422; refusal không gọi LLM; cache hit không gọi LLM lần hai; TTL hết hạn; metrics đếm đúng.
   - Callout `[!TIP]`: fixture tạo app mới cho mỗi test.
7. **Part 6: đóng gói và chạy thật.**
   - Fence `bash`: `uv run uvicorn main:app --reload` và một `curl` mẫu. Mô tả bằng lời rằng `main.py` chỉ có một dòng `app = create_app(DOCS, real_client, time.monotonic)`; dòng này nằm trong fence `bash` (vd `cat main.py`) hoặc trong câu văn, **không** nằm trong khối `python` chạy được.
   - Fence `dockerfile` ngắn đúng các luật của p8-02 (base có tag, copy requirements trước, không copy `.env`, `CMD` bind `0.0.0.0`).
8. **Common mistakes** (VI: `## 8. Lỗi thường gặp`). Mỗi lỗi có code sai, output sai thật và cách sửa:
   - app và cache ở mức module, nên test này làm hỏng test kia (cho thấy request thứ hai trong "test mới" trả `cached: true`);
   - embed lại toàn bộ tài liệu trong mỗi request (in số lần gọi `embed` tăng theo số request);
   - key cache thiếu `top_k`, nên `top_k=1` trả kết quả của `top_k=3`;
   - đo latency mà bỏ qua request lỗi hoặc request cache hit, nên p95 và hit rate sai.
9. **Recap / Tóm tắt** (4–6 gạch đầu dòng) và **Take it further / Mở rộng thêm**: thay FakeLLM bằng API thật qua `.env`, lưu cache vào Redis, gửi metric tới OpenTelemetry, thêm rate limit.

**meta.yaml**
- `phase: p8`, `order: 5`, `kind: project`, `tags: [production, rag, ...]` (tag có sẵn).
- `prerequisites: [p8-04-monitoring, p7-09-mini-project-rag]`.
- `duration_min` 40–50.
- `outcomes`: 3 outcome của syllabus giữ nguyên, có thể thêm 1.
- `review_by: "2027-05-01"`, không có `runner`.
- `further_reading`: FastAPI docs "Testing" hoặc "Settings and Environment Variables", và FastAPI docs "Deployment: FastAPI in Containers - Docker". Mở thử, ghi vào report.

## Examples (3)
- `01_service_basics`: `create_app` với 6–8 doc; gọi `/health`, 2 câu hỏi trả lời được, 1 câu từ chối; in status, answer, sources; in số lần gọi `embed` (1) và `chat` (2).
- `02_cache_in_action`: 6 request (có lặp, khác khoảng trắng, đổi `top_k`), mỗi dòng `t | question | top_k | cached | chat calls`; sau đó `clock.advance` vượt TTL và hỏi lại → miss.
- `03_metrics_dashboard`: 12 request mô phỏng một "ngày" (có lặp, có 1 payload 422 không tính vào `/ask` metric nếu Pydantic chặn trước, ghi rõ hành vi trong bài), in `/metrics` dạng bảng `metric | value` và `alerts`.

## Exercises (2, đều `kind: project`)
Test import code người học như module `exercise`. Test tạo app trong `@pytest.fixture` qua `exercise.create_app(...)`; import `TestClient`, `FakeLLM` trong file test được. Test chỉ dùng `assert`, `pytest.raises`, `pytest.approx`, `pytest.mark.parametrize`, `@pytest.fixture` định nghĩa trong file test. Test phải chạy theo mọi thứ tự.

### `ex01-rag-service`
- `create_app(docs: list[dict], client, min_score: float = 0.2) -> FastAPI`; `docs` là list `{"id": str, "text": str}`.
- Khi tạo app: gọi `client.embed` **đúng một lần** cho mọi `text`.
- `GET /health` → `{"status": "ok", "docs": <số doc>}`.
- `POST /ask`, body `question` (1–300), `top_k` (1–5, mặc định 2) → `{"answer": str, "sources": [id, ...], "usage": {"prompt_tokens": int, "completion_tokens": int}}`.
  - Xếp doc theo `cosine` giảm dần (hòa thì giữ thứ tự gốc), lấy `top_k`, bỏ doc có score < `min_score`.
  - Không còn doc nào: `answer = "I don't know based on the provided context."`, `sources = []`, usage 0/0, **không gọi `client.chat`**.
  - Ngược lại: gọi `client.chat` một lần với message chứa `Context:` và các dòng `[1] <text>`, `[2] <text>`... theo thứ tự `sources`; `answer` là `content` trả về.
- 8–10 test: health; embed gọi 1 lần dù nhiều request (spy client bọc `FakeLLM`); sources đúng cho câu dễ; `top_k` cắt đúng; refusal không gọi chat; usage lấy từ response; 422 cho question rỗng và `top_k=9` (`parametrize`); hai app độc lập không chia sẻ trạng thái.
- Starter import được (có `create_app` trả một `FastAPI()` rỗng hoặc route trả `None`), docstring kèm ví dụ, `# TODO`, fail **mọi** test.
- `alternatives/01_*`: cách khác thật sự (vd index bằng ma trận NumPy và `argsort(kind="stable")` thay cho `sorted` với `cosine`, hoặc state trong một class `RagService` mà route gọi vào). `.md` nói ưu, nhược.

### `ex02-cache-metrics`
- `create_app(docs, client, clock, cache_ttl: float = 300.0, price_in_per_1k: float = 0.0005, price_out_per_1k: float = 0.0015) -> FastAPI`. Starter cung cấp **sẵn** phần retrieve/answer đã chạy được (như lời giải ex01, viết gọn), người học thêm cache và metric.
- `POST /ask` trả thêm `cached: bool`.
  - Key cache: câu hỏi chuẩn hóa (strip, gộp khoảng trắng) + `top_k`. Hit khi `clock() < expires_at`; hit không gọi `chat`, `usage` 0/0.
  - Cache cả câu từ chối được không? Quy định: **có** (ghi rõ trong prompt).
- Mỗi lần `/ask` (sau khi Pydantic chấp nhận) ghi record: `latency_ms = (clock sau − clock trước) × 1000`, cost theo giá, `cached`.
- `GET /metrics` → `{"requests": int, "cache_hit_rate": float, "p95_ms": float, "total_cost": float}` (`p95` nearest-rank, `total_cost` làm tròn 6 chữ số; chưa có request thì 0 / 0.0). 
- 8–10 test (dùng `FakeClock` và `SlowClient` định nghĩa trong file test): lặp câu → `cached: True` và chat không gọi lần hai; khoảng trắng khác vẫn hit; `top_k` khác → miss; hết TTL ở đúng mốc → miss; metrics rỗng; `requests` và `cache_hit_rate` đúng; `p95_ms` đúng với latency mô phỏng; `total_cost` bằng tổng chi phí từng request (`pytest.approx`); cache hit có cost 0.
- Starter import được, fail **mọi** test (vd chưa có `cached` và `/metrics`).
- `alternatives/01_*`: cách khác thật sự (vd cache và metric là hai class riêng `TTLCache`/`MetricsTracker` như p8-03/p8-04, so với dict + list trong closure). `.md` nói ưu, nhược.

Chung:
- Hint 3 tầng đúng CONTENT_GUIDE. Hint 3 chỉ cho **khung**, để trống ít nhất 2–3 dòng logic chính.
- Lời giải exercise **không** là bản sao khối trong bài: bài học có thể xây từng phần, nhưng exercise có chữ ký và yêu cầu riêng (vd `min_score` tham số, `/health` có `docs`, giá là tham số). Ghi điểm khác vào report.
- Ghi vào report thời gian `pytest` từng exercise và thời gian `runner.run_tests` gọi trực tiếp; mỗi lần dưới 30 s.

## Quiz
- 15–18 câu; mỗi loại `mcq`, `output`, `fill`, `parsons` có ít nhất 2. Khoảng 5 dễ, 7 vừa, 3 khó. 6 flashcard.
- Câu `output` / `fill` / `parsons` có thể dùng `TestClient`; mỗi câu dưới 5 s, code dưới khoảng 15 dòng. Ưu tiên Python thuần khi không cần FastAPI.
- Phải có câu về: vì sao app factory; index một lần; từ chối không gọi LLM; key cache gồm `top_k`; cache hit và metric; p95 của dịch vụ; trạng thái module làm test phụ thuộc thứ tự; không log câu hỏi gốc; thứ tự các bước pipeline (parsons).
- Luật MCQ: đáp án đúng `len <= 1.2 ×` trung bình distractor (en và vi); đáp án đúng là phương án dài nhất duy nhất ở tối đa 1/3 số MCQ; không giấu lý do trong đáp án đúng. Chạy script độ dài trong `tasks/m4-p7-test.md` (đổi path), ghi kết quả.

## Tiêu chí hoàn thành (checklist)
1. [ ] Đủ file theo layout CONTENT_GUIDE. `meta.yaml` đúng như trên, không có `runner`.
2. [ ] Lesson đúng dàn ý và có: mermaid, picture in text, trace table, bảng so sánh, một lời mời Visualize (không FastAPI/FakeLLM), callout `[!WARNING]` và `[!TIP]`, mục Take it further.
3. [ ] Parity EN/VI: code Python chỉ khác comment; fence `text`/`bash`/`dockerfile` giống hệt; số dòng mermaid bằng nhau.
4. [ ] Quy tắc code: không đồng hồ thật, không trạng thái module, `-W error` sạch, stderr rỗng, output thật, grep bên dưới rỗng.
5. [ ] Exercise: starter fail **mọi** test (ghi số); solution và alternative pass pytest và runner trong validate; khác code trong bài.
6. [ ] Bản VI tự nhiên, xưng "bạn"; thuật ngữ giữ tiếng Anh, lần đầu kèm giải nghĩa.
7. [ ] Report ghi: số step Visualize; thời gian `validate.py --path`, pytest và `run_tests`; kết quả script MCQ; link đã mở.
8. [ ] Lệnh kiểm tra xanh.

## Lệnh kiểm tra
Từ gốc repo `D:\Proj\python-ai-platform`:
```
uv run python tools/validate.py --path curriculum/phase-08-production/p8-05-mini-project
uv run python tools/validate.py --fast
uv run python -m pytest curriculum/phase-08-production -p no:warnings --color=no
uv run ruff check curriculum/phase-08-production
grep -rnE "time\.time|time\.sleep|perf_counter\(\)|monotonic\(\)|datetime\.now|_chat_calls|open\(|subprocess|requests\.|eval\(|exec\(" curriculum/phase-08-production/p8-05-mini-project --include=*.py --include=*.yaml
git diff --numstat curriculum/glossary.yaml
uv run python tools/build_content.py
git status --short
```
Mong đợi: validate 0 lỗi; pytest exit 0; ruff sạch; grep rỗng; glossary chỉ có dòng thêm (hoặc không đổi); build_content 53 → 54 lesson; thay đổi chỉ trong file được phép (ngoài `tasks/`, `.hallmark/` vốn untracked).

## Ghi chú cho worker
- Đọc trước: `docs/CONTENT_GUIDE.md`; `p7-09-mini-project-rag`; `p8-01-fastapi`, `p8-03-caching`, `p8-04-monitoring`; `packages/pyai_llm/pyai_llm.py` và `README.md`.
- Thiết kế dữ liệu và chạy thử trước, rồi mới viết lời: mọi số trong bài phải là output thật. Kiểm từng câu hỏi mẫu thật sự retrieve đúng doc và `chat` trả lời (≥ 2 từ thô chung).
- Dùng `uv run python -m pytest`, không dùng `uv run pytest`. Trên Windows dùng Git Bash cho `grep`.
- Mọi lệnh phải tự kết thúc. Không chạy server.

## Trạng thái
- Bước hiện tại: xong, đã commit 5fca22d (đạt vòng 1; boss kiểm: validate toàn bộ 0 lỗi (54 bài), pytest phase 8 83 passed, ruff sạch, grep rỗng, glossary +33/-0, starter 10/10 và 9/9 fail, typecheck + build 78 trang; trong app qua runner cục bộ ex02 starter 0/9, solution qua hết; chờ user duyệt commit)
- Vòng: 1/3
- Số lần swap: 0
- Fallback: không
- Model: Gemini 4 Hydrogen (High)
