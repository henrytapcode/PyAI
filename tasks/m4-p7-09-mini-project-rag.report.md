# Báo cáo hoàn thành: `p7-09-mini-project-rag`

## 1. Đã làm gì

Đã hoàn thành bài mini-project cuối Phase 7 (`curriculum/phase-07-llm/p7-09-mini-project-rag/`) theo spec trong `tasks/m4-p7-09-mini-project-rag.md` và `docs/CONTENT_GUIDE.md`:

- **`meta.yaml`**: Khai báo metadata (`id: p7-09-mini-project-rag`, `phase: p7`, `order: 9`, `kind: project`, `tags: [llm, rag, evaluation]`, `prerequisites: [p7-08-evals]`, `duration_min: 45`, `review_by: "2027-05-01"`), 4 learning outcomes và 2 link `further_reading`.
- **`lesson.en.md` & `lesson.vi.md`**: Soạn bài học song ngữ EN/VI theo cấu trúc dự án (kiến trúc pipeline RAG + Mermaid 8 dòng, sơ đồ tách `dev_set`/`test_set`, khối **Visualize** 33 step không dùng `FakeLLM`, bảng so sánh cấu hình và trace table khớp output thật, callout `[!WARNING]` và `[!TIP]`, 4 lỗi thường gặp kèm output chạy `FakeLLM` thực tế, `Recap`/`Tóm tắt` và `Take it further`/`Làm thêm` kèm ví dụ `.env` không hardcode key).
- **Cập nhật vòng 2 (`lesson.en.md` & `lesson.vi.md`)**:
  1. Đổi `retrieve` ở §4 và §5 thành `top_k(index, question, client, k=2)` trả về list `(score, chunk)` (không lọc `min_score`, không làm tròn trong dict); ở §5 lọc `min_score` bằng comprehension một dòng trong `answer_with_sources`, còn ở §6 giữ bước lọc `min_score` bằng comprehension trong `eval_config` và giải thích rõ trong phần lời. Giữ nguyên exercise `ex01-ingest-retrieve`, giữ nguyên toàn bộ kết quả in ở §4–§7.
  2. Đổi heading cuối không đánh số theo `CONTENT_GUIDE` và `p5-05`: `## Recap` / `## Tóm tắt` và `## Take it further` / `## Làm thêm`.
  3. Bổ sung nửa câu ở Lỗi thường gặp 1 nói rõ khối minh họa dùng bản rút gọn 2 câu của `test_set` (`t1` và `t3`) để tránh hiểu nhầm `"2 of 2"` với tập test 4 câu ở §7.
  4. Đổi `OPENAI_API_KEY` thành `LLM_API_KEY` ở mục `Take it further` / `Làm thêm` trong cả EN và VI.
- **`examples/01_ingest_and_index.*`, `02_answer_with_sources.*`, `03_eval_report.*`**: Mỗi example gồm file `.py`, `.out`, `.en.md`, `.vi.md`; chạy sạch với `-W error`, không có warning/stderr, độ dài mỗi dòng output <= 67 ký tự.
- **`exercises/ex01-ingest-retrieve` & `exercises/ex02-eval-report`**: Mỗi bài gồm `exercise.yaml` (hint 3 tầng), `prompt.en.md`, `prompt.vi.md`, `starter.py`, `solution.py`, `test_exercise.py` (12 test cho ex01, 10 test cho ex02; dùng Spy client bọc `FakeLLM` để kiểm tra index chỉ gọi `embed` một lần), và `alternatives/01_*.py` kèm tài liệu EN/VI (cách làm thuần Python không dùng NumPy cho ex01; dùng `collections.Counter` và hàm `classify_row` cho ex02).
- **`quiz.yaml`**: Tạo 16 câu hỏi (`9` `mcq`, `3` `output`, `2` `fill`, `2` `parsons`) và `6` flashcards. Đảm bảo độ dài phương án đúng trong các câu `mcq` cân đối, thứ tự các câu `parsons` là duy nhất.
- **`curriculum/glossary.yaml`**: Chỉ bổ sung 3 thuật ngữ mới còn thiếu (`ingestion`, `dev set`, `held-out test set`), không sửa hoặc xóa dòng cũ.

## 2. Danh sách file đã tạo và chỉnh sửa

- **Chỉnh sửa ở vòng 2:**
  - `curriculum/phase-07-llm/p7-09-mini-project-rag/lesson.en.md`
  - `curriculum/phase-07-llm/p7-09-mini-project-rag/lesson.vi.md`
  - `tasks/m4-p7-09-mini-project-rag.report.md`
- **Chỉnh sửa ở vòng 1:**
  - `curriculum/glossary.yaml`
