# Báo cáo thực hiện: `p7-10-mini-project-agent`

## 1. Đã làm gì

- Xây dựng trọn bộ bài học dự án `curriculum/phase-07-llm/p7-10-mini-project-agent/` (`kind: project`, song ngữ EN/VI, chạy hoàn toàn offline/Pyodide bằng `FakeLLM` từ `pyai_llm`, không I/O, không gọi mạng, không dùng API key).
- **`meta.yaml`**: cấu hình `phase: p7`, `order: 10`, `kind: project`, `level: beginner`, `duration_min: 45`, `tags: [llm, agents, testing]`, `prerequisites: [p7-07-agents]`, giữ 2 outcome của `curriculum/syllabus.yaml` và thêm 2 outcome cụ thể về cổng duyệt/audit log và tổng hợp báo cáo kịch bản; `review_by: "2027-05-01"`.
- **`lesson.en.md` & `lesson.vi.md`**:
  - Dàn ý đầy đủ: `The plan` (kèm sơ đồ Mermaid `flowchart TD`, bảng trace 3 kịch bản, bảng so sánh `Agent loop vs Pipeline`), dữ liệu & 3 tool thuần Python (`lookup_order`, `track_shipment`, `check_refund_policy`) + 1 tool side effect (`issue_refund`), `ToolBox` an toàn (allowlist, kiểm tra `required` theo thứ tự, lọc tham số thừa, bắt exception thành `error: ...`, JSON hóa dict/list), vòng agent có giới hạn (`max_steps`, `repeat`, `token_budget`), cổng duyệt `approve` + audit log (`needs_approval` không thực thi side effect), bộ 7 kịch bản kiểm thử tất định so sánh `v1` (lỗi thiếu `repeat` guard -> `6/7`) với `v2` (đã sửa -> `7/7`), phần báo cáo tổng hợp, khối Visualize độc lập không dùng `FakeLLM`, 4 lỗi thường gặp có output thật, `Recap` và `Take it further` không đánh số.
  - Đầy đủ callout `[!NOTE]`, `[!WARNING]`, `[!TIP]`. Cả 12 khối code Python giữa EN và VI khớp logic và chạy sạch với `python -W error`, stderr rỗng.
- **Examples (3)**:
  - `01_toolbox`: đăng ký tool vào `ToolBox`, thử các ca hợp lệ, tên lạ, thiếu tham số, tham số thừa bị bỏ qua và exception.
  - `02_agent_with_approval`: chạy agent trên 3 task (chỉ đọc, hoàn tiền được duyệt, hoàn tiền bị từ chối kèm `pending` và audit log).
  - `03_scenario_suite`: chạy bộ kịch bản đầy đủ, in bảng `PASS`/`FAIL` và báo cáo.
- **Exercises (2, đều `kind: project`)**:
  - `ex01-toolbox`: `class ToolBox` (`register`, `schemas` deep copy, `is_side_effect`, `call`), kèm `alternatives/01_dataclass_registry.py` (dùng `@dataclass(frozen=True)` và một `dict` registry) và 10 test trong `test_exercise.py`.
  - `ex02-run-scenarios`: `run_scenario` và `summarize`, kèm `alternatives/01_step_runner_class.py` (tách trạng thái từng bước qua class `AgentSession`) và 12 test trong `test_exercise.py` (dùng `MiniToolbox` tự chứa và `FakeLLM`).
  - Cả hai bài đều có hint 3 tầng đúng quy tắc trong `prompt.en.md` / `prompt.vi.md`.
- **Quiz & Flashcards (`quiz.yaml`)**:
  - 16 câu hỏi: 9 `mcq`, 3 `output` (`p7-10-q04`, `p7-10-q10`, `p7-10-q11`), 2 `fill`, 2 `parsons` (`p7-10-q13`, `p7-10-q16`); phân bố độ khó: 5 câu mức 1, 8 câu mức 2, 3 câu mức 3; kèm 6 flashcard (`p7-10-f01`..`p7-10-f06`).
- **Glossary (`curriculum/glossary.yaml`)**:
  - Giữ nguyên các mục đã có (`side effect`, `allowlist` đã tồn tại từ trước), chỉ bổ sung 3 thuật ngữ còn thiếu vào cuối file: `approval gate`, `golden trajectory`, `scenario test`.

## 2. File đã sửa / tạo

