# Báo cáo thực hiện: `m3-p4-03-cleaning`

## 1. Đã làm gì

1. **Tạo bài học song ngữ `p4-03-cleaning` (`curriculum/phase-04-data/p4-03-cleaning/`)**:
   - `meta.yaml`: `id: p4-03-cleaning`, `phase: p4`, `order: 3`, `duration_min: 11`, `prerequisites: [p4-02-pandas]`, `tags: [data-cleaning, pandas, data]`, `review_by: "2027-11-01"`, `outcomes` khớp syllabus (+1 mục về pipeline), `further_reading` trỏ tới 2 trang User Guide chính thức của pandas (`missing_data.html`, `text.html`).
   - `lesson.en.md` và `lesson.vi.md`:
     - Opening không heading về dữ liệu bẩn trong thực tế ("garbage in, garbage out").
     - 7 section chính theo đúng dàn ý: (1) soi dữ liệu (`shape`, `dtypes`, `isna().sum()`, `unique()`, `value_counts()`, không dùng `info()`), (2) giá trị thiếu (`NaN`/`None`, `isna()`, `dropna(subset=[...])`, `fillna(median)`, `mean()` bỏ qua `NaN`, kèm trace table `| row | before | after |` và callout `TIP`), (3) sửa kiểu dữ liệu (`.str.replace`, `pd.to_numeric(..., errors="coerce")`, `astype("int64")`, `.map(...)` cho `"yes"`/`"no"`, kèm picture-in-text `text` fence), (4) làm sạch văn bản (`.str.strip()`, `.str.lower()`, `.str.replace(...)`, so `value_counts()` trước/sau và lời mời bấm **Visualize** trên Series ngắn), (5) dòng trùng và không hợp lệ (`duplicated()`, `drop_duplicates(subset=..., keep="last")`, `.between(1, 5)`), (6) pipeline `clean(df)` bắt đầu bằng `df = df.copy()` kèm Mermaid `flowchart TD` (7 node) và bảng `| problem | tool |`, (7) 4 lỗi thường gặp với thông báo lỗi thực tế trên pandas 2.3.3 (`IntCastingNaNError`, `AttributeError`, quên gán lại sau `fillna`, `== np.nan` kèm callout `WARNING`), và (8) `Recap` / `Tóm tắt`.
     - Tuân thủ quy tắc Pyodide 32-bit: không dùng `astype(int)`, `dtype=int`, `.info()`, không in scalar NumPy thô trong list/dict/tuple, mọi DataFrame in ra tối đa 3 cột và dưới 60 ký tự/dòng.
   - **3 Examples** (`01_survey_missing`, `02_price_text_to_numbers`, `03_training_labels`): mỗi ví dụ gồm `.py`, `.out` khớp stdout chính xác, `.en.md` và `.vi.md`.
   - **2 Exercises**:
     - `ex01-normalise-labels` (`kind: fill`): điền ô `___` trong thân hàm `normalise_labels(labels: pd.Series) -> pd.Series`, 4 test so bằng `.tolist()`, giữ index và không sửa `Series` đầu vào, 3 tầng hint EN/VI.
     - `ex02-clean-ratings` (`kind: code`): hàm `clean_ratings(df: pd.DataFrame) -> pd.DataFrame`, 6 test (gồm kiểm tra `str(result["rating"].dtype) == "int64"`, DataFrame toàn dòng hỏng trả bảng rỗng đúng 2 cột `["user", "rating"]` dtype `int64`, trùng user sau khi chuẩn hóa, reset index, không sửa `df` đầu vào), 3 tầng hint EN/VI, kèm `alternatives/01_loop.py` (duyệt từng dòng dùng `dict` theo `user`) + `.en.md`/`.vi.md`.
   - **Quiz (`quiz.yaml`)**: 16 câu hỏi (5 `mcq`, 5 `output`, 4 `fill`, 2 `parsons`; 5 dễ, 8 vừa, 3 khó) + 6 flashcard (`p4-03-f01`..`p4-03-f06`), tag chính `data-cleaning`.
2. **Sửa 2 câu trong `p4-01-numpy`**:
   - Cập nhật đúng dòng 18 và dòng 199 trong `lesson.en.md` và `lesson.vi.md` theo spec, không sửa gì khác trong `p4-01-numpy`.
3. **Bổ sung `curriculum/glossary.yaml`**:
   - Thêm 4 thuật ngữ mới: `data cleaning`, `missing value / NaN`, `duplicate`, `type coercion` (đủ EN/VI, `tags`, `example`, `in_practice`, `related`).
4. **Build nội dung cho app**:
   - Chạy `uv run python tools/build_content.py` để cập nhật JSON trong `apps/web/src/generated` (gitignored).

