# Báo cáo triển khai bài `p7-08-evals` (M4 bước 18)

## 1. Đã làm gì

1. **Metadata (`meta.yaml`)**
   - Tạo `curriculum/phase-07-llm/p7-08-evals/meta.yaml` với `phase: p7`, `order: 8`, `duration_min: 15`, `tags: [llm, rag, evaluation]`, `prerequisites: [p7-05-rag, p5-04-evaluation]`, `review_by: "2027-05-01"`, không dùng `runner: local` (chạy hoàn toàn trong Pyodide).
   - `outcomes` khớp `curriculum/syllabus.yaml`.
   - Đã mở kiểm tra trực tiếp 2 link `further_reading` (HTTP 200):
     - `https://arxiv.org/abs/2309.15217` — `[2309.15217] Ragas: Automated Evaluation of Retrieval Augmented Generation`
     - `https://platform.claude.com/docs/en/test-and-evaluate/develop-tests` — `Define success criteria and build evaluations - Claude Platform Docs`

2. **Bài học song ngữ (`lesson.en.md`, `lesson.vi.md`)**
   - Kho dữ liệu chung: 7 chunk chính sách cửa hàng (`refunds.md`, `shipping.md`, `warranty.md`, `hours.md`, `pickup.md`, `payment.md`, `loyalty.md`) và tập eval 6 câu (`q1`–`q6`, trong đó `q5` dùng `"money back"` và `q6` là câu không có trong tài liệu `expected_source: None, expected_facts: []`).
   - Đủ 8 phần theo dàn ý:
     - Opening không heading nối về bài toán "cảm giác mượt hơn" vs đo bằng số (`p5-04-evaluation`).
     - §1 Eval là gì & bảng so sánh `unit test` / `eval` / `đọc thử bằng mắt`.
     - §2 Xây eval set nhỏ + sơ đồ `text` tách tầng `hit@k` và `facts / faithful`.
     - §3 Chấm retrieval (`hit@2 = 4/5 = 0.8`), bảng trace `| id | top-2 sources | expected | hit |`, khối mời **Visualize** không gọi `FakeLLM` (**34 step** qua `tools/pyrunner/tracer.py`, giới hạn `< 600`).
     - §4 Chấm câu trả lời (`fact_score` chữ thường kèm phân tích ưu/nhược, `faithful` heuristic tách từ `[a-z0-9]+` dài `>= 4` bỏ `[n]`), demo câu thật vs câu bịa từ `FakeLLM(script=[...])` (`facts=1.0`, `faithful=False`, `unsupported=['with', 'free', 'courier', 'pickup']`), callout `[!NOTE]` về giới hạn heuristic / `LLM-as-judge` / vai trò của `script`, sơ đồ Mermaid `flowchart TD` 7 node.
     - §5 So sánh **cấu hình `k=1` vs `k=3`** trên cùng tập eval:
       - `k=1`: `hit@1 = 3/5 (60%)`, `facts = 3/5 (60%)`, `faithful = 6/6 (100%)`, `idk = 1/1 (100%)`
       - `k=3`: `hit@3 = 5/5 (100%)`, `facts = 4/5 (80%)`, `faithful = 6/6 (100%)`, `idk = 0/1 (0%)`
       - Phân tích từng câu đổi: `q2` tốt lên (`hit` & `facts` từ `0.0 -> 1.0`), `q5` tốt lên ở tầng retrieval (`hit: False -> True`) nhưng `facts` vẫn `0.0` (do `embed` hiểu `"money back"` còn `_try_rag` chỉ đếm từ thô), `q6` tệ đi (`idk: 1.0 -> 0.0` do `payment.md` lọt vào top-3 và trùng `"for"`, `"orders"`).
       - Callout `[!WARNING]` cảnh báo nhiễu 17–20% mỗi câu trên tập 5–6 câu.
     - §6 Regression test với `check_eval()` và lưu lịch sử sang phase 8.
     - §7 Lỗi thường gặp (kèm code & output thật) và §8 Tóm tắt.

3. **3 Examples (`examples/`)**
   - `01_build_eval_set.py` (+ `.out`, `.en.md`, `.vi.md`): bảng `hit@2` từng câu và tổng `4/5 (0.8)`.
   - `02_score_answers.py` (+ `.out`, `.en.md`, `.vi.md`): chạy RAG đầy đủ trên 6 câu + demo `FakeLLM(script=[...])` bịa chi tiết bị bắt `faithful=False`.
   - `03_compare_configs.py` (+ `.out`, `.en.md`, `.vi.md`): bảng so sánh `k=1` vs `k=3` và danh sách các câu thay đổi.
   - Mọi dòng output đều `<= 59` ký tự (`< 70`).

