# M4 bước 22: bài p8-01 FastAPI services

## Mục tiêu
Viết bài `p8-01-fastapi`, bài đầu tiên của phase 8, trong thư mục mới `curriculum/phase-08-production/`.
- Bài phải đúng `docs/CONTENT_GUIDE.md` (gồm mục "phase 6+") và song ngữ EN/VI.
- Syllabus đã đặt `runner: local` cho bài này. Trong app, code chạy qua runner cục bộ (CPython), vì `TestClient` cần thread mà Pyodide không có.
- Người học đã có:
  - phase 2: type hint, decorator, dataclass;
  - phase 3: pytest, fixture;
  - p7-02: validate JSON bằng tay theo schema;
  - p7-09: một pipeline RAG chạy được trong notebook.
- Ý chính: muốn app web, app di động hay đồng đội dùng được pipeline AI của bạn, bạn gói nó thành một dịch vụ HTTP. FastAPI đọc type hint để tự kiểm dữ liệu vào và tự trả lỗi đúng mã.
- Bài mẫu về giọng văn và hình dạng: `curriculum/phase-06-deep-learning/p6-03-huggingface/` (bài local runner) và `curriculum/phase-07-llm/p7-01-llm-api/`.

## Phiên bản (đã ghim trong `pyproject.toml`)
- `fastapi==0.162.7`, `pydantic==2.12.5`, `httpx==0.28.1`.
- Boss đã chạy thử: `FastAPI` + `TestClient` + `BaseModel`/`Field` + `HTTPException` sạch với `-W error`, khoảng 2,5 s mỗi lần chạy.
  - Body rỗng vi phạm `min_length` trả 422, với `detail[0]["type"] == "string_too_short"`.
  - Hàm đã gắn `@app.get(...)` vẫn gọi trực tiếp được như hàm thường.
- API có thể khác trí nhớ của bạn. Không chắc thì đọc source trong `.venv`, rồi ghi điều khác vào report.

## File được phép sửa/tạo
- Thư mục mới `curriculum/phase-08-production/p8-01-fastapi/` và mọi file bên trong. **Không** tạo `phase-test.yaml`.
- `curriculum/glossary.yaml`: chỉ **thêm** thuật ngữ mới. Thuật ngữ nào đã có thì bỏ qua.
  - Danh sách: endpoint, route, HTTP method, status code, request body, path parameter, query parameter, Pydantic, TestClient.
  - `git diff --numstat curriculum/glossary.yaml` phải có 0 dòng xóa.
- `tasks/m4-p8-01-fastapi.report.md`.

## Không được đụng
- Mọi file khác, gồm:
  - `apps/`, `tools/`, `curriculum/syllabus.yaml`, `curriculum/topics.yaml`;
  - phase 0–7, `exams/`;
  - `pyproject.toml`, `uv.lock`.
- Tag dùng tag có sẵn trong `topics.yaml`: `production` (chính), `apis`, `testing`, `typing`.
- Không xóa file, không `git commit`, **không chạy `pnpm --filter web build`**.
- Không chạy server, `uvicorn` hay dev server, kể cả ở background.
- `meta.yaml` **không** có trường `runner`.

## Quy tắc code (bắt buộc)
- Không gọi mạng thật, không mở port.
  - Mọi request đi qua `TestClient(app)` trong cùng process.
  - Lệnh `uvicorn` và `curl` chỉ nằm trong fence `bash`, không chạy, không chấm. Đặt ở §2: "chạy thật trên máy bạn", có `uv run uvicorn main:app --reload` và một lệnh `curl`, kèm một câu về trang `/docs` tự sinh.
- Mỗi khối `python` tự chạy được:
  - tự định nghĩa `app` và in kết quả bằng `print(r.status_code, r.json())` hoặc trường đã chọn;
  - output in ra phải là output **thật** (chạy rồi chép).
