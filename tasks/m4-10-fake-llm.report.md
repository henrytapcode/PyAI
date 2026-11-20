# Báo cáo thực hiện `m4-10-fake-llm`

## 1. Đã làm gì

- Tạo package Python thuần `packages/pyai_llm/` gồm một file module duy nhất `pyai_llm.py` (chỉ dùng thư viện chuẩn: `collections.abc`, `dataclasses`, `json`, `math`, `random`, `re`, `typing`, `zlib`), tương thích Python 3.11+:
  - Xuất đầy đủ: `__version__` (`"0.1.0"`), `FakeLLM`, `ChatResponse`, `ToolCall`, `Usage`, `RateLimitError`, `count_tokens`, `cosine`.
  - Kiểm tra hợp lệ `messages` (`role` thuộc `system|user|assistant|tool`, có `content` chuỗi — cho phép `content=None` khi `assistant` kèm `tool_calls`), báo `ValueError` khi sai/rỗng.
  - Thực hiện đúng thứ tự quyết định tất định của `FakeLLM.chat()`:
    1. `fail_times`: raise `RateLimitError("rate limit exceeded, retry later")` trên N lần gọi `chat()`/`embed()` đầu tiên.
    2. `script`: phát lần lượt từng câu `str` hoặc `dict` có `tool_calls`, ghi đè mọi quy tắc phía dưới; báo `IndexError("script exhausted after N replies")` khi cạn.
    3. Kết quả `tool`: nếu message cuối có `role == "tool"`, trả `"Based on the tool result: <content>"` với `finish_reason="stop"`.
    4. Chọn `tool`: so khớp giao tập từ chuẩn hóa (lowercase, tách `_`, bỏ dấu câu, giữ từ ≥ 3 ký tự) với `name` + `description`, hòa lấy tool đứng trước, trích tham số `integer`/`number`/`string`/`boolean` theo thứ tự `properties`, tạo `ToolCall(id="call_N", ...)`.
    5. `response_format={"type": "json", "schema": ...}`: trả JSON (`sort_keys=False`) giữ đúng key của `schema["properties"]`, hỗ trợ mẫu `<key>: <giá trị>` / `<key> is <giá trị>` cho key `string`.
    6. RAG: nhận diện dòng `Context:` và các đoạn `[n] ...` trong message `system`/`user`, đối chiếu với câu hỏi ở message `user` cuối (loại phần `Context:` nếu nằm cùng message), trả `"<câu đầu tiên> [n]"` nếu trùng ≥ 2 từ, ngược lại `"I don't know based on the provided context."`.
    7. Trả lời thường: bảng tra `KNOWLEDGE` (8 chủ đề AI/Python, gồm `"What is RAG?"`), fallback `"(fake model) I received: <tối đa 12 token>"`, tiền tố `"Arr! "` khi `system` chứa `"pirate"`, và biến thể theo `seed` + số lần gọi khi `temperature > 0`.
  - Hỗ trợ `max_tokens` (cắt theo token và đặt `finish_reason="length"`) và tính `Usage(prompt_tokens, completion_tokens, total_tokens)`.
  - Thực hiện `FakeLLM.embed(texts)` với chuẩn hóa từ, bỏ `s` cuối (> 3 ký tự), cụm `"money back"` → `"refund"`, `SYNONYMS` (10 nhóm), băm tất định bằng `zlib.crc32`, chuẩn hóa L2 làm tròn 6 chữ số, text rỗng → vector `0.0`.
- Viết 22 unit test trong `packages/pyai_llm/test_pyai_llm.py` và hướng dẫn ví dụ từng tính năng trong `packages/pyai_llm/README.md`.
- Khai báo `pyai-llm` editable local dependency trong `pyproject.toml` gốc và cập nhật `uv.lock` qua `uv sync`.
- Cập nhật `tools/build_content.py` để copy `packages/pyai_llm/pyai_llm.py` sang `apps/web/public/pyrunner/llm.py`.
- Cập nhật `apps/web/public/pyodide-worker.js` đổi vòng nạp thành `["runner", "tracer", "llm"]` để ghi `/home/pyodide/pyai_llm.py`.
- Bổ sung mục ngắn `Fake LLM client (pyai_llm)` (13 dòng nội dung) vào `docs/CONTENT_GUIDE.md` trong phần phase 6+.

## 2. File đã tạo / sửa

- Tạo mới:
  - `packages/pyai_llm/pyproject.toml`
  - `packages/pyai_llm/pyai_llm.py`
  - `packages/pyai_llm/test_pyai_llm.py`
  - `packages/pyai_llm/README.md`
  - `tasks/m4-10-fake-llm.report.md`