4. **2 Exercises (`exercises/`)**
   - `ex01-hit-rate` (`kind: fill`): `hit_rate(results, k)` bỏ qua `expected_source=None`. Browser runner: `starter.py` pass **0/7**, `solution.py` pass **7/7**.
   - `ex02-score-answer` (`kind: code`, đã cập nhật theo Feedback vòng 2): giữ nguyên `id: p7-08-ex02` và tên thư mục, đổi tên hàm thành `score_grounded(answer, expected_facts, context)` mở rộng từ `score_answer` ở §4 để kiểm tra thêm `citations` (số nguyên `n` trong `[n]` của `answer`, không trùng, giữ thứ tự xuất hiện kể cả với câu `"i don't know"`) và `bad_citations` (các số trong `citations` không có dòng `[n] ...` tương ứng trong `context`), đồng thời yêu cầu `faithful` phải có ít nhất một trích dẫn hợp lệ và không có trích dẫn sai (trừ câu `"i don't know"`). Browser runner: `starter.py` pass **0/10**, `solution.py` pass **10/10**, `alternatives/01_set_ops.py` pass **10/10**.
   - Hint 3 tầng đúng luật cho cả hai bài (hint 3 của `ex02-score-answer` chừa đúng một `...` cho phần tính `citations, bad_citations`).

5. **Quiz (`quiz.yaml`) & Glossary (`curriculum/glossary.yaml`)**
   - `quiz.yaml`: 16 câu hỏi (`9 mcq`, `3 output`, `2 fill`, `2 parsons`; 5 dễ, 8 vừa, 3 khó) + 6 flashcard.
   - `curriculum/glossary.yaml`: chỉ thêm 6 thuật ngữ chưa có (`eval set`, `golden answer`, `hit rate`, `faithfulness`, `groundedness`, `LLM-as-judge`); bỏ qua `eval` và `regression` vì đã tồn tại.

## 2. File đã tạo / sửa

- Tạo mới thư mục `curriculum/phase-07-llm/p7-08-evals/`:
  - `meta.yaml`, `lesson.en.md`, `lesson.vi.md`, `quiz.yaml`
  - `examples/01_build_eval_set.{py,out,en.md,vi.md}`
  - `examples/02_score_answers.{py,out,en.md,vi.md}`
  - `examples/03_compare_configs.{py,out,en.md,vi.md}`
  - `exercises/ex01-hit-rate/{exercise.yaml,prompt.en.md,prompt.vi.md,starter.py,solution.py,test_exercise.py}`
  - `exercises/ex02-score-answer/{exercise.yaml,prompt.en.md,prompt.vi.md,starter.py,solution.py,test_exercise.py}`
  - `exercises/ex02-score-answer/alternatives/01_set_ops.{py,en.md,vi.md}`
- Chỉ thêm dòng vào `curriculum/glossary.yaml` (`67 0`).
- Tạo báo cáo `tasks/m4-p7-08-evals.report.md`.

## 3. Kết quả lệnh kiểm tra (đã chạy lại sau sửa vòng 2)

- `uv run python tools/validate.py --path curriculum/phase-07-llm/p7-08-evals`:
  `OK: 0 error(s), 0 warning(s). Checked 1 lessons, 7 markdown pairs, 3 examples, 2 exercises, 1 alternatives, 16 questions.`
- `uv run python -m pytest curriculum/phase-07-llm`:
  `126 passed in 0.24s`
- `uv run ruff check curriculum/phase-07-llm`:
  `All checks passed!`
- Quét mẫu cấm trên toàn bộ `*.py` trong `p7-08-evals`:
  `forbidden matches: 0 []`
- Browser runner (`tools/pyrunner/runner.py`) cho `ex02-score-answer` (chạy với `-W error`):
  - `starter.py`: `{'passed': 0, 'total': 10, 'error': None}` (**0/10** pass)
  - `solution.py`: `{'passed': 10, 'total': 10, 'error': None}` (**10/10** pass)
  - `alternatives/01_set_ops.py`: `{'passed': 10, 'total': 10, 'error': None}` (**10/10** pass)
- Script độ dài MCQ:
  `violations: 0`
- `git diff --numstat curriculum/glossary.yaml`:
  `67	0	curriculum/glossary.yaml` (chỉ có dòng thêm).
- `uv run python tools/build_content.py`:
  `Built 47 lessons, 9 exams, 282 flashcards, 754 questions -> apps\web\src\generated`
- `git status --short`:
  `M curriculum/glossary.yaml`, `?? .hallmark/`, `?? curriculum/phase-07-llm/p7-08-evals/`, `?? tasks/`
- Lưu ý kết quả từ vòng 1 (lesson/examples/glossary không đổi ở vòng 2):
  - 10/10 khối Python ở mỗi bản `lesson.en.md` / `lesson.vi.md` chạy sạch với `-W error`; khối Visualize ở §3 có `34` bước (`< 600`); `ex01-hit-rate` pass `0/7` với `starter.py` và `7/7` với `solution.py`; `curriculum/glossary.yaml` có `0` lỗi (`257` terms).

## 4. Điều còn chưa chắc

- Không có vướng mắc về logic hay định dạng trong phạm vi bài `p7-08-evals` và `curriculum/glossary.yaml`. Toàn bộ các lệnh kiểm tra trong spec (`validate.py --path`, `pytest curriculum/phase-07-llm`, `ruff check`, quét mẫu cấm, `build_content.py`, `git diff --numstat curriculum/glossary.yaml`, script độ dài MCQ) đều đã chạy sau lần sửa cuối và đạt 100%.
- Lưu ý: khi chạy `uv run python tools/validate.py --fast` toàn curriculum (ngoài phạm vi bài) thì mất hơn 40s do chạy tracer cho các bài matplotlib ở phase 4/5 nên đã dừng background task đó và kiểm trực tiếp `curriculum/glossary.yaml` bằng hàm của `tools/validate.py`.
