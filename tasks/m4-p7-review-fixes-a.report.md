# Báo cáo thực hiện `tasks/m4-p7-review-fixes-a.md`

## 1. Đã làm gì

Đã thực hiện toàn bộ các hạng mục B1–B2, M1–M5 và m1–m13 cho 5 bài học đầu Phase 7 (`p7-01-llm-api` .. `p7-05-rag`) theo đúng spec:

- **B1 (Chống chép bài mẫu trong 3 bài tập):**
  - `p7-05-rag`: Đổi tên thư mục `ex01-chunk-words` thành `ex01-chunk-paragraphs` (giữ `id: p7-05-ex01`), chuyển đề sang `chunk_paragraphs(text: str, max_words: int) -> list[str]` (`kind: fill`) gộp các đoạn văn tách bởi `"\n\n"` theo ngưỡng `max_words`, giữ nguyên đoạn đơn lẻ vượt ngưỡng, kiểm tra biên `<= max_words`, chuỗi trắng `[]`, và `ValueError` khi `max_words <= 0`. Bổ sung giới thiệu paragraph chunking ở cuối §2 `lesson.{en,vi}.md`.
  - `p7-04-vector-db`: Cập nhật `ex02-mini-store` (`MiniStore`) sang `add()` có hành vi **upsert** tại chỗ cho ID đã có (vẫn raise `ValueError` nếu trùng ID trong cùng lô) và `search(..., where=...)` hỗ trợ lọc giá trị dạng `list` (kiểm tra `key in meta` rồi so khớp phần tử nằm trong danh sách). Cập nhật `solution.py` (dùng `_id_to_idx: dict[str, int]` để AST không trùng với `VectorStore`), `alternatives/01_list_of_records.py`, `prompt.{en,vi}.md`, `starter.py`, `test_exercise.py`, `exercise.yaml` và thêm câu giới thiệu ở cuối §4 `lesson.{en,vi}.md`.
  - `p7-02-structured-output`: Cập nhật `ex01-check-reply` (`check_reply`, `kind: fill`) thêm luật `enum` (`f"{key}: must be one of {allowed}"`), mở khóa lại các chỗ trống cơ bản của §3 và chỉ chừa `___` ở `spec.get(___, "")` cùng 3 chỗ trống mới cho nhánh `enum`, kèm 3 test case `enum` mới trong `test_exercise.py`.

- **B2 (Hint 3 tầng tăng dần cho toàn bộ 10 bài tập, EN + VI):**
  - Chuẩn hóa đủ 3 tầng cho mọi `exercise.yaml` trong `p7-01..p7-05`: Hint 1 nêu ý tưởng + mục `§` + ví dụ vào/ra; Hint 2 nêu từng bước bằng lời thường đánh số (không đưa biểu thức Python hoàn chỉnh); Hint 3 chỉ đưa khung hoặc phần khó nhất với `...` ở các chỗ lõi (bài `fill` không điền giúp các chỗ trống khác).
  - Đặc biệt đã thu gọn các Hint 3 từng lộ gần hết lời giải tại `p7-01` (`ex01`, `ex02`), `p7-02` (`ex01`, `ex02`), `p7-03` (`ex01`, `ex02`), `p7-04` (`ex01`, `ex02`), `p7-05` (`ex01`, `ex02`).

