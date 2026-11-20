# Báo cáo: m4-p7-01-llm-api

## 1. Đã làm gì

- Tạo bài học mới `p7-01-llm-api` ("Calling an LLM API" / "Gọi API LLM") trong `curriculum/phase-07-llm/p7-01-llm-api/` (chạy Pyodide, không đặt `runner`, không tạo `phase-test.yaml`).
- Viết `meta.yaml` đúng schema (`phase: p7`, `order: 1`, `tags: [llm]`, `prerequisites: [p2-05-typing, p3-01-pytest]`, `duration_min: 14`, `review_by: "2027-05-01"`, 2 link `further_reading` đã mở kiểm tra HTTP 200).
- Viết `lesson.en.md` và `lesson.vi.md` song ngữ EN/VI theo đúng dàn ý:
  - Opening (không heading) giới thiệu gọi LLM qua API và vai trò của `pyai_llm`.
  - §1: `FakeLLM()`, message dict `role`/`content`, các trường của `ChatResponse`, callout `[!NOTE]`.
  - §2: System message (`"pirate"` vs không có system), bảng so sánh `system` / `user` / `assistant`.
  - §3: Tính stateless, vòng lặp gửi lại `history`, Mermaid `flowchart LR` (4 node), bảng trace tăng dần số message và `prompt_tokens`, lời mời bấm **Visualize** (đã kiểm bằng `tools/pyrunner/tracer.py`: `len(steps) = 21`, `truncated = False`).
  - §4: `temperature=0.0` vs `0.8` với `seed` (`0, 3, 5`), bảng mức temperature, callout `[!TIP]`.
  - §5: `resp.usage`, `count_tokens`, sơ đồ `text` căn cột (giống hệt EN/VI), tính chi phí theo đơn giá ví dụ giả định (`$0.50` / 1M input, `$1.50` / 1M output), `max_tokens=5` và `finish_reason == "length"`.
  - §6: `FakeLLM(fail_times=2)` và `fail_times=3`, vòng `for` bắt `RateLimitError` kèm thời gian chờ backoff `0.5 * 2 ** (attempt - 1)` (không dùng `time.sleep`), Mermaid retry flow (6 node), callout `[!WARNING]`.
  - §7: Khối `bash` minh họa `.env`, `.gitignore`, heredoc `call_llm.py` dùng `os.environ["LLM_API_KEY"]` và `httpx.post("https://api.example-llm.com/v1/chat", ...)`, không in key, không gắn hãng cụ thể, callout `[!WARNING]`.
  - §8: 4 lỗi thường gặp với thông báo lỗi và output thật từ `pyai_llm`.
  - Tóm tắt / Recap 5 gạch đầu dòng.
- Tạo 3 example (`01_support_reply`, `02_chat_session`, `03_retry_with_backoff`) kèm `.out` sinh từ chạy thật và `.en.md` / `.vi.md`.
- Tạo 2 bài tập:
  - `ex01-build-messages` (`kind: fill`): điền chỗ trống trong `build_messages(system, history, user)`, 8 test case (kể cả `parametrize`), starter fail 8/8 (0 pass), solution pass 8/8.
  - `ex02-reliable-call` (`kind: code`): `ask_with_retry` và `estimate_cost`, 7 test case (có fake spy đếm số lần gọi khi `ValueError`, kiểm `None`, kiểu trả về, làm tròn 6 chữ số), `alternatives/01_while_loop.py` + `.en.md`/`.vi.md`, starter fail 7/7 (0 pass), solution và alternative pass 7/7.
  - Hint 3 tầng của cả 2 bài đúng quy tắc mới (hint 2 chỉ bằng lời, hint 3 chỉ để một `...` ở dòng cốt lõi).
- Tạo `quiz.yaml` với 16 câu (7 `mcq`, 3 `output`, 3 `fill`, 3 `parsons`; 5 dễ, 8 vừa, 3 khó) và 6 flashcard.
- Cập nhật `curriculum/glossary.yaml`: chỉ thêm thuật ngữ `system message` vì 7 thuật ngữ còn lại (`LLM`, `prompt`, `token`, `temperature`, `rate limit`, `API key`, `context window`) đã có sẵn trong file.

## 2. File đã sửa / tạo

