# Báo cáo thực hiện: M3 bước 15b — Visualize bảng cho DataFrame / Series / ndarray 2D

## 1. Đã làm gì

### Tracer (`tools/pyrunner/tracer.py`)
- Thêm hằng số `MAX_TABLE_ROWS = 8`, `MAX_TABLE_COLS = 6`, `MAX_CELL_CHARS = 24`.
- Thêm `_cell(value)` định dạng từng ô:
  - Unwrap numpy scalar có `ndim == 0` qua `.item()` trước (tránh in `np.float64(...)`).
  - `None` → `"None"`, `bool` → `"True"` / `"False"`, `float` NaN → `"NaN"`, `float` thường → `format(value, ".6g")`, các kiểu khác → `str(value)`.
  - Cắt tối đa 24 ký tự (thêm `"…"` ở cuối nếu dài hơn).
- Thêm `_table(value)` nhận diện không import `pandas`/`numpy` dựa trên `type(value).__name__` và `type(value).__module__`:
  - `DataFrame` (`pandas*`): `kind: "dataframe"`, `shape: [n_rows, n_cols]`, chỉ lấy lát cắt `.iloc[:8, :6]` qua `itertuples(index=False, name=None)`.
  - `Series` (`pandas*`): `kind: "series"`, `shape: [len, 1]`, `columns: [str(name)]` (hoặc `[""]` nếu `name is None`), chỉ lấy `.iloc[:8]`.
  - `ndarray` (`numpy`, `ndim == 2`): `kind: "array"`, `shape: [n_rows, n_cols]`, `columns`/`index` là chuỗi `"0"`, `"1"`, …, chỉ lấy `[:8, :6]`. Mảng 1D, 3+D và scalar không có khóa `table`.
  - Bọc trong `redirect_stdout(io.StringIO())` và `try/except Exception` để không làm rò stdout của người học hay làm gãy trace khi gặp đối tượng lỗi.
- Cập nhật `_vars(frame)` để gắn khóa `"table"` chỉ khi `_table(value)` khác `None`; biến thường vẫn giữ đúng 3 khóa `name`, `type`, `repr`.

### Types & i18n
- `apps/web/src/lib/types.ts`: Thêm interface `TraceTable` và trường `table?: TraceTable` vào `TraceVar`.
- `apps/web/messages/en.json` & `apps/web/messages/vi.json`: Thêm 2 key `tableShape` và `tablePartial` vào nhóm `visualize`.

### UI (`apps/web/src/components/visualizer.tsx`)
- Với biến có `table`, ô giá trị hiển thị `{rows} × {cols}` (qua `t("tableShape", ...)` màu `text-muted-foreground`) thay cho chuỗi `repr`.
- Ngay dưới hàng biến là một hàng `<td colSpan={3}>` chứa bảng nhỏ (`font-mono text-[11px]`, `border-border`, header `bg-muted/40` có ô góc trống + tên cột, cột index `text-muted-foreground`, `whitespace-nowrap`) được bọc trong `<div className="w-0 min-w-full overflow-x-auto">` để cuộn ngang mà không làm phình khung trên màn hình hẹp.
- Nếu `shape` lớn hơn phần được hiển thị, render dòng chú thích `t("tablePartial", ...)`.
- Cập nhật logic đánh dấu đổi giá trị: `changed = !old || old.repr !== v.repr || JSON.stringify(old.table) !== JSON.stringify(v.table)`.

### Test (`tools/pyrunner/test_tracer.py`)
- Tạo mới 14 test case (dùng `assert` và `pytest.mark.parametrize`) kiểm tra DataFrame 3×2, Series có tên và `name=None`, ndarray 2D vs 1D/3D/scalar, DataFrame 20×10 bị cắt còn 8×6, định dạng `NaN` / `0.1 + 0.2` / `np.float64` / `np.bool_` / `None` / cắt 24 ký tự, biến Python thuần không có khóa `table`, và đối tượng `__str__` in stdout hoặc ném lỗi không làm hỏng trace.

## 2. File đã sửa / tạo

