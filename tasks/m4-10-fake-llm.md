# M4 bước 10: fake LLM client `pyai_llm`

## Mục tiêu
Viết module Python thuần `pyai_llm`, một LLM giả, **tất định**, không cần mạng hay API key. Mọi bài phase 7 sẽ dùng module này để dạy chat, structured output, embedding, RAG, tool use, agent và eval.
Module phải import được ở cả 4 nơi:
1. Pyodide trong trình duyệt (editor, test, Visualize).
2. Runner cục bộ (`tools/localrunner`, chạy `python -I`).
3. `tools/validate.py` (chạy code bằng `python -I -c`).
4. `pytest curriculum`.

API theo dạng chung (message là dict `role`/`content`), **không** chép SDK của một hãng cụ thể.

## File được phép sửa/tạo
- Thư mục mới `packages/pyai_llm/`: `pyproject.toml`, `pyai_llm.py` (**một file module duy nhất**, chỉ dùng thư viện chuẩn), `test_pyai_llm.py`, `README.md`
- `pyproject.toml` ở gốc (thêm dependency path, editable) và `uv.lock`
- `tools/build_content.py` (copy `pyai_llm.py` sang `apps/web/public/pyrunner/llm.py`)
- `apps/web/public/pyodide-worker.js` (nạp thêm `llm`, ghi thành `/home/pyodide/pyai_llm.py`)
- `docs/CONTENT_GUIDE.md` (thêm mục ngắn "Fake LLM client (`pyai_llm`)" trong phần phase 6+)
- `tasks/m4-10-fake-llm.report.md`

## Không được đụng
- `curriculum/**`, `apps/web/src/**`, `tools/validate.py`, `tools/localrunner/**`, `tools/pyrunner/**`.
- Không `git commit`, không chạy dev server ở foreground.
- **Không chạy `pnpm --filter web build` khi dev server đang chạy.**

## Cách cài (boss chốt)
- `packages/pyai_llm/pyproject.toml`: project `pyai-llm`, version `0.1.0`, `requires-python = ">=3.11"`, không có dependency.
  - Build backend `uv_build` với `module-root = ""` và `module-name = "pyai_llm"` (module một file nằm ngay trong thư mục).
  - Nếu `uv_build` không hỗ trợ module một file thì dùng setuptools `py-modules = ["pyai_llm"]`.
  - Ghi lựa chọn và lý do vào report.
- Gốc `pyproject.toml`: thêm `"pyai-llm"` vào `dependencies`, và `pyai-llm = { path = "packages/pyai_llm", editable = true }` vào `[tool.uv.sources]`. Chạy `uv sync`.
- Bắt buộc kiểm: `uv run python -I -c "import pyai_llm; print(pyai_llm.__version__)"` in `0.1.0`. Đây là cách validate và runner cục bộ chạy code.
- Pyodide: trong `build_content.py`, copy `packages/pyai_llm/pyai_llm.py` → `apps/web/public/pyrunner/llm.py` (thư mục này đã gitignored). Trong `pyodide-worker.js`, đổi vòng nạp thành `["runner", "tracer", "llm"]`. File sẽ thành `/home/pyodide/pyai_llm.py`, đã nằm trên `sys.path`.

## API (boss chốt; tên và hành vi phải đúng như dưới)
```python
from pyai_llm import FakeLLM, ChatResponse, ToolCall, Usage, RateLimitError, count_tokens, cosine

client = FakeLLM(seed=0, script=None, fail_times=0, embed_dim=64)
resp = client.chat(messages, temperature=0.0, max_tokens=None, tools=None, response_format=None)
vectors = client.embed(["text a", "text b"])   # list[list[float]]
```
- `__version__ = "0.1.0"`.
- **Message:** dict `{"role": "system"|"user"|"assistant"|"tool", "content": str}`.
  - Message `assistant` có thể kèm `"tool_calls": [ToolCall, ...]`.
  - Message `tool` kèm `"tool_call_id": str` và `"name": str`.
  - Sai role, thiếu content hoặc `messages` rỗng → `ValueError` với thông báo dễ hiểu.
