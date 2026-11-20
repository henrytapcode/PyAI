# Báo cáo thực hiện: M3 bước 1 (`m3-01-foundation`)

## 1. Đã làm gì

### A. Thư viện local (`uv`) & `validate.py`
- Cài đặt các gói Data & ML vào môi trường `uv` (`pyproject.toml`, `uv.lock`):
  - `numpy==2.2.5`, `pandas==2.3.3`, `scikit-learn==1.7.0` (trùng phiên bản Pyodide 0.29.5).
  - `matplotlib==3.9.2`: đã thử `matplotlib==3.8.4` trước nhưng thất bại khi build từ source trên Python 3.13.15 Windows (`cp313`, `win_amd64`) vì không có sẵn wheel cho 3.8.4 và máy thiếu Microsoft Visual C++ 14.0 Build Tools để biên dịch `freetype`. Kiểm tra PyPI cho thấy `3.9.2` là phiên bản `3.9.x` thấp nhất có wheel `cp313` cho `win_amd64`, nên đã cài `matplotlib==3.9.2`.
- Cập nhật hàm `run_python` trong `tools/validate.py` để thêm `MPLBACKEND="Agg"` vào `env` của subprocess (`python -I`).

### B. Hiển thị biểu đồ Matplotlib & hỗ trợ `Agg` cho `test` / `trace`
- **`apps/web/public/pyodide-worker.js`**:
  - Cập nhật comment `Messages out` ở đầu file bổ sung `{type:"image", id, data}`.
  - Định nghĩa các helper Python trong `init()` (không import `matplotlib` lúc khởi động worker): `_pyai_uses_matplotlib` (kiểm tra bằng `ast.parse` để tránh kích hoạt nhầm với comment/chuỗi), `_pyai_prepare_mpl` (đặt `os.environ["MPLBACKEND"] = "Agg"`, gọi `matplotlib.use("Agg")`, thay `plt.show` bằng hàm không làm gì), `_pyai_collect_mpl_images` (lặp `plt.get_fignums()`, xuất PNG `dpi=100`, `bbox_inches="tight"` vào `io.BytesIO`, encode base64 dạng `data:image/png;base64,...`, rồi `plt.close("all")` trong `finally`), và `_pyai_close_mpl`.
  - Nhánh `run`: kiểm tra `usesMatplotlib(msg.code)` (lọc nhanh `/\bmatplotlib\b/` trước khi gọi AST). Nếu có import `matplotlib`, chuẩn bị `Agg` trước khi chạy; sau khi chạy xong (kể cả khi code lỗi), thu toàn bộ figure đang mở và gửi từng `{type:"image", id, data}` theo thứ tự figure **trước** khi gửi `{type:"done", ...}`. Code không import `matplotlib` không chạm tới và không tải `matplotlib`.
  - Nhánh `test` và `trace`: nếu `msg.code` có import `matplotlib`, chuẩn bị `Agg` + `plt.show` no-op trước khi chạy và đóng toàn bộ figure sau khi chạy xong (không gửi ảnh).
- **`tools/pyrunner/runner.py`**:
  - Thêm `_uses_matplotlib(*sources)` và xử lý đặt `MPLBACKEND="Agg"`, `matplotlib.use("Agg")`, `plt.show` no-op trước khi nạp `exercise`/`test_exercise` trong `run_tests` (chỉ khi `user_code` hoặc `test_code` có import `matplotlib`), kèm `plt.close("all")` trong `finally`.
- **`apps/web/src/lib/python.ts`**:
  - Mở rộng kiểu callback `onOutput` trong `Pending` từ `"stdout" | "stderr"` thành `"stdout" | "stderr" | "image"`.
  - Chuyển tiếp message `{ type: "image", data }` qua `p?.onOutput?.(String(msg.data), "image")`. Giữ nguyên chữ ký các hàm public khác.
- **`apps/web/src/components/workbench.tsx`**:
  - Mở rộng `OutLine.stream` thêm `"image"`.
  - Hiển thị dòng `image` bằng thẻ `<img>` trong ô Output với `alt={t("figureAlt", { n: figIndex })}` (`figIndex` đếm từ 1 trong lần chạy hiện tại), class `my-1 block max-w-full h-auto rounded-[10px] border border-border bg-white`. Không có nút copy output riêng trong `workbench.tsx`; nút Clear (`setOutput([])`) hoạt động bình thường.
- **`apps/web/messages/en.json` & `apps/web/messages/vi.json`**:
  - Thêm key `editor.figureAlt`: `"Figure {n}"` (en) và `"Biểu đồ {n}"` (vi); không sửa key cũ.

### C. Syllabus phase 4–5 & Topic tags
- **`curriculum/syllabus.yaml`**:
  - Chuyển toàn bộ các bài trong `p4` (6 bài) và `p5` (5 bài) từ dạng inline sang dạng nhiều dòng như `p3`, giữ nguyên `id`, `title`, `kind`, cập nhật `prerequisites` và thêm `outcomes` song ngữ `en`/`vi` đúng theo bảng spec. Không thay đổi `p0`–`p3`, `p6`–`p8`, `capstones`.
