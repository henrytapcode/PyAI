# M3 bước 1: nền tảng cho nội dung Data & ML

## Mục tiêu
Chuẩn bị để viết bài phase 4–5 (NumPy, Pandas, Matplotlib, SQLite, scikit-learn):
A. Môi trường local (`uv`) có đủ thư viện để `validate.py` và `pytest` chạy được example/exercise dùng các thư viện này, với kết quả in ra giống Pyodide.
B. Biểu đồ Matplotlib hiện thành ảnh trong ô Output của app (Pyodide không có cửa sổ).
C. Syllabus phase 4–5 có đủ `outcomes` song ngữ như phase 1–3.

Chưa viết bài học nào.

## File được phép sửa/tạo
- `pyproject.toml`, `uv.lock` (qua `uv add`/`uv lock`, không sửa tay `uv.lock`)
- `tools/validate.py` — chỉ hàm `run_python` (biến môi trường)
- `tools/pyrunner/runner.py` — chỉ nếu cần đặt backend Agg trước khi chạy test (xem B4)
- `apps/web/public/pyodide-worker.js`
- `apps/web/src/lib/python.ts`
- `apps/web/src/components/workbench.tsx`
- `apps/web/messages/en.json`, `apps/web/messages/vi.json` (thêm key mới, không sửa key cũ)
- `curriculum/syllabus.yaml` — chỉ khối `p4` và `p5`
- `curriculum/topics.yaml` — thêm tag mới (C3)

## Không được đụng
- Nội dung `curriculum/phase-*`, `exams/`, `placement/`, mọi file khác trong `apps/web/src`.
- Không đổi luồng message hiện có của worker (`stdout`/`stderr`/`done`/`result`), chỉ thêm loại mới.
- Không xóa file, không `git commit`.
- **Không chạy `pnpm --filter web build`** (boss tự build, vì dev server có thể đang chạy).

## Tiêu chí hoàn thành (checklist)

### A. Thư viện local
1. [ ] `uv add` các gói với phiên bản trùng Pyodide 0.29.5: `numpy==2.2.5`, `pandas==2.3.3`, `scikit-learn==1.7.0`. Matplotlib: `matplotlib==3.8.4` nếu có wheel cho Python 3.13 trên Windows; nếu không, dùng bản 3.9.x thấp nhất có wheel và ghi lý do vào report (ảnh không bị so sánh nên lệch bản nhỏ chấp nhận được).
2. [ ] `run_python` trong `tools/validate.py` đặt thêm `MPLBACKEND="Agg"` trong `env`, để example có `plt.show()` không mở cửa sổ và không treo.
3. [ ] Chứng minh: lệnh kiểm tra số 3 dưới đây in đúng phiên bản.

### B. Hiển thị biểu đồ Matplotlib
1. [ ] Trong `pyodide-worker.js`, ở nhánh `run`: nếu code có import `matplotlib`, trước khi chạy đặt backend Agg (vd `os.environ["MPLBACKEND"]="Agg"` hoặc `matplotlib.use("Agg")` sau khi `loadImports`) và thay `plt.show` bằng hàm không làm gì (để tránh warning của Agg). Sau khi chạy xong (kể cả khi lỗi), với mỗi figure đang mở (`plt.get_fignums()`): lưu PNG (`dpi=100`, `bbox_inches="tight"`) vào `io.BytesIO`, mã hóa base64, gửi `{type:"image", id, data:"data:image/png;base64,..."}` theo thứ tự figure, rồi `plt.close("all")`. Gửi các message `image` **trước** message `done`.
   - Code không import matplotlib: không đụng gì, không tải matplotlib.
