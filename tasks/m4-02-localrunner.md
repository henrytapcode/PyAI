# M4 bước 2: runner cục bộ (server FastAPI)

## Mục tiêu
Viết một server nhỏ chạy trên máy người học. Nó chạy code Python của các bài có `runner: local` (torch, transformers, FastAPI) bằng CPython local, thay cho Pyodide.
- Hợp đồng dữ liệu **giống worker Pyodide** (`apps/web/public/pyodide-worker.js`), để bước 3 chỉ cần đổi nơi gửi request.
- Bước này **chỉ làm server và test**, chưa đụng web.

## File được phép tạo
- `tools/localrunner/server.py`: `create_app(...)` trả về app FastAPI.
- `tools/localrunner/child.py`: script chạy trong subprocess.
- `tools/localrunner/serve.py`: điểm khởi động (CLI).
- `tools/localrunner/test_server.py`: test.
- `tools/localrunner/README.md`: tiếng Anh, ngắn: cách chạy, bảo mật, các endpoint.
- `tasks/m4-02-localrunner.report.md`.

## Không được đụng
- Mọi file đang có: `tools/pyrunner/`, `tools/validate.py`, `apps/`, `curriculum/`, `pyproject.toml`, `uv.lock`. Không thêm thư viện; fastapi, uvicorn, httpx đã có.
- Không xóa file, không `git commit`, không chạy `pnpm --filter web build`, không chạy dev server.

## Thiết kế (boss chốt)

### Endpoint
Mọi body và response là JSON, UTF-8.

| Endpoint | Vào | Ra |
|---|---|---|
| `GET /health` | | `{"ok": true, "protocol": 1, "python": "3.13.x", "torch": "<version>" hoặc null, "transformers": ... hoặc null}`. Lấy phiên bản bằng `importlib.metadata`, không import torch. |
| `POST /run` | `{"code": str}` | **Stream NDJSON** (`application/x-ndjson`), mỗi dòng một message giống worker nhưng không có `id`: `{"type":"stdout","text"}`, `{"type":"stderr","text"}`, `{"type":"image","data":"data:image/png;base64,..."}`, cuối cùng đúng một `{"type":"done","ok":bool,"error":str\|null}`. Khi quá giờ: `{"type":"done","ok":false,"error":null,"timedOut":true}`. stdout phải đẩy ra **ngay khi có** (vd training loop in từng epoch), không đợi chạy xong. |
| `POST /test` | `{"code": str, "tests": str}` | JSON đúng như `runner.run_tests(code, tests)` trả về. Khi quá giờ: `{"ok":false,"passed":0,"total":0,"tests":[],"error":null,"stdout":"","timedOut":true}`. |
| `POST /trace` | `{"code": str}` | JSON đúng như `tracer.trace(code)`. Khi quá giờ: `{"steps":[],"stdout":"","error":null,"truncated":false,"timedOut":true}`. |

Thời gian chờ là hằng số đầu `server.py` và truyền được qua `create_app`: `RUN_TIMEOUT_S = 120`, `TEST_TIMEOUT_S = 60`, `TRACE_TIMEOUT_S = 30`.

### Thực thi (`child.py`)
- Mỗi request là một subprocess mới: `[sys.executable, "-I", child.py, <mode>, <result_path>]`, code gửi vào qua stdin dưới dạng JSON.
- Môi trường của child:
  - `cwd` là một `tempfile.TemporaryDirectory()` riêng cho request đó, xóa sau khi chạy;
  - biến môi trường: `PYTHONIOENCODING=utf-8`, `PYTHONUNBUFFERED=1`, `MPLBACKEND=Agg`, `HF_HUB_OFFLINE=1`, `TRANSFORMERS_OFFLINE=1`;
  - child tự thêm `tools/pyrunner` vào `sys.path` (vì `-I` bỏ qua PYTHONPATH).
- Ba mode:
  - **`run`:**
    - gọi `runner.reset_state()`;
    - `input()` báo lỗi với câu hiện có trong worker (đổi chữ "browser editor" thành "the editor");
    - nếu code import matplotlib thì dùng backend Agg và `plt.show` không làm gì;
    - `exec(compile(code, "main.py", "exec"), {"__name__": "__main__"})`;
    - stdout và stderr của người học đi thẳng ra pipe;
    - sau khi chạy, ghi `{"ok", "error", "images": [...]}` vào `result_path`. `error` là traceback đã làm sạch: chỉ giữ frame `main.py`, không lộ đường dẫn của child hay server.
  - **`test`:** `runner.run_tests(code, tests)`, ghi JSON vào `result_path`.
  - **`trace`:** `tracer.trace(code)`, ghi JSON vào `result_path`.
- Kết quả có cấu trúc **chỉ** đi qua `result_path`, không trộn vào stdout. Nhờ vậy người học print gì cũng không làm hỏng protocol.
- **Windows:** không dùng `asyncio.create_subprocess_exec`, vì uvicorn có thể chạy SelectorEventLoop, không hỗ trợ subprocess. Dùng `subprocess.Popen` kèm thread đọc pipe, đẩy vào hàng đợi rồi stream ra.
- Quá giờ, hoặc client ngắt kết nối giữa lúc stream `/run` (kiểm `await request.is_disconnected()`): kill subprocess ngay, không để process mồ côi.
- Mỗi lúc chỉ chạy một request: dùng `asyncio.Lock`, request sau xếp hàng. Lý do: torch chiếm hết CPU, chạy song song chỉ chậm thêm.

