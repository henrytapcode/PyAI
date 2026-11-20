# Báo cáo triển khai: M3 bước 7 (`p4-06-mini-project`)

## 1. Đã làm gì

Tạo hoàn chỉnh mini-project cuối phase 4 tại `curriculum/phase-04-data/p4-06-mini-project/` theo spec trong `tasks/m3-p4-06-project.md` và `docs/CONTENT_GUIDE.md`:

- **Metadata (`meta.yaml`)**: `id: p4-06-mini-project`, `phase: p4`, `order: 6`, `kind: project`, `prerequisites: [p4-03-cleaning, p4-04-matplotlib, p4-05-sql]`, `duration_min: 45`, `review_by: "2027-11-01"`, `tags: [pandas, data-cleaning, sql, plotting]`, `outcomes` khớp `syllabus.yaml` (kèm 2 dòng mở rộng), và 2 link `further_reading` (`DataFrame.to_sql`, pandas "Comparison with SQL").
- **Bài học (`lesson.en.md`, `lesson.vi.md`)**:
  - Opening nêu bài toán hằng tuần của AI engineer (log CSV thô của chatbot qua 3 model) và nhấn mạnh gần như không có kiến thức mới mà chỉ ghép các mảnh phase 4.
  - Mục 1 (**The plan / Kế hoạch**): sơ đồ `mermaid` `flowchart LR` (6 node, cùng số dòng EN/VI) + bảng `Piece | Input | Output` cho `load_and_clean`, `model_report`, `plot_report`, chỉ rõ Exercise 1 và Exercise 2 làm mảnh nào.
  - Mục 2 (**Inspecting the raw logs / Nhìn dữ liệu thô**): bộ dữ liệu dùng chung 14 dòng CSV (`request_id,model,tokens,latency_ms,status,rating`), kiểm tra với `shape`, `dtypes`, `isna().sum()`, `value_counts()`, kèm hình minh họa `text` đánh dấu từng lỗi trên dòng CSV.
  - Mục 3 (**Part 1: cleaning the logs / Phần 1: làm sạch dữ liệu**): các khối code ngắn độc lập cho từng bước (chuẩn hóa `model`, `tokens` và `latency_ms` coerce, `rating` ngoài 1–5 thành `NaN`, loại `request_id` trùng giữ dòng đầu, bỏ dòng thiếu `tokens`, `reset_index`, ép `"int64"`), có lời mời bấm **Visualize** và bảng `problem | fix`.
  - Mục 4 (**Part 2: reporting with SQL / Phần 2: báo cáo bằng SQL**): `df.to_sql("requests", conn, index=False)` vào `:memory:`, một câu `GROUP BY model` tính `COUNT(*)`, `SUM(tokens)`, `ROUND(AVG(status = 'error'), 3)`, `ROUND(AVG(latency_ms), 1)`, `ROUND(AVG(rating), 2)`, `ORDER BY total_tokens DESC, model ASC`, in từng dòng bằng f-string (< 60 ký tự/dòng), kèm **Trace table** cho `gpt-4o`.
  - Mục 5 (**Part 3: plotting and reading the report / Phần 3: biểu đồ và đọc kết quả**): biểu đồ cột `total_tokens` theo `model` + nhận xét hành động (`gpt-4o` cần tối ưu trước) + callout `> [!TIP]`.
  - Mục 6 (**Common mistakes / Lỗi thường gặp**): 3 lỗi chạy thật (`to_sql` 2 lần -> `ValueError`, quên chuẩn hóa `model` trước `GROUP BY`, ép `"int64"` trước `dropna` -> `IntCastingNaNError`).
  - **Recap / Tóm tắt** và **Take it further / Đi xa hơn** (3 gợi ý mở rộng).
- **Ví dụ (`examples/`)** dùng chung cùng bộ CSV 14 dòng:
  - `01_raw_log_inspection.py` (+ `.out`, `.en.md`, `.vi.md`)
  - `02_sql_model_report.py` (+ `.out`, `.en.md`, `.vi.md`)
  - `03_report_chart.py` (+ `.out`, `.en.md`, `.vi.md`)
- **Bài tập (`exercises/`)**:
  - `ex01-load-and-clean` (`kind: project`, `difficulty: 3`): `load_and_clean(csv_text)`, 9 test trong `test_exercise.py`, starter `# TODO` trả `None`, 3 tầng hint (tầng 3 chừa 3 chỗ `...`), alternative `alternatives/01_csv_module_loop.py` (+ `.en.md`, `.vi.md`).
  - `ex02-model-report` (`kind: project`, `difficulty: 3`): `model_report(df)` + `plot_report(report)`, 9 test trong `test_exercise.py` (dùng `pytest.approx`, `pd.isna`, tự đóng figure bằng `plt.close(fig)`), starter `# TODO` trả `None`, 3 tầng hint (tầng 3 chừa 3 chỗ `...`), alternative `alternatives/01_pandas_groupby.py` (+ `.en.md`, `.vi.md`) kèm giải thích khi nào dùng SQL vs pandas.
