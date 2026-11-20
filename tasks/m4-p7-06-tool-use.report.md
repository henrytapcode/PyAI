# Báo cáo hoàn thành: M4 bước 16 — `p7-06-tool-use`

## 1. Đã làm gì

- Xây dựng trọn bộ bài học song ngữ EN/VI `curriculum/phase-07-llm/p7-06-tool-use/` chạy trong Pyodide (không đặt `runner: local`), sử dụng `FakeLLM` với `tools=` và `script=`, không mạng, không API key, không ghi file:
  - `meta.yaml`: `phase: p7`, `order: 6`, `duration_min: 15`, `prerequisites: [p7-02-structured-output]`, `tags: [llm, functions, dicts, agents]`, `outcomes` khớp `curriculum/syllabus.yaml`, `review_by: "2027-05-01"`.
  - `lesson.en.md` và `lesson.vi.md`:
    - Đủ 7 mục nội dung + `Recap` / `Tóm tắt`: đề nghị gọi tool & `content=None`, mô tả tool bằng schema + thí nghiệm stopword trong `description`, vòng tool hoàn chỉnh, `REGISTRY` & `dispatch()` an toàn, nhiều tool + `max_rounds`, an toàn với tool có side effect (`issue_refund`, allowlist, giới hạn ngưỡng, xác nhận con người), lỗi thường gặp và tóm tắt.
    - Đủ thành phần trực quan: picture in text (`text` fence cột `you | model | your code` giống hệt EN/VI), Mermaid `flowchart LR` (7 node, cùng 8 dòng trong fence ở EN/VI), bảng field schema, bảng trace `messages`, callout `> [!WARNING]` và 1 lời mời **Visualize** ở §4 (không gọi `FakeLLM`).
    - Số step của khối **Visualize** (§4, khối Python thứ 4) đo bằng `tools/pyrunner/tracer.py`: **39 steps** (< 600, `truncated: False`, `error: None`).
  - 3 ví dụ chạy độc lập kèm `.out` và giải thích `.en.md` / `.vi.md`:
    - `01_order_assistant.py`: 2 tool (`lookup_order`, `estimate_delivery`) đi trọn vòng tool với 2 câu hỏi.
    - `02_safe_dispatch.py`: `dispatch()` xử lý 5 `ToolCall` (hợp lệ có tham số tùy chọn rỗng, tool lạ, thiếu tham số bắt buộc, sai kiểu, hàm raise `ValueError`).
    - `03_refund_guard.py`: bảo vệ `issue_refund` bằng `ALLOWED_TOOLS`, `confirmed`, `MAX_AUTO_REFUND = 100.0` và `FakeLLM(script=...)` mô phỏng hoàn tiền nhỏ (duyệt) và lớn (chặn) kèm `ACTION_LOG`.
  - 2 bài tập kèm bộ test và gợi ý 3 tầng:
    - `ex01-tool-schema` (`kind: fill`): `tool_schema(name, description, params, required)` kiểm tra 4 kiểu JSON cơ bản và `required`, 6 test (starter pass **0/6**, solution pass **6/6** trên cả pytest và browser runner).
    - `ex02-run-tools` (`kind: code`): `run_with_tools(client, question, tools, registry, max_rounds=3)`, 8 test (starter pass **0/8**, solution pass **8/8**, `alternatives/01_dispatch_helper.py` pass **8/8** trên browser runner; không sửa `tools` hay `registry`).
  - `quiz.yaml`: 16 câu hỏi (`7 mcq`, `3 output`, `3 fill`, `3 parsons`; `5` mức 1, `7` mức 2, `4` mức 3) và 6 flashcard (`p7-06-f01` .. `p7-06-f06`).
- Bổ sung 5 thuật ngữ còn thiếu vào `curriculum/glossary.yaml`: `tool schema`, `tool call`, `dispatch`, `side effect`, `allowlist` (bỏ qua `tool use` và `function calling` vì đã tồn tại sẵn).

## 2. File đã sửa / tạo

- Tạo mới `curriculum/phase-07-llm/p7-06-tool-use/`:
  - `meta.yaml`, `lesson.en.md`, `lesson.vi.md`, `quiz.yaml`
  - `examples/01_order_assistant.{py,out,en.md,vi.md}`
  - `examples/02_safe_dispatch.{py,out,en.md,vi.md}`
  - `examples/03_refund_guard.{py,out,en.md,vi.md}`
  - `exercises/ex01-tool-schema/{exercise.yaml,prompt.en.md,prompt.vi.md,starter.py,solution.py,test_exercise.py}`
  - `exercises/ex02-run-tools/{exercise.yaml,prompt.en.md,prompt.vi.md,starter.py,solution.py,test_exercise.py}`
  - `exercises/ex02-run-tools/alternatives/01_dispatch_helper.{py,en.md,vi.md}`
