# M3 bước 15b: Visualize hiển thị DataFrame / Series / mảng 2D dạng bảng

## Mục tiêu
Hiện tại Visualize chỉ nhận một chuỗi `repr` (tối đa 120 ký tự) cho mỗi biến, nên DataFrame và mảng 2D bị dồn một dòng rồi cắt "...". Phase 4–5 mời người học bấm Visualize trên khối có DataFrame (vd p4-02 §"watch `calls` gain the `tokens` and `cost` columns", p4-06 "watch `df` shrink"), nên phải nhìn được bảng.
Thêm trường `table` (tùy chọn) vào mỗi biến trong trace cho pandas `DataFrame`, pandas `Series`, NumPy `ndarray` 2 chiều; UI vẽ bảng nhỏ cuộn ngang khi có `table`.

## File được phép sửa/tạo
- `tools/pyrunner/tracer.py`
- `tools/pyrunner/test_tracer.py` (mới)
- `apps/web/src/components/visualizer.tsx`
- `apps/web/src/lib/types.ts` (chỉ interface `TraceVar`)
- `apps/web/messages/en.json`, `apps/web/messages/vi.json` (chỉ nhóm `visualize`)

## Không được đụng
- `curriculum/`, `tools/validate.py`, `tools/build_content.py`, `tools/pyrunner/runner.py`, `apps/web/public/pyodide-worker.js`, mọi file khác. Không xóa file, không `git commit`.
- **Không chạy `pnpm --filter web build`** (boss chạy). Không chạy dev server.

## Thiết kế (boss chốt)

### Tracer (`tools/pyrunner/tracer.py`)
- Mỗi var vẫn có `name`, `type`, `repr` như cũ (giữ nguyên cách tính `repr`). Thêm khóa `table` **chỉ khi** biến là một trong ba loại dưới; biến khác không có khóa `table` (JSON y như cũ).
- Nhận diện **không import** pandas/numpy trong tracer (tracer phải chạy được khi code không dùng chúng): dựa vào `type(value).__module__` (bắt đầu bằng `"pandas"` / bằng `"numpy"`) và `type(value).__name__` (`DataFrame`, `Series`, `ndarray`), ndarray phải có `ndim == 2`. Mảng 1 chiều, 3+ chiều, scalar: không có `table`.
- Hình dạng:
  ```
  "table": {
    "kind": "dataframe" | "series" | "array",
    "shape": [n_rows, n_cols],          # kích thước thật (Series: [len, 1])
    "columns": ["tokens", "cost"],      # chuỗi; ndarray: "0", "1", ...; Series: [str(name)] hoặc [""] nếu name là None
    "index": ["0", "1", "2"],           # chuỗi, chỉ các dòng được hiển thị; ndarray: "0", "1", ...
    "rows": [["120", "0.02"], ...]      # chuỗi, len(rows) == len(index)
  }
  ```
- Giới hạn: `MAX_TABLE_ROWS = 8`, `MAX_TABLE_COLS = 6` (hằng số đầu file). Chỉ lấy phần đầu (`iloc[:8, :6]` cho pandas, slice cho ndarray). UI tự biết bị cắt nhờ so `shape` với số dòng/cột hiển thị.
- Định dạng ô `_cell(x)`: numpy scalar → `.item()` trước; `None` → `"None"`; float NaN → `"NaN"`; float → `format(x, ".6g")`; bool → `"True"`/`"False"`; còn lại `str(x)`; cắt còn tối đa 24 ký tự (thêm "…" nếu cắt). Không bao giờ in `np.float64(...)`.
- Bọc toàn bộ việc dựng bảng trong `try/except Exception` → lỗi thì bỏ `table` (không bao giờ làm hỏng trace). Không được in gì ra stdout của người học.
- Hiệu năng: chỉ đọc phần đầu (không `to_numpy()` cả DataFrame lớn). Thời gian `uv run python tools/validate.py` không được tăng quá ~10% (ghi thời gian trước/sau vào report).