- **`ChatResponse`** (dataclass): `content: str | None`, `tool_calls: list[ToolCall]` (mặc định rỗng), `finish_reason: str` (`"stop"`, `"length"` hoặc `"tool_calls"`), `usage: Usage`.
- **`ToolCall`** (dataclass): `id: str` (`"call_1"`, `"call_2"`, … đếm tăng theo client), `name: str`, `arguments: dict`.
- **`Usage`** (dataclass): `prompt_tokens`, `completion_tokens`, `total_tokens` (int).
- **`count_tokens(text) -> int`:** đếm theo regex `\w+|[^\w\s]` (từ và dấu câu). Prompt tokens = tổng `count_tokens` của mọi `content` + 4 mỗi message.
- **`max_tokens`:** nếu câu trả lời dài hơn thì cắt còn `max_tokens` token đầu (nối lại bằng khoảng trắng hợp lý) và `finish_reason="length"`.
- **`cosine(a, b) -> float`:** cosine similarity của hai list số. Vector có độ dài 0 thì trả `0.0`.

### Thứ tự quyết định của `chat()` (tất định)
1. **`fail_times`:** `fail_times` lần gọi `chat()`/`embed()` đầu tiên raise `RateLimitError("rate limit exceeded, retry later")`. Dùng để dạy retry.
2. **`script`:** nếu `script` là list, mỗi lần gọi lấy phần tử kế tiếp.
   - Phần tử `str` → `content`.
   - Phần tử `dict` có `tool_calls` (list dict `name`/`arguments`) → trả tool call.
   - Hết script → `IndexError("script exhausted after N replies")`.
   - Script thắng mọi quy tắc dưới.
3. **Kết quả tool:** message cuối có role `tool` → trả `content` = `"Based on the tool result: <content của tool>"`, `finish_reason="stop"`.
4. **Chọn tool:** có `tools` (list dict `{"name", "description", "parameters": JSON-schema object}`):
   - Chọn tool có nhiều từ chung nhất (lowercase, bỏ dấu câu, bỏ từ ngắn hơn 3 ký tự) giữa message user cuối và `name` + `description`. Hòa thì lấy tool đứng trước. Không tool nào có từ chung → trả lời thường (bước 6).
   - Tham số lấy từ message user, theo thứ tự trong `properties`:
     - `number`/`integer`: các số trong câu, lần lượt.
     - `string`: lần lượt các chuỗi trong nháy kép hoặc nháy đơn. Không có thì lấy cụm từ viết hoa đầu chữ đầu tiên không nằm ở đầu câu. Vẫn không có thì `""`.
     - `boolean`: `True` nếu câu có "yes" hoặc "true", ngược lại `False`.
   - `finish_reason="tool_calls"`, `content=None`.
5. **`response_format={"type": "json", "schema": {...}}`:** trả `content` là JSON (`json.dumps(..., sort_keys=False)`) gồm đúng các key trong `schema["properties"]`.
   - Giá trị trích từ message user cuối theo cùng luật bước 4.
   - Thêm luật cho key `string`: nếu câu có mẫu `<key>: <giá trị>` hoặc `<key> is <giá trị>` thì lấy giá trị đó (tới dấu phẩy hoặc dấu chấm).
6. **RAG:** nếu có message (system hoặc user) chứa dòng `Context:`, theo sau là các đoạn đánh số `[1] ...`, `[2] ...` (mỗi đoạn một dòng), và có câu hỏi ở message user cuối:
   - Chọn đoạn có nhiều từ chung với câu hỏi nhất (cùng luật chuẩn hóa).
   - Nếu số từ chung ≥ 2: trả `"<câu đầu tiên của đoạn đó> [n]"`.
   - Ngược lại trả đúng chuỗi `"I don't know based on the provided context."`.
7. **Trả lời thường:**
   - Có bảng tra nhỏ `KNOWLEDGE` (6–10 cặp câu hỏi khớp từ khóa → câu trả lời ngắn, chủ đề Python/AI, ví dụ "What is RAG?").
   - Khớp thì trả câu đó. Không khớp: `"(fake model) I received: <tối đa 12 token đầu của message user cuối>"`.
   - Nếu có message `system` chứa "pirate" thì thêm `"Arr! "` ở đầu (để dạy system message).
   - `temperature == 0`: luôn ra một câu. `temperature > 0`: chọn một trong 3 biến thể mở đầu (`""`, `"Sure. "`, `"Here is what I know: "`) bằng `random.Random(seed * 1000 + số lần đã gọi)`. Với cùng seed và cùng thứ tự gọi, kết quả lặp lại được.