- Cập nhật `curriculum/glossary.yaml` (chỉ thêm dòng mới, không xóa/sửa dòng cũ).
- Tạo báo cáo `tasks/m4-p7-06-tool-use.report.md`.
- Lưu ý phụ: lệnh `uv run python tools/build_content.py` sinh output vào `apps/web/src/generated` (thư mục ignored trong git, không hiện trong `git status`).

## 3. Quirk của `pyai_llm` và dạng message `_validate_messages` chấp nhận

Qua đọc `packages/pyai_llm/pyai_llm.py` và chạy thử trực tiếp:
- **Dạng message `_validate_messages` chấp nhận:**
  - Mỗi phần tử trong `messages` phải là `dict` có `"role"` thuộc `{"system", "user", "assistant", "tool"}` và bắt buộc có khóa `"content"`.
  - `"content"` phải là `str`, trừ duy nhất trường hợp `role == "assistant"` và `bool(msg.get("tool_calls"))` là `True` thì `"content"` được phép là `None`.
  - Nếu `role == "assistant"` nhưng `tool_calls` rỗng/vắng mặt mà `content=None`, hoặc nếu `role == "tool"` mà `content` là `dict` (chưa `json.dumps()`), hàm raise `ValueError: message at index ... must have string 'content'`.
- **Quirk quan sát được:**
  1. `_validate_messages` **không** kiểm tra sự tồn tại của message `assistant` có `tool_calls` đứng trước message `tool`, cũng **không** kiểm tra `tool_call_id`. Khi gửi `[user, {"role": "tool", "tool_call_id": "call_1", "content": "31C and sunny"}]` (thiếu message `assistant`), `FakeLLM` vẫn trả lời `"Based on the tool result: 31C and sunny"` thay vì báo lỗi. Lỗi thường gặp #1 trong bài đã ghi nhận trung thực hành vi này và nhấn mạnh API LLM thật sẽ từ chối lịch sử thiếu `assistant`.
  2. `_normalize_words()` giữ lại cả stopword ≥ 3 ký tự (`"the"`, `"for"`, `"what"`, `"and"`), và `FakeLLM.chat()` chọn tool chỉ cần `>= 1` từ trùng. Do đó description chứa nhiều từ phổ biến có thể đánh bại description ngắn gọn hơn của tool đúng (đã minh họa ở §2).
  3. `_extract_schema_values()` điền placeholder rỗng (`""` cho `string`, `0` cho `integer`, `0.0` cho `number`, `False` cho `boolean`) cho các tham số không trích được (kể cả tham số tùy chọn như `unit=''`). Code `dispatch()` trong bài và bài tập xử lý bằng cách bỏ `""`/`None` ở tham số tùy chọn trước khi gọi `func(**clean)`.
  4. `ToolCall.id` tăng dần theo instance (`call_1`, `call_2`, …), nên các ví dụ và hàm `ask()` đều khởi tạo `FakeLLM()` mới để giữ output tất định.

## 4. Link `further_reading` đã mở thử

Kiểm tra HTTP GET từ Python `urllib.request`:
- `https://developers.openai.com/api/docs/guides/function-calling` → **HTTP 200** (URL `https://platform.openai.com/docs/guides/function-calling` redirect tới URL này và trả 200).
- `https://json-schema.org/learn/getting-started-step-by-step` → **HTTP 200**.

## 5. Kết quả lệnh kiểm tra

- `uv run python tools/validate.py --path curriculum/phase-07-llm/p7-06-tool-use`:
  `OK: 0 error(s), 0 warning(s). Checked 1 lessons, 7 markdown pairs, 3 examples, 2 exercises, 1 alternatives, 16 questions.`
- `uv run python tools/validate.py --fast` (toàn curriculum, kiểm luôn `glossary.yaml`):
  `OK: 0 error(s), 0 warning(s). Checked 45 lessons, 343 markdown pairs, 133 examples, 90 exercises, 75 alternatives, 878 questions, 9 exams, 1 portfolio, 1 glossary, 1 interview.`
- `uv run python -m pytest curriculum/phase-07-llm`:
  `94 passed in 0.21s` (exit code 0).
- Browser runner (`tools/pyrunner/runner.py`):
  - `ex01-tool-schema`: `starter` pass **0/6**, `solution` pass **6/6**.
  - `ex02-run-tools`: `starter` pass **0/8**, `solution` pass **8/8**, `01_dispatch_helper.py` pass **8/8**.