- **Tạo mới:**
  - `curriculum/phase-07-llm/p7-09-mini-project-rag/meta.yaml`
  - `curriculum/phase-07-llm/p7-09-mini-project-rag/lesson.en.md`
  - `curriculum/phase-07-llm/p7-09-mini-project-rag/lesson.vi.md`
  - `curriculum/phase-07-llm/p7-09-mini-project-rag/quiz.yaml`
  - `curriculum/phase-07-llm/p7-09-mini-project-rag/examples/01_ingest_and_index.{py,out,en.md,vi.md}`
  - `curriculum/phase-07-llm/p7-09-mini-project-rag/examples/02_answer_with_sources.{py,out,en.md,vi.md}`
  - `curriculum/phase-07-llm/p7-09-mini-project-rag/examples/03_eval_report.{py,out,en.md,vi.md}`
  - `curriculum/phase-07-llm/p7-09-mini-project-rag/exercises/ex01-ingest-retrieve/{exercise.yaml,prompt.en.md,prompt.vi.md,starter.py,solution.py,test_exercise.py}`
  - `curriculum/phase-07-llm/p7-09-mini-project-rag/exercises/ex01-ingest-retrieve/alternatives/01_pure_python_rank.{py,en.md,vi.md}`
  - `curriculum/phase-07-llm/p7-09-mini-project-rag/exercises/ex02-eval-report/{exercise.yaml,prompt.en.md,prompt.vi.md,starter.py,solution.py,test_exercise.py}`
  - `curriculum/phase-07-llm/p7-09-mini-project-rag/exercises/ex02-eval-report/alternatives/01_counter_helper.{py,en.md,vi.md}`
  - `tasks/m4-p7-09-mini-project-rag.report.md` (báo cáo này)

## 3. Thông số bắt buộc

- **Số step khối Visualize (`lesson.en.md` & `lesson.vi.md`, Phần 3):** `33` steps, `error=None` (kiểm bằng `tools/pyrunner/tracer.py`), không import hay gọi `FakeLLM`.
- **Link `further_reading` đã kiểm tra:**
  - `https://arxiv.org/abs/2005.11401` (Lewis et al., 2020 — *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*)
  - `https://www.anthropic.com/news/contextual-retrieval` (Anthropic — *Contextual Retrieval*)
  - Ghi chú: Đã truy cập/xác nhận nội dung cả hai đường dẫn qua `search_web` trong phiên trước; khi thử `urllib` mặc định của Python thì `arxiv.org` trả HTTP 403 do thiếu `User-Agent`.
- **Các cấu hình đã so sánh trên `dev_set` (8 câu: 6 trả lời được, 2 không trả lời được) và cấu hình đã chọn:**
  - `words(8,2) m=0.2` (`mode="words"`, `size=8`, `overlap=2`, `k=2`, `min_score=0.2`): `hit=6/6 (100%)`, `facts=3/6 (50%)`, `idk=2/2 (100%)`
  - `sent k=2 m=0.2` (`mode="sentence"`, `k=2`, `min_score=0.2`): `hit=6/6 (100%)`, `facts=5/6 (83%)`, `idk=1/2 (50%)` — **Cấu hình được chọn** theo quy tắc định sẵn trên `dev_set` (ưu tiên `facts` cao nhất, hòa mới xét `idk`, sau đó tới `hit@2`).
  - `sent k=2 m=0.35` (`mode="sentence"`, `k=2`, `min_score=0.35`): `hit=4/6 (67%)`, `facts=4/6 (67%)`, `idk=2/2 (100%)`
- **Điểm `dev_set` và `test_set` của cấu hình đã chọn (`sent k=2 m=0.2`) từ `examples/03_eval_report.py`:**
  - `dev`: `hit=6/6 (100%)`, `facts=5/6 (83%)`, `idk=1/2 (50%)` — câu lỗi: `d6: answer_miss` (do `embed` ánh xạ `"money back"` sang `"refund"`, nhưng `FakeLLM.chat` khớp từ thô nên trả lời từ chối), `d8: no_refusal` (câu hỏi `"Can I pay with crypto for online orders?"` vượt ngưỡng `0.2` với `payment.md#0` do trùng các từ `pay`, `online`, `orders` nên model không từ chối).
  - `test` (chạy 1 lần duy nhất): `hit=3/3 (100%)`, `facts=2/3 (67%)`, `idk=1/1 (100%)` — câu lỗi: `t3: answer_miss` (paraphrase `"notebooks"` -> `"laptops"` ở lớp `embed`, còn `FakeLLM.chat` không nhận synonym nên từ chối dù đã truy xuất đúng `discounts.md`).
