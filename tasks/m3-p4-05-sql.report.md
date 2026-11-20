# Báo cáo thực hiện `m3-p4-05-sql`

## 1. Đã làm gì

Đã xây dựng hoàn chỉnh bài học `p4-05-sql` ("SQL basics with SQLite" / "SQL cơ bản với SQLite") theo đúng `tasks/m3-p4-05-sql.md` và `docs/CONTENT_GUIDE.md`, đồng thời bổ sung thuật ngữ mới vào `curriculum/glossary.yaml` và build dữ liệu tĩnh cho app qua `tools/build_content.py`:

- **Metadata (`meta.yaml`)**: `id: p4-05-sql`, `phase: p4`, `order: 5`, `kind: lesson`, `tags: [sql, pandas, data]`, `prerequisites: [p4-02-pandas]`, `duration_min: 11`, `outcomes` khớp `syllabus.yaml` (kèm 1 mục về parameterized query / SQL injection), `review_by: "2027-11-01"`, `further_reading` dẫn tới docs `sqlite3` và SQLite `lang.html`.
- **Nội dung bài học (`lesson.en.md`, `lesson.vi.md`)**:
  - Mở đầu không heading gắn với bài toán AI (lưu lịch sử chat, feedback, kết quả eval).
  - 7 mục nội dung + mục Tóm tắt (`Recap` / `Tóm tắt`), gồm đủ: picture in text (`text` fence về bảng `messages`), lời mời bấm **Visualize** ở §3, trace table cho `GROUP BY` ở §4, bảng so sánh `SQL | pandas` ở §5, mermaid `flowchart LR` 7 node cho thứ tự thực thi SQL ở §6, callout `> [!WARNING]` về SQL injection và 4 lỗi thường gặp với thông báo lỗi lấy từ lần chạy thật (`sqlite3.OperationalError: near "Brien": syntax error`, `sqlite3.ProgrammingError: Incorrect number of bindings supplied...`), `= NULL` vs `IS NULL`, và quên `ORDER BY`.
  - Toàn bộ code Python giữa `lesson.en.md` và `lesson.vi.md` giống hệt nhau (chỉ khác comment `#`), toàn bộ dùng `sqlite3.connect(":memory:")`, mọi `SELECT` nhiều dòng đều có `ORDER BY`, làm tròn số thực bằng `ROUND(..., 2)`.
- **Examples (3)**:
  - `01_chat_history`: bảng `messages`, chèn lượt chat với `?`, lấy hội thoại của `"an"` theo `id ASC`, đếm theo `role`.
  - `02_feedback_stats`: bảng `feedback`, `GROUP BY model`, `ROUND(AVG(rating), 2)`, `HAVING COUNT(*) >= 2`, in theo định dạng `model: avg (n ratings)`.
  - `03_eval_to_pandas`: bảng `eval_runs`, `pd.read_sql_query` với `params=(0.75,)`, tính trung bình theo `model` bằng pandas và in DataFrame nhỏ (2 cột).
- **Exercises (2)**:
  - `ex01-top-models` (`kind: fill`): `top_models(conn, min_runs)` trên `runs(model TEXT, score REAL)` với 4 ô `___`, fixture `@pytest.fixture` có `yield conn` và `conn.close()`, 5 test kiểm tra `min_runs`, biên `== min_runs`, sắp xếp giảm dần + phá hòa theo tên tăng dần, làm tròn 2 chữ số và trường hợp rỗng; có đủ 3 tầng hint (tầng 3 chừa 3 chỗ `...`).
  - `ex02-feedback-db` (`kind: code`): `create_feedback_db(rows)` và `low_rated_users(conn, max_rating)`, 6 test gồm tên `"O'Brien"`, bảng rỗng `[]`, loại trùng user, biên `rating == max_rating`, không có bản ghi đạt ngưỡng; kèm `alternatives/01_python_filter.py` (lọc bằng Python `set` + `sorted`) và `.en.md` / `.vi.md` giải thích vì sao lọc trong SQL tốt hơn khi dữ liệu lớn; đủ 3 tầng hint (tầng 3 chừa 3 chỗ `...`).
- **Quiz (`quiz.yaml`)**: 16 câu hỏi (5 `mcq`, 4 `output`, 4 `fill`, 3 `parsons`; độ khó: 5 mức 1, 8 mức 2, 3 mức 3) và 6 flashcard (`p4-05-f01`..`p4-05-f06`). Mọi câu `output` có `SELECT` nhiều dòng đều có `ORDER BY`.
- **Glossary (`curriculum/glossary.yaml`)**: thêm 8 thuật ngữ mới (`SQL`, `table`, `row`, `query`, `primary key`, `GROUP BY`, `placeholder / parameterized query`, `SQL injection`).

