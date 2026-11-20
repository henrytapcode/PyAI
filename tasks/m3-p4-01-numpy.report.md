# Báo cáo: M3 bước 2 — bài `p4-01-numpy` (NumPy arrays)

## 1. Đã làm gì

- Tạo bài học đầu tiên của Phase 4 tại `curriculum/phase-04-data/p4-01-numpy/` đúng cấu trúc `docs/CONTENT_GUIDE.md` và dàn ý trong `tasks/m3-p4-01-numpy.md`:
  - `meta.yaml`: `id: p4-01-numpy`, `phase: p4`, `order: 1`, `level: beginner`, `tags: [numpy, data]`, `prerequisites: [p2-01-comprehensions]`, `duration_min: 11`, `review_by: "2027-11-01"`, kèm 2 link `further_reading` chính thức trên `numpy.org` (Absolute beginners & Broadcasting).
  - `lesson.en.md` và `lesson.vi.md`:
    - Opening về lý do AI engineer cần NumPy (embedding 384 số, batch dự đoán).
    - 8 mục: (1) Array là gì (`np.array`, `shape`, `dtype`, `ndim`, `len`, bảng so sánh `list` vs `array`), (2) Tính toán vector hóa (`a * 2`, `a + b`, `a ** 2`, khác biệt `list * 2` vs `array * 2`, scalar broadcasting), (3) Hàm tổng hợp (`sum`, `mean`, `min`, `max`, `argmax`, `np.round` + trace table cộng dồn cho `mean`), (4) Mảng 2D (`shape == (rows, cols)`, `grid[r, c]`, `grid[1]`, `grid[:, 0]`, `axis=0` / `axis=1` + picture in text trong fence `text`), (5) Boolean mask (`a > 3`, `a[a > 3]`, `&`, `|` có ngoặc, `.sum()` + mermaid `flowchart LR` + lời mời bấm **Visualize**), (6) Tạo mảng nhanh (`np.arange`, `np.zeros`, `np.ones`, `np.linspace`, `reshape`), (7) 4 lỗi thường gặp (`and` thay `&`, quên ngoặc `a > 1 & a < 5`, gán float vào mảng int bị cắt phần thập phân, slice là view nên sửa slice làm đổi mảng gốc và cách dùng `.copy()`), (8) Tóm tắt (`Recap` / `Tóm tắt`).
    - Đảm bảo parity giữa EN và VI (cùng số heading, cùng callout `[!NOTE]`, `[!TIP]`, `[!WARNING]`, token code Python giống nhau, cùng số dòng mermaid, fence `text` giống hệt).
  - `examples/` (3 ví dụ, mỗi ví dụ gồm `.py`, `.out`, `.en.md`, `.vi.md`):
    - `01_sensor_readings`: nhiệt độ cảm biến, `min`/`max`/`mean`, lọc outlier bằng mask.
    - `02_score_matrix`: ma trận điểm 2D `(4, 3)`, trung bình theo `axis=0` và `axis=1`, tìm học viên cao nhất bằng `argmax()`.
    - `03_batch_predictions`: ma trận xác suất `(4, 3)`, `argmax(axis=1)`, đếm mẫu có xác suất `>= 0.8`.
    - Mọi lệnh `print` chỉ in array, scalar đơn lẻ hoặc `float()`/`int()`/`str`, không in list/tuple/dict chứa NumPy scalar.
  - `exercises/` (2 bài tập):
    - `ex01-min-max-scale` (`kind: fill`, `id: p4-01-ex01`): hoàn thành `min_max_scale(values)` giữ nguyên `shape`, không sửa mảng đầu vào; 5 test dùng `.tolist()` / `ravel().tolist()` với `pytest.approx`; 3 tầng hint EN/VI.
    - `ex02-predicted-labels` (`kind: code`, `id: p4-01-ex02`): viết `predicted_labels(probs, labels, threshold) -> list[str]`, `alternatives/01_loop.py` + `.en.md`/`.vi.md`; 5 test (gồm hòa điểm `argmax` lấy chỉ số đầu tiên, `prob == threshold` vẫn nhận, trả Python `list[str]`, batch rỗng và không sửa input); 3 tầng hint EN/VI.
  - `quiz.yaml`: 16 câu hỏi (`6 mcq`, `4 output`, `3 fill`, `3 parsons`; phân bố 5 dễ, 8 vừa, 3 khó) và 6 flashcard (`p4-01-f01`..`p4-01-f06`).