- **Kết quả starter / solution / alternative của bài tập:**
  - `ex01-ingest-retrieve`:
    - `starter.py`: pass `0/12` trên browser runner (`tools/pyrunner/runner.py`) và `12 failed` (`0 passed`) trên `pytest` (`EXERCISE_TARGET=starter`).
    - `solution.py`: pass `12/12` trên browser runner và `12/12` trên `pytest`.
    - `alternatives/01_pure_python_rank.py`: pass `12/12` trên browser runner.
  - `ex02-eval-report`:
    - `starter.py`: pass `0/10` trên browser runner (`tools/pyrunner/runner.py`) và `10 failed` (`0 passed`) trên `pytest` (`EXERCISE_TARGET=starter`).
    - `solution.py`: pass `10/10` trên browser runner và `10/10` trên `pytest`.
    - `alternatives/01_counter_helper.py`: pass `10/10` trên browser runner.

## 4. Kết quả các lệnh kiểm tra (chạy lại sau chỉnh sửa vòng 2)

| Lệnh / Kiểm tra | Kết quả |
| --- | --- |
| `uv run python tools/validate.py --path curriculum/phase-07-llm/p7-09-mini-project-rag` | `OK: 0 error(s), 0 warning(s). Checked 1 lessons, 8 markdown pairs, 3 examples, 2 alternatives, 2 exercises, 16 questions.` (exit 0) |
| `uv run python -m pytest curriculum/phase-07-llm` | `148 passed in 0.30s` (exit 0) |
| `uv run ruff check curriculum/phase-07-llm` | `All checks passed!` (exit 0) |
| Quét regex lệnh cấm trong `curriculum/phase-07-llm/p7-09-mini-project-rag/**/*.py` | `Forbidden pattern matches: 0` |
| `git diff --numstat curriculum/glossary.yaml` | `33	0	curriculum/glossary.yaml` (chỉ có 33 dòng thêm, 0 dòng xóa) |
| `uv run python tools/build_content.py` | `Built 48 lessons, 9 exams, 288 flashcards, 770 questions -> apps\web\src\generated` (exit 0) |
| `git status --short` | `M curriculum/glossary.yaml`, `?? .hallmark/`, `?? curriculum/phase-07-llm/p7-09-mini-project-rag/`, `?? tasks/` |
| Script kiểm tra độ dài MCQ (`L[a] > 1.2 * sum(d) / len(d)`) | `violations: 0` |
| Kiểm tra "không trùng nguyên văn" với `ex01-ingest-retrieve/solution.py` (`retrieve` & `build_index`) | Duyệt AST toàn bộ 11 khối Python trong `lesson.{en,vi}.md` và 3 file `examples/*.py`: `0` hàm tên `retrieve`, `0` hàm có thân AST trùng với `retrieve` hoặc `build_index` của `ex01-ingest-retrieve/solution.py` (`AST / function non-duplication check vs ex01 solution: OK`) |
| Chạy 11 khối Python trong `lesson.en.md` và 11 khối trong `lesson.vi.md` với `-W error` | Tất cả 22/22 khối exit 0, `stderr=""`, code EN/VI khớp hệt nhau ngoài comment, mọi dòng stdout `<= 65` ký tự (`< 70`), Block 4 & Block 5 khớp comment output |
| Chạy `examples/01..03` với `-W error` và so sánh `.out` | Cả 3 file exit 0, `stderr=""`, stdout khớp `.out`, độ dài dòng tối đa: `64`, `64`, `67` ký tự |
| Kiểm tra không còn `OPENAI_API_KEY` trong `p7-09-mini-project-rag` | `OPENAI_API_KEY absence check: OK` |

## 5. Điều còn chưa chắc / Giới hạn

1. **Chưa build/mở web app thực tế:** Theo yêu cầu spec, không chạy `pnpm --filter web build` và không bật dev server. Vì vậy hiển thị giao diện thực tế (Mermaid diagram, Pyodide thực thi trên trình duyệt) chưa được kiểm tra trực tiếp trên browser, mới được kiểm tra thông qua `tools/validate.py`, `tools/build_content.py`, `tools/pyrunner/runner.py` và `tools/pyrunner/tracer.py`.
2. **Thay thế lệnh `grep` trên Windows:** Do môi trường PowerShell không chạy trực tiếp lệnh `grep` dạng Unix, bước quét regex các hàm bị cấm được thực hiện bằng script Python áp dụng đúng biểu thức chính quy trong spec.
3. **Thư mục `.hallmark/` trong `git status --short`:** Xuất hiện sẵn ở trạng thái untracked trong workspace (`?? .hallmark/`), không thuộc phạm vi nhiệm vụ nên không chỉnh sửa hay xóa.
4. **Hành vi `FakeLLM`:** Các chỉ số đánh giá phản ánh hành vi tất định của `FakeLLM(embed_dim=256)` (embedding băm `crc32` kèm bảng từ đồng nghĩa nhỏ và khớp từ nguyên bản khi sinh câu trả lời), không đại diện cho chất lượng ngữ nghĩa của mô hình LLM/embedding thương mại thực tế.