- Khi in lỗi 422, chỉ in phần gọn, ví dụ `[(e["loc"], e["type"]) for e in r.json()["detail"]]`.
  - Không in nguyên `detail`, vì có `url` và `input`, dài và có thể đổi theo phiên bản.
  - Mỗi dòng in ra dưới 80 ký tự.
- Dùng `pydantic.BaseModel` và `Field(...)` cho ràng buộc (`min_length`, `max_length`, `ge`, `le`). Không dùng `@validator` / `field_validator` (ngoài phạm vi).
- Dữ liệu là dict hoặc list trong bộ nhớ, không dùng database, không ghi file.
- Có trạng thái toàn cục (vd dict notes) thì mỗi khối tự tạo lại, để chạy lại vẫn ra cùng output.
- LLM chỉ qua `from pyai_llm import FakeLLM` (§7, example 03). In `reply.content` và `reply.usage.total_tokens`, đều là output thật.
- Sạch với `uv run python -W error`, stderr rỗng. Mỗi khối chạy dưới 10 s.
- Khối mời **Visualize** phải dưới 600 step.
  - Kiểm bằng `tools/pyrunner/tracer.py`: in `len(steps)`, `truncated`, thời gian, và tracer có bước vào code thư viện hay không.
  - Nếu khối có FastAPI vượt giới hạn hoặc vô nghĩa khi trace, chọn khối gọi hàm route trực tiếp (không qua `TestClient`) hoặc khối Pydantic thuần, rồi ghi lý do vào report.

## Nội dung bài (boss chốt dàn ý, worker viết)
**Opening** (không heading): pipeline RAG ở p7-09 mới chạy trong một script. Muốn app web, app chat hay đồng đội gọi được nó, bạn đặt nó sau một endpoint HTTP. FastAPI biến hàm Python có type hint thành endpoint, tự kiểm dữ liệu vào và tự trả lỗi rõ ràng.

1. **HTTP trong 5 phút.**
   - Một request gồm method (`GET`, `POST`), path, có thể có query và JSON body. Một response gồm status code và JSON.
   - **Picture in text** (fence `text`, giống hệt nhau ở EN và VI): một request `POST /ask` có body JSON, mũi tên tới response `200` có JSON.
   - Ví von: endpoint là một quầy giao dịch, method là loại yêu cầu, status code là con dấu kết quả.
2. **App đầu tiên: `GET /health`.**
   - `app = FastAPI()`, `@app.get("/health")`, `TestClient(app)`, `r.status_code`, `r.json()`.
   - Nhắc decorator ở phase 2: hàm sau khi gắn decorator vẫn là hàm thường, gọi trực tiếp được.
   - Khối `bash` "chạy thật trên máy bạn" (xem Quy tắc code). Một câu: trong bài, `TestClient` gửi request ngay trong process, không mở port.
3. **Path và query parameter.**
   - `@app.get("/docs/{doc_id}")` với `doc_id: int` và query `limit: int = 3`.
   - FastAPI đổi `"7"` thành `7`; gửi `"abc"` thì nhận 422.
   - Không có id thì `raise HTTPException(status_code=404, detail=...)`.
   - Một **trace table** `| request | doc_id | limit | status |` cho 3–4 request, khớp output thật.
4. **POST với Pydantic: tự kiểm dữ liệu vào.**
   - `class AskRequest(BaseModel)` có `question: str = Field(min_length=1, max_length=200)` và `top_k: int = Field(default=3, ge=1, le=5)`.
   - Body hợp lệ cho 200. Thiếu field, sai kiểu hay vượt ngưỡng cho 422, in gọn `loc` + `type`.
   - So với p7-02: hồi đó bạn tự viết hàm validate, giờ Pydantic làm thay từ type hint.
   - **Mermaid** `flowchart TD` (≤ 8 node): request → đọc JSON → Pydantic kiểm → (lỗi → 422) → hàm xử lý → (`HTTPException` → 4xx) → response 200.
   - Callout `[!NOTE]`: 422 là lỗi do client gửi sai, code của bạn chưa chạy.
