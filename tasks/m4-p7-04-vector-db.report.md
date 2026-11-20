# Báo cáo hoàn thành: `m4-p7-04-vector-db`

## 1. Đã làm gì

- Tạo bài học song ngữ EN/VI `curriculum/phase-07-llm/p7-04-vector-db/` theo `docs/CONTENT_GUIDE.md` và spec `tasks/m4-p7-04-vector-db.md` (chạy hoàn toàn trong Pyodide, dùng `FakeLLM(embed_dim=256)` và NumPy, không ghi file, không gọi mạng):
  - `meta.yaml`: `id: p7-04-vector-db`, `phase: p7`, `order: 4`, `tags: [llm, numpy, oop]`, `prerequisites: [p7-03-embeddings, p4-01-numpy]`, `duration_min: 14`, `review_by: "2027-05-01"`, `outcomes` khớp `curriculum/syllabus.yaml`, kèm 2 link `further_reading` đã kiểm tra HTTP 200.
  - `lesson.en.md` và `lesson.vi.md`: đủ 8 phần theo dàn ý (mở bài không heading, §1 lỗi lệch index khi dùng 2 list rời + bảng `text` bản ghi, §2 `VectorStore` + `Hit` + Mermaid `flowchart LR` 8 node, §3 metadata pre-filter vs post-filter + trace table + khối mời **Visualize** trên store 2-D viết tay, §4 `delete` + `upsert`, §5 `to_json` / `from_json` + `[!TIP]`, §6 ước lượng `n × dim` + bảng so sánh NumPy store / FAISS / Chroma / pgvector / Qdrant + `[!NOTE]`, §7 4 lỗi thường gặp với thông báo chạy thật, §8 Tóm tắt).
  - 3 examples (`examples/`):
    - `01_faq_store` (`.py`, `.out`, `.en.md`, `.vi.md`): 8 chunk FAQ song ngữ có metadata `topic` và `lang`, 3 truy vấn (1 truy vấn có `where`), mọi dòng in `< 70` ký tự.
    - `02_filter_before_topk` (`.py`, `.out`, `.en.md`, `.vi.md`): so sánh post-filter (ra `0` hit) và pre-filter (ra đủ `k = 2` hit).
    - `03_save_and_reload` (`.py`, `.out`, `.en.md`, `.vi.md`): `to_json()`, `from_json()` với `CountingClient` chứng minh `embed_calls == 0` khi nạp lại, xóa `c2`, tìm lại kiểm tra chỉ số còn nguyên.
  - 2 exercises (`exercises/`):
    - `ex01-metadata-filter` (`kind: fill`): `matches` và `filter_indexes`, 8 test case (dùng `@pytest.mark.parametrize`), hint 3 tầng đúng luật.
    - `ex02-mini-store` (`kind: code`): `MiniStore(client)` với `add`, `search`, `delete`, `__len__`, 9 test (gồm spy client đếm đúng 1 lần `embed` mỗi `add`), hint 3 tầng đúng luật, kèm `alternatives/01_list_of_records.py` (lưu `list[_Record]` dataclass và tính dot product bằng vòng lặp) + `.en.md`/`.vi.md`.
  - `quiz.yaml`: 16 câu (8 `mcq`, 3 `output`, 3 `fill`, 2 `parsons`; độ khó 5 dễ, 8 vừa, 3 khó) và 6 flashcard (`p7-04-f01` … `p7-04-f06`).
- Cập nhật `curriculum/glossary.yaml`: chỉ **thêm** 4 thuật ngữ chưa có (`chunk`, `metadata`, `metadata filter`, `approximate nearest neighbor (ANN)`). Bỏ qua `vector database` và `index` vì đã tồn tại.

## 2. File đã tạo / sửa

- Tạo mới:
  - `curriculum/phase-07-llm/p7-04-vector-db/meta.yaml`
  - `curriculum/phase-07-llm/p7-04-vector-db/lesson.en.md`
  - `curriculum/phase-07-llm/p7-04-vector-db/lesson.vi.md`
  - `curriculum/phase-07-llm/p7-04-vector-db/quiz.yaml`
  - `curriculum/phase-07-llm/p7-04-vector-db/examples/01_faq_store.{py,out,en.md,vi.md}`
  - `curriculum/phase-07-llm/p7-04-vector-db/examples/02_filter_before_topk.{py,out,en.md,vi.md}`
  - `curriculum/phase-07-llm/p7-04-vector-db/examples/03_save_and_reload.{py,out,en.md,vi.md}`
  - `curriculum/phase-07-llm/p7-04-vector-db/exercises/ex01-metadata-filter/{exercise.yaml,prompt.en.md,prompt.vi.md,starter.py,solution.py,test_exercise.py}`
  - `curriculum/phase-07-llm/p7-04-vector-db/exercises/ex02-mini-store/{exercise.yaml,prompt.en.md,prompt.vi.md,starter.py,solution.py,test_exercise.py}`
  - `curriculum/phase-07-llm/p7-04-vector-db/exercises/ex02-mini-store/alternatives/01_list_of_records.{py,en.md,vi.md}`
  - `tasks/m4-p7-04-vector-db.report.md`
