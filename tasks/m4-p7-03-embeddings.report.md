# Báo cáo: M4 bước 13 — bài `p7-03-embeddings`

## 1. Đã làm gì

Tiếp nối phần file đã có sẵn từ lần chạy trước, đã rà soát toàn bộ nội dung bài học `curriculum/phase-07-llm/p7-03-embeddings/` theo `tasks/m4-p7-03-embeddings.md` và `docs/CONTENT_GUIDE.md`, kiểm tra hoạt động thực tế của mọi khối code, ví dụ, bài tập, quiz và các link tham khảo, rồi tổng hợp kết quả kiểm tra:

- **Lesson (`lesson.en.md`, `lesson.vi.md`):**
  - Mở đầu không heading dẫn vào bài toán `"I can't sign in"` vs `"reset your password"` và nối với semantic search, RAG (`p7-05-rag`), vector DB (`p7-04-vector-db`).
  - Đủ 8 phần theo dàn ý:
    1. Văn bản thành vector (`FakeLLM().embed()`, picture in text, callout `[!NOTE]` về bag-of-words + bảng đồng nghĩa của fake client vs neural embeddings `p6-03-huggingface`).
    2. Cosine similarity (`p5-01-math-bridge`), khối 3 chiều tính tay mời **Visualize**, chứng minh vector đã chuẩn hóa L2 có `norm == 1.0` và `a @ b == cosine()`, bảng thang đo cosine.
    3. Keyword search vs semantic search (`"affordable automobile"` khớp `"cheap car rental in Hanoi"`, giải thích hash collision và lý do dùng `embed_dim=256`, bảng so sánh).
    4. Xếp hạng top-k (`D @ q`, `np.argsort(-scores, kind="stable")[:k]`, Mermaid `flowchart LR` 6 node cùng số dòng EN/VI, trace table, nhấn mạnh embed tài liệu một lần và nối sang `p7-04-vector-db`).
    5. Ngưỡng `min_score = 0.3` và `"no good match"`, chọn ngưỡng bằng tập mẫu có nhãn (`p7-08-evals`).
    6. Chi phí & batching với `count_tokens` và callout `[!TIP]` lưu trữ embedding.
    7. Lỗi thường gặp (4 lỗi với thông báo thật: truyền chuỗi đơn `TypeError`, lệch `embed_dim` `ValueError`, dot product chưa chuẩn hóa, `argsort` tăng dần).
    8. Recap / Tóm tắt (5 gạch đầu dòng).
  - Toàn bộ 11 khối Python chạy sạch với `python -W error`, output khớp 100% với comment `#` minh họa, không in NumPy scalar thô hay vector dài.
  - Khối mời **Visualize** (phần 2, tính tay cosine trên vector 3 chiều): kiểm tra bằng `tools/pyrunner/tracer.py` cho kết quả **21 step** (`truncated: False`, `error: None`, stdout `'cosine: 0.96\n'`), dưới xa giới hạn 600 step.
- **Examples (3):**
  - `01_faq_search`: 6 FAQ, 3 câu hỏi khách, top-1 với `min_score = 0.3`, câu lạc đề in `"no good match"`.
  - `02_keyword_vs_semantic`: bảng so sánh `kw` vs `cos` cho 3 query × 4 tài liệu, mỗi dòng tối đa 38 ký tự (< 60 ký tự).
  - `03_dedupe_tickets`: dùng `matrix @ matrix.T` và tam giác trên (`j > i`) để tìm cặp ticket trùng (`THRESHOLD = 0.5`).
- **Exercises (2):**
  - `ex01-cosine` (`kind: fill`): `cosine_sim(a, b)` bằng NumPy, làm tròn 3 chữ số, vector 0 trả `0.0`, lệch độ dài raise `ValueError`. Starter import sạch và fail **6/6 test** (0 pass). Solution pass 6/6 test.
  - `ex02-top-k` (`kind: code`): `top_k(query, docs, client, k=2, min_score=0.0)` trả `list[tuple[int, float]]` (kiểu `float` Python), tie-break theo index nhỏ hơn, lọc `min_score`, không gọi `embed` khi `docs` rỗng, spy client kiểm batch call. Starter import sạch và fail **8/8 test** (0 pass). Solution và `alternatives/01_sorted_loop.py` đều pass 8/8 test.
  - Hint 3 tầng của cả 2 bài đúng quy tắc (hint 2 chỉ bằng lời, hint 3 là skeleton chừa một `...` ở dòng cốt lõi).
- **Quiz (`quiz.yaml`):**
  - 16 câu hỏi (`mcq`: 8, `output`: 3, `fill`: 3, `parsons`: 2; độ khó 1: 5, 2: 8, 3: 3) và 6 flashcard.
  - Script kiểm tra độ dài MCQ: `violations: 0`; phương án đúng dài nhất duy nhất ở 2/8 câu MCQ (`0.25 <= 1/3`) cho cả EN và VI.
