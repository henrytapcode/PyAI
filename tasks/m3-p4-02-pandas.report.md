# Báo cáo: M3 bước 3 — bài `p4-02-pandas`

## 1. Đã làm gì

- Tạo hoàn chỉnh bài học song ngữ EN/VI `p4-02-pandas` theo `docs/CONTENT_GUIDE.md` và spec `tasks/m3-p4-02-pandas.md`:
  - `meta.yaml`: `id: p4-02-pandas`, `phase: p4`, `order: 2`, `duration_min: 11`, `prerequisites: [p4-01-numpy, p1-09-files]`, `tags: [pandas, data]`, `outcomes` khớp `syllabus.yaml` (thêm 1 outcome về cột vector hóa và tránh lỗi chained indexing), `review_by: "2027-11-01"`, và 2 link `further_reading` chính thức của `pandas.pydata.org`.
  - `lesson.en.md` và `lesson.vi.md`: đủ mở bài + 8 mục theo đúng dàn ý:
    1. Series & DataFrame (tạo từ dict các list, `shape`, `columns`, `dtypes`, `head()`, `len(df)`, bảng so sánh `NumPy array` vs `pandas DataFrame`, callout `NOTE`).
    2. Đọc CSV qua `pd.read_csv(io.StringIO(text))` kèm giải thích ngắn `io.StringIO` và `pd.read_csv("data.csv")`.
    3. Chọn dữ liệu (`df["col"]`, `df[["a", "b"]]`, `df.loc[...]`, `df.iloc[...]`, `df.loc[rows, cols]`) kèm sơ đồ ASCII trong fence `text` phân biệt nhãn (`loc`) và vị trí (`iloc`).
    4. Lọc và sắp xếp (boolean mask, `&`/`|` có ngoặc, `isin`, `sort_values(..., ascending=False)`, `reset_index(drop=True)`, callout `TIP`).
    5. Tạo cột mới theo kiểu vector hóa và `.round(3)` — có lời mời bấm **Visualize** trên khối code 3 dòng gán (`calls`).
    6. `groupby`: `.mean()`, `.agg(["mean", "count"])`, `.value_counts()`, kèm sơ đồ Mermaid `flowchart LR` (split → apply → combine, số dòng EN/VI bằng nhau) và trace table 3 nhóm.
    7. Lỗi thường gặp (4 lỗi): `KeyError` do sai hoa thường/dấu cách, chained indexing `df[df["x"] > 0]["y"] = 1` kèm cảnh báo `SettingWithCopyWarning` thật của pandas 2.3.3 và cách sửa `df.loc[mask, "y"] = 1` (callout `WARNING`), nhầm `loc`/`iloc` sau khi lọc (`KeyError: 0`), dùng `and` thay `&`.
    8. Recap / Tóm tắt (5 gạch đầu dòng).
  - Mọi khối code Python giữa EN và VI giống hệt nhau (chỉ khác comment), đã chạy thực tế trên Python/pandas 2.3.3 để khớp từng comment output, mỗi DataFrame được `print` đều có tối đa 3 cột và chiều rộng mỗi dòng tối đa 35 ký tự (< 60 ký tự).
- Viết 3 ví dụ (`examples/01_chat_logs`, `02_api_costs_csv`, `03_eval_by_model`), chạy lấy stdout chính xác vào `.out`, kiểm tra `tools/pyrunner/tracer.py` không lỗi, kèm giải thích `.en.md` / `.vi.md`.
- Viết 2 bài tập:
  - `ex01-slow-requests` (`kind: debug`): hàm `slow_requests(df, limit_ms)`, starter chạy không crash nhưng có đúng 3 bug (`>=` thay `>`, sort tăng dần, thiếu `reset_index(drop=True)`), 4 test so bằng `to_dict("list")`, `list(result.columns)`, `index.tolist()`, hint 3 tầng song ngữ.
  - `ex02-average-score-by-model` (`kind: code`): hàm `average_score_by_model(df)` trả về `dict[str, float]` với `float` thuần, bỏ model không có dòng `"ok"`, làm tròn 2 chữ số, 6 test (gồm trường hợp không có dòng `"ok"` và DataFrame rỗng → `{}`), có `alternatives/01_loop.py` dùng `df.itertuples()` kèm giải thích `.en.md`/`.vi.md`, hint 3 tầng song ngữ.