2. [ ] Cập nhật comment đầu file worker (danh sách "Messages out") thêm `{type:"image", id, data}`.
3. [ ] `python.ts`: chuyển message `image` tới callback output của lần chạy đó với stream mới `"image"` (mở rộng kiểu stream thành `"stdout" | "stderr" | "image"`). Không đổi chữ ký các hàm public khác.
4. [ ] Với `test` và `trace`: chỉ cần đảm bảo code có `plt.show()` không treo/không lỗi (đặt Agg trước khi chạy). Không cần gửi ảnh. Nếu việc này cần sửa `runner.py`, chỉ thêm đúng phần đặt backend.
5. [ ] `workbench.tsx`: `OutLine.stream` thêm `"image"`; dòng image hiển thị thành `<img>` trong ô Output:
   - `alt` lấy từ i18n, key mới `editor.figureAlt` = "Figure {n}" / "Biểu đồ {n}" (n đếm từ 1 trong lần chạy đó).
   - `max-w-full h-auto`, nền trắng (biểu đồ Matplotlib nền trắng, đọc được cả ở dark mode), bo `rounded-[10px]`, viền hairline `border border-border`, khoảng cách dọc như các dòng output khác. Theo `apps/web/design.md`; không dùng màu cứng ngoài `bg-white` cho nền ảnh.
   - Nút xóa/copy output (nếu có) không bị vỡ: copy chỉ lấy dòng chữ, bỏ qua ảnh.
6. [ ] Thêm key vào **cả** `en.json` và `vi.json`.

### C. Syllabus phase 4–5
1. [ ] Đổi mỗi bài trong `p4` và `p5` từ dạng một dòng `{ id: ..., title: ..., prerequisites: [...] }` sang dạng nhiều dòng như phase 3, giữ nguyên `id`, `title`, `kind`, và thêm `outcomes` đúng như bảng dưới. Prerequisites theo bảng (đã chỉnh so với bản outline).
2. [ ] Không đổi gì ở `p0`–`p3`, `p6`–`p8`, `capstones`.
3. [ ] Thêm vào `curriculum/topics.yaml` các tag (theo đúng định dạng file đó, có tên en/vi): `numpy`, `pandas`, `data-cleaning`, `plotting`, `sql`, `ml-math`, `supervised-learning`, `sklearn`, `model-evaluation`. Tag nào đã có thì bỏ qua.

