# Báo cáo thực hiện: M3 bước 8 — Phase test 4 (Data)

## 1. Đã làm gì
- Đọc spec `tasks/m3-p4-test.md`, mẫu `curriculum/phase-03-code-quality/phase-test.yaml`, schema `tools/schema/exam.schema.json` và `tools/schema/common.schema.json`, `curriculum/topics.yaml`, `curriculum/syllabus.yaml`, cùng toàn bộ 6 file `quiz.yaml` của phase 4 (`p4-01-numpy` .. `p4-06-mini-project`) và `p4-04-matplotlib/lesson.en.md` để đảm bảo câu hỏi mới hoàn toàn, không trùng ý/trùng code và chỉ dùng API đã dạy.
- Tạo `curriculum/phase-04-data/phase-test.yaml` với `id: p4-phase-test`, `kind: phase_test`, `phase: p4`, `duration_min: 25`, `pass_score: 0.7`, gồm 18 câu hỏi (`p4-test-q01` … `p4-test-q18`) song ngữ EN/VI đầy đủ, có `tags` hợp lệ trong `curriculum/topics.yaml` và `explanation` giải thích lý do.
- Trong quá trình validate lần đầu, phát hiện `p4-test-q01` có phương án VI `"Cả hai biểu thức đều trả về [4, 6]"` chạm regex `POSITIONAL_OPTION` (`cả hai`) của `tools/validate.py`, đã sửa lại thành `"Hai biểu thức py_a + py_b và np_a + np_b đều cho ra [4, 6]"` (và chỉnh tương ứng ở EN) để an toàn khi đảo thứ tự đáp án.

### Bảng đếm thực tế theo blueprint

| Chủ đề (nhóm) | Số câu | Phân bổ loại câu | Phân bổ độ khó |
|---|---:|---|---|
| NumPy (`p4-01`) | 3 | `mcq`: 1, `fill`: 1, `output`: 1 | mức 1: 1, mức 2: 2 |
| pandas (`p4-02`) | 3 | `output`: 1, `mcq`: 1, `fill`: 1 | mức 1: 1, mức 2: 1, mức 3: 1 |
| Cleaning (`p4-03`) | 3 | `mcq`: 1, `output`: 1, `parsons`: 1 | mức 2: 2, mức 3: 1 |
| Plotting (`p4-04`) | 3 | `mcq`: 1, `fill`: 1, `output`: 1 | mức 1: 1, mức 2: 2 |
| SQL (`p4-05`) | 3 | `mcq`: 2, `output`: 1 | mức 1: 1, mức 2: 1, mức 3: 1 |
| Mini-project (`p4-06`) | 3 | `parsons`: 1, `mcq`: 2 | mức 2: 2, mức 3: 1 |
| **Tổng cộng** | **18** | **`mcq`: 8, `output`: 5, `fill`: 3, `parsons`: 2** | **mức 1: 4, mức 2: 10, mức 3: 4** |

### Liệt kê 18 câu và ý kiểm tra (không trùng với quiz 6 bài p4)