- Viết `quiz.yaml`: 16 câu hỏi (`6 mcq`, `4 output`, `3 fill`, `3 parsons`; 5 dễ, 8 vừa, 3 khó) và 6 flashcard.
- Cập nhật `curriculum/glossary.yaml`: chỉ thêm 3 thuật ngữ chưa có (`Series`, `groupby`, `aggregation`), bỏ qua `DataFrame` và `index` vì đã có sẵn.
- Chạy `uv run python tools/build_content.py` và mở kiểm tra trực tiếp trên web app đang chạy tại `http://localhost:3000/lesson/p4-02-pandas/`.

## 2. File đã sửa / tạo

- Sửa:
  - `curriculum/glossary.yaml` (thêm `Series`, `groupby`, `aggregation`)
- Tạo mới trong `curriculum/phase-04-data/p4-02-pandas/` (30 file):
  - `meta.yaml`, `lesson.en.md`, `lesson.vi.md`, `quiz.yaml`
  - `examples/01_chat_logs.{py,out,en.md,vi.md}`
  - `examples/02_api_costs_csv.{py,out,en.md,vi.md}`
  - `examples/03_eval_by_model.{py,out,en.md,vi.md}`
  - `exercises/ex01-slow-requests/{exercise.yaml,prompt.en.md,prompt.vi.md,starter.py,solution.py,test_exercise.py}`
  - `exercises/ex02-average-score-by-model/{exercise.yaml,prompt.en.md,prompt.vi.md,starter.py,solution.py,test_exercise.py}`
  - `exercises/ex02-average-score-by-model/alternatives/01_loop.{py,en.md,vi.md}`
- Tạo báo cáo:
  - `tasks/m3-p4-02-pandas.report.md`

## 3. Kết quả lệnh kiểm tra

- `uv run python tools/validate.py --path curriculum/phase-04-data/p4-02-pandas`:
  - `OK: 0 error(s), 0 warning(s). Checked 1 lessons, 7 markdown pairs, 3 examples, 2 exercises, 1 alternatives, 16 questions.`
- `uv run python tools/validate.py`:
  - `OK: 0 error(s), 0 warning(s). Checked 26 lessons, 207 markdown pairs, 76 examples, 52 exercises, 53 alternatives, 498 questions, 5 exams, 1 portfolio, 1 glossary, 1 interview.`
- `uv run python -m pytest curriculum/phase-04-data`:
  - `20 passed in 0.37s` (gồm các test của `p4-01-numpy` và 10 test mới của `p4-02-pandas`).
- `uv run ruff check curriculum/phase-04-data`:
  - `All checks passed!`
- `uv run python tools/build_content.py`:
  - `Built 26 lessons, 5 exams, 156 flashcards, 419 questions -> apps\web\src\generated`
- Kiểm tra trên app (`http://localhost:3000/lesson/p4-02-pandas/` bằng Playwright headless sau khi hoàn tất onboarding):
  - Trang render tiêu đề `DataFrame với Pandas`, 11 khối code Python có nút `Chạy thử` và `Visualize`.
  - Bấm `Chạy thử` ở khối DataFrame mục 1 rồi bấm `Chạy` trong sandbox: Pyodide tải pandas và chạy ra output khớp (`['model', 'tokens', 'score']`, v.v.).
  - Bấm `Visualize` ở khối mục 5 (`calls`) và bấm `Tiếp` tới `Bước 10/10`: hiển thị biến toàn cục `calls` (`DataFrame`) và `Kết quả in ra` bảng 3 cột `model`, `tokens`, `cost`; `Page errors: []`, `Console errors: []`.
- `git status --short`:
  - Chỉ có `M curriculum/glossary.yaml` và thư mục mới `?? curriculum/phase-04-data/p4-02-pandas/` (ngoài `.hallmark/` và `tasks/` có sẵn từ trước). Không đụng vào `apps/`, `tools/`, `syllabus.yaml`, `topics.yaml`, `p4-01-numpy`, các phase khác hay `exams/`.

## 4. Điều còn chưa chắc

- Hai URL trong `further_reading` (`https://pandas.pydata.org/docs/user_guide/10min.html` và `https://pandas.pydata.org/docs/user_guide/groupby.html`) chưa được fetch HTTP trực tiếp để kiểm tra mã 200.
- Trên app web, đã bấm `Chạy thử` và `Visualize` cho các khối code trong tab Bài học, còn thao tác bấm nộp bài trực tiếp trên tab `Bài tập` và `Quiz` trong trình duyệt chỉ mới được kiểm chứng gián tiếp qua `tools/pyrunner/runner.py` và `tools/validate.py` (không mở tab UI để bấm từng câu).
- Phiên bản Pyodide đang dùng trong app chưa được kiểm tra tường minh `pd.__version__` trong output, nhưng hành vi in `DataFrame` và `dtype: object` trên trình duyệt khớp với output đã ghi trong bài.