- Sửa:
  - `curriculum/glossary.yaml` (thêm mục `system message`)
- Tạo mới:
  - `curriculum/phase-07-llm/p7-01-llm-api/meta.yaml`
  - `curriculum/phase-07-llm/p7-01-llm-api/lesson.en.md`
  - `curriculum/phase-07-llm/p7-01-llm-api/lesson.vi.md`
  - `curriculum/phase-07-llm/p7-01-llm-api/quiz.yaml`
  - `curriculum/phase-07-llm/p7-01-llm-api/examples/01_support_reply.py`
  - `curriculum/phase-07-llm/p7-01-llm-api/examples/01_support_reply.out`
  - `curriculum/phase-07-llm/p7-01-llm-api/examples/01_support_reply.en.md`
  - `curriculum/phase-07-llm/p7-01-llm-api/examples/01_support_reply.vi.md`
  - `curriculum/phase-07-llm/p7-01-llm-api/examples/02_chat_session.py`
  - `curriculum/phase-07-llm/p7-01-llm-api/examples/02_chat_session.out`
  - `curriculum/phase-07-llm/p7-01-llm-api/examples/02_chat_session.en.md`
  - `curriculum/phase-07-llm/p7-01-llm-api/examples/02_chat_session.vi.md`
  - `curriculum/phase-07-llm/p7-01-llm-api/examples/03_retry_with_backoff.py`
  - `curriculum/phase-07-llm/p7-01-llm-api/examples/03_retry_with_backoff.out`
  - `curriculum/phase-07-llm/p7-01-llm-api/examples/03_retry_with_backoff.en.md`
  - `curriculum/phase-07-llm/p7-01-llm-api/examples/03_retry_with_backoff.vi.md`
  - `curriculum/phase-07-llm/p7-01-llm-api/exercises/ex01-build-messages/exercise.yaml`
  - `curriculum/phase-07-llm/p7-01-llm-api/exercises/ex01-build-messages/prompt.en.md`
  - `curriculum/phase-07-llm/p7-01-llm-api/exercises/ex01-build-messages/prompt.vi.md`
  - `curriculum/phase-07-llm/p7-01-llm-api/exercises/ex01-build-messages/starter.py`
  - `curriculum/phase-07-llm/p7-01-llm-api/exercises/ex01-build-messages/solution.py`
  - `curriculum/phase-07-llm/p7-01-llm-api/exercises/ex01-build-messages/test_exercise.py`
  - `curriculum/phase-07-llm/p7-01-llm-api/exercises/ex02-reliable-call/exercise.yaml`
  - `curriculum/phase-07-llm/p7-01-llm-api/exercises/ex02-reliable-call/prompt.en.md`
  - `curriculum/phase-07-llm/p7-01-llm-api/exercises/ex02-reliable-call/prompt.vi.md`
  - `curriculum/phase-07-llm/p7-01-llm-api/exercises/ex02-reliable-call/starter.py`
  - `curriculum/phase-07-llm/p7-01-llm-api/exercises/ex02-reliable-call/solution.py`
  - `curriculum/phase-07-llm/p7-01-llm-api/exercises/ex02-reliable-call/test_exercise.py`
  - `curriculum/phase-07-llm/p7-01-llm-api/exercises/ex02-reliable-call/alternatives/01_while_loop.py`
  - `curriculum/phase-07-llm/p7-01-llm-api/exercises/ex02-reliable-call/alternatives/01_while_loop.en.md`
  - `curriculum/phase-07-llm/p7-01-llm-api/exercises/ex02-reliable-call/alternatives/01_while_loop.vi.md`
  - `tasks/m4-p7-01-llm-api.report.md`

## 3. Kết quả lệnh kiểm tra

- `uv run python tools/validate.py --path curriculum/phase-07-llm/p7-01-llm-api`:
  `OK: 0 error(s), 0 warning(s). Checked 1 lessons, 7 markdown pairs, 3 examples, 2 exercises, 1 alternatives, 16 questions.` (exit 0).
- `uv run python -m pytest curriculum/phase-07-llm`:
  `15 passed in 0.03s` (exit 0).
- Kiểm riêng starter của từng bài tập (`EXERCISE_TARGET=starter`):
  - `ex01-build-messages`: 8 failed, 0 passed (`NameError: name '___' is not defined`).
  - `ex02-reliable-call`: 7 failed, 0 passed.