- **Sửa (chỉ thêm dòng ở cuối):**
  - `curriculum/glossary.yaml` (`+34` dòng, `-0` dòng theo `git diff --numstat`)
- **Tạo mới (34 file trong `curriculum/phase-07-llm/p7-10-mini-project-agent/`):**
  - `curriculum/phase-07-llm/p7-10-mini-project-agent/meta.yaml`
  - `curriculum/phase-07-llm/p7-10-mini-project-agent/lesson.en.md`
  - `curriculum/phase-07-llm/p7-10-mini-project-agent/lesson.vi.md`
  - `curriculum/phase-07-llm/p7-10-mini-project-agent/quiz.yaml`
  - `curriculum/phase-07-llm/p7-10-mini-project-agent/examples/01_toolbox.{py,out,en.md,vi.md}`
  - `curriculum/phase-07-llm/p7-10-mini-project-agent/examples/02_agent_with_approval.{py,out,en.md,vi.md}`
  - `curriculum/phase-07-llm/p7-10-mini-project-agent/examples/03_scenario_suite.{py,out,en.md,vi.md}`
  - `curriculum/phase-07-llm/p7-10-mini-project-agent/exercises/ex01-toolbox/{exercise.yaml,prompt.en.md,prompt.vi.md,starter.py,solution.py,test_exercise.py}`
  - `curriculum/phase-07-llm/p7-10-mini-project-agent/exercises/ex01-toolbox/alternatives/01_dataclass_registry.{py,en.md,vi.md}`
  - `curriculum/phase-07-llm/p7-10-mini-project-agent/exercises/ex02-run-scenarios/{exercise.yaml,prompt.en.md,prompt.vi.md,starter.py,solution.py,test_exercise.py}`
  - `curriculum/phase-07-llm/p7-10-mini-project-agent/exercises/ex02-run-scenarios/alternatives/01_step_runner_class.{py,en.md,vi.md}`
- **Báo cáo:**
  - `tasks/m4-p7-10-mini-project-agent.report.md`
- *(Ghi chú: `uv run python tools/build_content.py` cập nhật output build trong `apps/web/src/generated` theo lệnh kiểm tra; thư mục `.hallmark/` có sẵn trên workspace và không bị chạm tới.)*

## 3. Kết quả lệnh kiểm tra (chạy sau lần chỉnh sửa cuối)

- `uv run python tools/validate.py --path curriculum/phase-07-llm/p7-10-mini-project-agent`:
  - `OK: 0 error(s), 0 warning(s). Checked 1 lessons, 8 markdown pairs, 3 examples, 2 alternatives, 2 exercises, 16 questions.` (exit 0)
- `uv run python -m pytest curriculum/phase-07-llm`:
  - `170 passed in 0.34s` (exit 0)
- `uv run ruff check curriculum/phase-07-llm`:
  - `All checks passed!` (exit 0)
- Kiểm tra mẫu cấm (`input(|time.sleep|requests.|urllib|open(|[^_a-z]eval(|exec(|subprocess|os.system|while True`) trên `*.py` và `while True` trên `*.md` trong `curriculum/phase-07-llm/p7-10-mini-project-agent`:
  - Kết quả: rỗng (`[]`), không có vi phạm.
- `git diff --numstat curriculum/glossary.yaml`:
  - `34	0	curriculum/glossary.yaml` (chỉ thêm dòng, 0 dòng xóa).
- `uv run python tools/build_content.py`:
  - `Built 49 lessons, 9 exams, 294 flashcards, 786 questions -> apps\web\src\generated` (exit 0)
- Script kiểm tra độ dài MCQ (`quiz.yaml`):
  - `violations: 0` (từ script kiểm tra độ dài MCQ).
- Kiểm tra `-W error` cho từng phần code (stderr rỗng, exit 0):
  - 12 khối Python trong `lesson.en.md` và `lesson.vi.md`: chạy độc lập sạch, stderr rỗng; output Part 5 khớp comment (`passed: 6/7`, `total_tokens: 812`, `FAIL repeat_guard: stopped_reason, tools`, và `v2 -> passed: 7/7 total_tokens: 716 failures: none`).
  - 3 example `.py`: chạy sạch với `-W error`, stdout khớp 100% file `.out` (`01_toolbox.out`: 5 dòng, max 56 ký tự; `02_agent_with_approval.out`: 12 dòng, max 67 ký tự; `03_scenario_suite.out`: 15 dòng, max 63 ký tự).
