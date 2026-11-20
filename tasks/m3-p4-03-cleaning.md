# M3 bước 4: bài p4-03 Cleaning data (+ sửa nhỏ câu chữ p4-01)

## Mục tiêu
1. Viết bài `p4-03-cleaning` đúng `docs/CONTENT_GUIDE.md`, song ngữ EN/VI, chạy được cả local và trong app.
   Người học đã xong `p4-01-numpy` và `p4-02-pandas` (DataFrame, `read_csv` + `io.StringIO`, `loc`/`iloc`, mask, `groupby`, `reset_index`).
2. Sửa câu chữ trong `p4-01-numpy` cho đúng với app (xem mục "Sửa p4-01").

Bài mẫu về giọng văn và hình dạng: `curriculum/phase-04-data/p4-02-pandas/` (đã duyệt).

## File được phép sửa/tạo
- Thư mục mới `curriculum/phase-04-data/p4-03-cleaning/` và mọi file bên trong.
- `curriculum/phase-04-data/p4-01-numpy/lesson.en.md` và `lesson.vi.md`: **chỉ** hai câu nêu ở mục "Sửa p4-01".
- `curriculum/glossary.yaml`: chỉ **thêm** thuật ngữ mới (missing value / NaN, data cleaning, duplicate, type coercion; bỏ qua cái đã có).

## Không được đụng
- `apps/`, `tools/`, `curriculum/syllabus.yaml`, `curriculum/topics.yaml`, `p4-02-pandas`, các phase khác, `exams/`.
- Không xóa file, không `git commit`, **không chạy `pnpm --filter web build`** (dev server đang chạy).

## Quy tắc output (bắt buộc, do app chạy Pyodide 32-bit)
- Số nguyên mặc định của NumPy trong app là `int32`, ở local là `int64`; cột số nguyên pandas là `int64` ở cả hai. Vì vậy:
  - **Không dùng `astype(int)` hay `dtype=int`** (trong app ra `int32`). Luôn viết `astype("int64")`.
  - Không in `dtype` của mảng NumPy số nguyên. In `df.dtypes` thì được (cột pandas).
- **Không in `df.info()`** (dòng memory usage khác nhau giữa 32/64-bit). Muốn xem tổng quan thì dùng `df.isna().sum()`, `df.dtypes`, `df.shape`.
- Không in list/tuple/dict chứa numpy scalar (numpy 2 in `np.float64(2.5)`): dùng `.tolist()`, `float()`, `int()`.
- Mọi DataFrame được `print` có tối đa 4 cột, mỗi dòng dưới 60 ký tự (hoặc dùng `to_string()`).
- Mọi `print(...)  # ...` trong khối python của lesson phải khớp output thật (boss chạy từng khối để đối chiếu).

## Nội dung bài (boss chốt dàn ý, worker viết)
Opening (không heading): dữ liệu thật luôn bẩn: đánh giá bị trống, nhãn `" GPT-4o"` và `"gpt-4o"` bị coi là hai model, số lưu dạng chữ `"1,200"`, dòng trùng. Dạy mô hình bằng dữ liệu bẩn thì kết quả sai ("garbage in, garbage out").

