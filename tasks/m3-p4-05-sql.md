# M3 bước 6: bài p4-05 SQL basics with SQLite

## Mục tiêu
Viết bài `p4-05-sql` đúng `docs/CONTENT_GUIDE.md`, song ngữ EN/VI, chạy được cả local và trong app.
Người học đã xong `p4-01`…`p4-04` (NumPy, pandas, cleaning, plotting) và phase 1–3 (gồm context manager `with`), nhưng **chưa biết SQL**.
Bài mẫu về giọng văn và hình dạng: `curriculum/phase-04-data/p4-04-matplotlib/` và `p4-03-cleaning/` (đã duyệt).

Đã đo (2026-11-13): `import sqlite3` chạy được trong app (Pyodide tự tải gói), `pd.read_sql_query(sql, conn, params=...)` chạy được. **SQLite trong app là 3.39.0, local là 3.50.4.**

## File được phép sửa/tạo
- Thư mục mới `curriculum/phase-04-data/p4-05-sql/` và mọi file bên trong.
- `curriculum/glossary.yaml`: chỉ **thêm** thuật ngữ mới (SQL, table, row, query, primary key, GROUP BY, placeholder / parameterized query, SQL injection; bỏ qua cái đã có).

## Không được đụng
- `apps/`, `tools/`, `curriculum/syllabus.yaml`, `curriculum/topics.yaml`, các bài p4 khác, các phase khác, `exams/`.
- Không xóa file, không `git commit`, **không chạy `pnpm --filter web build`** (dev server đang chạy).

## Quy tắc output (bắt buộc)
- **Chỉ dùng database trong bộ nhớ**: `sqlite3.connect(":memory:")`. Không tạo file `.db`.
- **Chỉ dùng tính năng SQLite có từ 3.39 trở xuống** (vd không `RETURNING` cũng được nhưng tránh cho gọn; không `STRICT`, không hàm JSON mới, không `unixepoch()`). Không in `sqlite3.sqlite_version` hay bất cứ thứ gì phụ thuộc phiên bản.
- **Mọi `SELECT` có in ra kết quả nhiều dòng phải có `ORDER BY`** để thứ tự xác định.
- Không in object `Connection`/`Cursor` (repr có địa chỉ bộ nhớ). In `fetchall()` (list các tuple Python thuần) là được.
- Số thực từ SQL: dùng `ROUND(x, 2)` trong SQL hoặc `round(...)` trong Python trước khi in.
- App chạy Pyodide 32-bit: không in `dtype` của mảng NumPy số nguyên, không `astype(int)`/`dtype=int` (dùng `"int64"`), không `df.info()`. Không in list/dict chứa numpy scalar.
- DataFrame in ra tối đa 4 cột, mỗi dòng dưới 60 ký tự.
- Mọi `print(...)  # ...` trong lesson phải khớp output thật (boss chạy từng khối để đối chiếu). Thông báo lỗi ghi trong bài phải lấy từ lần chạy thật.
- SQL viết từ khóa IN HOA (`SELECT`, `FROM`, `WHERE`), tên bảng/cột chữ thường; câu dài dùng chuỗi `"""..."""` nhiều dòng.

## Nội dung bài (boss chốt dàn ý, worker viết)
Opening (không heading): ứng dụng AI lưu lịch sử chat, feedback người dùng, kết quả eval trong database. SQL là ngôn ngữ chung để hỏi database; SQLite có sẵn trong Python, không cần cài server.