| ID | Chủ đề | Loại | Mức | Ý kiểm tra | Khác biệt với quiz p4 |
|---|---|---|---:|---|---|
| `p4-test-q01` | NumPy | `mcq` | 1 | Cộng vector hóa `np_a + np_b` so với nối list `py_a + py_b` | `p4-01-q03` kiểm `* 2`; câu này kiểm `+` giữa hai sequence |
| `p4-test-q02` | NumPy | `fill` | 2 | Tham số `axis=0` để tổng hợp theo cột trên mảng 2D `(3, 2)` | `p4-01-q07` là `mcq` về `mean(axis=1)`; câu này `fill` `sum(axis=0)` và dùng `.tolist()` |
| `p4-test-q03` | NumPy | `output` | 2 | Boolean mask với `&` và ngoặc đơn (`150 <= x <= 450`) | Khác dữ liệu/ngữ cảnh latency so với `p4-01-q09`/`q13`/`q14` |
| `p4-test-q04` | pandas | `output` | 3 | Phân biệt `iloc[0]` (vị trí) và `loc[1, "model"]` (nhãn gốc) sau lọc & `sort_values` | `p4-02-q15` là `mcq` hỏi `KeyError: 0`; câu này kiểm tra đọc giá trị song song `iloc` vs `loc` |
| `p4-test-q05` | pandas | `mcq` | 2 | Cấu trúc kết quả của `df.groupby("model")["tokens"].agg(["count", "mean"])` | `p4-02-q13` chỉ là `parsons` với `.mean()`; câu này kiểm `.agg([...])` |
| `p4-test-q06` | pandas | `fill` | 1 | Tạo cột mới vector hóa `df["latency_ms"] / 1000` | `p4-02-q11` là `output` với `round((tokens * 0.002), 2)` |
| `p4-test-q07` | Cleaning | `mcq` | 2 | `pd.to_numeric(..., errors="coerce")` với chuỗi có dấu phẩy `"1,200"` thành `NaN` | `p4-03-q06`/`q07` kiểm từ khóa `"coerce"` và `.isna().sum()`; câu này kiểm bẫy dấu phẩy |
| `p4-test-q08` | Cleaning | `output` | 2 | Quên gán lại sau `df.dropna(subset=["user"])` nên `len(df)` vẫn là `3` | `p4-03-q08` là `mcq` về `fillna(0)`; câu này là `output` về `dropna` |
| `p4-test-q09` | Cleaning | `parsons` | 3 | Thứ tự lọc khoảng hợp lệ `between(1, 5)` trước rồi mới `drop_duplicates(keep="first")` | Dữ liệu `["an", "an", "an"]` với `[9, 4, 2]` ép đúng 1 thứ tự chạy duy nhất, khác `p4-03-q15` |
| `p4-test-q10` | Plotting | `mcq` | 1 | Chọn biểu đồ đường `ax.plot` để theo dõi xu hướng `val_loss` qua các epoch | `p4-04-q04` hỏi `scatter`, `p4-04-q09` hỏi `barh`; câu này hỏi biểu đồ đường |
| `p4-test-q11` | Plotting | `fill` | 2 | Đặt nhãn trục x qua `ax.set_xlabel("epoch")` (và kiểm tra `ax.get_xlabel()`) | Chưa có câu `fill` nào về `set_xlabel` trong `p4-04` |
| `p4-test-q12` | Plotting | `output` | 2 | Kết hợp `df.plot(..., ax=ax)` và `ax.set_title(...)`, đọc `ax.get_title()` và `len(ax.lines)` | Gộp cả tiêu đề lẫn số đường từ `DataFrame.plot`, khác `p4-04-q02`/`q05` |
| `p4-test-q13` | SQL | `mcq` | 2 | Chọn câu `conn.execute` an toàn với placeholder `?` và tuple 1 phần tử `(target,)` | Đối chiếu 4 cách viết (`target`, `(target)`, `(target,)`, f-string), khác `p4-05-q08`/`q14` |
| `p4-test-q14` | SQL | `mcq` | 3 | Phân biệt vai trò `WHERE` (lọc dòng trước `GROUP BY`) và `HAVING` (lọc nhóm sau `COUNT(*)`) trong cùng 1 query | Gắn vào truy vấn cụ thể có cả `WHERE score >= 0.5` lẫn `HAVING COUNT(*) >= 2` |
| `p4-test-q15` | SQL | `output` | 1 | Truy vấn `WHERE rating IS NULL ORDER BY id` trên SQLite `:memory:` | `p4-05-q06` là `fill` từ khóa `IS`; câu này là `output` |
| `p4-test-q16` | Mini-project | `parsons` | 3 | Pipeline đọc CSV bẩn (`io.StringIO`) → `to_numeric` → `dropna` → chuẩn hóa `.str` → `groupby().mean()` | Kết hợp đủ pipeline và kiểm tra thứ tự phụ thuộc duy nhất |
| `p4-test-q17` | Mini-project | `mcq` | 2 | Giải thích cơ chế `AVG(status = 'error')` trong SQLite khi có `'ok'`, `'error'`, `'timeout'` | `p4-06-q02`/`q09`/`q16` chỉ kiểm tra output/fill/parsons; câu này kiểm tra lý giải với 3 trạng thái |
| `p4-test-q18` | Mini-project | `mcq` | 2 | Chọn pandas (thay vì SQLite) cho bài toán làm sạch CSV lộn xộn trước khi vẽ Matplotlib | Bổ sung góc nhìn ngược lại so với `p4-06-q11` (khi nào chọn SQL) |

## 2. File đã sửa / tạo
- Tạo mới: `curriculum/phase-04-data/phase-test.yaml`
- Tạo mới (báo cáo theo yêu cầu): `tasks/m3-p4-test.report.md`
- Không sửa bất kỳ file curriculum, `tools/`, hay `apps/` nào khác (lưu ý `uv run python tools/build_content.py` sinh file vào thư mục generated được gitignore).