| id | prerequisites | outcomes en | outcomes vi |
|---|---|---|---|
| p4-01-numpy | p2-01-comprehensions | "Create arrays and read shape and dtype"; "Vectorised math instead of loops"; "Index, slice and filter with boolean masks" | "Tạo mảng, đọc shape và dtype"; "Tính toán vector hóa thay cho vòng lặp"; "Index, slice và lọc bằng boolean mask" |
| p4-02-pandas | p4-01-numpy, p1-09-files | "Build a DataFrame from dicts and CSV"; "Select rows and columns with loc and filters"; "Group and aggregate with groupby" | "Tạo DataFrame từ dict và CSV"; "Chọn hàng, cột bằng loc và bộ lọc"; "Gom nhóm và tổng hợp bằng groupby" |
| p4-03-cleaning | p4-02-pandas | "Find and fill missing values"; "Fix column types and messy text"; "Drop duplicates and invalid rows" | "Tìm và điền giá trị thiếu"; "Sửa kiểu cột và văn bản lộn xộn"; "Bỏ dòng trùng và dòng không hợp lệ" |
| p4-04-matplotlib | p4-02-pandas | "Line, bar and scatter plots"; "Label axes, titles and legends"; "Plot straight from a DataFrame" | "Biểu đồ đường, cột và scatter"; "Đặt nhãn trục, tiêu đề và chú thích"; "Vẽ trực tiếp từ DataFrame" |
| p4-05-sql | p4-02-pandas | "Create a table and insert rows with sqlite3"; "SELECT with WHERE, ORDER BY and GROUP BY"; "Load query results into pandas" | "Tạo bảng và thêm dòng bằng sqlite3"; "SELECT với WHERE, ORDER BY và GROUP BY"; "Đưa kết quả truy vấn vào pandas" |
| p4-06-mini-project (kind: project) | p4-03-cleaning, p4-04-matplotlib, p4-05-sql | "Clean, aggregate and plot a realistic dataset"; "Answer business questions with pandas and SQL" | "Làm sạch, tổng hợp và vẽ một bộ dữ liệu thực tế"; "Trả lời câu hỏi nghiệp vụ bằng pandas và SQL" |
| p5-01-math-bridge | p4-01-numpy, p4-04-matplotlib | "Vectors and the dot product in NumPy"; "A gradient as the downhill direction"; "Gradient descent on a straight line" | "Vector và tích vô hướng trong NumPy"; "Gradient là hướng xuống dốc"; "Gradient descent cho một đường thẳng" |
| p5-02-supervised | p5-01-math-bridge, p4-02-pandas | "Features, labels and the train/test split"; "Regression versus classification"; "Spot overfitting on a plot" | "Feature, label và chia train/test"; "Regression và classification khác nhau thế nào"; "Nhận ra overfitting trên biểu đồ" |
| p5-03-sklearn | p5-02-supervised | "fit, predict and score"; "Pipelines with preprocessing"; "Compare two models fairly" | "fit, predict và score"; "Pipeline có bước tiền xử lý"; "So sánh hai mô hình công bằng" |
| p5-04-evaluation | p5-03-sklearn | "Accuracy, precision, recall and F1"; "Read a confusion matrix"; "Cross-validation" | "Accuracy, precision, recall và F1"; "Đọc confusion matrix"; "Cross-validation" |
| p5-05-mini-project (kind: project) | p5-04-evaluation, p4-03-cleaning | "Train and evaluate a classifier end to end"; "Report results honestly" | "Huấn luyện và đánh giá một bộ phân loại từ đầu đến cuối"; "Báo cáo kết quả trung thực" |

## Lệnh kiểm tra
Từ gốc repo `D:\Proj\python-ai-platform`:
```
uv sync
uv run python tools/validate.py
uv run python -m pytest curriculum
uv run python -c "import numpy, pandas, sklearn, matplotlib; print(numpy.__version__, pandas.__version__, sklearn.__version__, matplotlib.__version__)"
uv run python -c "import os,subprocess,sys; sys.path.insert(0,'tools'); import validate; print(validate.run_python('import matplotlib.pyplot as plt; plt.plot([1,2]); plt.show(); print(\"ok\")'))"
pnpm --filter web typecheck
git diff --stat
```
Mong đợi: validate OK (như trước, không lỗi mới); pytest exit 0; dòng phiên bản `2.2.5 2.3.3 1.7.0 3.x`; lệnh matplotlib in `(0, 'ok\n', '')` hoặc tương đương (exit 0, không treo); typecheck 0 lỗi; diff chỉ các file trong danh sách được phép.
Tự kiểm tra trong app (nếu dev server đang chạy ở `http://localhost:3000/playground/`): chạy `import matplotlib.pyplot as plt` / `plt.plot([1, 4, 9])` / `plt.show()` → ô Output hiện một ảnh biểu đồ. Không bật/tắt dev server.

## Ghi chú cho worker
- Đọc `apps/web/design.md` trước khi sửa `workbench.tsx`.
- Windows: dùng `pnpm.cmd` nếu PowerShell chặn `pnpm`. Dùng `uv run python -m pytest`, không dùng `uv run pytest` (lỗi launcher).
- Không nhúng chuỗi UI cứng; mọi chữ mới qua next-intl.
- `validate.py` dùng `python -I`, nên biến môi trường phải đặt qua `env`, không qua `sitecustomize`.

## Trạng thái
- Bước hiện tại: 5 (đạt sau vòng 1, chờ user duyệt commit)
- Vòng: 1/3
- Số lần swap: 0
- Fallback: không
- Model: Gemini 4 Hydrogen (High)
