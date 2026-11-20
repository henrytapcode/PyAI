# Report: m4-p7-05-rag

## 1. Đã làm gì

- Viết mới bài học song ngữ EN/VI `curriculum/phase-07-llm/p7-05-rag/` chạy hoàn toàn trong Pyodide với `FakeLLM(embed_dim=256)` và NumPy:
  - `meta.yaml`: `phase: p7`, `order: 5`, `duration_min: 15`, `tags: [llm, rag, numpy, strings]`, `prerequisites: [p7-04-vector-db]`, `outcomes` khớp `curriculum/syllabus.yaml`, `review_by: "2027-05-01"`, không có `runner: local`.
  - `lesson.en.md` và `lesson.vi.md`: mở đầu không heading, 7 phần nội dung + phần Tóm tắt/Recap, đúng dàn ý spec gồm:
    - Gọi `FakeLLM.chat()` không context ở §1, bảng so sánh `| approach | cost | freshness | good for |`.
    - `chunk_words(text, size, overlap)` ở §2, picture-in-text `text` fence giống hệt EN/VI, khối mời **Visualize** không gọi `FakeLLM`, và bảng tradeoff kích thước chunk.
    - Mermaid `flowchart LR` (8 node, khớp số dòng EN/VI), pipeline RAG hoàn chỉnh trên 3 tài liệu (`refunds.md`, `shipping.md`, `warranty.md` → 6 chunk), và callout `[!NOTE]` giải thích trung thực cơ chế `FakeLLM` so với LLM thật.
    - `build_messages(question, hits)` theo định dạng `Context:\n[1] ...\n[2] ...` trong `system` và callout `[!WARNING]` về prompt injection qua tài liệu.
    - Parse/kiểm biên trích dẫn `[n]` và trace table 3 câu hỏi ở §5.
    - Hai lớp bảo vệ từ chối trả lời ở §6 (`min_score` bỏ qua gọi LLM + model nói `"I don't know based on the provided context."`), nối sang `p7-08-evals`.
    - 4 lỗi thường gặp ở §7 kèm output thật.
  - 3 examples (`01_policy_bot`, `02_chunk_size_compare`, `03_citation_check`) kèm `.out`, `.en.md`, `.vi.md`. Mọi dòng output của `02_chunk_size_compare` đều `<= 22` ký tự (`< 60`).
  - 2 exercises:
    - `ex01-chunk-words` (`kind: fill`): 6 hàm test (tổng 12 test case qua parametrize), `starter.py` fail toàn bộ `12/12` (`0` pass), `solution.py` pass `12/12`.
    - `ex02-answer-with-sources` (`kind: code`): 8 test với spy client kiểm tra skip `chat()` khi điểm `< min_score`, `chunks` rỗng, format `Context:` với `k` dòng `[n]`, lọc `[n]` ngoài biên, giữ thứ tự + bỏ trùng nguồn, tối đa 2 lần gọi `embed()`, và cấu trúc dict trả về. `starter.py` fail `8/8` (`0` pass); `solution.py` và `alternatives/01_two_helpers.py` pass `8/8`.
  - `quiz.yaml`: 16 câu hỏi (7 `mcq`, 3 `output`, 3 `fill`, 3 `parsons`; độ khó 6 dễ / 7 vừa / 3 khó) và 6 flashcard (`p7-05-f01`..`p7-05-f06`).
- Cập nhật `curriculum/glossary.yaml`: chỉ thêm 4 thuật ngữ chưa có (`retrieval`, `chunk overlap`, `grounding`, `citation`); giữ nguyên `RAG`, `chunking`, `hallucination`, `context window` đã có sẵn (`+44/-0` dòng).

## 2. File đã sửa / tạo

- Sửa:
  - `curriculum/glossary.yaml` (chỉ thêm dòng, 0 dòng xóa)
- Tạo mới:
  - `curriculum/phase-07-llm/p7-05-rag/meta.yaml`
  - `curriculum/phase-07-llm/p7-05-rag/lesson.en.md`
  - `curriculum/phase-07-llm/p7-05-rag/lesson.vi.md`
  - `curriculum/phase-07-llm/p7-05-rag/quiz.yaml`
  - `curriculum/phase-07-llm/p7-05-rag/examples/01_policy_bot.{py,out,en.md,vi.md}`
  - `curriculum/phase-07-llm/p7-05-rag/examples/02_chunk_size_compare.{py,out,en.md,vi.md}`
  - `curriculum/phase-07-llm/p7-05-rag/examples/03_citation_check.{py,out,en.md,vi.md}`
  - `curriculum/phase-07-llm/p7-05-rag/exercises/ex01-chunk-words/{exercise.yaml,prompt.en.md,prompt.vi.md,starter.py,solution.py,test_exercise.py}`
  - `curriculum/phase-07-llm/p7-05-rag/exercises/ex02-answer-with-sources/{exercise.yaml,prompt.en.md,prompt.vi.md,starter.py,solution.py,test_exercise.py}`
  - `curriculum/phase-07-llm/p7-05-rag/exercises/ex02-answer-with-sources/alternatives/01_two_helpers.{py,en.md,vi.md}`
  - `tasks/m4-p7-05-rag.report.md`
- Lưu ý: lệnh `uv run python tools/build_content.py` sinh lại các file trong `apps/web/src/generated` (đã nằm trong `.gitignore`).

## 3. Kết quả kiểm tra

