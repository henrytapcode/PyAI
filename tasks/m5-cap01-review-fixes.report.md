# Báo cáo M5 bước 2f: Sửa capstone 1 theo review Opus

## 1. Đã làm gì (19 điểm review)

| # | Điểm review | File đã sửa | Đã sửa gì |
|---|---|---|---|
| 1 | ex03 bộ đếm ID không cần `nonlocal` | `exercises/ex03-session-service/solution.py`, `starter.py`, `exercise.yaml`, `prompt.en.md`, `prompt.vi.md` | Thay `seq = 0` + `nonlocal seq` / `counter = 0` + `nonlocal counter` bằng `state = {"next_id": 1}` (đọc/cập nhật phần tử dict). Thêm 1 câu trong Rules của `prompt.en.md` và `prompt.vi.md` giải thích dùng dict vì gán lại biến ở scope ngoài trong hàm lồng sẽ gây `UnboundLocalError`. Alternative `01_session_store_depends.py` dùng `self._counter` trong class nên không có `nonlocal`. |
| 2 | ex02 prompt Example (EN/VI) | `exercises/ex02-dialog-eval/prompt.en.md`, `prompt.vi.md` | Định nghĩa rõ lớp stub `StubBot` (`make_bot = StubBot`) ngay trong khối ví dụ với bảng `replies` khớp 100% kết quả trả về (`d1#t1` pass, `d1#t2` fail `"wrong_source"`, `d2#t1` pass), không ngụ ý dùng `ChatBot` thật. |
| 3 | ex02 hint 3 (EN/VI) | `exercises/ex02-dialog-eval/exercise.yaml` | Bỏ code hoàn chỉnh của `score_turn` (để `...` ở nhánh `exp is None` và nhánh kiểm tra `expected_facts`) và bổ sung khung vòng lặp cho `run_dialog_eval` có `...`. |
| 4 | ex03 hint 3 (EN/VI) | `exercises/ex03-session-service/exercise.yaml` | Thay `min(...)` đầy đủ bằng `victim = min(sessions, key=...)`, cho sẵn khung `require_session(sid, now)` và dùng `state = {"next_id": 1}` (không `nonlocal`), cập nhật tiêu đề hint EN/VI khớp đúng các chỗ để trống. |
| 5 | ex01 test | `exercises/ex01-chatbot/test_exercise.py` | Thêm `chat_kwargs` trong `SpyClient` và test `test_chat_called_once_with_temperature_zero_on_hit`; tách `test_long_question_and_android_prefix_are_not_rewritten` thành `test_long_standalone_and_android_prefix_are_not_rewritten` và `test_long_questions_with_followup_prefixes_are_rewritten` (gồm câu > 4 từ bắt đầu bằng `"What about "`, `"How about "`, `"And "`); thêm `test_followup_prefix_matching_is_case_insensitive` (gồm `"WHAT ABOUT ..."` và `"AND ..."` > 4 từ); ghi chú ở 2 test cũ dùng `"How much does delivery cost?"` rằng lượt 1 bị từ chối nhưng vẫn vào history. |
| 6 | Câu mẫu bị từ chối | `lesson.en.md`, `lesson.vi.md`, `exercises/ex01-chatbot/exercise.yaml`, `examples/01_follow_up_chat.en.md`, `examples/01_follow_up_chat.vi.md`, `exercises/ex03-session-service/prompt.en.md`, `exercises/ex03-session-service/prompt.vi.md` | Thay lượt 1 sang `"How much does express delivery cost?"` (trả lời `shipping.md` ở lượt 1) và câu nối tiếp `"What about free shipping?"` (ra `shipping.md` ở lượt 2) ở §1 Story 1, ex01 hint 1, ex01 "Try it", và ex03 prompt Example (dùng `"How much does express delivery cost?"`). Đã kiểm bằng `ex01/solution.py` trên `docs` (xem mục 3). |
| 7 | Lesson tự giải ex01 (§9 lỗi #2) | `lesson.en.md`, `lesson.vi.md` | Giữ code sai (`bad`) và output sai (`wrong roles: ['user', 'assistant', 'user']`), xóa đoạn code `# Fix` ghim `system` và chỉ giữ giải thích bằng lời hướng dẫn học viên tự làm ở `ex01`. Giữ nguyên cột "not implemented in lesson yet" / "phần bài học chưa làm" của §7. |
| 8 | Số dòng trong `examples/*.en.md` và `.vi.md` | `examples/01_follow_up_chat.{en,vi}.md`, `examples/02_dialog_eval.{en,vi}.md`, `examples/03_session_store.{en,vi}.md` | Đối chiếu lại từng số dòng theo file `.py` hiện tại: ex01 (`6–24`, `27–34`, `37–60`, `63–76`), ex02 (`17–32`, `44–77`, `80–81`, `83–92`, `line 81`), ex03 sau sửa mục 15 (`2–10`, `13–47`, `50–63`, `65–71`). |
| 9 | quiz q02 explanation (EN/VI) | `quiz.yaml` | Tính lại bằng `count_tokens`: `sys_msg=5`, lượt user cũ nhất=6, assistant=5, `"What about express?"`=4; tổng ban đầu `5+6+5+4=20 > 16`, bỏ lượt `6` token còn `5+5+4=14 <= 16`. Sửa cả EN và VI explanation cho khớp. |
| 10 | quiz distractor q01, q05, q08, q09, q13 | `quiz.yaml` | Thay toàn bộ các lựa chọn phi lý bằng hiểu lầm thực tế (cắt từ cuối, chỉ cắt khi tràn context window model, `retrieve` tìm trong `self.history`, `rewritten` làm sai `len(words) <= 4`/nhầm `prev_user`, dùng chung bot re-embed hoặc làm sai `turn`, gán lại `s1['history'] = []` làm sạch `s2`, v.v.). Độ dài các lựa chọn đều xấp xỉ nhau, đáp án đúng không phải lựa chọn dài nhất duy nhất ở bất kỳ câu nào (xem bảng mục 4). |
| 11 | Claim "tested end to end" | `meta.yaml`, `curriculum/syllabus.yaml`, `curriculum/portfolio.yaml` | Sửa outcome 4 (EN/VI) ở `meta.yaml` + `syllabus.yaml` và `pitch` / `cv_bullet` (EN/VI) ở `portfolio.yaml` để nêu chính xác: dịch vụ FastAPI nhận bất kỳ bot nào có `ask()`, được kiểm thử bằng bot giả (stub) qua `TestClient` + `FakeClock`, và nối với `ChatBot` khi chạy thật. |
| 12 | ex03 starter | `exercises/ex03-session-service/starter.py` | Bỏ `class MessageRequest` viết sẵn, thay bằng `# TODO` hướng dẫn học viên tự viết model Pydantic (strip whitespace, `min_length=1`, trả `422` khi rỗng). Starter import bình thường, 0/16 test pass. |
| 13 | ex02 test | `exercises/ex02-dialog-eval/test_exercise.py` | Thay case thứ 4 trùng `wrong_source` trong `test_score_turn_failure_reasons_and_priority` bằng `{"answer": REFUSAL, "sources": ["shipping.md"]}` với `expected_source=None` → `"no_refusal"`. |
| 14 | quiz q11 | `quiz.yaml` | Bỏ `not ` đứng trước `___` thành `gate_ok = ___ and pass_rate >= ___`, chấp nhận list đáp án tương đương: `["not broken", "len(broken) == 0", "broken == []"]` cho ô 1 và `["min_pass_rate", "0.8"]` cho ô 2. |
| 15 | `examples/03_session_store.py` | `examples/03_session_store.py`, `examples/03_session_store.{en,vi}.md` | Thêm nhánh `if sid in self.sessions:` cập nhật `last_seen` và `return` để `create()` với `sid` đang hoạt động không ghi đè `history`. Output `.out` giữ nguyên (đã chạy đối chiếu khớp 100%). |
| 16 | Lesson §4 (EN/VI) | `lesson.en.md`, `lesson.vi.md` | Thêm 1 câu giải thích giới hạn quy tắc `<= 4` từ (ví dụ `"Thanks"` cũng bị ghép câu hỏi trước) và `ex01` chấp nhận đánh đổi này để giữ tất định không gọi LLM. |
| 17 | Alternative ex01 `.en.md`/`.vi.md` | `exercises/ex01-chatbot/alternatives/01_functional_deque.en.md`, `.vi.md`, `.py` | Sửa mô tả (và docstring ở `.py`) để nêu đúng việc chuyển `list`↔`deque` mỗi lượt vẫn tốn `O(N)` sao chép, không khẳng định toàn thao tác là `O(1)`. |
| 18 | Rubric §8 (EN/VI) | `lesson.en.md`, `lesson.vi.md` | Ghi rõ "100% grounded" và "zero wasted `chat()` calls" được đo bằng bộ unit test của `ex01` (`SpyClient` + kiểm tra `sources` và `[n]`), bên cạnh kiểm tra trên golden dialogs ở `ex02`. |
| 19 | Sửa câu chữ VI | `exercises/ex03-session-service/prompt.vi.md`, `exercises/ex01-chatbot/prompt.vi.md`, `exercises/ex01-chatbot/exercise.yaml`, `lesson.vi.md` | Sửa `"vẫn còn đủ max_sessions"` → `"nếu sau khi dọn mà số phiên vẫn đạt max_sessions"`; `"từ đầu (chữ thường)"` → `"từ đầu tiên (viết thường)"` (ở cả prompt và hint 2); `"vừa khít budget"` → `"nằm trong budget"`; gloss `"**tất định** (deterministic)"` ở lần xuất hiện đầu tiên trong `lesson.vi.md` (§2 bảng thành phần). |

---

## 2. Danh sách file đã sửa

- `curriculum/capstones/cap-01-rag-chatbot/meta.yaml`
- `curriculum/capstones/cap-01-rag-chatbot/lesson.en.md`
- `curriculum/capstones/cap-01-rag-chatbot/lesson.vi.md`
- `curriculum/capstones/cap-01-rag-chatbot/quiz.yaml`
- `curriculum/capstones/cap-01-rag-chatbot/examples/01_follow_up_chat.en.md`
- `curriculum/capstones/cap-01-rag-chatbot/examples/01_follow_up_chat.vi.md`
- `curriculum/capstones/cap-01-rag-chatbot/examples/02_dialog_eval.en.md`
- `curriculum/capstones/cap-01-rag-chatbot/examples/02_dialog_eval.vi.md`
- `curriculum/capstones/cap-01-rag-chatbot/examples/03_session_store.py`
- `curriculum/capstones/cap-01-rag-chatbot/examples/03_session_store.en.md`
- `curriculum/capstones/cap-01-rag-chatbot/examples/03_session_store.vi.md`
- `curriculum/capstones/cap-01-rag-chatbot/exercises/ex01-chatbot/exercise.yaml`
- `curriculum/capstones/cap-01-rag-chatbot/exercises/ex01-chatbot/prompt.vi.md`
- `curriculum/capstones/cap-01-rag-chatbot/exercises/ex01-chatbot/test_exercise.py`
- `curriculum/capstones/cap-01-rag-chatbot/exercises/ex01-chatbot/alternatives/01_functional_deque.en.md`
- `curriculum/capstones/cap-01-rag-chatbot/exercises/ex01-chatbot/alternatives/01_functional_deque.vi.md`
- `curriculum/capstones/cap-01-rag-chatbot/exercises/ex01-chatbot/alternatives/01_functional_deque.py`
- `curriculum/capstones/cap-01-rag-chatbot/exercises/ex02-dialog-eval/exercise.yaml`
- `curriculum/capstones/cap-01-rag-chatbot/exercises/ex02-dialog-eval/prompt.en.md`
- `curriculum/capstones/cap-01-rag-chatbot/exercises/ex02-dialog-eval/prompt.vi.md`
- `curriculum/capstones/cap-01-rag-chatbot/exercises/ex02-dialog-eval/test_exercise.py`
- `curriculum/capstones/cap-01-rag-chatbot/exercises/ex03-session-service/exercise.yaml`
- `curriculum/capstones/cap-01-rag-chatbot/exercises/ex03-session-service/prompt.en.md`
- `curriculum/capstones/cap-01-rag-chatbot/exercises/ex03-session-service/prompt.vi.md`
- `curriculum/capstones/cap-01-rag-chatbot/exercises/ex03-session-service/solution.py`
- `curriculum/capstones/cap-01-rag-chatbot/exercises/ex03-session-service/starter.py`
- `curriculum/syllabus.yaml` (chỉ outcomes của `cap-01-rag-chatbot`)
- `curriculum/portfolio.yaml` (chỉ `pitch` và `cv_bullet` của `cap-rag-chatbot`)
- `tasks/m5-cap01-review-fixes.report.md` (file báo cáo này)

---

## 3. Kiểm chứng điểm 6 bằng `ex01/solution.py` trên `docs` trong lesson

Đoạn chạy:

```python
import sys
sys.path.insert(0, "curriculum/capstones/cap-01-rag-chatbot/exercises/ex01-chatbot")
from solution import ChatBot
from pyai_llm import FakeLLM

# docs gồm 8 trang FAQ trong lesson §1
bot = ChatBot(docs, FakeLLM(embed_dim=256))
for q in ["How much does express delivery cost?", "What about free shipping?"]:
    print(q, "->", bot.ask(q))
```

Output thực tế:

```text
How much does express delivery cost? -> {'answer': 'Express delivery arrives next day for 12 dollars. [1]', 'sources': ['shipping.md'], 'rewritten': 'How much does express delivery cost?'}
What about free shipping? -> {'answer': 'Free shipping applies on orders over 50 dollars. [1]', 'sources': ['shipping.md'], 'rewritten': 'How much does express delivery cost? What about free shipping?'}
```

---

## 4. Bảng độ dài lựa chọn MCQ (`quiz.yaml`)

Mọi câu MCQ đều có độ dài các lựa chọn xấp xỉ nhau, `ratio = len(đáp án đúng) / max(len(distractor)) <= 1.00`, không câu nào đáp án đúng dài nhất duy nhất:

| ID | Lang | Ans | Độ dài 4 lựa chọn | `ans / max_other` | Đáp án đúng dài nhất duy nhất? |
|---|---|---|---|---|---|
| `cap-01-q01` | en | 2 | `[57, 62, 61, 57]` | `0.98` | False |
| `cap-01-q01` | vi | 2 | `[58, 60, 58, 60]` | `0.97` | False |
| `cap-01-q04` | en | 1 | `[68, 69, 64, 69]` | `1.00` | False |
| `cap-01-q04` | vi | 1 | `[67, 67, 62, 61]` | `1.00` | False |
| `cap-01-q05` | en | 0 | `[64, 63, 61, 64]` | `1.00` | False |
| `cap-01-q05` | vi | 0 | `[69, 62, 70, 61]` | `0.99` | False |
| `cap-01-q08` | en | 3 | `[64, 63, 63, 63]` | `0.98` | False |
| `cap-01-q08` | vi | 3 | `[62, 69, 65, 68]` | `0.99` | False |
| `cap-01-q09` | en | 1 | `[66, 63, 63, 66]` | `0.95` | False |
| `cap-01-q09` | vi | 1 | `[68, 68, 62, 61]` | `1.00` | False |
| `cap-01-q10` | en | 2 | `[57, 64, 63, 67]` | `0.94` | False |
| `cap-01-q10` | vi | 2 | `[67, 68, 68, 67]` | `1.00` | False |
| `cap-01-q13` | en | 2 | `[67, 65, 64, 63]` | `0.96` | False |
| `cap-01-q13` | vi | 2 | `[64, 65, 60, 60]` | `0.92` | False |
| `cap-01-q16` | en | 0 | `[68, 69, 63, 60]` | `0.99` | False |
| `cap-01-q16` | vi | 0 | `[65, 63, 68, 67]` | `0.96` | False |

---

## 5. Kết quả các lệnh kiểm tra (chạy sau lần sửa cuối)

1. `uv run python tools/validate.py --path curriculum/capstones/cap-01-rag-chatbot`:
   `OK: 0 error(s), 0 warning(s). Checked 1 lessons, 10 markdown pairs, 3 examples, 20 lesson output blocks, 3 alternatives, 3 exercises, 16 questions.`
2. `uv run python -m pytest curriculum/capstones/cap-01-rag-chatbot -q`:
   `45 passed in 0.45s` (`ex01`: 16 passed, `ex02`: 13 passed, `ex03`: 16 passed).
3. Starter tests (`EXERCISE_TARGET=starter`):
   - `ex01-chatbot`: 16 failed, 0 passed (`FFFFFFFFFFFFFFFF`)
   - `ex02-dialog-eval`: 13 failed, 0 passed (`FFFFFFFFFFFFF`)
   - `ex03-session-service`: 16 failed, 0 passed (`FFFFFFFFFFFFFFFF`)
4. `uv run ruff check curriculum/capstones/cap-01-rag-chatbot`:
   `All checks passed!`
5. Kiểm tra `nonlocal` trong `curriculum/capstones/cap-01-rag-chatbot`:
   `no nonlocal` (0 dòng).
6. Kiểm tra `(^|[ .:("'])(Ta|ta|Chúng ta|chúng ta) ` (trừ `"người ta"`) trong `*.vi.md`:
   `no Ta/chung ta` (0 dòng).
7. `examples/03_session_store.py` đối chiếu với `examples/03_session_store.out`:
   Khớp 100% (`True`).
8. `uv run python tools/validate.py --fast`:
   `OK: 0 error(s), 33 warning(s). Checked 55 lessons, 419 markdown pairs, 163 examples, 111 exercises, 90 alternatives, 1073 questions, 594 lesson output blocks, 11 exams, 1 portfolio, 1 glossary, 1 interview.`
   (33 cảnh báo đều là cảnh báo sẵn có ở các phase 01–08; `cap-01-rag-chatbot` không có cảnh báo nào).
9. Kiểm tra mutant trong thư mục tạm:
   - `ex01` bỏ `temperature=0.0` trong `client.chat(...)`: `1 failed, 15 passed` (bị bắt bởi `test_chat_called_once_with_temperature_zero_on_hit`).
   - `ex01` khớp tiền tố phân biệt hoa thường: `2 failed, 14 passed` (bị bắt bởi `test_followup_prefix_matching_is_case_insensitive`).
   - `ex03` dùng chung 1 `bot = make_bot()` cho mọi session: `2 failed, 14 passed`.
   - `ex03` dùng `>` thay `>=` cho `session_ttl`: `2 failed, 14 passed`.

---

## 6. Điều còn chưa chắc

- Trong `ex01-chatbot/test_exercise.py`, hai test cũ `test_followup_what_about_express_rewrites_and_returns_shipping` và `test_consecutive_followups_rewrite_from_original_user_question` vẫn giữ câu hỏi lượt 1 là `"How much does delivery cost?"` (bị `ChatBot` thật từ chối ở lượt 1) vì tổ hợp `"How much does delivery cost?" + "What about express?"` giúp `FakeLLM` ở lượt 2 truy xuất và trả lời `"Express delivery arrives next day for 12 dollars. [1]"`; đã thêm chú thích rõ ngay trong test rằng lượt 1 bị từ chối nhưng vẫn vào `history`. Nếu reviewer muốn test lượt 1 cũng không bị từ chối, có thể đổi lượt 1 sang `"How much does express delivery cost?"` và lượt 2 sang `"What about free shipping?"`.
- Khi chạy `uv run python tools/validate.py --fast`, `pyrunner/tracer.py` có in 1 ngoại lệ `_TooManySteps` được bỏ qua (`Exception ignored`) ở một bài thuộc repo ngoài phạm vi capstone này, nhưng `validate.py --fast` vẫn kết thúc với `0 error(s)`.