### Bảo mật (bắt buộc, có test)
Server chạy code tùy ý, nên chỉ app của người học được gọi.
1. Chỉ bind `127.0.0.1`. `serve.py` **không có** tùy chọn host.
2. **Host header** phải là `127.0.0.1:<port>` hoặc `localhost:<port>`, nếu không trả 403. Việc này chặn DNS rebinding.
3. **Origin:**
   - có Origin mà không thuộc danh sách cho phép → 403;
   - không có Origin (curl, test) → cho qua.
   - Danh sách mặc định: `http://localhost:3000`, `http://127.0.0.1:3000`. Thêm bằng `--allow-origin URL` (lặp được) hoặc biến môi trường `PYAI_RUNNER_ORIGINS` (phân tách bằng dấu phẩy). Đây là chỗ để thêm domain GitHub Pages của app.
4. Mọi `POST` phải có header `X-PyAI-Runner: 1`, thiếu thì 403. Header tùy biến buộc trình duyệt gửi preflight, nên trang lạ không gửi "simple request" được.
5. **CORS:**
   - viết tay hoặc dùng `CORSMiddleware`, chỉ cho đúng các origin trong danh sách, method `GET` và `POST`, header `Content-Type` và `X-PyAI-Runner`;
   - preflight của origin hợp lệ trả thêm `Access-Control-Allow-Private-Network: true` (Chrome cần header này khi trang trên internet gọi tới localhost).
6. Giới hạn body: `code` và `tests` mỗi cái tối đa 200 KB, quá thì 413.

### `serve.py`
- Lệnh: `uv run python tools/localrunner/serve.py [--port 8765] [--allow-origin URL ...]`.
- Khi khởi động in một dòng tiếng Anh: địa chỉ và các origin được phép. Chạy `uvicorn.run(app, host="127.0.0.1", port=port)`.

## Test (`tools/localrunner/test_server.py`)
Dùng `fastapi.testclient.TestClient`. Gửi kèm header `X-PyAI-Runner: 1` và `Host` hợp lệ (`base_url="http://127.0.0.1:8765"`). Tối thiểu:
1. `/health` trả `ok`, `protocol == 1`, có phiên bản torch.
2. `/run` với `print("a"); print("b")`: các dòng NDJSON có stdout chứa `a` rồi `b`, dòng cuối là `done` với `ok: true`.
3. `/run` lỗi `1/0`: `done.ok == false`, error có `ZeroDivisionError` và `main.py`, không có `child.py`.
4. `/run` có matplotlib vẽ một hình: đúng một message `image` bắt đầu bằng `data:image/png;base64,`.
5. `/run` người học tự in một chuỗi giống JSON hoặc giống `{"type":"done"}`: protocol vẫn đúng (chỉ một `done`, chuỗi đó nằm trong stdout).
6. Quá giờ: `create_app(run_timeout=2)` với `while True: pass` → `timedOut: true`, trả về trong vòng khoảng 5 giây.
7. `input()` → lỗi có thông báo.
8. Trong child: `os.environ["HF_HUB_OFFLINE"] == "1"`, và `os.getcwd()` không phải thư mục repo.
9. `/test` với một code và test nhỏ: kết quả bằng đúng `runner.run_tests` gọi trực tiếp, so cả dict.
10. `/trace` với `x = 1\ny = x + 1`: bằng đúng `tracer.trace` gọi trực tiếp.
11. torch: `/run` với `import torch; print(torch.tensor([1, 2]).sum().item())` → stdout `3`.
12. Bảo mật: thiếu `X-PyAI-Runner` → 403; Origin `https://evil.example` → 403; Host `evil.example` → 403; preflight từ `http://localhost:3000` có `Access-Control-Allow-Origin` và `Access-Control-Allow-Private-Network: true`; preflight từ origin lạ không có `Access-Control-Allow-Origin`; `PYAI_RUNNER_ORIGINS` thêm được origin.
13. Body quá 200 KB → 413.

## Tiêu chí hoàn thành (checklist)
1. [ ] Bốn endpoint đúng hợp đồng; `/run` stream thật (test 2 kiểm thứ tự; report ghi cách đã kiểm stdout ra từng phần, vd chạy thử `serve.py` với `curl -N` và code `time.sleep` giữa hai lần print).
2. [ ] Subprocess bị kill khi quá giờ hoặc client ngắt; không còn process `python` mồ côi (kiểm bằng tay, ghi vào report).
3. [ ] Đủ 6 điểm bảo mật, đủ test 1–13, tất cả pass.
4. [ ] `serve.py` chạy được thật: report dán output của `curl http://127.0.0.1:8765/health` và một `curl -N` tới `/run`.
5. [ ] Lệnh kiểm tra xanh; `git status` chỉ có file mới trong `tools/localrunner/` (ngoài `tasks/`, `.hallmark/`).

## Lệnh kiểm tra
Từ gốc repo `D:\Proj\python-ai-platform`:
```
uv run python -m pytest tools/localrunner -q
uv run python -m pytest tools/pyrunner -q
uv run ruff check tools/localrunner
git status --short
```
Mong đợi: tất cả xanh, ruff 0 lỗi trong `tools/localrunner`.

## Ghi chú cho worker
- Dùng `uv run python -m pytest`, không dùng `uv run pytest`.
- Xem cách `tools/pyrunner/test_tracer.py` import module để làm theo.
- Khi tự chạy `serve.py` để thử, nhớ dừng nó trước khi kết thúc.

## Trạng thái
- Bước hiện tại: 5 (đạt vòng 1; boss chạy lại test 16 passed, ruff sạch, bật serve.py thật: stream đúng thời gian, 403 cho origin lạ/thiếu header/Host lạ, preflight có PNA, ngắt kết nối thì child bị kill; đã commit `06790e8`)
- Vòng: 1/3
- Số lần swap: 0
- Fallback: không
- Model: Gemini 4 Hydrogen (High)