5. **Chọn status code có chủ ý.**
   - `@app.post("/notes", status_code=201)` khi tạo mới; 404 khi không thấy; 400 khi dữ liệu đúng kiểu nhưng sai nghiệp vụ.
   - **Bảng so sánh** `| code | meaning | when you use it |`: 200, 201, 400, 404, 422, 500.
   - Callout `[!WARNING]`: đừng trả `{"error": ...}` kèm status 200, vì client và monitoring (p8-04) sẽ tưởng là thành công.
6. **Kiểm thử bằng TestClient và pytest.**
   - Một file test mẫu trong fence `python`: fixture `client`, ba test (ok, 422, 404).
   - Khối này phải tự chạy được, ví dụ gọi các hàm test ở cuối và in `all tests passed`.
   - Nối với phase 3: test endpoint giống test hàm thường, chỉ khác là bạn gửi request.
   - Đây là section mời bấm **Visualize** nếu đạt giới hạn step; nếu không thì chọn section khác theo Quy tắc code.
7. **Đặt LLM sau một endpoint.**
   - `POST /chat` nhận `ChatRequest(message: str, temperature: float = Field(0.0, ge=0, le=1))` và trả `{"answer": ..., "tokens": ...}` từ `FakeLLM(seed=0)`.
   - Trả về token để đo chi phí ở p8-04. Một câu: tạo client một lần ở mức module, không tạo lại mỗi request.
   - Một câu nối sang p8-05: mini-project sẽ gói pipeline RAG theo cách này.
8. **Lỗi thường gặp** (VI: `## 8. Lỗi thường gặp`). Chạy thật để lấy đúng output:
   - gửi `data=` thay cho `json=` trong `TestClient.post` → 422 (in gọn);
   - khai báo body là `dict` thay cho model Pydantic → không còn kiểm dữ liệu, body sai vẫn lọt qua và 200 (cho thấy hậu quả);
   - trả dict lỗi với status 200 thay cho `HTTPException`;
   - quên `status_code=201` khi tạo mới, nên test mong 201 thì fail.
9. **Recap / Tóm tắt**: 4–6 gạch đầu dòng.

**meta.yaml**
- `phase: p8`, `order: 1`, `kind: lesson`, `level` như các bài cùng mức.
- `tags: [production, apis]` (có thể thêm `testing`, `typing`), `prerequisites: [p2-05-typing]`.
- `duration_min` 14–18; `outcomes` khớp syllabus (có thể thêm 1 dòng).
- `review_by: "2027-05-01"`.
- `further_reading`: FastAPI Tutorial (First Steps), FastAPI "Testing", và Pydantic "Models". Dùng URL chính thức, mở thử từng link để chắc còn sống, rồi ghi vào report.

## Examples (3)
- `01_notes_api`: API ghi chú trong bộ nhớ.
  - `GET /notes`, `GET /notes/{note_id}` (404 khi không có), `POST /notes` (201, trả id mới).
  - Chạy một chuỗi request qua `TestClient` và in mỗi request một dòng: method, path, status, body gọn.
- `02_validation_report`: model `AskRequest` như §4.
  - Gửi 5 payload: 1 hợp lệ và 4 sai kiểu khác nhau (thiếu field, chuỗi rỗng, `top_k` = 9, `top_k` = "many").
  - In một bảng gọn: payload số mấy, status, `loc` + `type` của lỗi đầu.
- `03_chat_endpoint`: `POST /chat` dùng `FakeLLM`. Gửi 3 tin nhắn, in câu trả lời và token, rồi in tổng token. Thêm 1 request `temperature=2` để thấy 422.

## Exercises (2)
Test import code người học như module `exercise`.
- Test lấy `exercise.app` và tạo `TestClient` trong một `@pytest.fixture`.
- Test phải chạy được theo **mọi thứ tự**. Trạng thái toàn cục phải được reset trong fixture, hoặc thiết kế sao cho không phụ thuộc thứ tự.
- Test chỉ dùng: `assert`, `pytest.raises`, `pytest.approx`, `pytest.mark.parametrize`, và `@pytest.fixture` định nghĩa trong file test. Import `TestClient` trong file test thì được.