1. **Kết nối và tạo bảng**: `sqlite3.connect(":memory:")`, `conn.execute("CREATE TABLE ...")`, kiểu `INTEGER`, `TEXT`, `REAL`, `PRIMARY KEY`. **Picture in text** (fence `text`): bảng như một lưới có tên cột + kiểu, mỗi dòng là một row.
2. **Thêm dữ liệu**: `INSERT INTO ... VALUES (?, ?, ?)` với placeholder `?`, `executemany` với list các tuple, `conn.commit()`; `with conn:` tự commit (nối với bài context manager). Một câu: database trong bộ nhớ biến mất khi chương trình kết thúc, dự án thật dùng `sqlite3.connect("app.db")`.
3. **SELECT cơ bản**: `SELECT cols FROM t`, `fetchall()` / `fetchone()`, `WHERE` với `=`, `>`, `AND`, `OR`, `LIKE`, `ORDER BY ... DESC`, `LIMIT`. Đây là section mời bấm **Visualize** (khối nhỏ: một truy vấn rồi vòng `for` in từng dòng).
4. **Tổng hợp với GROUP BY**: `COUNT(*)`, `SUM`, `AVG`, `ROUND`, `GROUP BY`, `HAVING`. **Trace table** cho một `GROUP BY` nhỏ (`| model | rows | ratings | AVG |`).
5. **SQL và pandas**: `pd.read_sql_query(sql, conn, params=(...))` ra DataFrame. **Bảng so sánh** `| SQL | pandas |` (WHERE ↔ boolean mask, ORDER BY ↔ sort_values, GROUP BY ↔ groupby, LIMIT ↔ head). Một câu: lọc/gom trong SQL trước khi kéo về pandas giúp tải ít dữ liệu hơn.
6. **Thứ tự SQL thực sự chạy**: **mermaid** `flowchart LR` (tối đa 8 node, mọi nhãn trong ngoặc kép): FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT. Một câu giải thích vì sao `WHERE` không dùng được hàm tổng hợp còn `HAVING` thì được.
7. **Lỗi thường gặp** (3–4, chạy thật để lấy đúng thông báo):
   - Ghép chuỗi/f-string vào SQL: tên `"O'Brien"` làm vỡ câu lệnh (`sqlite3.OperationalError: near "Brien": syntax error`) và mở đường cho **SQL injection**; dùng placeholder `?`. Callout `[!WARNING]` về SQL injection.
   - Một tham số mà quên dấu phẩy: `("ab")` là chuỗi, không phải tuple → `sqlite3.ProgrammingError: Incorrect number of bindings supplied...`; viết `("ab",)`.
   - `WHERE col = NULL` không bao giờ đúng; dùng `IS NULL`.
   - Quên `ORDER BY` nên thứ tự dòng không được đảm bảo (giải thích bằng lời + sửa; không cần chứng minh bằng output khác nhau).
8. **Recap / Tóm tắt**.

Thời lượng 10–12 phút. `review_by: "2027-11-01"`. `further_reading`: tài liệu Python `sqlite3` (docs.python.org) và trang "SQL As Understood By SQLite" (sqlite.org/lang.html).

## Examples (3)
- `01_chat_history`: bảng `messages` (id, user, role, text), thêm vài tin nhắn, lấy hội thoại của một user theo thứ tự id, đếm tin nhắn mỗi role.
- `02_feedback_stats`: bảng `feedback` (model, rating), `GROUP BY model` lấy `COUNT` và `ROUND(AVG(rating), 2)`, `HAVING COUNT(*) >= 2`, in từng dòng dạng `model: avg (n ratings)`.
- `03_eval_to_pandas`: bảng `eval_runs` (model, task, score), `pd.read_sql_query` với `params`, rồi pandas tính trung bình theo model; in DataFrame nhỏ.

## Exercises (2)
- `ex01-top-models` (`kind: fill`): `top_models(conn: sqlite3.Connection, min_runs: int) -> list[tuple[str, float]]` chạy một câu SQL trên bảng `runs(model TEXT, score REAL)` có các ô `___` (vd `GROUP BY ___`, `HAVING COUNT(*) >= ___`, `ORDER BY ___ DESC`): trả list `(model, avg_score)` với avg làm tròn 2 chữ số bằng `ROUND`, chỉ model có ít nhất `min_runs` lần chạy, sắp giảm dần theo avg, hòa thì theo tên tăng dần. Test tự tạo bảng trong `:memory:` (dùng `@pytest.fixture`).
- `ex02-feedback-db` (`kind: code`): hai hàm
  - `create_feedback_db(rows: list[tuple[str, str, int]]) -> sqlite3.Connection`: tạo DB trong bộ nhớ, bảng `feedback(user TEXT, model TEXT, rating INTEGER)`, thêm mọi dòng bằng placeholder, trả connection.
  - `low_rated_users(conn: sqlite3.Connection, max_rating: int) -> list[str]`: tên user (không trùng, sắp xếp tăng dần) có ít nhất một rating `<= max_rating`, dùng placeholder cho `max_rating`.
  5–6 test, gồm: user tên `"O'Brien"` phải hoạt động (bắt buộc dùng placeholder), danh sách rỗng → `[]`, user trùng chỉ xuất hiện một lần, biên `rating == max_rating` được tính. Có `alternatives/01_python_filter.py` (lấy hết dòng rồi lọc bằng Python set) + `.md` giải thích vì sao để database lọc tốt hơn khi dữ liệu lớn.

