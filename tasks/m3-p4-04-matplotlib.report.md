# Báo cáo: M3 bước 5 — bài `p4-04-matplotlib`

## 1. Đã làm gì

- Xây dựng hoàn chỉnh bài học `curriculum/phase-04-data/p4-04-matplotlib/` song ngữ EN/VI theo `docs/CONTENT_GUIDE.md` và spec `tasks/m3-p4-04-matplotlib.md`:
  - `meta.yaml`: `id: p4-04-matplotlib`, `phase: p4`, `order: 4`, `tags: [plotting, pandas, data]`, `prerequisites: [p4-02-pandas]`, `duration_min: 11`, `review_by: "2027-11-01"`, kèm `further_reading` tới Matplotlib quick start guide và pandas Chart visualization.
  - `lesson.en.md` và `lesson.vi.md`: mở bài nêu lý do trực quan hóa + ghi chú lần Run đầu tải matplotlib mất vài giây; 8 mục chính đúng dàn ý (Figure vs Axes kèm picture in text; nhãn/tiêu đề/marker/grid/chú thích + bảng 6 epoch train/val loss + nhận diện overfitting; `ax.bar` sắp xếp & `ax.barh`; `ax.scatter`; vẽ từ DataFrame với `df.plot` & `groupby + sort_values + plot(kind="bar")` kèm lời mời bấm **Visualize**; mermaid `flowchart TD` 7 node chọn loại biểu đồ + bảng so sánh + callout `> [!TIP]`; `plt.subplots(1, 2, figsize=(8, 3))` + `fig.tight_layout()`; 4 lỗi thường gặp với thông báo lỗi/cảnh báo chạy thật) và mục Tóm tắt/Recap.
  - 3 ví dụ chạy được kèm `.out`, `.en.md`, `.vi.md`, có dòng `print(...)` tóm tắt kết quả bằng chữ:
    - `01_loss_curve.py` (in `Best epoch: 4 (val_loss=0.54)`)
    - `02_cost_by_model.py` (in `gpt-4o: 4.25`, `claude: 2.95`, `mini: 0.40`)
    - `03_latency_scatter.py` (in `Correlation: 0.99`)
  - 2 bài tập kèm bộ test (`test_exercise.py`), cả hai đều trả `(fig, ax)`, không gọi `plt.show()` bên trong hàm và luôn `plt.close(fig)` trong `finally:` của mỗi test:
    - `ex01-loss-chart` (`kind: fill`): `plot_loss(epochs, losses)` với 4 chỗ trống `___`, 5 test, gợi ý 3 tầng EN/VI (tầng 3 chừa 4 chỗ trống).
    - `ex02-cost-bar-chart` (`kind: code`): `cost_bar_chart(df)` với 5 test (không kiểm `xlabel` để tương thích với cách pandas), gợi ý 3 tầng EN/VI (tầng 3 chừa 3 chỗ `...`), kèm `alternatives/01_pandas_plot.py` dùng `Series.plot(kind="bar", ax=ax)` và giải thích EN/VI.
  - `quiz.yaml`: 16 câu hỏi (`5 mcq`, `4 output`, `4 fill`, `3 parsons`; phân bổ độ khó: `5` dễ, `8` vừa, `3` khó) + 6 flashcard (`p4-04-f01`..`p4-04-f06`).
- Thêm 6 thuật ngữ mới vào `curriculum/glossary.yaml`: `figure`, `axes`, `legend`, `line chart`, `bar chart`, `scatter plot`.
- Chạy `uv run python tools/build_content.py` để cập nhật bundle nội dung cho web app (`apps/web/src/generated`).
- Xử lý **Feedback vòng 1** (hạ tầng headless matplotlib):
  - `tools/validate.py`: thêm `os.environ.setdefault("MPLBACKEND", "Agg")` ngay sau các dòng import đầu file (với comment ngắn giải thích tracer và browser runner chạy in-process), giữ nguyên `MPLBACKEND="Agg"` trong `run_python`.
  - `curriculum/conftest.py`: thêm `os.environ.setdefault("MPLBACKEND", "Agg")` ở cấp module sau `import pytest` (với comment ngắn) để `uv run python -m pytest curriculum` luôn dùng backend không mở cửa sổ.

## 2. File đã sửa / tạo