### `ex01-notes-routes` (`kind: fill`)
- App ghi chú nhỏ có sẵn, với 4–5 ô `___`:
  - method của decorator (`get` / `post`);
  - kiểu của path param;
  - `status_code=___` cho POST;
  - mã trong `HTTPException`;
  - field của model Pydantic.
- 4–5 test:
  - `GET /notes` trả list;
  - `POST` trả 201 cùng id;
  - `GET` id không tồn tại trả 404;
  - `GET /notes/abc` trả 422;
  - body thiếu `text` trả 422.
- Starter có `___` ở mức module nên được phép crash khi import (CONTENT_GUIDE cho phép với `fill`). Starter fail mọi test.

### `ex02-ask-service` (`kind: code`)
Viết một dịch vụ "hỏi tài liệu" nhỏ.
- `DOCS: dict[int, str]` có sẵn trong starter, 4–5 câu ngắn.
- `GET /health` → `{"status": "ok"}`.
- `POST /ask`, body `AskRequest`:
  - `question` có độ dài 1–200;
  - `top_k` có giá trị 1–5, mặc định 2.
- Trả `{"question": ..., "sources": [doc_id, ...]}`.
  - `sources` là các id có số từ chung với câu hỏi > 0 (so chữ thường, tách theo khoảng trắng). Xếp theo số từ chung giảm dần, hòa thì id tăng dần; lấy tối đa `top_k`.
  - Không id nào khớp thì `404` với `detail = "no matching documents"`.
- Starter:
  - import được;
  - có `app`, khung `AskRequest` chưa có ràng buộc, hai hàm route có docstring kèm ví dụ, `# TODO`, rồi `return None`;
  - fail **mọi** test.
- 6 test:
  - health;
  - thứ tự `sources` đúng;
  - `top_k` cắt đúng số lượng;
  - 404 khi không khớp;
  - 422 cho `question` rỗng và cho `top_k=9` (dùng `parametrize`);
  - mặc định `top_k=2`.
- `alternatives/01_*`: một cách khác thật sự, ví dụ đếm từ chung bằng `set` + `sorted` với key tuple, thay cho vòng lặp tay; hoặc ràng buộc bằng `Annotated[...]`. File `.md` giải thích khi nào nên dùng cách nào.

Chung cho cả hai bài:
- Hint 3 tầng đúng CONTENT_GUIDE. Hint 3 để trống ít nhất 2–3 dòng thật sự.
- Ghi vào report thời gian `pytest` của cả bài và thời gian `runner.run_tests` gọi trực tiếp cho mỗi exercise. Mỗi lần phải dưới 30 s.

## Quiz
- 15–18 câu; mỗi loại `mcq`, `output`, `fill`, `parsons` có ít nhất 2. Khoảng 5 dễ, 7 vừa, 3 khó. 6 flashcard.
- Câu `output` / `fill` / `parsons` dùng `TestClient` được. Mỗi câu chạy dưới 5 s; câu có code ngắn, dưới khoảng 15 dòng.
- Phải có câu về:
  - 422 so với 400;
  - path param so với query param;
  - `status_code=201`;
  - `json=` so với `data=`;
  - hàm route gọi trực tiếp được;
  - vì sao không trả lỗi kèm 200.
- Luật MCQ:
  - đáp án đúng `len <= 1.2 ×` trung bình độ dài distractor (cả en và vi);
  - đáp án đúng là phương án dài nhất duy nhất ở tối đa 1/3 số MCQ;
  - không giấu lý do trong đáp án đúng.
  - Chạy script độ dài trong `tasks/m4-p7-test.md` (đổi path sang `quiz.yaml` của bài này) và ghi kết quả.

