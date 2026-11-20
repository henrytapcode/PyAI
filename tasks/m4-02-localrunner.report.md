# Báo cáo M4 bước 2: runner cục bộ (`tools/localrunner`)

## 1. Đã làm gì

Implement server FastAPI chạy code Python cục bộ trong subprocess cô lập (`python -I -u -X utf8`), giữ đúng hợp đồng dữ liệu với `apps/web/public/pyodide-worker.js`:

- **`tools/localrunner/child.py`**:
  - Tự thêm `tools/pyrunner` vào `sys.path`, cấu hình lại `stdin`/`stdout`/`stderr` sang UTF-8 (`write_through=True` trên stdout/stderr).
  - Đọc JSON đầu vào từ `stdin`, ghi kết quả có cấu trúc ra `result_path` (tách biệt hoàn toàn khỏi `stdout`).
  - Mode `run`: gọi `runner.reset_state()`, thay `builtins.input` bằng hàm báo `RuntimeError("input() is not available in the editor. Assign a value directly, e.g. name = 'Lan'.")`, nếu code import `matplotlib` thì dùng backend `Agg`, vô hiệu hóa `plt.show` và gom hình ảnh `data:image/png;base64,...`, chạy `exec(compile(code, "main.py", "exec"), {"__name__": "__main__"})`, và lọc traceback giữ duy nhất các frame của `main.py` (không lộ đường dẫn `child.py` hay site-packages).
  - Mode `test`: gọi `runner.run_tests(code, tests)`.
  - Mode `trace`: gọi `runner.reset_state()` và `tracer.trace(code)`.
- **`tools/localrunner/server.py`**:
  - Hàm `create_app(allowed_origins=None, port=None, run_timeout=RUN_TIMEOUT_S, test_timeout=TEST_TIMEOUT_S, trace_timeout=TRACE_TIMEOUT_S)` với các hằng số `RUN_TIMEOUT_S = 120`, `TEST_TIMEOUT_S = 60`, `TRACE_TIMEOUT_S = 30`.
  - 4 endpoint:
    - `GET /health`: trả về `{"ok": true, "protocol": 1, "python": ..., "torch": ..., "transformers": ...}` bằng `importlib.metadata.version`, không import `torch`.
    - `POST /run`: stream NDJSON (`application/x-ndjson`) qua `subprocess.Popen` + thread đọc `os.read` đẩy vào `asyncio.Queue` (không dùng `asyncio.create_subprocess_exec` để tương thích EventLoop trên Windows). Đẩy `stdout`/`stderr` ngay khi có, sau đó phát `image` (nếu có) và một `done` cuối (`timedOut: true` khi quá giờ).
    - `POST /test`: chạy `runner.run_tests`, trả JSON hoặc payload `timedOut: true` đúng spec khi quá giờ.
    - `POST /trace`: chạy `tracer.trace`, trả JSON hoặc payload `timedOut: true` đúng spec khi quá giờ.
  - Mỗi request chạy tuần tự qua `asyncio.Lock`, trong `cwd` là `tempfile.TemporaryDirectory` riêng (tách biệt với thư mục chứa `result.json`) và biến môi trường `PYTHONIOENCODING=utf-8`, `PYTHONUNBUFFERED=1`, `MPLBACKEND=Agg`, `HF_HUB_OFFLINE=1`, `TRANSFORMERS_OFFLINE=1`.
  - Kill subprocess ngay khi quá giờ hoặc `await request.is_disconnected()` trả `True`.
  - Middleware bảo mật ASGI (`_SecurityMiddleware`) + kiểm tra body:
    1. Chỉ bind `127.0.0.1` trong `serve.py` (không có tùy chọn `--host`).
    2. Kiểm tra `Host` là `127.0.0.1:<port>` hoặc `localhost:<port>` → sai trả `403`.
    3. Kiểm tra `Origin` theo danh sách mặc định (`http://localhost:3000`, `http://127.0.0.1:3000`) + `PYAI_RUNNER_ORIGINS` + `--allow-origin` → không hợp lệ trả `403`, không có `Origin` cho qua.
    4. Mọi `POST` bắt buộc có `X-PyAI-Runner: 1` → thiếu trả `403`.
    5. CORS chỉ cho phép origin hợp lệ, method `GET, POST`, header `Content-Type, X-PyAI-Runner`, và preflight hợp lệ trả `Access-Control-Allow-Private-Network: true` (preflight origin lạ trả `403` và không có `Access-Control-Allow-Origin`).
    6. Giới hạn `code` và `tests` tối đa `200 * 1024` byte mỗi trường (và raw body tối đa 512 KB) → vượt quá trả `413`.
- **`tools/localrunner/serve.py`**:
  - CLI hỗ trợ `--port 8765` và `--allow-origin URL` (lặp được), in 1 dòng tiếng Anh khi khởi động và gọi `uvicorn.run(app, host="127.0.0.1", port=args.port)`.