## 2. File đã sửa / tạo

- Sửa:
  - `curriculum/glossary.yaml` (thêm 8 thuật ngữ SQL & SQLite ở cuối file)
- Tạo mới trong `curriculum/phase-04-data/p4-05-sql/`:
  - `meta.yaml`, `lesson.en.md`, `lesson.vi.md`, `quiz.yaml`
  - `examples/01_chat_history.{py,out,en.md,vi.md}`
  - `examples/02_feedback_stats.{py,out,en.md,vi.md}`
  - `examples/03_eval_to_pandas.{py,out,en.md,vi.md}`
  - `exercises/ex01-top-models/{exercise.yaml,prompt.en.md,prompt.vi.md,starter.py,solution.py,test_exercise.py}`
  - `exercises/ex02-feedback-db/{exercise.yaml,prompt.en.md,prompt.vi.md,starter.py,solution.py,test_exercise.py}`
  - `exercises/ex02-feedback-db/alternatives/01_python_filter.{py,en.md,vi.md}`
  - `tasks/m3-p4-05-sql.report.md` (file báo cáo này)
- Sinh artifact build web (gitignored) khi chạy `uv run python tools/build_content.py` vào `apps/web/src/generated/`.

Không đụng vào `apps/`, `tools/`, `curriculum/syllabus.yaml`, `curriculum/topics.yaml`, các bài khác hay `exams/`, không chạy `pnpm --filter web build`.

## 3. Kết quả lệnh kiểm tra

Chạy sau lần chỉnh sửa code cuối cùng:

| Lệnh | Kết quả |
|---|---|
| `uv run python tools/validate.py --path curriculum/phase-04-data/p4-05-sql` | Exit 0 — `OK: 0 error(s), 0 warning(s). Checked 1 lessons, 7 markdown pairs, 3 examples, 2 exercises, 1 alternatives, 16 questions.` |
| `uv run python tools/validate.py` | Exit 0 — `OK: 0 error(s), 0 warning(s). Checked 29 lessons, 228 markdown pairs, 85 examples, 58 exercises, 56 alternatives, 546 questions, 5 exams, 1 portfolio, 1 glossary, 1 interview.` |
| `uv run python -m pytest curriculum/phase-04-data` | Exit 0 — `51 passed, 14 warnings in 1.12s` (14 warning từ matplotlib/pyparsing có sẵn trong môi trường) |
| `uv run ruff check curriculum/phase-04-data` | Exit 0 — `All checks passed!` |
| Kiểm tra `sqlite_version\|astype(int)\|dtype=int\b\|\.info(` trong `curriculum/phase-04-data/p4-05-sql` (bằng PowerShell `Select-String` và `git grep --untracked`) | Không có kết quả khớp nào (rỗng). |
| Kiểm tra `connect(` không chứa `:memory:` trong `curriculum/phase-04-data/p4-05-sql` | Rỗng (`lesson.en.md:46` và `lesson.vi.md:46` có nhắc `sqlite3.connect("app.db")` trong câu văn cùng dòng với `:memory:`, không nằm trong khối code python). |
| `uv run python tools/build_content.py` | Exit 0 — `Built 29 lessons, 5 exams, 174 flashcards, 467 questions -> apps\web\src\generated` |
| `git status --short` | Chỉ hiện `M curriculum/glossary.yaml`, `?? curriculum/phase-04-data/p4-05-sql/`, `?? tasks/` (và `?? .hallmark/` có sẵn từ trước trong repo). |

## 4. Điều còn chưa chắc

- **Chưa kiểm thử trực tiếp trên trình duyệt / Pyodide 32-bit (SQLite 3.39.0)**: Môi trường hiện tại không mở trình duyệt web để bấm thử **Run**, **Visualize**, **Test**, và **Quiz** trên app (local dùng SQLite 3.50.4). Đã cố gắng giảm rủi ro bằng cách chỉ dùng cú pháp SQLite cơ bản (`CREATE TABLE`, `INSERT`, `SELECT`, `GROUP BY`, `HAVING`, `ROUND`, `ORDER BY`, `LIMIT`, `IS NULL`), chạy `tools/pyrunner/runner.py` và `tools/pyrunner/tracer.py` thông qua `tools/validate.py`, và chạy `tools/build_content.py` — nhờ anh/chị kiểm tra lại một lượt trên dev server của app.
- **Tác dụng của `with conn:`**: Trong bài chỉ giải thích `with conn:` tự động commit/rollback transaction (không tự đóng kết nối), và mọi khối code độc lập đều gọi `conn.close()` ở cuối. Nếu người học chạy lại nhiều lần trong cùng phiên hoặc quen `with open(...)`, cần đảm bảo giải thích ngắn gọn hiện tại trong §2 đã đủ rõ.