- `tools/pyrunner/tracer.py` (sửa)
- `tools/pyrunner/test_tracer.py` (mới)
- `apps/web/src/lib/types.ts` (sửa `TraceVar` / thêm `TraceTable`)
- `apps/web/messages/en.json` (sửa nhóm `visualize`)
- `apps/web/messages/vi.json` (sửa nhóm `visualize`)
- `apps/web/src/components/visualizer.tsx` (sửa)

Xác nhận `git status --short` chỉ gồm các file trên (ngoài `.hallmark/` và `tasks/`).

## 3. Thời gian `validate.py` trước / sau & ví dụ JSON từ `p4-02`

- Thời gian `uv run python tools/validate.py` **trước** khi sửa (theo spec): **165 s**
- Thời gian `uv run python tools/validate.py` **sau** khi sửa: **163.47 s** (không tăng thời gian chạy).

Ví dụ JSON của biến `calls` (DataFrame thật trong `curriculum/phase-04-data/p4-02-pandas/lesson.en.md`, mục 5 "Adding new columns") ở bước cuối của `trace()`:

```json
{
  "name": "calls",
  "type": "DataFrame",
  "repr": "    model  prompt  reply  tokens  cost\n0  gpt-4o     200    100     300  0.60\n1  claude     150    160     310  0.62\n...",
  "table": {
    "kind": "dataframe",
    "shape": [3, 5],
    "columns": ["model", "prompt", "reply", "tokens", "cost"],
    "index": ["0", "1", "2"],
    "rows": [
      ["gpt-4o", "200", "100", "300", "0.6"],
      ["claude", "150", "160", "310", "0.62"],
      ["llama", "300", "120", "420", "0.84"]
    ]
  }
}
```

## 4. Kết quả lệnh kiểm tra (chạy sau lần sửa cuối)

| Lệnh | Kết quả | Ghi chú |
|---|---|---|
| `uv run python -m pytest tools/pyrunner -q` | Pass (exit 0) | 14/14 test pass |
| `uv run python tools/validate.py` | Pass (exit 0) | `OK: 0 error(s), 0 warning(s). Checked 35 lessons, 272 markdown pairs, 103 examples, 70 exercises, 64 alternatives, 702 questions, 8 exams, 1 portfolio, 1 glossary, 1 interview.` (163.47 s) |
| `uv run python -m pytest curriculum -q` | Pass (exit 0) | Toàn bộ test suite trong `curriculum/` xanh |
| `uv run ruff check tools curriculum` | Exit 1 (68 lỗi có sẵn) | 0 lỗi mới ở code vừa thêm/sửa (`uv run ruff check tools/pyrunner/test_tracer.py` pass hoàn toàn; 5 lỗi E501 còn lại trong `tracer.py` là ở các dòng gốc trước khi sửa) |
| `cmd /c pnpm --filter web typecheck` | Pass (exit 0) | Chạy qua `cmd /c` vì PowerShell execution policy chặn `pnpm.ps1`; `tsc --noEmit` và `build_content.py` pass |
| `git status --short` | Đạt | Chỉ có 6 file trong danh sách được phép (+ `.hallmark/`, `tasks/`) |

## 5. Điều còn chưa chắc

- **Hiển thị trực quan trên trình duyệt & Pyodide thực tế:** Chưa chạy `next dev` / `pnpm --filter web build` (bị cấm theo spec) và chưa kiểm thử tương tác trực tiếp trong trình duyệt (Pyodide pandas 2.3.3 / numpy 2.2.5, cuộn ngang trên màn hình hẹp 375px, và tương phản highlight `bg-warning-soft` ở cả light/dark mode). Cần verify khi boss chạy build / preview UI.
- **Ruff toàn cục `tools curriculum`:** Lệnh `uv run ruff check tools curriculum` trả về exit 1 do 68 lỗi lint có sẵn trong các file không được phép đụng (`tools/build_content.py`, `tools/validate.py`, `tools/pyrunner/runner.py`, v.v.) và các dòng cũ trong `tracer.py`.
