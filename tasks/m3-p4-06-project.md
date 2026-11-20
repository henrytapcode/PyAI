# M3 bước 7: p4-06 Mini-project: data analysis

## Mục tiêu
Viết mini-project cuối phase 4 (`p4-06-mini-project`, `kind: project`): một **báo cáo sử dụng API của chatbot** từ log thô.
Người học gộp mọi thứ của phase 4: làm sạch bằng pandas (p4-03), tổng hợp bằng SQL/SQLite (p4-05), vẽ biểu đồ (p4-04), trên nền NumPy/pandas (p4-01, p4-02).
Gần như không có kiến thức mới; mục đích là **kết hợp**.
Bài mẫu về hình dạng mini-project: `curriculum/phase-03-code-quality/p3-05-mini-project/` (opening, "The plan" có mermaid + bảng các mảnh, 2 bài tập `kind: project`, ~10 test mỗi bài). Giọng văn: các bài `curriculum/phase-04-data/p4-0*` đã duyệt.

## File được phép sửa/tạo
- Thư mục mới `curriculum/phase-04-data/p4-06-mini-project/` và mọi file bên trong.
- `curriculum/glossary.yaml`: chỉ **thêm** thuật ngữ mới nếu thật sự có (vd error rate); có thể không thêm gì.

## Không được đụng
- `apps/`, `tools/`, `curriculum/syllabus.yaml`, `curriculum/topics.yaml`, các bài p4 khác, các phase khác, `exams/`.
- Không xóa file, không `git commit`, **không chạy `pnpm --filter web build`** (dev server đang chạy).
- Không tạo `phase-test.yaml` (bước 8).

## Quy tắc output (bắt buộc)
- App chạy Pyodide 32-bit: không in `dtype` của mảng NumPy số nguyên; không `astype(int)`/`dtype=int` (dùng `"int64"`); không `df.info()`. Không in list/dict chứa numpy scalar.
- SQLite trong app là 3.39.0: chỉ `sqlite3.connect(":memory:")`, không tính năng mới hơn 3.39, không in `sqlite_version`, không in object `Connection`. Mọi `SELECT` nhiều dòng có `ORDER BY` (kèm cột phụ để phá hòa).
- DataFrame in ra tối đa 4 cột, mỗi dòng dưới 60 ký tự (cần rộng hơn thì in từng dòng bằng f-string).
- Biểu đồ không vào stdout: example vẽ biểu đồ phải in thêm dòng tóm tắt; trong lesson ghi `# (shows ...)` / `# (hiện ...)` sau `plt.show()`. Hàm vẽ trong bài tập trả `(fig, ax)` và không gọi `plt.show()`.
- Số thực in ra phải làm tròn (`ROUND` trong SQL hoặc `round(float(x), n)`).
- Mọi `print(...)  # ...` trong lesson phải khớp output thật (boss chạy từng khối để đối chiếu).

## Dữ liệu dùng chung
Một CSV log request viết thẳng trong code (qua `io.StringIO`), 12–16 dòng, cột:
`request_id,model,tokens,latency_ms,status,rating`
Cố tình bẩn theo đúng những gì p4-03 đã dạy: tên model lẫn hoa thường/khoảng trắng/`_` (`" GPT-4o"`, `"gpt_4o"`, `"Claude "`), `tokens` dạng `"1,200"` và một ô trống, `latency_ms` có `"N/A"`, `status` là `ok`/`error`, `rating` 1–5 hoặc trống hoặc ngoài khoảng (`9`), có 1–2 `request_id` bị lặp.
Dùng **cùng một bộ dữ liệu** trong lesson và examples để người học quen; bài tập có thể dùng biến thể nhỏ trong test.

## Nội dung bài (boss chốt dàn ý, worker viết)
Opening (không heading): team muốn biết model nào tốn token nhất, chậm nhất, lỗi nhiều nhất và được người dùng chấm điểm ra sao. Dữ liệu là log thô. Đây là việc AI engineer làm hằng tuần. Một câu: "gần như không có gì mới, bạn ghép những gì đã học".