- **`curriculum/topics.yaml`**:
  - Thêm 9 tag mới (đều chưa tồn tại trước đó) với tên `en`/`vi`: `numpy`, `pandas`, `data-cleaning`, `plotting`, `sql`, `ml-math`, `supervised-learning`, `sklearn`, `model-evaluation`.

## 2. File đã sửa / tạo
- `pyproject.toml`
- `uv.lock`
- `tools/validate.py`
- `tools/pyrunner/runner.py`
- `apps/web/public/pyodide-worker.js`
- `apps/web/src/lib/python.ts`
- `apps/web/src/components/workbench.tsx`
- `apps/web/messages/en.json`
- `apps/web/messages/vi.json`
- `curriculum/syllabus.yaml`
- `curriculum/topics.yaml`
- `tasks/m3-01-foundation.report.md` (báo cáo này)

*(Lưu ý: `apps/web/public/pyrunner/runner.py` là bản sao được tạo tự động bởi `tools/build_content.py` khi chạy `pnpm.cmd --filter web typecheck` và nằm trong `.gitignore`.)*

## 3. Kết quả lệnh kiểm tra

| Lệnh | Kết quả |
|---|---|
| `uv sync` | Thành công (exit 0): `Resolved 34 packages in 0.67ms`, `Checked 30 packages in 0.90ms` |
| `uv run python tools/validate.py` | Thành công (exit 0): `OK: 0 error(s), 0 warning(s). Checked 24 lessons, 193 markdown pairs, 70 examples, 48 exercises, 51 alternatives, 466 questions, 5 exams, 1 portfolio, 1 glossary, 1 interview.` |
| `uv run python -m pytest curriculum` | Thành công (exit 0): `510 passed in 0.80s` |
| `uv run python -c "import numpy, pandas, sklearn, matplotlib; print(numpy.__version__, pandas.__version__, sklearn.__version__, matplotlib.__version__)"` | Thành công (exit 0): `2.2.5 2.3.3 1.7.0 3.9.2` |
| `validate.run_python('import matplotlib.pyplot as plt; plt.plot([1,2]); plt.show(); print("ok")')` | Thành công (exit 0, không treo): `(0, 'ok\n', '<string>:1: UserWarning: FigureCanvasAgg is non-interactive, and thus cannot be shown\n')` |
| `runner.run_tests(...)` với code dùng `matplotlib` + `plt.show()` | Thành công: `{'ok': True, 'passed': 1, 'total': 1, 'tests': [{'name': 'test_make', 'label': 'make', 'status': 'passed', 'message': None, 'line': None}], 'error': None, 'stdout': ''}` |
| `pnpm.cmd --filter web typecheck` | Thành công (exit 0): `Built 24 lessons, 5 exams, 144 flashcards, 387 questions -> apps\web\src\generated`, `tsc --noEmit` 0 lỗi |
| `git diff --stat` | Chỉ gồm 11 file trong danh sách được phép (+ `tasks/m3-01-foundation.report.md` mới tạo) |
| Kiểm tra trực tiếp trên `http://localhost:3000/playground/` bằng Playwright (headless Chromium) | Chạy `import matplotlib.pyplot as plt` / `plt.plot([1, 4, 9])` / `plt.show()` / `print('done_plot')` → xuất hiện `<img>` hợp lệ (`alt="Biểu đồ 1"`, `class="my-1 block max-w-full h-auto rounded-[10px] border border-border bg-white"`, kích thước `536x415`, `src="data:image/png;base64,..."` độ dài 21638 ký tự), kèm text `done_plot` và `✓ Xong`, `Errors: []`. |

## 4. Điều còn chưa chắc
- Không chạy `pnpm --filter web build` theo yêu cầu spec, nên quá trình production build/ESLint của Next.js chưa được kiểm chứng trong bước này.
- Nhánh `test` và `trace` với code `matplotlib` trong môi trường Pyodide trình duyệt chưa có bài tập thực tế để chạy thử trực tiếp trên UI (mới kiểm tra `run_tests` ở CPython local và kiểm tra trực tiếp nhánh `run` trong Pyodide trên `/playground/`).
- Trong `tools/validate.py`, hàm `check_examples` gọi `tracer.trace(...)` in-process sau `run_python(...)`; vì `tracer.py` không nằm trong danh sách file được phép sửa, nếu sau này có example ở phase 4 dùng `plt.show()`, `tracer.trace` chạy in-process trên Windows có thể cần đặt `MPLBACKEND="Agg"` trong môi trường chạy hoặc trong `validate.py`/`tracer.py` ở bước viết bài (khi chạy `validate.py` thông thường trên Windows).
- Khi chạy `validate.run_python(...)` có `plt.show()`, `stderr` vẫn có `UserWarning: FigureCanvasAgg is non-interactive, and thus cannot be shown` (vì `validate.py` không monkeypatch `plt.show`, chỉ đặt `MPLBACKEND="Agg"`). Khi chạy trong app (`pyodide-worker.js`) hoặc `runner.py`, `plt.show` đã được thay bằng no-op nên không có warning này.
