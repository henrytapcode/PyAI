# Báo cáo thực hiện `m4-p7-review-fixes-b`

## 1. Đã làm gì

- **B1 (`p7-06` §6 guard chống spoofing):**
  - Cập nhật [lesson.en.md](file:///D:/Proj/python-ai-platform/curriculum/phase-07-llm/p7-06-tool-use/lesson.en.md) và [lesson.vi.md](file:///D:/Proj/python-ai-platform/curriculum/phase-07-llm/p7-06-tool-use/lesson.vi.md) §6: dùng hằng số `MAX_AUTO_REFUND = 100.0`, tách `issue_refund(order_id, amount)` khỏi trạng thái xác nhận, và đổi `run_guarded(tool_name, args, user_confirmed: bool)` để nhận `user_confirmed` từ code ứng dụng, chỉ đọc hai khóa `order_id` và `amount` nhằm bỏ qua các khóa giả mạo (`{"confirmed": True, "max_amount": 1000.0}`).
  - Bổ sung hai ca `spoofed` và `spoofed cap` vào ví dụ kèm `# output` thực chạy với `-W error`, đồng thời cập nhật câu lưu ý bên dưới code block.
- **M1 (`p7-10` `ex02` kiểm tra lịch sử message):**
  - Thêm `_SpyClient` và test `test_appends_assistant_and_tool_messages_to_history` trong [test_exercise.py](file:///D:/Proj/python-ai-platform/curriculum/phase-07-llm/p7-10-mini-project-agent/exercises/ex02-run-scenarios/test_exercise.py) để xác nhận ở lượt gọi `chat()` thứ 2 có `messages[1]["role"] == "assistant"` (kèm `tool_calls`) và `messages[2]["role"] == "tool"` (kèm `tool_call_id` khớp và `content` đúng).
- **M2 (`p7-10` tách `needs_approval` và `rejected`):**
  - Tách hai trạng thái dừng `needs_approval` (khi `approve is None`) và `rejected` (khi `approve(name, args)` trả về `False`) đồng bộ trên [lesson.en.md](file:///D:/Proj/python-ai-platform/curriculum/phase-07-llm/p7-10-mini-project-agent/lesson.en.md), [lesson.vi.md](file:///D:/Proj/python-ai-platform/curriculum/phase-07-llm/p7-10-mini-project-agent/lesson.vi.md) (§1 bảng kế hoạch, §5 `run_with_gate`, §6 `run_agent_v1`/`run_agent_v2`/`SCENARIOS`/bảng kết quả, §7 `v1_results`/`v2_results`, §8 lỗi 1 và Recap), hai ví dụ [02_agent_with_approval.py](file:///D:/Proj/python-ai-platform/curriculum/phase-07-llm/p7-10-mini-project-agent/examples/02_agent_with_approval.py) và [03_scenario_suite.py](file:///D:/Proj/python-ai-platform/curriculum/phase-07-llm/p7-10-mini-project-agent/examples/03_scenario_suite.py) (kèm `.out`, `.en.md`, `.vi.md`), flashcard `p7-10-f03` trong [quiz.yaml](file:///D:/Proj/python-ai-platform/curriculum/phase-07-llm/p7-10-mini-project-agent/quiz.yaml), và toàn bộ `p7-10` `ex02-run-scenarios` (`prompt`, `solution.py`, `alternatives/01_step_runner_class.py`, `test_exercise.py`, `exercise.yaml`).
  - Ghi chú phạm vi: mục ví dụ của term `approval gate` trong `curriculum/glossary.yaml` vẫn giữ nguyên vì spec quy định chỉ được phép append vào cuối `glossary.yaml`.
- **M3 (`p7-08` `ex01` và `p7-06` `ex01`):**
  - `p7-08` `ex01`: chuyển `hit_rate(results, k)` thành `hit_rates(results: list[dict], ks: list[int]) -> dict[int, float]` làm tròn 3 chữ số thập phân, ném `ValueError` khi có `k <= 0` trong `ks` (gộp **m2**), giữ `kind: fill` với chỗ trống `___` chỉ đặt ở phần logic mới (`rates`, kiểm tra `k <= 0`, làm tròn `round`), bổ sung test cho nhiều mức `k`, `ks=[]`, `k=0`, `k=-1`.
  - `p7-06` `ex01`: chuyển các chỗ trống `___` ra khỏi các dòng dựng `properties`/`required` trùng §2 sang hai bước validate (`ALLOWED_TYPES`, `req not in params`) và khử trùng lặp giữ nguyên thứ tự `deduped_required` (`list(dict.fromkeys(required))`), kèm test `test_deduplicates_required_preserving_order`.
- **M4 (chuẩn hóa hints 3 tầng ở các bài tập):**
  - `p7-06 ex01`, `p7-07 ex01`, `p7-08 ex01` (`fill`): Hint 3 chỉ gợi ý chỗ trống khó nhất (`deduped_required`, biểu thức so sánh trả về, `rates[k]`) và giữ nguyên các chỗ trống còn lại dưới dạng `___`.
  - `p7-06 ex02`, `p7-07 ex02`, `p7-08 ex02`: thu gọn Hint 3 về khung chỉ còn 1–2 `...` trên phần logic chính (không lộ `facts`/`faithful` hay thứ tự nhánh lặp).
  - `p7-09 ex01`: bỏ biểu thức code `k <= 0` khỏi Hint 2 EN/VI.
  - `p7-10 ex01`: bỏ `schema["name"]` và `json.dumps()` khỏi Hint 2 EN/VI; thu gọn Hint 3 từ 4 `...` xuống 2 `...` (`schemas` và `call`).
  - `p7-10 ex02`: bỏ `make_client(list(scenario["script"]))`, `client.chat(messages, tools=toolbox.schemas())` và `toolbox.call(tc.name, dict(tc.arguments))` khỏi Hint 2 EN/VI và cập nhật mô tả `needs_approval`/`rejected`.
- **M5 (`copy.deepcopy` ở `p7-10` §3 và glossary):**
  - Bổ sung giải thích shallow copy vs `copy.deepcopy` kèm khối code minh họa (đã chạy `-W error`) ở cuối §3 trong `p7-10` `lesson.en.md` và `lesson.vi.md`.
  - Append term `deep copy` vào cuối [glossary.yaml](file:///D:/Proj/python-ai-platform/curriculum/glossary.yaml) (không sửa hay xóa dòng cũ nào).
- **m1–m11:**
  - **m1:** thêm `assert json.loads(res["trace"][0]["observation"])["note"] == "ok"` trong `p7-07` `ex02` `test_exercise.py`.
  - **m2:** gộp vào **M3** (`k <= 0` raise `ValueError`).
  - **m3:** thêm test `ValueError` cho `size <= 0`, `overlap < 0`, `overlap >= size` và `SpyClient` kiểm tra `embed_calls == 0` khi không có chunk nào trong `p7-09` `ex01` `test_exercise.py`.
  - **m4:** giải thích lý do kiểm tra `budget` ngay sau `client.chat(...)` (và phương án kiểm tra `final` trước) ở `p7-07` §4 và `p7-10` §4.
  - **m5:** thêm `> [!NOTE]` về API thực tế có thể trả nhiều `tool_calls` trong một lượt so với `resp.tool_calls[0]` cho gọn (nhắc lại `p7-06` `ex02`) ở `p7-07` §2 và `p7-10` §4.
  - **m6:** sửa mô tả `FakeLLM` ở `p7-06` dòng 36 (điền mọi trường `string` kể cả bắt buộc và tùy chọn bằng giá trị trích từ prompt hoặc `''`) và dòng 59 (khớp từ `>= 3` ký tự trên cả `name` và `description`).
  - **m7:** sửa giải thích `user_confirmed` và ghi chú "Try it yourself" ở [03_refund_guard.en.md](file:///D:/Proj/python-ai-platform/curriculum/phase-07-llm/p7-06-tool-use/examples/03_refund_guard.en.md) và [03_refund_guard.vi.md](file:///D:/Proj/python-ai-platform/curriculum/phase-07-llm/p7-06-tool-use/examples/03_refund_guard.vi.md) (ghi rõ `ACTION_LOG` ghi `blocked: user confirmation required` trong khi câu trả lời scripted giữ nguyên).
  - **m8:** nối tên chỉ số giữa `p7-08` và `p7-09` trong `p7-09` §1 (`grounded` = `faithful` + trích dẫn `[n]` hợp lệ như `p7-08 ex02`; `idk` = `refusals`), và thống nhất tiêu đề cột `'grounded'` ở `p7-09` §6.
  - **m9:** giải thích regex lookbehind `r"(?<=[.!?])\s+"` ở `p7-09` §3 và tách biểu thức điều kiện `ans = (... if top_hits else ...)` thành `if top_hits:` / `else:` ở §6 và §7.
  - **m10:** bổ sung lưu ý ở `p7-08` §5 rằng tập eval dùng để chọn `k` là `dev set` và cần chấm lại lựa chọn cuối trên tập test giữ kín như `p7-09`.
  - **m11:** sửa "(5) in câu trả lời cuối" thành "(5) trả về câu trả lời cuối" ở `p7-06` `lesson.vi.md` §3.

## 2. File đã sửa

- `curriculum/glossary.yaml` (append-only thêm `deep copy`)
- `curriculum/phase-07-llm/p7-06-tool-use/lesson.en.md`
- `curriculum/phase-07-llm/p7-06-tool-use/lesson.vi.md`
- `curriculum/phase-07-llm/p7-06-tool-use/examples/03_refund_guard.en.md`
- `curriculum/phase-07-llm/p7-06-tool-use/examples/03_refund_guard.vi.md`
- `curriculum/phase-07-llm/p7-06-tool-use/exercises/ex01-tool-schema/exercise.yaml`
- `curriculum/phase-07-llm/p7-06-tool-use/exercises/ex01-tool-schema/prompt.en.md`
- `curriculum/phase-07-llm/p7-06-tool-use/exercises/ex01-tool-schema/prompt.vi.md`
- `curriculum/phase-07-llm/p7-06-tool-use/exercises/ex01-tool-schema/solution.py`
- `curriculum/phase-07-llm/p7-06-tool-use/exercises/ex01-tool-schema/starter.py`
- `curriculum/phase-07-llm/p7-06-tool-use/exercises/ex01-tool-schema/test_exercise.py`
- `curriculum/phase-07-llm/p7-06-tool-use/exercises/ex02-run-tools/exercise.yaml`
- `curriculum/phase-07-llm/p7-07-agents/lesson.en.md`
- `curriculum/phase-07-llm/p7-07-agents/lesson.vi.md`
- `curriculum/phase-07-llm/p7-07-agents/exercises/ex01-detect-repeat/exercise.yaml`
- `curriculum/phase-07-llm/p7-07-agents/exercises/ex02-run-agent/exercise.yaml`
- `curriculum/phase-07-llm/p7-07-agents/exercises/ex02-run-agent/test_exercise.py`
- `curriculum/phase-07-llm/p7-08-evals/lesson.en.md`
- `curriculum/phase-07-llm/p7-08-evals/lesson.vi.md`
- `curriculum/phase-07-llm/p7-08-evals/exercises/ex01-hit-rate/exercise.yaml`
- `curriculum/phase-07-llm/p7-08-evals/exercises/ex01-hit-rate/prompt.en.md`
- `curriculum/phase-07-llm/p7-08-evals/exercises/ex01-hit-rate/prompt.vi.md`
- `curriculum/phase-07-llm/p7-08-evals/exercises/ex01-hit-rate/solution.py`
- `curriculum/phase-07-llm/p7-08-evals/exercises/ex01-hit-rate/starter.py`
- `curriculum/phase-07-llm/p7-08-evals/exercises/ex01-hit-rate/test_exercise.py`
- `curriculum/phase-07-llm/p7-08-evals/exercises/ex02-score-answer/exercise.yaml`
- `curriculum/phase-07-llm/p7-09-mini-project-rag/lesson.en.md`
- `curriculum/phase-07-llm/p7-09-mini-project-rag/lesson.vi.md`
- `curriculum/phase-07-llm/p7-09-mini-project-rag/exercises/ex01-ingest-retrieve/exercise.yaml`
- `curriculum/phase-07-llm/p7-09-mini-project-rag/exercises/ex01-ingest-retrieve/test_exercise.py`
- `curriculum/phase-07-llm/p7-10-mini-project-agent/lesson.en.md`
- `curriculum/phase-07-llm/p7-10-mini-project-agent/lesson.vi.md`
- `curriculum/phase-07-llm/p7-10-mini-project-agent/quiz.yaml`
- `curriculum/phase-07-llm/p7-10-mini-project-agent/examples/02_agent_with_approval.py`
- `curriculum/phase-07-llm/p7-10-mini-project-agent/examples/02_agent_with_approval.out`
- `curriculum/phase-07-llm/p7-10-mini-project-agent/examples/02_agent_with_approval.en.md`
- `curriculum/phase-07-llm/p7-10-mini-project-agent/examples/02_agent_with_approval.vi.md`
- `curriculum/phase-07-llm/p7-10-mini-project-agent/examples/03_scenario_suite.py`
- `curriculum/phase-07-llm/p7-10-mini-project-agent/examples/03_scenario_suite.out`
- `curriculum/phase-07-llm/p7-10-mini-project-agent/examples/03_scenario_suite.en.md`
- `curriculum/phase-07-llm/p7-10-mini-project-agent/examples/03_scenario_suite.vi.md`
- `curriculum/phase-07-llm/p7-10-mini-project-agent/exercises/ex01-toolbox/exercise.yaml`
- `curriculum/phase-07-llm/p7-10-mini-project-agent/exercises/ex02-run-scenarios/exercise.yaml`
- `curriculum/phase-07-llm/p7-10-mini-project-agent/exercises/ex02-run-scenarios/prompt.en.md`
- `curriculum/phase-07-llm/p7-10-mini-project-agent/exercises/ex02-run-scenarios/prompt.vi.md`
- `curriculum/phase-07-llm/p7-10-mini-project-agent/exercises/ex02-run-scenarios/solution.py`
- `curriculum/phase-07-llm/p7-10-mini-project-agent/exercises/ex02-run-scenarios/alternatives/01_step_runner_class.py`
- `curriculum/phase-07-llm/p7-10-mini-project-agent/exercises/ex02-run-scenarios/test_exercise.py`

## 3. Kết quả lệnh kiểm tra (chạy sau lần sửa cuối)

- **`tools/validate.py --path` cho 5 bài (`p7-06`..`p7-10`):**
  - `p7-06-tool-use`: `OK: 0 error(s), 0 warning(s). Checked 1 lessons, 7 markdown pairs, 3 examples, 2 exercises, 1 alternatives, 16 questions.`
  - `p7-07-agents`: `OK: 0 error(s), 0 warning(s). Checked 1 lessons, 7 markdown pairs, 3 examples, 2 exercises, 1 alternatives, 15 questions.`
  - `p7-08-evals`: `OK: 0 error(s), 0 warning(s). Checked 1 lessons, 7 markdown pairs, 3 examples, 2 exercises, 1 alternatives, 16 questions.`
  - `p7-09-mini-project-rag`: `OK: 0 error(s), 0 warning(s). Checked 1 lessons, 8 markdown pairs, 3 examples, 2 alternatives, 2 exercises, 16 questions.`
  - `p7-10-mini-project-agent`: `OK: 0 error(s), 0 warning(s). Checked 1 lessons, 8 markdown pairs, 3 examples, 2 alternatives, 2 exercises, 16 questions.`
- **`uv run python -m pytest curriculum/phase-07-llm -q -p no:warnings`:** toàn bộ passed (`100%`, exit code `0`).
- **`uv run ruff check curriculum`:** `All checks passed!` (exit code `0`).
- **`git diff --numstat curriculum/glossary.yaml`:** `11\t0\tcurriculum/glossary.yaml` (`0` dòng xóa).
- **Chạy các khối Python trong bài học với `-W error` và các file ví dụ `p7-10`:**
  - Mọi khối `print(...)`/`assert` trong `lesson.en.md` của 5 bài chạy qua `-W error` đều exit `0`, stderr rỗng; các khối sửa (`p7-06` §6, `p7-09` §6, `p7-10` §3/§5/§6/§7/§8) khớp chính xác từng dòng với `# output` trong bài.
  - `02_agent_with_approval.py` và `03_scenario_suite.py` chạy với `-W error`, stderr rỗng, và tạo `.out` khớp thực tế (`total_tokens: 644`, `rejected: 1`).
- **Kiểm tra độ dài MCQ (`quiz.yaml` của `p7-06`..`p7-10`):**
  - `p7-06-tool-use`: `mcq 7`, `longest-unique 0`
  - `p7-07-agents`: `mcq 7`, `longest-unique 0`
  - `p7-08-evals`: `mcq 9`, `longest-unique 0`
  - `p7-09-mini-project-rag`: `mcq 9`, `longest-unique 0`
  - `p7-10-mini-project-agent`: `mcq 9`, `longest-unique 2` (<= 9/3 = 3)
  - `violations: 0`
- **Kiểm tra starter-fail và alternatives trong thư mục tạm:**
  - `p7-06 ex01-tool-schema`: starter `7 failed`, solution `7 passed`
  - `p7-07 ex02-run-agent`: starter `9 failed`, solution `9 passed`, alt `01_class_agent.py` `9 passed`
  - `p7-08 ex01-hit-rate`: starter `9 failed`, solution `9 passed`
  - `p7-09 ex01-ingest-retrieve`: starter `18 failed`, solution `18 passed`, alt `01_pure_python_rank.py` `18 passed`
  - `p7-10 ex02-run-scenarios`: starter `13 failed`, solution `13 passed`, alt `01_step_runner_class.py` `13 passed`
- **Kiểm tra mutant:**
  - Mutant M1 (`p7-10 ex02`: xóa hai lệnh `history.append(...)`): `1 failed, 12 passed` (`FAILED test_appends_assistant_and_tool_messages_to_history`).
  - Mutant m1 (`p7-07 ex02`: đổi `v not in ("", None)` thành `v is not None`): `1 failed, 8 passed` (`FAILED test_three_step_scripted_task_reaches_final`).

## 4. Điều còn chưa chắc

- Trong `curriculum/glossary.yaml` dòng 2886 (thuộc term `approval gate` có sẵn), dòng `example` cũ vẫn dùng `needs_approval` cho trường hợp `not approve(name, args)`; mình không sửa dòng này để tuân thủ ràng buộc chỉ được phép append vào `glossary.yaml` (`0` dòng xóa/sửa cũ).
- Script chạy khối Python trong bài kiểm tra toàn bộ block có `print(`/assert ở `lesson.en.md`; sự khớp nhau với `lesson.vi.md` được đảm bảo thông qua kiểm tra parity token của `tools/validate.py` chứ không tách chạy lại riêng từng block của `lesson.vi.md`.