- Sửa đổi:
  - `curriculum/glossary.yaml`
- Sinh tự động (gitignore, bởi `tools/build_content.py`): `apps/web/src/generated/`.

## 3. Kết quả kiểm tra

| Kiểm tra | Kết quả |
|---|---|
| `uv run python tools/validate.py --path curriculum/phase-07-llm/p7-04-vector-db` | `OK: 0 error(s), 0 warning(s). Checked 1 lessons, 7 markdown pairs, 3 examples, 2 exercises, 1 alternatives, 16 questions.` |
| `uv run python tools/validate.py --fast` (kiểm tra thêm `glossary.yaml`) | `OK: 0 error(s), 0 warning(s). Checked 43 lessons, 329 markdown pairs, 127 examples, 86 exercises, 73 alternatives, 846 questions, 9 exams, 1 portfolio, 1 glossary, 1 interview.` |
| `uv run python -m pytest curriculum/phase-07-llm` | `60 passed in 0.16s` (bao gồm 8 test của `ex01` và 9 test của `ex02`) |
| Kiểm tra `starter.py` từng bài tập bằng `EXERCISE_TARGET=starter` | `ex01-metadata-filter`: `8 failed` (`0 passed`); `ex02-mini-store`: `9 failed` (`0 passed`) |
| `uv run ruff check curriculum/phase-07-llm` | `All checks passed!` |
| Kiểm tra pattern cấm (`input(`, `time.sleep`, `requests.`, `urllib`, `open(`, `eval(`, `astype(int)`, `dtype=int`, `faiss`, `chromadb`, `qdrant`) trên `*.py` trong `p7-04-vector-db` | `0` kết quả khớp |
| Script kiểm tra độ dài MCQ trên `quiz.yaml` | `violations: 0` (`mcq: 8`, đáp án đúng là phương án dài nhất duy nhất: `longest_en: 1`, `longest_vi: 1`, đều `<= 8/3`) |
| Chạy `-W error` cho 11/11 khối python trong `lesson.en.md` & `lesson.vi.md`, 3/3 examples, 8/8 câu `output`/`fill`/`parsons` trong `quiz.yaml` | Toàn bộ exit `0`, stderr rỗng, stdout khớp chính xác |
| Khối **Visualize** (§3) kiểm tra bằng `tools/pyrunner/tracer.py` | `58` step (`< 600`), `truncated: False`, `error: None`, không gọi `FakeLLM` |
| 3 examples kiểm tra bằng `tools/pyrunner/tracer.py` | `01_faq_store`: `326` step; `02_filter_before_topk`: `67` step; `03_save_and_reload`: `131` step (đều `truncated: False`, `error: None`) |
| `uv run python tools/build_content.py` | `Built 43 lessons, 9 exams, 258 flashcards, 691 questions -> apps\web\src\generated` |
| Link `further_reading` đã mở kiểm tra | `https://github.com/facebookresearch/faiss/wiki` → HTTP `200`; `https://github.com/pgvector/pgvector` → HTTP `200` |
| `git status --short` | Chỉ thấy `M curriculum/glossary.yaml`, `?? curriculum/phase-07-llm/p7-04-vector-db/`, `?? tasks/` (và `?? .hallmark/` có sẵn trong working tree) |

## 4. Ghi chú về `pyai_llm` và điều còn chưa chắc

- Hành vi của `pyai_llm`:
  - `FakeLLM.embed(texts)` trả về `list[list[float]]` đã chuẩn hóa L2 và không ghi nhận `Usage` (khác với `FakeLLM.chat()`), nên ví dụ `03_save_and_reload.py` và bài giảng §5 dùng một wrapper `CountingClient` nhỏ để đếm số lần gọi `embed()` thay vì đọc `usage`.
  - `FakeLLM.embed()` băm từ bằng `zlib.crc32(...) % embed_dim` và chỉ bỏ đuôi `"s"` với từ dài `> 3` ký tự; vì vậy trên `embed_dim=256`, các ví dụ/test đã được chọn câu chữ để tránh va chạm băm ngoài ý muốn giữa các chủ đề khác nhau. Không có hành vi nào của `pyai_llm` cản trở bài học.
- Điều chưa chắc / chưa chạy theo ràng buộc spec:
  - Không chạy `pnpm --filter web build` và không khởi động dev server để kiểm tra render trên trình duyệt (theo đúng yêu cầu trong spec).
  - Trong working tree ban đầu đã có thư mục `?? .hallmark/` không thuộc phạm vi task nên được giữ nguyên không đụng vào.