- `uv run ruff check curriculum/phase-07-llm`:
  `All checks passed!` (exit code 0).
- Chạy tất cả khối Python trong `lesson.en.md` (10 khối), `lesson.vi.md` (10 khối), 3 file `examples/*.py` và toàn bộ code quiz (`output`, `fill`, `parsons`) với `python -W error -I`:
  tất cả exit code 0, stderr rỗng.
- Kiểm tra `grep` (quét regex `input\(|time\.sleep|requests\.|urllib|open\(|eval\(|exec\(|subprocess|os\.system` trên mọi file trong `curriculum/phase-07-llm/p7-06-tool-use`):
  `matches: 0` (chỉ nhắc tới `eval` dạng chữ thường trong prose callout `[!WARNING]`).
- Script cân bằng độ dài MCQ:
  `mcqs: 7 sole_longest: {'en': 0, 'vi': 0} violations: 0`.
- `git diff --numstat curriculum/glossary.yaml`:
  `56	0	curriculum/glossary.yaml` (56 dòng thêm, 0 dòng xóa).
- `uv run python tools/build_content.py`:
  `Built 45 lessons, 9 exams, 270 flashcards, 723 questions -> apps\web\src\generated`.

## 6. Điều còn chưa chắc

- Chưa chạy `pnpm --filter web build` và chưa mở dev server / trình duyệt Pyodide thật theo đúng ràng buộc không build web và không chạy server, nên hiển thị giao diện web (Mermaid render, nút Visualize trong browser) chỉ mới được xác minh gián tiếp qua `tools/validate.py`, `tools/pyrunner/tracer.py`, `tools/pyrunner/runner.py` và `tools/build_content.py`.
- Vì môi trường offline không gọi API LLM thật, hành vi API thật từ chối orphan `tool` message chỉ được đối chiếu theo spec và tài liệu OpenAI Function Calling chứ chưa bắn request thật.

## 7. Vòng 2

Đã sửa đúng các điểm trong `## Feedback vòng 2` ở [lesson.en.md](file:///D:/Proj/python-ai-platform/curriculum/phase-07-llm/p7-06-tool-use/lesson.en.md) và [lesson.vi.md](file:///D:/Proj/python-ai-platform/curriculum/phase-07-llm/p7-06-tool-use/lesson.vi.md) (mục §2, không đổi code hay output):

- **(a)** Thêm callout `> [!NOTE]` ngay sau phần giải thích khối so sánh `vague_tools`/`clear_tools` ở cùng vị trí trong cả `lesson.en.md` và `lesson.vi.md`, giải thích rằng bài dùng `description` kiểu từ khóa để khớp cơ chế đếm từ chung của `FakeLLM`, còn với LLM thật cần viết **một câu rõ ràng** nêu tool làm gì và khi nào dùng (ví dụ `"Get the current weather for a city."`), giữ nguyên tắc chung là cụ thể, phân biệt được các tool và không lan man.
- **(b)** Cập nhật cột `tip` / `mẹo viết` của dòng `description` trong bảng ở §2:
  - EN: `One clear sentence: what it does and when to use it; make tools easy to tell apart`
  - VI: `Một câu rõ ràng: tool làm gì và khi nào dùng; dễ phân biệt với tool khác`
- **(c)** Sửa câu ngay sau khối code ở §2 để không ngụ ý liệt kê từ khóa là cách tốt nhất, chỉ giữ ý loại bỏ từ đệm chung chung và tập trung vào phạm vi riêng của từng tool giúp sửa định tuyến ở ví dụ này.

### Kết quả kiểm tra lại sau Vòng 2

- `uv run python tools/validate.py --path curriculum/phase-07-llm/p7-06-tool-use`:
  `OK: 0 error(s), 0 warning(s). Checked 1 lessons, 7 markdown pairs, 3 examples, 2 exercises, 1 alternatives, 16 questions.`
- `uv run python -m pytest curriculum/phase-07-llm`: `94 passed in 0.22s`.
- `uv run ruff check curriculum/phase-07-llm`: `All checks passed!`.
- Quét pattern cấm (`input(|time.sleep|requests.|urllib|open(|eval(|exec(|subprocess|os.system`) trên `curriculum/phase-07-llm/p7-06-tool-use`: `matches: 0`.
- `git diff --numstat curriculum/glossary.yaml`: `56	0	curriculum/glossary.yaml`.
- `uv run python tools/build_content.py`: `Built 45 lessons, 9 exams, 270 flashcards, 723 questions -> apps\web\src\generated`.