- **Glossary (`curriculum/glossary.yaml`):**
  - `embedding`, `vector`, `cosine similarity` đã có sẵn từ trước; chỉ bổ sung 3 thuật ngữ còn thiếu là `semantic search`, `top-k`, `normalize`.

## 2. `embed_dim` đã dùng ở từng chỗ

- `lesson.en.md` / `lesson.vi.md`:
  - §1 (minh họa output `embed()`): `FakeLLM()` mặc định `embed_dim=64`.
  - §2 (kiểm chứng `norm(v1)` và `a @ b == cosine()`): `FakeLLM()` mặc định `embed_dim=64`.
  - §3, §4, §5, §6 (keyword vs semantic, top-k ranking, threshold, batching): `FakeLLM(embed_dim=256)` để tránh hash collision.
  - §7 lỗi 1 (single string `TypeError`): `FakeLLM()` mặc định `embed_dim=64`.
  - §7 lỗi 2 (shape mismatch `ValueError`): `FakeLLM(embed_dim=64)` vs `FakeLLM(embed_dim=256)`, phần fix dùng `FakeLLM(embed_dim=256)`.
- `examples/` (`01_faq_search.py`, `02_keyword_vs_semantic.py`, `03_dedupe_tickets.py`): tất cả dùng `FakeLLM(embed_dim=256)`.
- `exercises/ex02-top-k/test_exercise.py` & `prompt.*.md`: dùng `FakeLLM(embed_dim=256)` (kể cả `_SpyClient(embed_dim=256)`).
- `quiz.yaml`: `q02`, `q12`, `q16` dùng `FakeLLM(embed_dim=256)`; `q05` (parsons) dùng `FakeLLM(embed_dim=256)`.

## 3. Link `further_reading` đã kiểm tra

Đã mở kiểm tra HTTP thực tế bằng Python `urllib.request`:
- `https://developers.google.com/machine-learning/crash-course/embeddings` -> HTTP `200` (không redirect lỗi).
- `https://numpy.org/doc/stable/reference/generated/numpy.argsort.html` -> HTTP `200` (không redirect lỗi).

## 4. Hành vi đáng chú ý của `pyai_llm`

Khi đọc `packages/pyai_llm/pyai_llm.py` (`_embed_one` và `embed`), không sửa code thư viện, ghi nhận các đặc điểm ảnh hưởng tới thiết kế bài học:
- `_embed_one` chỉ tách từ theo `\w+`, chuyển chữ thường, bỏ `s` cuối với từ dài hơn 3 ký tự, áp dụng `_PHRASE_SYNONYMS` (`"money back"` -> `"refund"`) và `_SYNONYMS` (10 nhóm từ đồng nghĩa), rồi băm `zlib.crc32` modulo `embed_dim`, chuẩn hóa L2 và làm tròn 6 chữ số.
- Vì tất cả trọng số đếm từ đều dương (`+1.0`), cosine của `FakeLLM().embed()` luôn nằm trong `[0, 1]`, không bao giờ âm như embedding neural thật (đã ghi rõ trong bảng §2).
- Với `embed_dim=64` mặc định, xác suất va chạm băm giữa các từ khác nhau đáng kể (có thể tạo điểm tương đồng giả trên câu không liên quan), nên các ví dụ và bài tập xếp hạng đều chọn `embed_dim=256` và giải thích rõ trong bài.

## 5. File đã sửa / tạo

- Tạo mới thư mục `curriculum/phase-07-llm/p7-03-embeddings/` gồm:
  - `meta.yaml`, `lesson.en.md`, `lesson.vi.md`, `quiz.yaml`
  - `examples/01_faq_search.{py,out,en.md,vi.md}`
  - `examples/02_keyword_vs_semantic.{py,out,en.md,vi.md}`
  - `examples/03_dedupe_tickets.{py,out,en.md,vi.md}`
  - `exercises/ex01-cosine/{exercise.yaml,prompt.en.md,prompt.vi.md,starter.py,solution.py,test_exercise.py}`
  - `exercises/ex02-top-k/{exercise.yaml,prompt.en.md,prompt.vi.md,starter.py,solution.py,test_exercise.py}`
  - `exercises/ex02-top-k/alternatives/01_sorted_loop.{py,en.md,vi.md}`
- Sửa `curriculum/glossary.yaml`: chỉ thêm 3 thuật ngữ mới (`semantic search`, `top-k`, `normalize`).
- Tạo báo cáo `tasks/m4-p7-03-embeddings.report.md`.
- Lưu ý: khi chạy `uv run python tools/build_content.py`, tool ghi ra thư mục `apps/web/src/generated` (đã gitignore nên không hiện trong `git status --short`).

## 6. Kết quả lệnh kiểm tra