1. **The plan / Kế hoạch**: **mermaid** `flowchart LR` (≤ 8 node): CSV thô → làm sạch (pandas) → bảng sạch → SQLite → báo cáo theo model (SQL) → biểu đồ. **Bảng các mảnh** `| Piece | Input | Output |` cho `load_and_clean`, `model_report`, `plot_report`; nói rõ Exercise 1 / Exercise 2 làm mảnh nào.
2. **Nhìn dữ liệu thô**: in CSV qua `read_csv`, dùng `shape`, `dtypes`, `isna().sum()`, `value_counts()` để liệt kê vấn đề. **Picture in text** (fence `text`): vài dòng CSV với chú thích vấn đề từng ô.
3. **Phần 1: làm sạch** (từng bước nhỏ, mỗi bước một khối code ngắn): chuẩn hóa model → `tokens` sang số `"int64"` → `latency_ms` coerce → `rating` ngoài 1–5 thành thiếu (`where`/`between`) → bỏ `request_id` trùng (giữ dòng đầu) → bỏ dòng thiếu `tokens` → `reset_index`. Bảng `| problem | fix |`. Mời bấm **Visualize** ở một khối nhỏ trong phần này.
4. **Phần 2: báo cáo bằng SQL**: `df.to_sql("requests", conn, index=False)` vào `:memory:`, một câu `GROUP BY model` tính: `COUNT(*)` requests, `SUM(tokens)`, tỉ lệ lỗi `ROUND(AVG(status = 'error'), 3)` (giải thích mẹo: so sánh trả 1/0), `ROUND(AVG(latency_ms), 1)` (AVG bỏ qua NULL), `ROUND(AVG(rating), 2)`; `ORDER BY` tổng token giảm dần rồi tên model. `pd.read_sql_query` ra DataFrame. **Trace table** cho một model: các dòng của nó → các con số tổng hợp.
5. **Phần 3: biểu đồ và đọc kết quả**: biểu đồ cột tổng token theo model (đã sắp xếp), nhãn đầy đủ; 2–3 câu "đọc báo cáo" (model nào nên tối ưu trước và vì sao). Callout `[!TIP]`: báo cáo tốt trả lời một câu hỏi cụ thể.
6. **Lỗi thường gặp** (3, chạy thật để lấy đúng output/thông báo): gọi `to_sql` hai lần cùng tên bảng → `ValueError: Table 'requests' already exists.` (sửa bằng `if_exists="replace"`); quên chuẩn hóa model trước khi group nên một model bị tách đôi; ép `"int64"` trước khi bỏ dòng thiếu → `IntCastingNaNError`.
7. **Recap / Tóm tắt** + một đoạn "Đi xa hơn" (2–3 gợi ý tự làm: thêm cột chi phí theo giá mỗi model, biểu đồ latency, xuất báo cáo CSV).

`duration_min: 45–50`. `review_by: "2027-11-01"`. `further_reading`: 1–2 link chính thức (pandas `DataFrame.to_sql`, pandas user guide "Comparison with SQL").

## Examples (3)
- `01_raw_log_inspection`: đọc CSV thô, in các dấu hiệu bẩn (số ô thiếu theo cột, các biến thể tên model, số `request_id` trùng).
- `02_sql_model_report`: (làm sạch gọn trong vài dòng rồi) `to_sql` + câu GROUP BY, in từng model một dòng f-string.
- `03_report_chart`: báo cáo → biểu đồ cột tokens theo model; in model tốn token nhất.

## Exercises (2, đều `kind: project`, difficulty 3)
- `ex01-load-and-clean`: `load_and_clean(csv_text: str) -> pd.DataFrame` làm đúng các bước ở Phần 1. Kết quả: cột theo thứ tự `["request_id", "model", "tokens", "latency_ms", "status", "rating"]`; `model` đã `strip().lower()` và `_` → `-`; `tokens` dtype `"int64"`; `latency_ms`, `rating` là số thực (thiếu = NaN; rating ngoài 1–5 = NaN); `request_id` duy nhất (giữ lần đầu); không còn dòng thiếu tokens; index 0..n-1. **8–10 test** (mỗi quy tắc một test, cộng: dtype tokens là `"int64"`, CSV toàn dòng hỏng → DataFrame rỗng đủ 6 cột). Starter: khung hàm với `# TODO` từng bước, `return None`.
- `ex02-model-report`: hai hàm
  - `model_report(df: pd.DataFrame) -> pd.DataFrame`: nhận DataFrame **đã sạch**, đưa vào SQLite `:memory:` bằng `to_sql`, chạy **một** câu `GROUP BY`, trả DataFrame cột `["model", "requests", "total_tokens", "error_rate", "avg_latency", "avg_rating"]` (làm tròn: error_rate 3, avg_latency 1, avg_rating 2; thiếu hết rating → NaN), sắp `total_tokens` giảm dần rồi `model` tăng dần, index 0..n-1. Đóng connection trước khi trả.
  - `plot_report(report: pd.DataFrame) -> tuple`: biểu đồ cột `total_tokens` theo `model` đúng thứ tự của report, title `"Tokens by model"`, ylabel `"tokens"`; trả `(fig, ax)`.
  **8–10 test** (gồm: model chỉ có request lỗi → error_rate 1.0; NaN latency/rating bị bỏ qua khi tính trung bình; thứ tự phá hòa theo tên; chiều cao cột và nhãn trục x khớp report; không sửa df đầu vào). Test tự đóng figure (`plt.close(fig)`). Test so số thực bằng `pytest.approx`; so cột NaN bằng `pd.isna`.
  Có `alternatives/01_pandas_groupby.py` làm `model_report` thuần pandas (`groupby().agg(...)`) + `.md` so sánh khi nào SQL tiện hơn, khi nào pandas tiện hơn. Alternative phải qua **cùng** bộ test.