- **M1–M5 & m1–m13:**
  - **M1:** Giải thích regex `r"\[(\d+)\]"`, escape `\[`/`\]`, group `(\d+)` và lý do `re.findall` trả về `list[str]` kèm snippet Python chạy thật tại `p7-05-rag/lesson.{en,vi}.md` §5.
  - **M2:** Giải thích `__post_init__` tại `p7-01` (`examples/02_chat_session.{en,vi}.md`), `p7-02` (`lesson.{en,vi}.md` §4), và bổ sung thuật ngữ `__post_init__` (append-only, 11 dòng thêm, 0 dòng xóa) vào `curriculum/glossary.yaml`.
  - **M3:** Sửa giải thích `overlap` ở `p7-05-rag/lesson.{en,vi}.md` §2 & §7 để không khẳng định sai rằng mọi câu dài đều được giữ nguyên khi `overlap` nhỏ.
  - **M4:** Thêm `test_estimate_cost_rounds_beyond_six_decimals` vào `p7-01/exercises/ex02-reliable-call/test_exercise.py` (`Usage(333, 777, 1110)`, `0.35`, `1.25` -> `0.001088`); đã xác minh bằng mutant bỏ `round(..., 6)` làm test mới fail.
  - **M5:** Viết lại các đáp án nhiễu lộ liễu (vẫn giữ nguyên `answer` và độ dài cân bằng) ở `p7-03` (`q01`, `q03`), `p7-04` (`q01`, `q07`, `q09`, `q10`), `p7-05` (`q08`, `q14`).
  - **m1:** Sửa các tham chiếu số dòng bị lệch trong `examples/*.{en,vi}.md` ở `p7-01` (`01`, `02`, `03`), `p7-02` (`01`, `02`, `03`), `p7-03` (`01`), `p7-04` (`01`, `03`), `p7-05` (`01`, `02`).
  - **m2–m13:** Đảo `echo '.env' >> .gitignore` lên trước tại `p7-01`; sửa TIP `temperature=0` ở `p7-01` `lesson` & `q09`; thêm NOTE `FakeLLM` + `strict=True` Pydantic tại `p7-02`; bỏ `if not isinstance(data, dict)` thừa ở `p7-02 ex02`; thay `meta.get(key)` bằng `key in meta and meta[key] == val` ở `p7-04` (`lesson`, `examples`, `ex02`); sửa NOTE pre/post filter tại `p7-04`; thêm lưu ý `cosine > 0` với embedding thật ở `p7-03`; sửa prose Mistake 2 (`step <= 0`) tại `p7-05`; đổi tên `build_messages` thành `build_rag_messages` và thêm câu nối `Hit` tại `p7-05` §4; sửa Hint `RuntimeError -> ValueError` (`p7-01 ex02`) và gọi đúng tên `chunk_paragraphs` (`p7-05 ex01`); sửa thuật ngữ tiếng Việt tự nhiên (`True`/`False`, `bool`, `` `0.0` ``) ở `p7-02 ex01`, `p7-03 ex01`, `p7-04 ex01`; sửa Mistake 1 trong `p7-04/lesson.{en,vi}.md` bằng lệnh gọi `VectorStore.add` trùng lặp thực thi được.

## 2. Các file đã sửa / đổi tên

Chỉ sửa các file trong `curriculum/glossary.yaml` (append-only), `curriculum/phase-07-llm/p7-01-llm-api/**` .. `p7-05-rag/**`, và tạo báo cáo này:

- `curriculum/glossary.yaml` (`+11/-0`)
- `curriculum/phase-07-llm/p7-01-llm-api/`: `lesson.{en,vi}.md`, `quiz.yaml`, `examples/{01_support_reply,02_chat_session,03_retry_with_backoff}.{en,vi}.md`, `exercises/ex01-build-messages/exercise.yaml`, `exercises/ex02-reliable-call/{exercise.yaml,test_exercise.py}`
- `curriculum/phase-07-llm/p7-02-structured-output/`: `lesson.{en,vi}.md`, `examples/{01_ticket_extractor,02_robust_parser,03_retry_then_fallback}.{en,vi}.md`, `exercises/ex01-check-reply/{exercise.yaml,prompt.{en,vi}.md,solution.py,starter.py,test_exercise.py}`, `exercises/ex02-structured-call/{exercise.yaml,prompt.{en,vi}.md,solution.py,alternatives/01_raw_decode.py}`
- `curriculum/phase-07-llm/p7-03-embeddings/`: `lesson.{en,vi}.md`, `quiz.yaml`, `examples/01_faq_search.{en,vi}.md`, `exercises/ex01-cosine/exercise.yaml`, `exercises/ex02-top-k/exercise.yaml`
- `curriculum/phase-07-llm/p7-04-vector-db/`: `lesson.{en,vi}.md`, `quiz.yaml`, `examples/{01_faq_store.py,01_faq_store.{en,vi}.md,02_filter_before_topk.py,03_save_and_reload.{en,vi}.md}`, `exercises/ex01-metadata-filter/exercise.yaml`, `exercises/ex02-mini-store/{exercise.yaml,prompt.{en,vi}.md,solution.py,starter.py,test_exercise.py,alternatives/01_list_of_records.py}`
- `curriculum/phase-07-llm/p7-05-rag/`: `lesson.{en,vi}.md`, `quiz.yaml`, `examples/{01_policy_bot,02_chunk_size_compare}.{en,vi}.md`, `exercises/ex01-chunk-words/` (đã chuyển sang `exercises/ex01-chunk-paragraphs/{exercise.yaml,prompt.{en,vi}.md,solution.py,starter.py,test_exercise.py}`), `exercises/ex02-answer-with-sources/exercise.yaml`
- `tasks/m4-p7-review-fixes-a.report.md` (file này)

## 3. Kết quả các lệnh kiểm tra (chạy sau lần sửa cuối cùng)