## Quiz
15–18 câu, mỗi loại `mcq`/`output`/`fill`/`parsons` ít nhất 2; khoảng 5 dễ, 7 vừa, 3 khó. 6 flashcard. Tag: `sql` (chính), có thể thêm `pandas`. Mọi câu `output` có `SELECT` nhiều dòng phải có `ORDER BY`.

## Tiêu chí hoàn thành (checklist)
1. [ ] Đủ file theo layout CONTENT_GUIDE; `meta.yaml` có `phase: p4`, `order: 5`, `tags` gồm `sql`, `prerequisites: [p4-02-pandas]`, `outcomes` khớp syllabus (có thể thêm 1–2 dòng).
2. [ ] Lesson đúng dàn ý trên, đủ: mermaid, trace table, picture in text, bảng so sánh, một lời mời Visualize, callout.
3. [ ] Code giữa `lesson.en.md` và `lesson.vi.md` giống hệt (trừ comment); số dòng mermaid bằng nhau; fence `text` giống hệt.
4. [ ] Tuân thủ "Quy tắc output" ở trên (boss sẽ grep `connect(` khác `":memory:"`, `sqlite_version`, `astype(int`, `.info(`).
5. [ ] Exercise: starter fail, solution và alternative pass (pytest **và** browser runner); hint đủ 3 tầng; gợi ý tầng 3 chừa ít nhất 2 chỗ `...`.
6. [ ] Bản VI tự nhiên, xưng "bạn", thuật ngữ giữ tiếng Anh kèm giải nghĩa lần đầu.
7. [ ] Lệnh kiểm tra xanh, chạy **đúng** như ghi dưới đây (không thêm biến môi trường).
8. [ ] Chạy `uv run python tools/build_content.py` (an toàn khi dev server đang chạy). Không có công cụ trình duyệt thì ghi rõ trong report (boss tự kiểm tra trong app).

## Lệnh kiểm tra
Từ gốc repo `D:\Proj\python-ai-platform`:
```
uv run python tools/validate.py --path curriculum/phase-04-data/p4-05-sql
uv run python tools/validate.py
uv run python -m pytest curriculum/phase-04-data
uv run ruff check curriculum/phase-04-data
grep -rnE "sqlite_version|astype\(int\)|dtype=int\b|\.info\(" curriculum/phase-04-data/p4-05-sql
grep -rn "connect(" curriculum/phase-04-data/p4-05-sql | grep -v ":memory:"
git status --short
```
Mong đợi: validate 0 lỗi; pytest exit 0; ruff sạch; hai lệnh grep rỗng (ngoại trừ câu văn nhắc `sqlite3.connect("app.db")` trong lesson, nếu có, phải nằm ngoài khối code python); file mới chỉ trong `p4-05-sql/` (và `glossary.yaml`).

## Ghi chú cho worker
- Đọc `docs/CONTENT_GUIDE.md`, rồi `curriculum/phase-04-data/p4-04-matplotlib/`.
- Test chỉ dùng: assert, pytest.raises, pytest.approx, pytest.mark.parametrize, `@pytest.fixture` định nghĩa trong file test. Đóng connection trong fixture (`yield conn` rồi `conn.close()`).
- Dùng `uv run python -m pytest`, không dùng `uv run pytest` (lỗi launcher).

## Trạng thái
- Bước hiện tại: 5 (đạt sau vòng 1; boss tự kiểm tra trong app: Visualize 21 bước, ex02 6/6 trên Pyodide; chờ user duyệt commit)
- Vòng: 1/3
- Số lần swap: 0
- Fallback: không
- Model: Gemini 4 Hydrogen (High)