- `uv run python tools/validate.py --path curriculum/phase-07-llm/p7-03-embeddings` -> **PASS**: `OK: 0 error(s), 0 warning(s). Checked 1 lessons, 7 markdown pairs, 3 examples, 2 exercises, 1 alternatives, 16 questions.`
- `uv run python -m pytest curriculum/phase-07-llm` -> **PASS**: `43 passed in 0.13s`
- `uv run python -m pytest -W error curriculum/phase-07-llm` -> **PASS**: `43 passed in 0.13s`
- `uv run ruff check curriculum/phase-07-llm` -> **PASS**: `All checks passed!`
- Kiểm tra pattern cấm (`input(|time\.sleep|requests\.|urllib|open\(|eval\(|astype\(int\)|dtype=int\b`) trên mọi `.py` trong `curriculum/phase-07-llm/p7-03-embeddings` bằng Python regex (PowerShell không có `grep`) -> **PASS**: `[]` (0 kết quả).
- Kiểm tra `starter.py` với `test_exercise.py` -> **PASS (đúng kỳ vọng fail 100%)**:
  - `ex01-cosine`: `6 failed in 0.21s` (0 passed)
  - `ex02-top-k`: `8 failed in 0.19s` (0 passed)
- Kiểm tra `-W error` cho 11 khối code trong `lesson.en.md` / `lesson.vi.md`, 3 file `examples/*.py` (so khớp `.out`), và toàn bộ code `output`/`fill`/`parsons` trong `quiz.yaml` -> **PASS**: exit code `0`, `stderr == ''`, output khớp hoàn toàn.
- Script kiểm tra độ dài MCQ -> **PASS**: `violations: 0`, phương án đúng dài nhất duy nhất `2/8` (`0.25`) ở cả `en` và `vi`.
- `uv run python tools/build_content.py` -> **PASS**: `Built 42 lessons, 9 exams, 252 flashcards, 675 questions -> apps\web\src\generated`
- `git status --short`:
  ```text
   M curriculum/glossary.yaml
  ?? .hallmark/
  ?? curriculum/phase-07-llm/p7-03-embeddings/
  ?? tasks/
  ```
  (Ghi chú: `.hallmark/` và `tasks/` là thư mục sẵn có trên workspace từ trước, không phải do bài này sửa.)

## 7. Điều còn chưa chắc

- Chưa chạy `pnpm --filter web build` và chưa khởi động frontend/Pyodide browser thực tế (bị cấm theo spec của task), nên giao diện web render Markdown/Mermaid và môi trường Pyodide wasm32 thực tế trên trình duyệt chưa được kiểm thử trực tiếp; mọi kiểm tra Pyodide runner và schema được xác minh thông qua `tools/validate.py` và `tools/pyrunner/tracer.py`.

## Vòng 2

Đã xử lý đúng 2 điểm trong `## Feedback vòng 2` (không chỉnh sửa các phần khác):

1. **Hint 3 lộ dòng cốt lõi** (`exercises/ex01-cosine/exercise.yaml`, `exercises/ex02-top-k/exercise.yaml` — cả `en` và `vi`):
   - Xóa câu mô tả phép tính ngay sau fence Python trong hint 3 ở cả hai bài, thay bằng câu dẫn ngắn chỉ về section lý thuyết (`Look back at §2.` / `Xem lại §2.` cho `ex01-cosine`; `Look back at §4.` / `Xem lại §4.` cho `ex02-top-k`), giữ nguyên skeleton và một dấu `...`.
2. **Thông báo lỗi NumPy quá dài** (`lesson.en.md` và `lesson.vi.md`, §7 lỗi 2):
   - Đổi `print("error:", err)` thành `print("error:", type(err).__name__, "- shapes", v64.shape, v256.shape)` ở cả `lesson.en.md` và `lesson.vi.md`.
   - Chạy thực tế với `-W error` và cập nhật comment output thành `# error: ValueError - shapes (64,) (256,)`. Code giữa EN và VI khớp 100% (chỉ khác comment).

### Kiểm tra lại sau sửa vòng 2
- `uv run python tools/validate.py --path curriculum/phase-07-llm/p7-03-embeddings` -> **PASS**: `OK: 0 error(s), 0 warning(s). Checked 1 lessons, 7 markdown pairs, 3 examples, 2 exercises, 1 alternatives, 16 questions.`
- `uv run python -m pytest curriculum/phase-07-llm` -> **PASS**: `43 passed in 0.14s`
- `uv run ruff check curriculum/phase-07-llm` -> **PASS**: `All checks passed!`
- `uv run python tools/build_content.py` -> **PASS**: `Built 42 lessons, 9 exams, 252 flashcards, 675 questions -> apps\web\src\generated`
- Kiểm tra toàn bộ 11 khối Python trong `lesson.en.md` / `lesson.vi.md` chạy với `-W error` (`code_diffs: []`, exit `0`, `stderr` rỗng), script độ dài MCQ `violations: 0`, kiểm tra pattern cấm trên `.py` ra `[]`.