## Tiêu chí hoàn thành (checklist)
1. [ ] Đủ file theo layout CONTENT_GUIDE. `meta.yaml` đúng mục meta, không có `runner`.
2. [ ] Lesson đúng dàn ý và đủ các phần sau:
   - picture in text;
   - trace table;
   - mermaid;
   - bảng so sánh;
   - khối `bash` chạy thật;
   - một lời mời Visualize;
   - callout.
3. [ ] Code giữa `lesson.en.md` và `lesson.vi.md` giống hệt nhau, chỉ khác comment; số dòng mermaid bằng nhau; fence `text` giống hệt nhau.
4. [ ] Tuân thủ Quy tắc code: `-W error` sạch, stderr rỗng, không mở port, output là output thật. Các lệnh grep bên dưới rỗng.
5. [ ] Exercise:
   - starter fail **mọi** test; ghi số test pass với starter, phải là 0;
   - solution và alternative pass cả pytest **lẫn** browser runner trong validate;
   - test chạy đúng khi đảo thứ tự (`-p no:randomly` không cần; tự chạy ngược bằng `pytest ... -k` hoặc chạy từng test riêng để chứng minh, rồi ghi cách làm vào report).
6. [ ] Bản VI tự nhiên, xưng "bạn". Thuật ngữ giữ tiếng Anh, lần đầu kèm giải nghĩa, ví dụ "endpoint (điểm nhận request)", "status code (mã trạng thái)".
7. [ ] Report ghi:
   - số step và thời gian của khối Visualize;
   - thời gian `validate.py --path`;
   - kết quả script độ dài MCQ;
   - link `further_reading` đã mở được.
8. [ ] Lệnh kiểm tra xanh, chạy đúng như ghi.

## Lệnh kiểm tra
Từ gốc repo `D:\Proj\python-ai-platform`:
```
uv run python tools/validate.py --path curriculum/phase-08-production/p8-01-fastapi
uv run python tools/validate.py --fast
uv run python -m pytest curriculum/phase-08-production -p no:warnings --color=no
uv run ruff check curriculum/phase-08-production
grep -rnE "uvicorn\.run|\.run\(app|requests\.|api_key|OPENAI|time\.sleep|open\(" curriculum/phase-08-production/p8-01-fastapi --include=*.py --include=*.yaml
git diff --numstat curriculum/glossary.yaml
uv run python tools/build_content.py
git status --short
```
Mong đợi:
- validate 0 lỗi; pytest exit 0; ruff sạch;
- grep rỗng;
- glossary chỉ có dòng thêm;
- build_content in số lesson tăng 1;
- thay đổi chỉ nằm trong các file được phép, ngoài `tasks/` và `.hallmark/` vốn đã untracked.

## Ghi chú cho worker
- Đọc trước:
  - `docs/CONTENT_GUIDE.md`;
  - `tasks/m4-p6-03-huggingface.md` (cách làm bài `runner: local`);
  - bài `p6-03-huggingface` và `p7-01-llm-api`;
  - `curriculum/phase-03-code-quality/p3-01-pytest` (giọng văn khi dạy test);
  - `packages/pyai_llm/pyai_llm.py` và `README.md` (API fake client).
- Dùng `uv run python -m pytest`, không dùng `uv run pytest`. Trên Windows có thể không có `grep` trong PATH; dùng Git Bash.
- Mọi lệnh phải tự kết thúc. Không chạy server.
- Kiểm cảnh báo bằng `uv run python -W error <file>`.

## Trạng thái
- Bước hiện tại: xong, đã commit `85b81fc` (đạt vòng 1; boss kiểm: validate toàn bộ 0 lỗi (50 bài), pytest phase 8 12 passed, ruff sạch, grep rỗng, glossary +78/-0, typecheck + build 74 trang; trong app qua runner cục bộ: khối §7 chạy đúng, ex02 starter 0/7, solution qua hết; )
- Vòng: 1/3
- Số lần swap: 0
- Fallback: không
- Model: Gemini 4 Hydrogen (High)