- `uv run ruff check curriculum/phase-07-llm`:
  `All checks passed!` (exit 0).
- Quét từ cấm (`input\(|time\.sleep|requests\.|urllib|open\(`) trong mọi `.py` thuộc `curriculum/phase-07-llm/p7-01-llm-api`: rỗng (0 kết quả).
- Kiểm script độ dài `mcq`: `violations: 0` (trong 7 câu `mcq`, chỉ 3/14 cặp `(câu, ngôn ngữ)` có đáp án đúng dài nhất tuyệt đối).
- Kiểm `python -W error` trên toàn bộ 11 khối `python` của `lesson.en.md`, 11 khối của `lesson.vi.md`, 3 file `examples/*.py`, và 9 câu code chạy được trong `quiz.yaml` (`output`, `fill`, `parsons`): exit 0, stderr rỗng.
- Kiểm schema `curriculum/glossary.yaml` với `tools/schema/glossary.schema.json`: `schema errors: 0`, `dups: []`, `total terms: 226`.
- `uv run python tools/build_content.py`:
  `Built 40 lessons, 9 exams, 240 flashcards, 643 questions -> apps\web\src\generated` (exit 0).
- `git status --short`:
  Chỉ có `M curriculum/glossary.yaml` và `?? curriculum/phase-07-llm/`, `?? tasks/` (cùng `.hallmark/` đã có từ trước trong workspace).

## 4. Kiểm tra Visualize (`tracer.py`), `further_reading`, và hành vi của `pyai_llm`

- **Khối Visualize (§3)**: kiểm tra bằng `tools/pyrunner/tracer.py` cho kết quả `steps: 21`, `truncated: False`, `error: None`. `tracer` **không** bước vào code bên trong `pyai_llm` vì hàm `tracer()` kiểm tra `if frame.f_code.co_filename != FILENAME: return None` (`FILENAME = "<main>"`).
- **Link `further_reading` đã mở kiểm tra bằng `httpx.get(..., follow_redirects=True)`**:
  - `https://huggingface.co/learn/llm-course/chapter2/4` -> HTTP 200 (`Tokenizers · Hugging Face`).
  - `https://www.python-httpx.org/quickstart/` -> HTTP 200 (`QuickStart - HTTPX`).
- **Hành vi cần lưu ý của `pyai_llm`**:
  1. `_normal_reply()` chỉ đọc tin nhắn `user` cuối cùng (`last_user`) và kiểm tra chuỗi `"pirate"` trong các tin nhắn `system`; nó không đọc nội dung các lượt `user`/`assistant` trước đó trong `messages`. Vì vậy ở §8 mục 3 ("quên gửi lại lịch sử"), nếu chỉ dùng tin nhắn `user` bình thường thì `resp.content` giữa "quên" và "nhớ" sẽ không tự khác nhau trên `FakeLLM` — bài học đã dùng ví dụ quên kèm cả `system` message `"You are a pirate."` kết hợp với việc đối chiếu `prompt_tokens` (`9` vs `53`) để thấy rõ việc mất ngữ cảnh ngay trên output thật.
  2. Khi `temperature > 0`, `_normal_reply` chỉ chọn ngẫu nhiên một trong 3 tiền tố `("", "Sure. ", "Here is what I know: ")` dựa trên `self._seed * 1000 + call_index`, nên nhiều giá trị seed liên tiếp (như `0, 1, 2`) cho cùng kết quả `"Sure. "`. Cần chọn các seed như `0, 3, 5` để minh họa 3 mở đầu khác nhau. (Không thấy lỗi cản trở bài học đến mức phải sửa `pyai_llm`.)

## 5. Điều còn chưa chắc

- Code và bài tập đã được kiểm tra bằng CPython của workspace cùng `tools/pyrunner/runner.py` và `tools/pyrunner/tracer.py`, nhưng chưa chạy trực tiếp trong runtime Pyodide wasm32 trên trình duyệt. (Tuy nhiên `pyai_llm` và toàn bộ code bài học chỉ dùng thư viện chuẩn Python 3.13.)
- Không chạy `pnpm --filter web build` theo đúng quy định của spec.