- Sửa:
  - `curriculum/glossary.yaml` (chỉ thêm 6 thuật ngữ mới ở cuối file)
  - `tools/validate.py` (thêm `os.environ.setdefault("MPLBACKEND", "Agg")` sau phần import đầu file)
  - `curriculum/conftest.py` (thêm `os.environ.setdefault("MPLBACKEND", "Agg")` ở cấp module)
- Tạo mới trong `curriculum/phase-04-data/p4-04-matplotlib/`:
  - `meta.yaml`, `lesson.en.md`, `lesson.vi.md`, `quiz.yaml`
  - `examples/01_loss_curve.{py,out,en.md,vi.md}`
  - `examples/02_cost_by_model.{py,out,en.md,vi.md}`
  - `examples/03_latency_scatter.{py,out,en.md,vi.md}`
  - `exercises/ex01-loss-chart/{exercise.yaml,prompt.en.md,prompt.vi.md,starter.py,solution.py,test_exercise.py}`
  - `exercises/ex02-cost-bar-chart/{exercise.yaml,prompt.en.md,prompt.vi.md,starter.py,solution.py,test_exercise.py}`
  - `exercises/ex02-cost-bar-chart/alternatives/01_pandas_plot.{py,en.md,vi.md}`
  - (Cùng `apps/web/src/generated` được sinh lại bởi `tools/build_content.py` theo checklist.)

## 3. Kết quả lệnh kiểm tra

Tất cả các lệnh sau được chạy trong shell **không** đặt biến môi trường `MPLBACKEND`:

- `uv run python tools/validate.py --path curriculum/phase-04-data/p4-04-matplotlib`:
  - Kết quả: `OK: 0 error(s), 0 warning(s). Checked 1 lessons, 7 markdown pairs, 3 examples, 2 exercises, 1 alternatives, 16 questions.` (exit 0, `11.43s`).
- `uv run python tools/validate.py`:
  - Kết quả: `OK: 0 error(s), 0 warning(s). Checked 28 lessons, 221 markdown pairs, 82 examples, 56 exercises, 55 alternatives, 530 questions, 5 exams, 1 portfolio, 1 glossary, 1 interview.` (exit 0, `79.38s`).
- `uv run python -m pytest curriculum`:
  - Kết quả: `550 passed, 14 warnings in 1.20s` (exit 0, tổng thời gian chạy lệnh `1.59s`; các warning là `PyparsingDeprecationWarning` từ matplotlib).
- `uv run python -m pytest curriculum/phase-04-data`:
  - Kết quả: `40 passed, 14 warnings in 0.68s` (exit 0).
- `uv run ruff check curriculum/phase-04-data curriculum/conftest.py`:
  - Kết quả: `All checks passed!` (exit 0).
- Tìm kiếm các mẫu bị cấm (`astype\(int\)|dtype=int\b|\.info\(`) trong `curriculum/phase-04-data/p4-04-matplotlib`:
  - Kết quả: rỗng (exit 0, không có dòng khớp).
- `git status --short`:
  - `M curriculum/conftest.py`, `M curriculum/glossary.yaml`, `M tools/validate.py`, `?? curriculum/phase-04-data/p4-04-matplotlib/`, cùng `.hallmark/` và `tasks/` có sẵn từ trước.

## 4. Điều còn chưa chắc

- **Kiểm tra trên trình duyệt thực tế (`http://localhost:3000/lesson/p4-04-matplotlib/`)**: Môi trường của worker không có công cụ trình duyệt nên chưa mở trang bài học thực tế để bấm **Run** / **Visualize** và kiểm tra việc hiển thị ảnh PNG từ Pyodide matplotlib 3.8.4 (boss cần tự kiểm bước này).
- **Khác biệt Matplotlib 3.9.2 (local) vs 3.8.4 (Pyodide app)**: Toàn bộ API đã dùng (`plt.subplots`, `ax.plot`, `ax.bar`, `ax.barh`, `ax.scatter`, `ax.set_title`, `ax.set_xlabel`, `ax.set_ylabel`, `ax.legend`, `ax.grid`, `fig.tight_layout`, `df.plot`, `Series.plot`, `ax.lines`, `ax.patches`, `ax.get_xticklabels`, `ax.get_legend`) đều là API ổn định có từ các bản 3.x cũ, nhưng chưa chạy trực tiếp trong runtime Pyodide 3.8.4 trên trình duyệt.