- **`tools/localrunner/test_server.py`**:
  - Đủ 13 nhóm test theo spec và bổ sung thêm test timeout `/test`, `/trace`, kiểm tra `Host` theo port cố định, streaming `stderr`, streaming UTF-8 từng phần theo thời gian thực.
- **`tools/localrunner/README.md`**:
  - Tài liệu tiếng Anh ngắn gọn về cách chạy, cơ chế bảo mật và các endpoint.

## 2. File đã tạo

- [tools/localrunner/server.py](file:///D:/Proj/python-ai-platform/tools/localrunner/server.py)
- [tools/localrunner/child.py](file:///D:/Proj/python-ai-platform/tools/localrunner/child.py)
- [tools/localrunner/serve.py](file:///D:/Proj/python-ai-platform/tools/localrunner/serve.py)
- [tools/localrunner/test_server.py](file:///D:/Proj/python-ai-platform/tools/localrunner/test_server.py)
- [tools/localrunner/README.md](file:///D:/Proj/python-ai-platform/tools/localrunner/README.md)
- [tasks/m4-02-localrunner.report.md](file:///D:/Proj/python-ai-platform/tasks/m4-02-localrunner.report.md)

Không chỉnh sửa bất kỳ file nào đang có sẵn (`tools/pyrunner/`, `tools/validate.py`, `apps/`, `curriculum/`, `pyproject.toml`, `uv.lock`).

## 3. Kết quả kiểm tra

### Lệnh kiểm tra theo spec (chạy sau lần sửa cuối)

- `uv run python -m pytest tools/localrunner -q`: **16 passed** (`................ [100%]`), exit code 0.
- `uv run python -m pytest tools/pyrunner -q`: **14 passed** (`.............. [100%]`), exit code 0.
- `uv run ruff check tools/localrunner`: **All checks passed!** (0 lỗi), exit code 0.
- `git status --short`:
  ```text
  ?? .hallmark/
  ?? tasks/
  ?? tools/localrunner/
  ```

### Kiểm tra thủ công với `serve.py` thật, `curl` và tiến trình mồ côi

(Chạy trước lần sửa cuối — lần sửa cuối chỉ ngắt 2 dòng > 100 ký tự trong `server.py` và sửa test `/trace` timeout trong `test_server.py`.)

1. Khởi động `uv run python tools/localrunner/serve.py` và gọi `curl.exe -s http://127.0.0.1:8765/health`:
   ```text
   PyAI local runner listening on http://127.0.0.1:8765 (allowed origins: http://localhost:3000, http://127.0.0.1:3000)
   INFO:     127.0.0.1:57039 - "GET /health HTTP/1.1" 200 OK
   {"ok":true,"protocol":1,"python":"3.13.15","torch":"2.15.0+cpu","transformers":"5.23.0"}
   ```

2. Streaming thật với `curl.exe -sN` tới `POST /run` (`print("epoch 1"); time.sleep(1.0); print("epoch 2")`), ghi nhận mốc thời gian từng dòng về tới client:
   ```text
   16:40:24.735  {"type": "stdout", "text": "epoch 1"}
   16:40:24.737  {"type": "stdout", "text": "\n"}
   16:40:25.734  {"type": "stdout", "text": "epoch 2"}
   16:40:25.735  {"type": "stdout", "text": "\n"}
   16:40:25.749  {"type": "done", "ok": true, "error": null}
   ```
   `epoch 1` ra ở giây `24.735`, `epoch 2` ra sau đúng `~1.0s` ở giây `25.734` (không bị gom đợi chạy xong mới gửi).

3. Kiểm tra ngắt kết nối giữa chừng và tiến trình `python.exe` mồ côi (`Get-CimInstance Win32_Process` lọc `child.py`):
   ```text
   child.py processes before: 0
   child.py processes during stream: 2
   child.py processes after disconnect: 0
   ```
   Đã dừng `serve.py` và xác nhận không còn tiến trình `localrunner`/`child.py` nào chạy nền.

## 4. Điều còn chưa chắc

- **Con cháu cấp 2 của subprocess**: `proc.kill()` kết thúc trực tiếp tiến trình `child.py` (đã xác minh `child.py` = 0 sau disconnect và timeout). Tuy nhiên nếu code của người học tự spawn tiến trình con khác (ví dụ `subprocess.Popen` hoặc `multiprocessing`), việc chỉ gọi `proc.kill()` trên Windows không dùng Job Object/`taskkill /T` có thể không giết các tiến trình cháu đó.
- **Kiểm tra từ trình duyệt thật**: Các header CORS và `Access-Control-Allow-Private-Network: true` đã được kiểm bằng `TestClient`, chưa kiểm end-to-end từ Chrome gọi từ một domain HTTPS ngoài tới `http://127.0.0.1:8765` (thuộc phạm vi bước 3 khi nối web).