### `embed(texts)`
- Text → lowercase → tách từ `\w+` → bỏ `s` cuối với từ dài hơn 3 ký tự → map qua `SYNONYMS` (dict nhỏ, 8–12 nhóm từ đồng nghĩa về chủ đề hay gặp: car/automobile/vehicle, refund/reimbursement/money back (cụm), laptop/notebook/computer, cat/kitten, doctor/physician, cheap/inexpensive/affordable, fast/quick/rapid, error/bug/failure). Mỗi nhóm về một từ gốc.
- Mỗi từ cộng `1.0` vào chiều `zlib.crc32(word.encode()) % embed_dim`. Chuẩn hóa L2, làm tròn 6 chữ số.
- Text rỗng → vector toàn `0.0`. Không dùng `hash()` (giá trị đổi theo mỗi lần chạy).
- Kết quả cần có: `cosine(embed("cheap car")[0], embed("affordable automobile")[0])` > `cosine` của "cheap car" với "fast kitten".

## Test (`packages/pyai_llm/test_pyai_llm.py`, ≥ 20 test)
Phủ:
- Từng bước trong thứ tự quyết định, kể cả thứ tự ưu tiên (script thắng tool, tool result thắng tool chọn mới).
- `usage` đúng số, `max_tokens` → `"length"`.
- Cùng seed cho cùng kết quả khi `temperature > 0`. Seed khác có thể khác: chứng minh bằng một cặp seed cụ thể.
- `fail_times` rồi mới thành công.
- Script cạn → `IndexError`. Message sai → `ValueError`.
- RAG trúng thì có trích `[n]`, trật thì ra câu "I don't know…".
- JSON parse được và đúng key.
- Embedding: tất định giữa hai lần gọi, chuẩn hóa (độ dài ≈ 1), có hiệu ứng đồng nghĩa, text rỗng.
- ToolCall id tăng dần.

## Tiêu chí hoàn thành (checklist)
- [ ] `uv run python -I -c "import pyai_llm; print(pyai_llm.__version__)"` → `0.1.0`
- [ ] `uv run python -m pytest packages/pyai_llm -q` xanh (≥ 20 test)
- [ ] `uv run ruff check packages/pyai_llm` sạch
- [ ] `pyai_llm.py` chỉ import thư viện chuẩn và chạy được trên Python 3.11+. Pyodide 0.29.5 dùng Python 3.13.
- [ ] `uv run python tools/build_content.py` tạo `apps/web/public/pyrunner/llm.py`. Worker nạp thành `pyai_llm`.
- [ ] `uv run python tools/validate.py --fast` 0 lỗi. `uv run python -m pytest curriculum -q` không có test fail mới.
- [ ] `pnpm --filter web typecheck` và `pnpm --filter web build` xanh.
- [ ] CONTENT_GUIDE có mục ngắn (≤ 25 dòng) nêu API và các quy tắc kích hoạt (script, tool, json, RAG `Context:` + `[n]`, temperature, fail_times), để người viết bài p7 dùng đúng.
- [ ] README của package có ví dụ ngắn cho từng tính năng.

## Lệnh kiểm tra
```
uv sync
uv run python -I -c "import pyai_llm; print(pyai_llm.__version__)"
uv run python -m pytest packages/pyai_llm -q
uv run ruff check packages/pyai_llm
uv run python tools/build_content.py
uv run python tools/validate.py --fast
pnpm --filter web typecheck
pnpm --filter web build
git status --short
```

## Ghi chú cho worker
- Đọc `apps/web/public/pyodide-worker.js` (cách nạp `runner`/`tracer`) và `tools/build_content.py` (cách copy pyrunner).
- Code rõ ràng, có docstring, vì người học sẽ đọc README và đôi khi đọc cả source. Không dùng tính năng quá 3.11.
- Không chạy server hay dev server. Boss sẽ tự kiểm trong app (Pyodide và runner cục bộ).

## Trạng thái
- Bước hiện tại: 5 (đạt vòng 1; boss thêm `*.egg-info/` vào .gitignore; boss kiểm 13 tình huống hành vi, import với -I, 22 test, chạy trong app bằng Pyodide và runner cục bộ, typecheck, build, validate --fast, pytest curriculum 0 fail; đã commit `e72fa21`)
- Vòng: 1/3
- Số lần swap: 0
- Fallback: không
- Model: Gemini 4 Hydrogen (High)
