# Báo cáo M4 bước 17: `p7-07-agents` (Simple agents)

## 1. Đã làm gì
- Tạo bài học song ngữ EN/VI `curriculum/phase-07-llm/p7-07-agents/` chạy trong Pyodide (không dùng `runner: local`), nối tiếp từ `p7-06-tool-use`:
  - `meta.yaml`: `phase: p7`, `order: 7`, `duration_min: 15`, `tags: [llm, loops, functions, agents]` (đều có trong `curriculum/topics.yaml`), `prerequisites: [p7-06-tool-use]`, `outcomes` khớp `curriculum/syllabus.yaml`, `review_by: "2027-05-01"`.
  - `further_reading` (đã mở thử qua HTTP GET, cả hai trả về status `200`):
    - `https://arxiv.org/abs/2210.03629` (ReAct: Synergizing Reasoning and Acting in Language Models)
    - `https://www.anthropic.com/engineering/building-effective-agents` (Anthropic: Building Effective Agents)
  - `lesson.en.md` & `lesson.vi.md`: đủ 8 mục theo dàn ý (mở đầu thực tế đơn #1042, picture in text chu trình observe–think–act, bảng so sánh workflow/router/agent, vòng lặp `run_agent` 3 bước bằng `script`, biểu đồ Mermaid `flowchart LR` 6 node, callout `[!NOTE]` về vai trò của `script` so với LLM thật, bảng trace, 4 điều kiện dừng `final`/`max_steps`/`repeat`/`budget`, khối mời **Visualize** bằng agent đồ chơi không gọi `FakeLLM`, tự sửa khi tool trả `"error: ..."`, cổng duyệt `needs_approval` với callout `[!WARNING]` và khi nào không dùng agent, 4 lỗi thường gặp với output thật, tóm tắt).
  - 3 ví dụ chạy độc lập trong `examples/`: `01_order_agent.py`, `02_stop_conditions.py`, `03_approval_gate.py` kèm `.out`, `.en.md`, `.vi.md`.
  - 2 bài tập trong `exercises/`:
    - `ex01-detect-repeat` (`kind: fill`): hàm `is_repeat(history, name, args)` với 6 test parametrize.
    - `ex02-run-agent` (`kind: code`): hàm `run_agent(client, task, tools, registry, max_steps=5, token_budget=None)` với 9 test (gồm spy kiểm tra thứ tự message `assistant` -> `tool` và kiểm tra không mutate input), kèm lời giải thay thế `alternatives/01_class_agent.py` (`.en.md`, `.vi.md`) cài đặt bằng class `Agent` và `step()`.
  - `quiz.yaml`: 15 câu hỏi (7 `mcq`, 3 `output`, 3 `fill`, 2 `parsons`; 5 dễ / 7 vừa / 3 khó) và 6 flashcard.
- Bổ sung 7 thuật ngữ mới vào `curriculum/glossary.yaml` (`agent loop`, `observe-think-act`, `ReAct`, `max steps`, `trace`, `stop condition`, `workflow`); bỏ qua `agent` vì đã tồn tại sẵn.

## 2. File đã tạo / sửa
- Tạo mới thư mục `curriculum/phase-07-llm/p7-07-agents/` gồm:
  - `meta.yaml`, `lesson.en.md`, `lesson.vi.md`, `quiz.yaml`
  - `examples/01_order_agent.{py,out,en.md,vi.md}`
  - `examples/02_stop_conditions.{py,out,en.md,vi.md}`
  - `examples/03_approval_gate.{py,out,en.md,vi.md}`
  - `exercises/ex01-detect-repeat/{exercise.yaml,prompt.en.md,prompt.vi.md,starter.py,solution.py,test_exercise.py}`
  - `exercises/ex02-run-agent/{exercise.yaml,prompt.en.md,prompt.vi.md,starter.py,solution.py,test_exercise.py}`
  - `exercises/ex02-run-agent/alternatives/01_class_agent.{py,en.md,vi.md}`
- Chỉ thêm dòng vào `curriculum/glossary.yaml`.
- Tạo `tasks/m4-p7-07-agents.report.md`.

## 3. Kết quả lệnh kiểm tra
- `uv run python tools/validate.py --path curriculum/phase-07-llm/p7-07-agents`:
  - `OK: 0 error(s), 0 warning(s). Checked 1 lessons, 7 markdown pairs, 3 examples, 2 exercises, 1 alternatives, 15 questions.`
- `uv run python -m pytest curriculum/phase-07-llm`:
  - `109 passed in 0.24s` (exit 0).
- `uv run ruff check curriculum/phase-07-llm`:
  - `All checks passed!` (exit 0).
- Kiểm tra pattern cấm trên `*.py` (`input(`, `time.sleep`, `requests.`, `urllib`, `open(`, `eval(`, `exec(`, `subprocess`, `os.system`, `while True`) và `while True` trên `*.md`:
  - Rỗng (`bad_py: []`, `bad_md: []`).
- Kiểm tra `starter` fail toàn bộ test:
  - Browser runner (`tools/pyrunner/runner.py`): `ex01-detect-repeat` starter `0 / 6` pass (solution `6 / 6`), `ex02-run-agent` starter `0 / 9` pass (solution `9 / 9`, `01_class_agent.py` `9 / 9`).
  - Pytest với `EXERCISE_TARGET=starter`: `15 failed` (0 pass trên cả 2 bài).
- Kiểm tra **Visualize** qua `tools/pyrunner/tracer.py`:
  - Khối đồ chơi không gọi `FakeLLM` trong §4 (`run_toy_agent`): **25 steps** (`< 600`), `truncated=False`, `error=None`.
  - Các example: `01_order_agent.py` = **101 steps**, `02_stop_conditions.py` = **238 steps**, `03_approval_gate.py` = **71 steps** (`truncated=False`, `error=None`).
- Kiểm tra `-W error` và stderr rỗng:
  - Cả 3 file trong `examples/*.py` và toàn bộ 11 khối Python trong `lesson.en.md` / `lesson.vi.md` chạy độc lập với `python -W error`, exit 0, stderr rỗng, stdout khớp chú thích.
- Script độ dài MCQ trên `quiz.yaml`:
  - `violations: 0` (trên 7 câu MCQ ở cả `en` và `vi`; số câu mà đáp án đúng là phương án dài nhất duy nhất: `longest_en: 0`, `longest_vi: 0`).
- `git diff --numstat curriculum/glossary.yaml`:
  - `77	0	curriculum/glossary.yaml` (chỉ thêm dòng, 0 dòng xóa/sửa); kiểm tra bằng `tools/validate.py` (`glossary.schema.json`, trùng tên, tag trong `topics.yaml`): `schema_errors: 0, dups: [], bad_tags: [], total_terms: 251`.
- `uv run python tools/build_content.py`:
  - `Built 46 lessons, 9 exams, 276 flashcards, 738 questions -> apps\web\src\generated` (exit 0).
- `git status --short`:
  - `M curriculum/glossary.yaml`
  - `?? .hallmark/` (có sẵn từ trước trong repo, không do tác vụ này tạo)
  - `?? curriculum/phase-07-llm/p7-07-agents/`
  - `?? tasks/`

## 4. Điều còn chưa chắc
- Theo yêu cầu không chạy server/dev server, nên chưa mở giao diện web để kiểm tra trực tiếp hiển thị React/Pyodide thực tế trên trình duyệt; tuy nhiên toàn bộ logic chạy trong trình duyệt đã được kiểm gián tiếp qua `tools/pyrunner/runner.py`, `tools/pyrunner/tracer.py` và `tools/build_content.py`.