1. **Soi dữ liệu trước**: `df.shape`, `df.dtypes`, `df.isna().sum()`, `df["col"].unique()`, `value_counts()`. Không dùng `info()`.
2. **Giá trị thiếu**: `NaN`/`None`, `isna`, `dropna(subset=[...])`, `fillna(value)`, điền bằng `median()`; `mean()` tự bỏ qua NaN. **Trace table** cho một lần `fillna` bằng median (`| row | before | after |`).
3. **Sửa kiểu dữ liệu**: số dạng chữ `"1,200"` → `.str.replace(",", "")` + `pd.to_numeric(..., errors="coerce")`, rồi `astype("int64")` khi chắc chắn không còn NaN; `"yes"/"no"` → bool bằng `map`. **Picture in text** (fence `text`) cho cột trước/sau khi sửa.
4. **Làm sạch văn bản**: `.str.strip()`, `.str.lower()`, `.str.replace(...)`; so `value_counts()` trước/sau để thấy nhãn được gộp. Đây là section mời bấm **Visualize** (một khối nhỏ trên Series ngắn).
5. **Dòng trùng và dòng không hợp lệ**: `duplicated()`, `drop_duplicates(subset=..., keep="last")`, lọc khoảng hợp lệ bằng `between(1, 5)`.
6. **Gộp thành pipeline**: hàm `clean(df)` bắt đầu bằng `df = df.copy()` rồi làm lần lượt các bước, trả DataFrame mới. **Mermaid** `flowchart TD` (tối đa 8 node): load → inspect → fix text → fix types → missing values → duplicates → validate. Bảng `| problem | tool |`.
7. **Lỗi thường gặp** (3–4, chạy thật để lấy đúng thông báo của pandas 2.3.3):
   - Quên gán lại: `df.dropna()` / `df.fillna(0)` trả DataFrame mới, `df` không đổi.
   - `astype("int64")` trên cột còn NaN → lỗi (lấy đúng tên và thông báo lỗi khi chạy).
   - So sánh `== np.nan` luôn `False`; dùng `isna()`.
   - Gọi `.strip()` thẳng trên Series → `AttributeError`; phải qua `.str`.
8. **Recap / Tóm tắt**.

Thời lượng 10–12 phút. `review_by: "2027-11-01"`. `further_reading`: pandas user guide "Working with missing data" và "Working with text data" (URL chính thức pandas.pydata.org).

## Examples (3)
- `01_survey_missing`: khảo sát người dùng có ô trống; đếm thiếu, bỏ dòng thiếu cột bắt buộc, điền cột phụ bằng median.
- `02_price_text_to_numbers`: cột giá kiểu `"1,200"`, `"N/A"`, `" 350 "` → số bằng `to_numeric(errors="coerce")`, báo bao nhiêu dòng không đọc được.
- `03_training_labels`: bộ dữ liệu (text, label) để huấn luyện bộ phân loại: chuẩn hóa nhãn, bỏ text rỗng, bỏ dòng trùng, in `value_counts()` cuối cùng.

## Exercises (2)
- `ex01-normalise-labels` (`kind: fill`): hàm `normalise_labels(labels: pd.Series) -> pd.Series`: bỏ khoảng trắng hai đầu, chữ thường, thay `"_"` và `"-"` bằng dấu cách. Các ô `___` trong thân hàm. Test so bằng `.tolist()`, không sửa Series đầu vào, giữ nguyên index.
- `ex02-clean-ratings` (`kind: code`): hàm `clean_ratings(df: pd.DataFrame) -> pd.DataFrame`, đầu vào có cột `user` (chữ, có thể thừa khoảng trắng, hoa thường lẫn lộn) và `rating` (chữ: `" 4 "`, `"five"`, `""`, `None`, `"7"`). Kết quả:
  1. `user` đã `strip().lower()`;
  2. `rating` thành số bằng `to_numeric(errors="coerce")`; bỏ dòng không đọc được hoặc ngoài 1–5;
  3. mỗi user chỉ giữ dòng **cuối cùng**;
  4. `rating` có dtype `int64`; cột theo thứ tự `["user", "rating"]`; index đánh lại từ 0; không sửa `df` đầu vào.
  5–6 test (gồm: dtype là `"int64"` (so `str(result["rating"].dtype) == "int64"`), DataFrame toàn dòng hỏng → kết quả rỗng có đúng 2 cột, user trùng sau khi chuẩn hóa tên). Có `alternatives/01_loop.py` (duyệt từng dòng, dùng dict theo user) + `.md` so sánh.

## Quiz
15–18 câu, mỗi loại `mcq`/`output`/`fill`/`parsons` ít nhất 2; khoảng 5 dễ, 7 vừa, 3 khó. 6 flashcard. Tag: `data-cleaning` (chính), có thể thêm `pandas`.