## 2. File đã sửa / tạo

- **Sửa**:
  - `curriculum/phase-04-data/p4-01-numpy/lesson.en.md`
  - `curriculum/phase-04-data/p4-01-numpy/lesson.vi.md`
  - `curriculum/glossary.yaml`
- **Tạo mới**:
  - `curriculum/phase-04-data/p4-03-cleaning/meta.yaml`
  - `curriculum/phase-04-data/p4-03-cleaning/lesson.en.md`
  - `curriculum/phase-04-data/p4-03-cleaning/lesson.vi.md`
  - `curriculum/phase-04-data/p4-03-cleaning/quiz.yaml`
  - `curriculum/phase-04-data/p4-03-cleaning/examples/01_survey_missing.{py,out,en.md,vi.md}`
  - `curriculum/phase-04-data/p4-03-cleaning/examples/02_price_text_to_numbers.{py,out,en.md,vi.md}`
  - `curriculum/phase-04-data/p4-03-cleaning/examples/03_training_labels.{py,out,en.md,vi.md}`
  - `curriculum/phase-04-data/p4-03-cleaning/exercises/ex01-normalise-labels/{exercise.yaml,prompt.en.md,prompt.vi.md,starter.py,solution.py,test_exercise.py}`
  - `curriculum/phase-04-data/p4-03-cleaning/exercises/ex02-clean-ratings/{exercise.yaml,prompt.en.md,prompt.vi.md,starter.py,solution.py,test_exercise.py}`
  - `curriculum/phase-04-data/p4-03-cleaning/exercises/ex02-clean-ratings/alternatives/01_loop.{py,en.md,vi.md}`
  - `tasks/m3-p4-03-cleaning.report.md` (báo cáo này)

## 3. Kết quả lệnh kiểm tra

Các lệnh chạy sau lần chỉnh sửa cuối cùng:

- `uv run python tools/validate.py --path curriculum/phase-04-data/p4-03-cleaning`
  - Kết quả: exit 0 — `OK: 0 error(s), 0 warning(s). Checked 1 lessons, 7 markdown pairs, 3 examples, 2 exercises, 1 alternatives, 16 questions.`
- `uv run python tools/validate.py`
  - Kết quả: exit 0 — `OK: 0 error(s), 0 warning(s). Checked 27 lessons, 214 markdown pairs, 79 examples, 54 exercises, 54 alternatives, 514 questions, 5 exams, 1 portfolio, 1 glossary, 1 interview.`
- `uv run python -m pytest curriculum/phase-04-data`
  - Kết quả: exit 0 — `30 passed in 0.38s`
- `uv run ruff check curriculum/phase-04-data`
  - Kết quả: exit 0 — `All checks passed!`
- Kiểm tra pattern cấm (`astype\(int\)|dtype=int\b|\.info\(`) trên toàn bộ file trong `curriculum/phase-04-data/p4-03-cleaning`:
  - Kết quả: không có kết quả khớp nào (trống).
- Kiểm tra toàn bộ 10 khối ```python``` trong `lesson.en.md` bằng `python -I -c` và kiểm tra khối Visualize với `tools/pyrunner/tracer.py`:
  - Kết quả: cả 10 khối chạy exit 0 khớp stdout; khối Visualize trace hoàn tất 8 bước (`error: None`, `truncated: False`).
- `uv run python tools/build_content.py`
  - Kết quả: exit 0 — `Built 27 lessons, 5 exams, 162 flashcards, 435 questions -> apps\web\src\generated`.
- `git diff --stat`
  - Chỉ thay đổi đúng 3 file tracked: `curriculum/glossary.yaml` (+44), `curriculum/phase-04-data/p4-01-numpy/lesson.en.md` (+2/-2), `curriculum/phase-04-data/p4-01-numpy/lesson.vi.md` (+2/-2).

## 4. Điều còn chưa chắc

- **Kiểm tra trực tiếp trên trình duyệt (Pyodide trong web app, checklist mục 9) chưa thực hiện được** do phiên làm việc hiện tại không có công cụ điều khiển trình duyệt và khi kiểm tra `Invoke-WebRequest http://localhost:3000/lesson/p4-03-cleaning/` nhận mã lỗi HTTP 404.
  - Đã chạy `tools/build_content.py` thành công và đã kiểm tra qua `tools/pyrunner/runner.py` + `tools/pyrunner/tracer.py` (qua `validate.py`) ở môi trường local CPython (pandas 2.3.3 / numpy 2.2.5), nhưng việc bấm **Run**, **Visualize** và chạy test bài `ex02` (đặc biệt assertion `str(result["rating"].dtype) == "int64"`) trực tiếp trên Pyodide trong trình duyệt cần được xác nhận thủ công trên app.