- `curriculum/glossary.yaml`: thêm 6 thuật ngữ mới (`dtype`, `shape`, `vectorization`, `broadcasting`, `boolean mask`, `axis`). Thuật ngữ `array` đã tồn tại sẵn trong `glossary.yaml` (dòng 1012) nên không thêm trùng.
- **Không** tạo file cấp phase nào trong `curriculum/phase-04-data/` (validator không yêu cầu file cấp phase khi không có `phase-test.yaml`).

## 2. File đã sửa / tạo

- Sửa: `curriculum/glossary.yaml`
- Tạo mới thư mục `curriculum/phase-04-data/p4-01-numpy/`:
  - `meta.yaml`
  - `lesson.en.md`, `lesson.vi.md`
  - `quiz.yaml`
  - `examples/01_sensor_readings.{py,out,en.md,vi.md}`
  - `examples/02_score_matrix.{py,out,en.md,vi.md}`
  - `examples/03_batch_predictions.{py,out,en.md,vi.md}`
  - `exercises/ex01-min-max-scale/{exercise.yaml,prompt.en.md,prompt.vi.md,starter.py,solution.py,test_exercise.py}`
  - `exercises/ex02-predicted-labels/{exercise.yaml,prompt.en.md,prompt.vi.md,starter.py,solution.py,test_exercise.py}`
  - `exercises/ex02-predicted-labels/alternatives/01_loop.{py,en.md,vi.md}`
- Chạy `uv run python tools/build_content.py` để cập nhật JSON sinh sẵn trong `apps/web/src/generated/` (gitignored) cho dev server.

## 3. Kết quả lệnh kiểm tra

- `uv run python tools/validate.py --path curriculum/phase-04-data/p4-01-numpy`: exit 0 — `OK: 0 error(s), 0 warning(s). Checked 1 lessons, 7 markdown pairs, 3 examples, 2 exercises, 1 alternatives, 16 questions.`
- `uv run python tools/validate.py`: exit 0 — `OK: 0 error(s), 0 warning(s). Checked 25 lessons, 200 markdown pairs, 73 examples, 50 exercises, 52 alternatives, 482 questions, 5 exams, 1 portfolio, 1 glossary, 1 interview.`
- `uv run python -m pytest curriculum/phase-04-data`: exit 0 — `10 passed in 0.08s`
- `uv run ruff check curriculum/phase-04-data`: exit 0 — `All checks passed!`
- `uv run python tools/build_content.py`: exit 0 — `Built 25 lessons, 5 exams, 150 flashcards, 403 questions -> apps\web\src\generated`
- `git status --short`:
  ```text
   M curriculum/glossary.yaml
  ?? .hallmark/
  ?? curriculum/phase-04-data/
  ?? tasks/
  ```
- Kiểm tra trực tiếp trên app (`http://localhost:3000/lesson/p4-01-numpy/`) bằng Playwright Chromium headless:
  - Trang load tiêu đề `Mảng NumPy`, 0 pageerror.
  - Bấm **Run/Chạy** ở khối code mục 5 (`Boolean mask`): Pyodide tải numpy và in đúng `[False  True False  True]`.
  - Bấm **Visualize** ở khối code mục 5 và bước tới bước `9/9`: hiển thị đủ biến toàn cục (`scores`, `mask`, `high`, `count`) với kiểu `ndarray`/`int` và stdout `[False  True False  True] / [0.9 0.8] / 2`.

## 4. Điều còn chưa chắc

- Trên trình duyệt thực tế (`http://localhost:3000/lesson/p4-01-numpy/`), mới tự động kiểm tra trang bài học tiếng Việt cùng nút **Run/Chạy** và **Visualize** ở khối code mục 5; chưa bấm thử trực tiếp trên trình duyệt các tab **Ví dụ**, **Bài tập** (trình soạn thảo) và **Quiz** hay giao diện EN của trang này (tuy nhiên `validate.py` đã chạy kiểm chứng toàn bộ 3 example bằng `tracer.py`, 2 exercise bằng cả `pytest` lẫn `tools/pyrunner/runner.py` giống Pyodide, và cả 16 câu quiz).
- Thuật ngữ `array` đã có sẵn trong `curriculum/glossary.yaml` từ trước nên giữ nguyên bản gốc và chỉ bổ sung 6 thuật ngữ còn lại (`dtype`, `shape`, `vectorization`, `broadcasting`, `boolean mask`, `axis`).