## Sửa p4-01
Trong `curriculum/phase-04-data/p4-01-numpy/lesson.en.md` (và câu tương ứng trong `lesson.vi.md`):
- Dòng 18: `(such as \`int64\` or \`float64\`)` → `(such as \`int64\`, \`int32\` or \`float64\`)`.
- Dòng 199: `writing a decimal into an \`int64\` slot` → `writing a decimal into an integer slot`.
Không sửa gì khác trong p4-01.

## Tiêu chí hoàn thành (checklist)
1. [ ] Đủ file theo layout CONTENT_GUIDE; `meta.yaml` có `phase: p4`, `order: 3`, `tags` gồm `data-cleaning`, `prerequisites: [p4-02-pandas]`, `outcomes` khớp syllabus (có thể thêm 1–2 dòng).
2. [ ] Lesson đúng dàn ý trên, đủ: mermaid, trace table, picture in text, bảng so sánh, một lời mời Visualize, callout.
3. [ ] Code giữa `lesson.en.md` và `lesson.vi.md` giống hệt (trừ comment); số dòng mermaid bằng nhau; fence `text` giống hệt.
4. [ ] Tuân thủ đủ "Quy tắc output" ở trên (boss sẽ grep `astype(int`, `dtype=int`, `.info(`).
5. [ ] Exercise: starter fail, solution và alternative pass (pytest **và** browser runner); hint đủ 3 tầng; gợi ý tầng 3 chừa ít nhất 2 chỗ `...`.
6. [ ] Bản VI tự nhiên, xưng "bạn", thuật ngữ giữ tiếng Anh kèm giải nghĩa lần đầu.
7. [ ] Sửa p4-01 đúng hai câu, không hơn.
8. [ ] Lệnh kiểm tra xanh.
9. [ ] Xem bài trong app: `uv run python tools/build_content.py` (an toàn khi dev server chạy), mở `http://localhost:3000/lesson/p4-03-cleaning/`, bấm Run một khối và Visualize ở khối được mời, ghi kết quả vào report. Trong app, chạy thêm solution của `ex02` trên trang bài tập (nút kiểm tra) để chắc test dtype `int64` qua được trên Pyodide.

## Lệnh kiểm tra
Từ gốc repo `D:\Proj\python-ai-platform`:
```
uv run python tools/validate.py --path curriculum/phase-04-data/p4-03-cleaning
uv run python tools/validate.py
uv run python -m pytest curriculum/phase-04-data
uv run ruff check curriculum/phase-04-data
grep -rnE "astype\(int\)|dtype=int\b|\.info\(" curriculum/phase-04-data/p4-03-cleaning
git status --short
git diff --stat
```
Mong đợi: validate 0 lỗi; pytest exit 0; ruff sạch; grep rỗng; file mới chỉ trong `p4-03-cleaning/`; diff chỉ `p4-01-numpy/lesson.*.md` (2 câu mỗi file) và `glossary.yaml`.

## Ghi chú cho worker
- Đọc `docs/CONTENT_GUIDE.md`, rồi `curriculum/phase-04-data/p4-02-pandas/` để bắt chước giọng văn và hình dạng.
- Local dùng pandas 2.3.3 / numpy 2.2.5, giống Pyodide; `.out` phải khớp chính xác stdout.
- Test so DataFrame bằng `.to_dict("list")`, `.tolist()`, `list(df.columns)`; không `assert df1 == df2`.
- Dùng `uv run python -m pytest`, không dùng `uv run pytest` (lỗi launcher).

## Trạng thái
- Bước hiện tại: 5 (đạt sau vòng 1; boss tự kiểm tra trong app vì worker không có trình duyệt; chờ user duyệt commit)
- Vòng: 1/3
- Số lần swap: 0
- Fallback: không
- Model: Gemini 4 Hydrogen (High)