- `uv run python tools/validate.py --path curriculum/phase-07-llm/p7-05-rag`
  → `OK: 0 error(s), 0 warning(s). Checked 1 lessons, 7 markdown pairs, 3 examples, 2 exercises, 1 alternatives, 16 questions.`
- `uv run python -m pytest curriculum/phase-07-llm`
  → `80 passed in 0.17s`
- Browser runner (`tools/pyrunner/runner.py`) & `pytest` trên từng bài tập:
  - `ex01-chunk-words`: `starter.py` pass `0/12` (browser `ok=False`, pytest exit `1`); `solution.py` pass `12/12`.
  - `ex02-answer-with-sources`: `starter.py` pass `0/8` (browser `ok=False`, pytest exit `1`); `solution.py` pass `8/8`; `alternatives/01_two_helpers.py` pass `8/8`.
- `uv run ruff check curriculum/phase-07-llm`
  → `All checks passed!`
- Quét pattern cấm (`input(|time\.sleep|requests\.|urllib|open\(|eval\(|astype\(int\)|dtype=int\b`) trên `curriculum/phase-07-llm/p7-05-rag/*.py`: `0` kết quả.
- Chạy tất cả 11 khối Python trong `lesson.en.md` và cả 3 file `examples/*.py` với `-W error`: exit `0`, `stderr` rỗng, output khớp 100%.
- Script kiểm độ dài MCQ trong `quiz.yaml`: `violations: 0` (đáp án đúng dài nhất tuyệt đối: `3/14` cặp EN/VI, tức `1/7` EN và `2/7` VI, dưới ngưỡng `1/3`).
- `tools/pyrunner/tracer.py` cho khối **Visualize** ở §2: `22` steps (`< 600`), `truncated: False`, `error: None`.
- Kiểm `curriculum/glossary.yaml` bằng schema validator trong `tools/validate.py`: `schema ok: True`, `239` thuật ngữ duy nhất; `git diff curriculum/glossary.yaml` chỉ có `+44` dòng, `0` dòng xóa.
- `uv run python tools/build_content.py`: `Built 44 lessons, 9 exams, 264 flashcards, 707 questions -> apps\web\src\generated`.
- Mở thử link `further_reading` bằng `urllib.request`:
  - `https://arxiv.org/abs/2005.11401` → HTTP `200`
  - `https://docs.langchain.com/oss/python/integrations/splitters` → HTTP `200`

## 4. Quirk của fake RAG đã gặp (lưu ý cho p7-08 và p7-09)

1. **Bất đối xứng giữa `embed()` và `_try_rag()`:**
   - `embed()` bỏ đuôi `'s'` với từ `> 3` ký tự (`refunds` → `refund`, `days` → `day`) và có bảng `_SYNONYMS` / `_PHRASE_SYNONYMS` (`"money back"` ↔ `"refund"`, `"laptop"` ↔ `"notebook"`).
   - Ngược lại, `_try_rag()` dùng `_normalize_words()` thuần chữ thường ≥ 3 ký tự, **không** bỏ `'s'` và **không** dùng `_SYNONYMS`. Vì vậy câu hỏi có `"money back"` hay `"refund"` sẽ không khớp từ `"refunds"` trong `_try_rag()`, dù bước retrieval tìm đúng chunk. Khi thiết kế tập eval cho `p7-08` và mini-project `p7-09`, cần chú ý câu hỏi dùng đúng dạng từ với chunk nếu muốn `FakeLLM` (không script) trả câu đầu thay vì `"I don't know based on the provided context."`.
2. **Đếm cả stopword (`>= 3` ký tự):**
   - Các từ như `"the"`, `"and"`, `"are"`, `"for"`, `"with"`, `"how"`, `"does"`, `"what"` đều được đếm vào overlap. Nếu chunk dài có nhiều từ chức năng phổ thông (`"for"`, `"and"`, `"with"`, `"are"`), câu hỏi chỉ trùng stopword + 1 từ khóa vẫn có thể vượt ngưỡng `>= 2` từ chung.
3. **Chỉ trả về câu đầu tiên (`_first_sentence`):**
   - Nếu câu hỏi nhắm vào câu thứ 2 của chunk (ví dụ `"Is express shipping free on weekends?"` khi câu 1 là `"Standard shipping delivers orders in three to five business days."` và câu 2 nói về express shipping), `_try_rag()` vẫn trả câu 1 kèm `[n]` vì chung từ `"shipping"` và `"express"`. Cho `p7-08`/`p7-09`, mỗi chunk nên để ý chính nằm ngay câu đầu, hoặc chia nhỏ theo câu/ý, hoặc dùng `FakeLLM(script=...)` khi kiểm tra tổng hợp đa câu/đa chunk.
4. **Hành vi hòa điểm trong `_try_rag()`:**
   - `_try_rag()` dùng `if overlap > best_overlap:` (strict `>`), nên nếu `[1]` và `[2]` có cùng số từ chung, `[1]` luôn thắng. Đặt chunk điểm retrieval cao nhất ở `[1]` tự nhiên phù hợp với hành vi này.

## 5. Điều còn chưa chắc

- Nội dung bài và các ví dụ/bài tập đã được kiểm tra bằng CPython (`tools/validate.py`, `tools/pyrunner/runner.py`, `tools/pyrunner/tracer.py`, `pytest`), chưa mở trình duyệt để chạy trực tiếp trong WebAssembly Pyodide của app web (vì không chạy dev server theo yêu cầu).