1. `uv run python tools/validate.py --path` cho từng bài `p7-01-llm-api` .. `p7-05-rag` (lưu ý `tools/validate.py` chỉ nhận 1 đường dẫn mỗi lần gọi nên chạy vòng lặp cả 5 bài):
   - `p7-01-llm-api`: `OK: 0 error(s), 0 warning(s). Checked 1 lessons, 7 markdown pairs, 3 examples, 2 exercises, 1 alternatives, 16 questions.`
   - `p7-02-structured-output`: `OK: 0 error(s), 0 warning(s). Checked 1 lessons, 7 markdown pairs, 3 examples, 2 exercises, 1 alternatives, 16 questions.`
   - `p7-03-embeddings`: `OK: 0 error(s), 0 warning(s). Checked 1 lessons, 7 markdown pairs, 3 examples, 2 exercises, 1 alternatives, 16 questions.`
   - `p7-04-vector-db`: `OK: 0 error(s), 0 warning(s). Checked 1 lessons, 7 markdown pairs, 3 examples, 2 exercises, 1 alternatives, 16 questions.`
   - `p7-05-rag`: `OK: 0 error(s), 0 warning(s). Checked 1 lessons, 7 markdown pairs, 3 examples, 2 exercises, 1 alternatives, 16 questions.`
2. `uv run python -m pytest curriculum/phase-07-llm -q -p no:warnings`:
   - `PYTEST_EXIT=0` (`172 passed in 0.39s` khi chạy `-v -p no:warnings` trước đó và `PYTEST_EXIT=0` với 172 test chấm pass khi chạy lại sau lần sửa cuối).
3. `uv run ruff check curriculum/phase-07-llm` (và bản giới hạn `p7-01..p7-05`):
   - `All checks passed!` (`RUFF_EXIT=0`). (Lưu ý: chạy `uv run ruff check` không đối số trên toàn repo vẫn có các lỗi `E501`/`E713` có sẵn từ trước trong `tools/build_content.py` và `tools/validate.py`, nằm ngoài phạm vi file được phép sửa.)
4. `git diff --numstat curriculum/glossary.yaml`:
   - `11	0	curriculum/glossary.yaml` (0 dòng xóa).
5. Script kiểm tra độ dài phương án MCQ trên `p7-01..p7-05/quiz.yaml`:
   - `p7-01-llm-api`: `mcqs=7 violations=0 longest-unique=3/14 (threshold=4.7)`
   - `p7-02-structured-output`: `mcqs=6 violations=0 longest-unique=1/12 (threshold=4.0)`
   - `p7-03-embeddings`: `mcqs=8 violations=0 longest-unique=3/16 (threshold=5.3)`
   - `p7-04-vector-db`: `mcqs=8 violations=0 longest-unique=0/16 (threshold=5.3)`
   - `p7-05-rag`: `mcqs=7 violations=0 longest-unique=4/14 (threshold=4.7)`
6. Kiểm tra `starter.py` fail toàn bộ test, `alternatives/` pass, và mutant M4 (chạy trong `TemporaryDirectory`):
   - `ex01-check-reply` starter: `9 failed in 0.08s` (0 passed)
   - `ex02-mini-store` starter: `11 failed in 0.15s` (0 passed); alternative `01_list_of_records.py`: `11 passed in 0.08s`
   - `ex01-chunk-paragraphs` starter: `8 failed in 0.08s` (0 passed)
   - Mutant M4 (`p7-01 ex02` bỏ `round(..., 6)`): `1 failed, 7 passed in 0.13s`
7. Kiểm tra trùng AST giữa `solution.py`/`alternatives/` của 3 bài mới (B1) với toàn bộ hàm/class trong `lesson.*.md` & `examples/*.py`:
   - Cả 4 file (`p7-02 ex01/solution.py`, `p7-04 ex02/solution.py`, `p7-04 ex02/alternatives/01_list_of_records.py`, `p7-05 ex01/solution.py`) đều cho `ast_dups=0`.
8. Chạy mọi khối code Python trong `lesson.{en,vi}.md` của `p7-01..p7-05` bằng `python -W error`:
   - `ALL EN + VI lesson python blocks passed python -W error with empty stderr`.

## 4. Điều còn chưa chắc

- Đã chạy `starter`-fail check trên 3 bài thay đổi trọng tâm (`p7-02 ex01`, `p7-04 ex02`, `p7-05 ex01`), chưa chạy lại riêng `starter.py` trong `TemporaryDirectory` cho các bài chỉ sửa Hint 3 hoặc test bổ sung (`p7-01 ex01`, `p7-01 ex02`, `p7-02 ex02`, `p7-03 ex01`, `p7-03 ex02`, `p7-04 ex01`, `p7-05 ex02`), nhưng `starter.py` của các bài đó không bị sửa trừ doc/blank không đổi và `validate.py` đã xác nhận toàn bộ các bài đều đạt.
- Việc đổi tên thư mục `p7-05-rag/exercises/ex01-chunk-words` sang `ex01-chunk-paragraphs` (giữ `id: p7-05-ex01`): `validate.py` và `pytest` đều không tham chiếu cứng tên thư mục cũ; tuy nhiên chưa khởi động web app/build script (`apps/**`, `tools/build_content.py`) theo ràng buộc không sửa ngoài scope và không chạy dev server.