- **Quiz (`quiz.yaml`)**: 16 câu hỏi (5 `mcq`, 4 `output`, 4 `fill`, 3 `parsons`; độ khó: 3 mức 1, 9 mức 2, 4 mức 3; tag trong `[pandas, data-cleaning, sql, plotting]`) và 6 flashcard.
- Không sửa `curriculum/glossary.yaml` (không cần thêm thuật ngữ bắt buộc).

## 2. File đã tạo / cập nhật

Tất cả file tạo mới đều nằm trong `curriculum/phase-04-data/p4-06-mini-project/` (cùng file báo cáo này tại `tasks/m3-p4-06-project.report.md`):

- `curriculum/phase-04-data/p4-06-mini-project/meta.yaml`
- `curriculum/phase-04-data/p4-06-mini-project/lesson.en.md`
- `curriculum/phase-04-data/p4-06-mini-project/lesson.vi.md`
- `curriculum/phase-04-data/p4-06-mini-project/quiz.yaml`
- `curriculum/phase-04-data/p4-06-mini-project/examples/01_raw_log_inspection.{py,out,en.md,vi.md}`
- `curriculum/phase-04-data/p4-06-mini-project/examples/02_sql_model_report.{py,out,en.md,vi.md}`
- `curriculum/phase-04-data/p4-06-mini-project/examples/03_report_chart.{py,out,en.md,vi.md}`
- `curriculum/phase-04-data/p4-06-mini-project/exercises/ex01-load-and-clean/{exercise.yaml,prompt.en.md,prompt.vi.md,starter.py,solution.py,test_exercise.py}`
- `curriculum/phase-04-data/p4-06-mini-project/exercises/ex01-load-and-clean/alternatives/01_csv_module_loop.{py,en.md,vi.md}`
- `curriculum/phase-04-data/p4-06-mini-project/exercises/ex02-model-report/{exercise.yaml,prompt.en.md,prompt.vi.md,starter.py,solution.py,test_exercise.py}`
- `curriculum/phase-04-data/p4-06-mini-project/exercises/ex02-model-report/alternatives/01_pandas_groupby.{py,en.md,vi.md}`
- Chạy `uv run python tools/build_content.py` để sinh dữ liệu cho web (`apps/web/src/generated`, file gitignored).

## 3. Kết quả lệnh kiểm tra (chạy sau lần sửa cuối)

| Lệnh kiểm tra | Kết quả |
|---|---|
| `uv run python tools/validate.py --path curriculum/phase-04-data/p4-06-mini-project` | Pass (`OK: 0 error(s), 0 warning(s). Checked 1 lessons, 8 markdown pairs, 3 examples, 2 alternatives, 2 exercises, 16 questions.`) |
| `uv run python tools/validate.py` | Pass (`OK: 0 error(s), 0 warning(s). Checked 30 lessons, 236 markdown pairs, 88 examples, 60 exercises, 58 alternatives, 562 questions, 5 exams, 1 portfolio, 1 glossary, 1 interview.`) |
| `uv run python -m pytest curriculum/phase-04-data` | Pass (`69 passed, 14 warnings in 0.75s`) |
| `uv run ruff check curriculum/phase-04-data` | Pass (`All checks passed!`) |
| Kiểm tra regex `sqlite_version\|astype\(int\)\|dtype=int\b\|\.info\(` (bằng PowerShell `Select-String`) | Rỗng (0 kết quả) |
| Kiểm tra `connect\(` không phải `:memory:` (bằng PowerShell `Select-String`) | Rỗng (0 kết quả) |
| `uv run python tools/build_content.py` | Pass (`Built 30 lessons, 5 exams, 180 flashcards, 483 questions -> apps\web\src\generated`) |
| `git status --short` | Chỉ hiện `?? curriculum/phase-04-data/p4-06-mini-project/` (cùng `?? .hallmark/` và `?? tasks/` có sẵn từ trước) |

## 4. Điều còn chưa chắc

- **Chưa mở trình duyệt / Pyodide 32-bit thực tế**: Môi trường không chạy UI trình duyệt nên chưa kiểm tra trực quan rendering Mermaid, bảng, biểu đồ Matplotlib và Step-through **Visualize** trên Pyodide 32-bit trong app web (dù `tools/validate.py` đã chạy `tools/pyrunner/runner.py` và `tools/pyrunner/tracer.py` trên CPython local, và mọi quy tắc tránh 32-bit int dtype / NumPy scalar / SQLite 3.39.0 đã được kiểm tra).
- **Lệnh kiểm tra pattern trên Windows PowerShell**: Thực hiện bằng `Get-ChildItem ... | Select-String` với cùng biểu thức regex thay cho binary `grep` của POSIX.