## Quiz
15–18 câu, mỗi loại `mcq`/`output`/`fill`/`parsons` ít nhất 2; nghiêng về khó vừa (vd 3 dễ, 9 vừa, 4 khó) vì là project. 6 flashcard. Tag: `pandas`, `data-cleaning`, `sql`, `plotting` (dùng các tag có sẵn). Câu hỏi xoay quanh quyết định trong pipeline (thứ tự bước, chọn SQL hay pandas, đọc báo cáo), không lặp lại câu của các bài trước.

## Tiêu chí hoàn thành (checklist)
1. [ ] Đủ file theo layout CONTENT_GUIDE; `meta.yaml` có `phase: p4`, `order: 6`, `kind: project`, `prerequisites: [p4-03-cleaning, p4-04-matplotlib, p4-05-sql]`, `outcomes` khớp syllabus (có thể thêm 2–3 dòng như p3-05), `tags` từ danh sách trên.
2. [ ] Lesson đúng dàn ý, đủ: mermaid, bảng các mảnh, picture in text, trace table, bảng problem/fix, một lời mời Visualize, callout.
3. [ ] Code giữa `lesson.en.md` và `lesson.vi.md` giống hệt (trừ comment); số dòng mermaid bằng nhau; fence `text` giống hệt.
4. [ ] Tuân thủ "Quy tắc output".
5. [ ] Exercise: starter fail, solution và alternative pass (pytest **và** browser runner); hint đủ 3 tầng; gợi ý tầng 3 chừa ít nhất 2 chỗ `...`.
6. [ ] Bản VI tự nhiên, xưng "bạn".
7. [ ] Lệnh kiểm tra xanh, chạy **đúng** như ghi (không thêm biến môi trường).
8. [ ] Chạy `uv run python tools/build_content.py`. Không có trình duyệt thì ghi rõ trong report (boss tự kiểm trong app).

## Lệnh kiểm tra
Từ gốc repo `D:\Proj\python-ai-platform`:
```
uv run python tools/validate.py --path curriculum/phase-04-data/p4-06-mini-project
uv run python tools/validate.py
uv run python -m pytest curriculum/phase-04-data
uv run ruff check curriculum/phase-04-data
grep -rnE "sqlite_version|astype\(int\)|dtype=int\b|\.info\(" curriculum/phase-04-data/p4-06-mini-project
grep -rn "connect(" curriculum/phase-04-data/p4-06-mini-project | grep -v ":memory:"
git status --short
```
Mong đợi: validate 0 lỗi; pytest exit 0; ruff sạch; hai grep rỗng; file mới chỉ trong `p4-06-mini-project/` (và `glossary.yaml` nếu thêm).

## Ghi chú cho worker
- Đọc `docs/CONTENT_GUIDE.md`, `curriculum/phase-03-code-quality/p3-05-mini-project/` (hình dạng project), rồi `curriculum/phase-04-data/p4-03-cleaning/` và `p4-05-sql/` (giọng văn, quy ước).
- `pd.read_sql_query` / `df.to_sql` với connection `sqlite3` chạy được cả local và app, không cần SQLAlchemy.
- Test chỉ dùng: assert, pytest.raises, pytest.approx, pytest.mark.parametrize, `@pytest.fixture` định nghĩa trong file test.
- Dùng `uv run python -m pytest`, không dùng `uv run pytest`.

## Trạng thái
- Bước hiện tại: 5 (đạt sau vòng 1; boss tự kiểm tra trong app: ex01, ex02, ex02-alt đều 9/9 trên Pyodide, Visualize 10 bước; chờ user duyệt commit)
- Vòng: 1/3
- Số lần swap: 0
- Fallback: không
- Model: Gemini 4 Hydrogen (High)