### UI (`visualizer.tsx`)
- `TraceVar` thêm `table?: TraceTable` (định nghĩa interface `TraceTable` theo đúng hình dạng trên trong `types.ts`).
- Biến có `table`: dòng thường vẫn hiện `name` và badge `type`; ô giá trị thay `repr` bằng chữ nhỏ màu muted `"{rows} × {cols}"` (theo `shape`). Ngay dưới là một hàng `colSpan` đủ cột chứa bảng nhỏ:
  - bảng `font-mono text-[11px]`, viền `border-border`, header `bg-muted/40` có ô góc trống + tên cột; cột index chữ `text-muted-foreground`; bọc `overflow-x-auto` để không vỡ khung trên màn hình hẹp; không xuống dòng trong ô (`whitespace-nowrap`).
  - nếu bị cắt (shape lớn hơn phần hiển thị) thì thêm một dòng chú thích nhỏ dưới bảng: i18n `visualize.tablePartial` ("Showing the first {rows} rows and {cols} columns." / VI "Đang hiện {rows} dòng và {cols} cột đầu tiên.").
- Đánh dấu "đã đổi" (nền `bg-warning-soft`) phải tính cả bảng: `changed = !old || old.repr !== v.repr || JSON.stringify(old.table) !== JSON.stringify(v.table)` (để thay đổi ở dòng sau 120 ký tự vẫn được tô).
- Chỉ dùng token màu có sẵn (xem `apps/web/design.md`); không chuỗi UI cứng; thêm key vào **cả** `en.json` và `vi.json` (key `tableShape` nếu cần cho "{rows} × {cols}", và `tablePartial`).

### Test (`tools/pyrunner/test_tracer.py`, mới)
Chỉ dùng assert / pytest.mark.parametrize. Gọi `trace(code)` và tìm var theo tên ở bước cuối. Tối thiểu:
1. DataFrame 3×2: `kind == "dataframe"`, `shape == [3, 2]`, columns, index, rows đúng (cả float và int).
2. Series có tên: `kind == "series"`, `shape == [n, 1]`, `columns == [name]`.
3. ndarray 2D `(2, 3)`: `kind == "array"`, columns `["0","1","2"]`; ndarray 1D: **không** có `table`.
4. DataFrame 20×10: `shape == [20, 10]`, `len(rows) == 8`, mỗi dòng 6 ô.
5. Ô NaN → `"NaN"`, float `0.1 + 0.2` → `"0.3"`, numpy float không ra `np.float64`.
6. Code không dùng pandas/numpy (`x = [1, 2]`): var không có khóa `table`, trace y như trước.

## Tiêu chí hoàn thành (checklist)
1. [ ] Tracer thêm `table` đúng hình dạng, đúng giới hạn, không import pandas/numpy, không làm hỏng trace khi lỗi.
2. [ ] UI vẽ bảng, cuộn ngang, chú thích khi bị cắt, highlight tính cả bảng; i18n đủ EN/VI.
3. [ ] Test mới pass; toàn bộ lệnh kiểm tra xanh.
4. [ ] Report: thời gian validate trước/sau; ví dụ JSON `table` của một DataFrame thật trong p4-02.

## Lệnh kiểm tra
Từ gốc repo `D:\Proj\python-ai-platform`:
```
uv run python -m pytest tools/pyrunner -q
uv run python tools/validate.py
uv run python -m pytest curriculum -q
uv run ruff check tools curriculum
pnpm --filter web typecheck
git status --short
```
Mong đợi: tất cả xanh; `git status` chỉ có các file trong danh sách được phép (ngoài `tasks/`, `.hallmark/` vốn untracked).

## Ghi chú cho worker
- Tracer chạy trong cả CPython (validate) lẫn Pyodide (pandas 2.3.3, numpy 2.2.5); chỉ dùng API có ở cả hai.
- Dùng `uv run python -m pytest`, không dùng `uv run pytest`.

## Trạng thái
- Bước hiện tại: 5 (đạt vòng 1; boss chạy lại cổng, validate 165→167 s, xem bảng `calls` p4-02 trên Pyodide, mobile 375px không tràn; đã commit `bc7ba47`)
- Vòng: 1/3
- Số lần swap: 0
- Fallback: không
- Model: Gemini 4 Hydrogen (High)
- Boss đo validate trước khi sửa: 165 s