## 3. Kết quả lệnh kiểm tra
Tất cả lệnh chạy từ gốc repo `D:\Proj\python-ai-platform` sau lần sửa cuối cùng của `curriculum/phase-04-data/phase-test.yaml`:

1. `uv run python tools/validate.py --path curriculum/phase-04-data`
   - Exit code: `0`
   - Kết quả: `OK: 0 error(s), 0 warning(s). Checked 6 lessons, 43 markdown pairs, 18 examples, 12 exercises, 7 alternatives, 114 questions, 1 exams.`
2. `uv run python tools/validate.py`
   - Exit code: `0`
   - Kết quả: `OK: 0 error(s), 0 warning(s). Checked 30 lessons, 236 markdown pairs, 88 examples, 60 exercises, 58 alternatives, 580 questions, 6 exams, 1 portfolio, 1 glossary, 1 interview.` (số `exams` là `6`, tăng 1 so với 5 exam trước đó).
3. `uv run python -m pytest curriculum`
   - Exit code: `0`
   - Kết quả: `580 passed, 14 warnings in 1.37s` (warnings từ `matplotlib`/`pyparsing` có sẵn).
4. `uv run python tools/build_content.py`
   - Exit code: `0`
   - Kết quả: `Built 30 lessons, 6 exams, 180 flashcards, 483 questions -> apps\web\src\generated`
5. Kiểm tra pattern cấm (`astype\(int\)|dtype=int\b|\.info\(|sqlite_version|plt\.show`) trên `curriculum/phase-04-data/phase-test.yaml` bằng `Select-String`:
   - Exit code: `0`, không có dòng nào khớp (rỗng).
6. `git status --short`:
   - `?? .hallmark/`
   - `?? curriculum/phase-04-data/phase-test.yaml`
   - `?? tasks/`

## 4. Điều còn chưa chắc
- Không chạy `pnpm --filter web build` (tuân thủ spec) và không chạy thử trực tiếp trên runtime Pyodide 32-bit trong trình duyệt; các câu `output`/`fill`/`parsons` đã qua trình chạy Python cục bộ trong `tools/validate.py` và tuân thủ đầy đủ quy tắc Pyodide 32-bit trong spec.
- Trong `p4-test-q14` và `p4-test-q17` (đều là `mcq`), trường `code:` chứa snippet SQL thuần (tương tự `p4-05-f04`); chưa rõ component UI của web app có highlight cú pháp SQL hay mặc định highlight Python cho `code` của exam hay không (không chạy web build để kiểm tra giao diện).

## 5. Sửa theo Feedback vòng 1
- Đã đảo thứ tự `options` (đồng bộ giống hệt cả `en.options` và `vi.options`, giữ nguyên nội dung từng option, `prompt` và `explanation`) và cập nhật `answer` của các câu `mcq` (`p4-test-q01`, `p4-test-q07`, `p4-test-q14`, `p4-test-q17`, `p4-test-q18`) để đáp án đúng rải đều đúng 2 câu cho mỗi vị trí `0, 1, 2, 3`.
- Chỉ sửa `curriculum/phase-04-data/phase-test.yaml` và cập nhật báo cáo `tasks/m3-p4-test.report.md`.

### Bảng `id → answer` mới cho 8 câu MCQ

| ID | `answer` cũ | `answer` mới | Vị trí |
|---|---:|---:|---|
| `p4-test-q01` | `0` | `2` | C |
| `p4-test-q05` | `1` | `1` | B |
| `p4-test-q07` | `0` | `3` | D |
| `p4-test-q10` | `0` | `0` | A |
| `p4-test-q13` | `2` | `2` | C |
| `p4-test-q14` | `0` | `1` | B |
| `p4-test-q17` | `0` | `3` | D |
| `p4-test-q18` | `1` | `0` | A |

- Phân bổ sau khi sửa: `0` (2 câu: `q10`, `q18`), `1` (2 câu: `q05`, `q14`), `2` (2 câu: `q01`, `q13`), `3` (2 câu: `q07`, `q17`).
- Đã chạy lại toàn bộ lệnh kiểm tra ở mục 3 sau khi sửa vòng 1 (`validate.py --path curriculum/phase-04-data`, `validate.py`, `pytest curriculum`, `build_content.py`, `Select-String`, `git status --short`), tất cả đều exit `0` với `0 error(s), 0 warning(s)` và `580 passed`.