- Kiểm tra AST trùng thân hàm giữa `solution.py` / `alternatives/*.py` với 12 khối trong bài học và 3 file example:
  - `AST exact body matches: 0 []`.

## 4. Cập nhật vòng 2 (theo `## Feedback vòng 2`)

1. **Thống nhất tên lý do fail `"tools"`**: đổi `"trajectory"` (như tên lý do lỗi) sang `"tools"` trong Part 5 (`lesson.en.md`, `lesson.vi.md`) và `examples/03_scenario_suite.py` cho khớp `ex02-run-scenarios` và `quiz.yaml` (giữ nguyên thuật ngữ "golden trajectory").
2. **Làm rõ phiên bản được báo cáo ở Part 5**: thêm câu dẫn trước khối code Part 5 nêu rõ đang báo cáo kết quả `v1` (`v1_results`, dùng số token thật đo từ Part 4: `total_tokens: 812`, `passed: 6/7`) để thấy dòng `FAIL`, kèm dòng tóm tắt sau khi sửa sang `v2` (`passed: 7/7 total_tokens: 716 failures: none`).
3. **Giải thích ký hiệu `final(2)` ở Part 4**: bổ sung nửa câu giải thích trước bảng `v2` trong `lesson.en.md` và `lesson.vi.md` rằng số trong ngoặc là số tool đã chạy.

## 5. Số step Visualize & `further_reading`

- **Khối Visualize (`toy_scenarios` / `run_toy` trong bài học):**
  - Chạy qua `tools/pyrunner/tracer.py`: `steps=69`, `truncated=False`, `error=None`.
- **Trace các example qua `tools/pyrunner/tracer.py`:**
  - `01_toolbox.py`: `steps=114`, `truncated=False`, `error=None`.
  - `02_agent_with_approval.py`: `steps=190`, `truncated=False`, `error=None`.
  - `03_scenario_suite.py`: `steps=600`, `truncated=True`, `error=None` (chạm ngưỡng `MAX_STEPS = 600` của tracer khi bước từng dòng, còn chạy Python bình thường kết thúc trọn vẹn và khớp `.out`).
- **`further_reading` trong `meta.yaml`:**
  - `https://www.anthropic.com/engineering/building-effective-agents` (HTTP 200)
  - `https://docs.pytest.org/en/stable/how-to/parametrize.html` (HTTP 200)

## 6. Danh sách kịch bản Part 4 & kết quả

- `happy_lookup`: kỳ vọng `final(2)` | `v1`: `final(2)` (`PASS`) | `v2`: `final(2)` (`PASS`)
- `missing_order`: kỳ vọng `final(1)` | `v1`: `final(1)` (`PASS`) | `v2`: `final(1)` (`PASS`)
- `repeat_guard`: kỳ vọng `repeat(1)` | `v1`: `max_steps(3)` (`FAIL` do thiếu kiểm tra lặp tool+args liên tiếp) | `v2`: `repeat(1)` (`PASS`)
- `max_steps_cap`: kỳ vọng `max_steps(2)` | `v1`: `max_steps(2)` (`PASS`) | `v2`: `max_steps(2)` (`PASS`)
- `refund_approved`: kỳ vọng `final(3)` | `v1`: `final(3)` (`PASS`) | `v2`: `final(3)` (`PASS`)
- `refund_rejected`: kỳ vọng `needs_approval(1)` | `v1`: `needs_approval(1)` (`PASS`) | `v2`: `needs_approval(1)` (`PASS`)
- `budget_stop`: kỳ vọng `budget(0)` | `v1`: `budget(0)` (`PASS`) | `v2`: `budget(0)` (`PASS`)
- Tổng hợp: `v1` đạt `6/7`; `v2` đạt `7/7`.

## 7. Điều còn chưa chắc

- Hai URL `further_reading` chưa được fetch lại ở vòng 2 này.
- `03_scenario_suite.py` chạm ngưỡng `MAX_STEPS = 600` nếu chạy bằng `tracer.py` (`truncated=True`), nên nếu người học bấm Visualize trên example 3 thay vì khối Visualize chuyên dụng (`69` step) thì trace sẽ cắt ở step 600.
- Ở vòng 2 chưa chạy lại trực tiếp `tools/pyrunner/runner.py` và `tools/pyrunner/tracer.py` (không sửa file `exercises/` hay khối Visualize).
- Theo yêu cầu nhiệm vụ, không chạy `pnpm --filter web build` hay khởi động web dev server.