- Đã sửa:
  - `pyproject.toml`
  - `uv.lock`
  - `tools/build_content.py`
  - `apps/web/public/pyodide-worker.js`
  - `docs/CONTENT_GUIDE.md`
- Sinh ra khi build (gitignored):
  - `apps/web/public/pyrunner/llm.py` (cùng các file JSON trong `apps/web/src/generated/`).

## 3. Lựa chọn build backend và lý do

- **Đã thử trước:** `uv_build` (`uv_build>=0.8,<0.13`) với `[tool.uv.build-backend]` đặt `module-name = "pyai_llm"` và `module-root = ""`.
- **Kết quả khi chạy `uv sync`:** thất bại với lỗi:
  `Expected a Python module at: packages\pyai_llm\pyai_llm\__init__.py`.
  `uv_build` (trên `uv 0.12.13`) yêu cầu layout thư mục gói `<module>/__init__.py` và không hỗ trợ module một file `pyai_llm.py` đặt trực tiếp ở root package.
- **Lựa chọn cuối cùng:** dùng `setuptools.build_meta` (`requires = ["setuptools>=68"]`) với `[tool.setuptools] py-modules = ["pyai_llm"]`.
- **Lý do:** giữ đúng yêu cầu kiến trúc một file duy nhất `packages/pyai_llm/pyai_llm.py` (để `build_content.py` copy thẳng sang `apps/web/public/pyrunner/llm.py`) và cài editable thành công để `python -I -c "import pyai_llm"` hoạt động.

## 4. Kết quả lệnh kiểm tra

Tất cả lệnh sau được chạy sau lần sửa code/tài liệu cuối cùng (trừ `git status --short` chạy sau cùng):

| Lệnh | Kết quả |
| --- | --- |
| `uv sync` | Thành công (`pyai-llm==0.1.0` editable installed) |
| `uv run python -I -c "import pyai_llm; print(pyai_llm.__version__)"` | Thành công, in `0.1.0` |
| `uv run python -m pytest packages/pyai_llm -q` | Thành công, 22 passed (`22` chấm xanh) |
| `uv run ruff check packages/pyai_llm` | Thành công (`All checks passed!`) |
| `uv run python tools/build_content.py` | Thành công (`Built 39 lessons, 9 exams, 234 flashcards, 627 questions -> apps\web\src\generated`; đã tạo `apps/web/public/pyrunner/llm.py`) |
| `uv run python tools/validate.py --fast` | Thành công (`OK: 0 error(s), 0 warning(s)`) |
| `uv run python -m pytest curriculum -q` | Thành công (exit code 0, toàn bộ test curriculum xanh) |
| `pnpm.cmd --filter web typecheck` | Thành công (`tsc --noEmit` exit code 0; chạy qua `pnpm.cmd` vì PowerShell chặn ExecutionPolicy đối với `pnpm.ps1`) |
| `pnpm.cmd --filter web build` | Thành công (`next build` compile và tạo 62 static pages, exit code 0; không có dev server nào đang chạy) |
| `git status --short` | Chỉ thay đổi đúng các file trong spec (`apps/web/public/pyodide-worker.js`, `pyproject.toml`, `uv.lock`, `tools/build_content.py`, `packages/`, `tasks/`, và `.hallmark/` có sẵn trước đó; `docs/` nằm trong `.gitignore`) |

## 5. Điều còn chưa chắc

- **Chạy thực tế trong Pyodide trình duyệt và `tools/localrunner`:** theo hướng dẫn không chạy dev server hay server, nên chưa chạy thử trực tiếp `import pyai_llm` bên trong Pyodide Web Worker (trên trình duyệt) hoặc qua `tools/localrunner` để xác nhận end-to-end khi tải `pyrunner/llm.py` → `/home/pyodide/pyai_llm.py`. Tuy nhiên, `pyai_llm.py` chỉ dùng thư viện chuẩn Python 3.11+ và vòng nạp trong `pyodide-worker.js` dùng chung cơ chế với `runner` và `tracer`.
- **Các quy ước tinh tế của tác giả bài phase 7:** trong bước chọn `tool` / trích tham số JSON, khi người dùng không dùng nháy đơn/kép, heuristic lấy cụm từ viết hoa không đứng đầu câu sẽ không trích được chuỗi thường không viết hoa (khi đó trả `""` theo spec). Nếu bài học phase 7 có mẫu câu cụ thể cần trích khác, có thể cần điều chỉnh nhỏ sau khi có nội dung phase 7 thực tế.
