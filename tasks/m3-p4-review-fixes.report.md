# Báo cáo: Sửa 25 điểm review Phase 4 (`curriculum/phase-04-data/`)

## 1. Tóm tắt công việc theo từng mục (25/25)

### Major
1. **Thứ tự làm sạch (`p4-03` + `p4-06`)**
   - File đã sửa: `curriculum/phase-04-data/p4-03-cleaning/lesson.{en,vi}.md`, `curriculum/phase-04-data/p4-06-mini-project/lesson.{en,vi}.md`.
   - Đã làm: Cập nhật `p4-03` §5 để lọc `between(1, 5)` trước `drop_duplicates(subset=["user"], keep="last")` kèm output thật (`binh 5`, `an 4`), đổi thứ tự node mermaid/bảng/mô tả ở §6 sang validate trước khi dedupe, và bổ sung giải thích ở `p4-06` Recap về việc §3 che `rating` thành `NaN` và dùng `keep="first"` theo request gốc.

2. **Thay `zip(*pairs)` ở `p4-04`**
   - File đã sửa: `curriculum/phase-04-data/p4-04-matplotlib/lesson.{en,vi}.md`.
   - Đã làm: Thay `zip(*pairs)` ở §3 và mục lỗi "unsorted x" bằng `pd.Series(...).sort_values(ascending=False)` / `.sort_index()` kết hợp `.tolist()` đã học và kiểm chứng lại với `MPLBACKEND=Agg`.

3. **Giải thích `.astype(str)` ở `p4-06`**
   - File đã sửa: `curriculum/phase-04-data/p4-06-mini-project/lesson.{en,vi}.md`, `curriculum/phase-04-data/p4-06-mini-project/exercises/ex01-load-and-clean/prompt.{en,vi}.md`.
   - Đã làm: Bổ sung giải thích trước lần dùng đầu ở §3 kèm thông báo lỗi thật `AttributeError: Can only use .str accessor with string values!` khi cột toàn số, đồng thời thêm quy tắc tương ứng vào phần Rules của `ex01-load-and-clean`.

4. **Dạy `SELECT DISTINCT` ở `p4-05`**
   - File đã sửa: `curriculum/phase-04-data/p4-05-sql/lesson.{en,vi}.md`.
   - Đã làm: Thêm phần giải thích `SELECT DISTINCT` cùng ví dụ `SELECT DISTINCT user FROM prompts ORDER BY user ASC` có output thật `[('an',), ('binh',), ('chi',)]` vào §3 (giữ nguyên lời giải và hint `ex02` dùng `DISTINCT`).

5. **Thay câu "almost nothing new" ở `p4-06`**
   - File đã sửa: `curriculum/phase-04-data/p4-06-mini-project/lesson.{en,vi}.md`.
   - Đã làm: Thay mở đầu bằng mục **New in this lesson** / **Mới trong bài này** liệt kê và giải thích 6 API mới (`df.to_sql(..., if_exists=...)`, `Series.where`, `.astype(str)`, `AVG(status = 'error')`, `iterrows()`, định dạng `:<7`), đặt giải thích `.where` trước lần dùng đầu tiên.

6. **Hint tầng 3 lộ lời giải (`p4-03 ex02`, `p4-05 ex02`, `p4-06 ex01`, `p4-06 ex02`)**
   - File đã sửa: `curriculum/phase-04-data/p4-03-cleaning/exercises/ex02-clean-ratings/exercise.yaml`, `curriculum/phase-04-data/p4-05-sql/exercises/ex02-feedback-db/exercise.yaml`, `curriculum/phase-04-data/p4-06-mini-project/exercises/ex01-load-and-clean/exercise.yaml`, `curriculum/phase-04-data/p4-06-mini-project/exercises/ex02-model-report/exercise.yaml`.
   - Đã làm: Giữ khung cấu trúc ở cả EN và VI nhưng thay các dòng xử lý/truy vấn chính trong hint 3 của cả 4 bài tập bằng ít nhất 3 dòng trống `...` để người học tự hoàn thành.

7. **Thuật ngữ ngoặc vuông trong tiếng Việt (`p4-02` và rà cả phase 4)**
   - File đã sửa: `curriculum/phase-04-data/p4-02-pandas/lesson.vi.md`.
   - Đã làm: Sửa `"ngoặc đơn"` -> `"ngoặc vuông đơn"` và `"ngoặc kép lồng"` -> `"ngoặc vuông kép"` ở `p4-02-pandas/lesson.vi.md`, đồng thời grep toàn bộ `curriculum/phase-04-data` xác nhận không còn lỗi tương tự ở `p4-01`..`p4-06`.

8. **Lỗi diễn đạt `"Hợp nhất cho"` ở `p4-02`**
   - File đã sửa: `curriculum/phase-04-data/p4-02-pandas/lesson.vi.md`.
   - Đã làm: Đổi cả hai ô trong bảng từ `"Hợp nhất cho"` thành `"Phù hợp nhất cho"`.

9. **Sửa mục "Try it yourself" sai số liệu (`p4-01`, `p4-02`)**
   - File đã sửa: `curriculum/phase-04-data/p4-01-numpy/examples/01_sensor_readings.{en,vi}.md`, `curriculum/phase-04-data/p4-02-pandas/examples/03_eval_by_model.{en,vi}.md`.
   - Đã làm: Cập nhật `01_sensor_readings` sang đổi giới hạn dưới `10` thành `20` ở dòng 9 và 12 (`normal count` giảm từ `5` xuống `4`, `clean mean` tăng từ `22.26` lên `22.98`), và `03_eval_by_model` sang hạ điểm `"code"` của `claude` từ `0.94` xuống `0.80` (`gpt-4o` lên hạng nhất với `0.9` so với `0.84`).

10. **Cảnh báo `legend()` không dùng tiền tố `UserWarning` (`p4-04`)**
    - File đã sửa: `curriculum/phase-04-data/p4-04-matplotlib/lesson.{en,vi}.md`, `curriculum/phase-04-data/p4-04-matplotlib/quiz.yaml`.
    - Đã làm: Đổi `# UserWarning: No artists...` trong lesson thành cách diễn đạt trung tính (`matplotlib prints a warning: No artists...` / `matplotlib in ra cảnh báo: No artists...`) và cập nhật phần giải thích của `p4-04-q11` (EN + VI) bỏ tên `UserWarning`.

11. **VI recap `p4-06`**
    - File đã sửa: `curriculum/phase-04-data/p4-06-mini-project/lesson.vi.md`.
    - Đã làm: Đổi `"lọc giá trị ngoài khoảng"` thành `"biến giá trị ngoài khoảng thành `NaN`"` khớp bản EN và đồng bộ thứ tự recap với §3.

### Minor
12. **So sánh hai chiến lược làm sạch `p4-03` vs `p4-06`**
    - File đã sửa: `curriculum/phase-04-data/p4-06-mini-project/lesson.{en,vi}.md`.
    - Đã làm: Bổ sung giải thích ở §3 phân biệt khi nào bỏ dòng vs che thành `NaN` và vì sao `p4-06` dùng `keep="first"` (request đầu là bản gốc) còn `p4-03` dùng `keep="last"` (đánh giá mới thay bản cũ).

13. **Giới thiệu `.tolist()` ở `p4-01`**
    - File đã sửa: `curriculum/phase-04-data/p4-01-numpy/lesson.{en,vi}.md`.
    - Đã làm: Thêm câu giới thiệu `a.tolist()` đổi mảng thành list Python thường kèm ví dụ `scores.tolist()` ngay tại §1 (trước khi xuất hiện ở ví dụ/bài tập sau).

14. **Bổ sung/quy chuẩn API dùng mà chưa dạy**
    - File đã sửa: `curriculum/phase-04-data/p4-03-cleaning/lesson.{en,vi}.md` (`.nunique()`), `curriculum/phase-04-data/p4-02-pandas/exercises/ex02-average-score-by-model/exercise.yaml` và `curriculum/phase-04-data/p4-04-matplotlib/examples/02_cost_by_model.{en,vi}.md` (`Series.items()`), `curriculum/phase-04-data/p4-05-sql/examples/03_eval_to_pandas.py` (`groupby(...)[...].mean().reset_index()`), `curriculum/phase-04-data/p4-05-sql/lesson.{en,vi}.md` (`SELECT *`), `curriculum/phase-04-data/p4-05-sql/quiz.yaml` (`p4-05-q13`, `p4-05-q16`) và `curriculum/phase-04-data/p4-06-mini-project/quiz.yaml` (`p4-06-q09`, `p4-06-q16`) (`INSERT INTO` liệt kê cột), `curriculum/phase-04-data/p4-01-numpy/exercises/ex02-predicted-labels/solution.py` và `curriculum/phase-04-data/p4-03-cleaning/exercises/ex02-clean-ratings/alternatives/01_loop.py` (bỏ `strict=True` trong `zip`, thêm `# noqa: B905`), `curriculum/phase-04-data/p4-04-matplotlib/examples/03_latency_scatter.{en,vi}.md` (`np.corrcoef`).
    - Đã làm: Chú thích ngắn gọn hoặc đổi cú pháp về dạng đã dạy cho toàn bộ 7 mục API trong spec.

15. **Sửa Hint 1 của `p4-01 ex02` và bổ sung `max/argmax(axis=1)` ở lesson**
    - File đã sửa: `curriculum/phase-04-data/p4-01-numpy/exercises/ex02-predicted-labels/exercise.yaml`, `curriculum/phase-04-data/p4-01-numpy/lesson.{en,vi}.md`.
    - Đã làm: Trỏ Hint 1 của `ex02-predicted-labels` tới §4 và example `03_batch_predictions`, đồng thời thêm `grid.max(axis=1)` và `grid.argmax(axis=1)` kèm output thật (`[30 60]`, `[2 2]`) vào §4.

16. **Sửa repr của `p4-01 ex01`**
    - File đã sửa: `curriculum/phase-04-data/p4-01-numpy/exercises/ex01-min-max-scale/{prompt.en.md,prompt.vi.md,starter.py,solution.py,exercise.yaml}`.
    - Đã làm: Đổi `array([0.0, 0.5, 1.0])` thành repr thực tế của NumPy `array([0. , 0.5, 1. ])`.

17. **Đồng bộ số dòng trong phần giải thích example (`p4-03`, `p4-05`, `p4-06`)**
    - File đã sửa: `curriculum/phase-04-data/p4-03-cleaning/examples/{01_survey_missing,03_training_labels}.{en,vi}.md`, `curriculum/phase-04-data/p4-05-sql/examples/{01_chat_history,03_eval_to_pandas}.{en,vi}.md`, `curriculum/phase-04-data/p4-06-mini-project/examples/03_report_chart.{en,vi}.md`.
    - Đã làm: Đếm lại số dòng thực tế trong các file `.py` tương ứng và cập nhật toàn bộ trích dẫn dòng (bao gồm mục "Try it yourself"), đồng thời kiểm tra các example `.md` còn lại của phase 4.

18. **Làm rõ mục "Try it" ở `p4-05 ex01` và `p4-06 ex03`**
    - File đã sửa: `curriculum/phase-04-data/p4-05-sql/examples/01_chat_history.{en,vi}.md`, `curriculum/phase-04-data/p4-06-mini-project/examples/03_report_chart.{en,vi}.md`.
    - Đã làm: Chỉ rõ đổi tham số `("an",)` thành `("binh",)` ở `01_chat_history` và hướng dẫn thêm `ROUND(AVG(latency_ms), 1) AS avg_latency` vào câu `SELECT` ở `03_report_chart`.

19. **Làm rõ alternative `p4-06 ex02`**
    - File đã sửa: `curriculum/phase-04-data/p4-06-mini-project/exercises/ex02-model-report/alternatives/01_pandas_groupby.{en,vi}.md`.
    - Đã làm: Giữ nguyên `01_pandas_groupby.py` và bổ sung ghi chú ở file `.md` (EN + VI) rằng cách này cố ý tránh SQL để đối chiếu, đồng thời giải thích named aggregation `agg(new_col=("col", "func"))`.

20. **Thống nhất bộ dữ liệu ví dụ ở `p4-05 ex01`**
    - File đã sửa: `curriculum/phase-04-data/p4-05-sql/exercises/ex01-top-models/{starter.py,solution.py,exercise.yaml}`.
    - Đã làm: Đồng bộ docstring của `starter.py`/`solution.py` và Hint 1 theo đúng bộ dữ liệu trong `prompt.*.md` (`"gpt-4o"` 2 runs avg `0.90`, `"claude"` 2 runs avg `0.88`, `"mini"` 1 run `0.95` -> `[("gpt-4o", 0.9), ("claude", 0.88)]`).

21. **Sửa diễn đạt và code tiếng Việt trong `p4-02-pandas/lesson.vi.md`**
    - File đã sửa: `curriculum/phase-04-data/p4-02-pandas/lesson.vi.md`.
    - Đã làm: Sửa `"được chống lưng bởi mảng NumPy bên dưới"` -> `"được xây trên mảng NumPy bên dưới"`, `"chạy trực tiếp ngay lập tức"` -> `"chạy được ngay"`, và `calls["ten_cot"]` -> `calls["new_col"]`.

22. **Viết lại các câu quiz bị trùng (`p4-06` và `p4-02-q12`)**
    - File đã sửa: `curriculum/phase-04-data/p4-06-mini-project/quiz.yaml`, `curriculum/phase-04-data/p4-02-pandas/quiz.yaml`.
    - Đã làm: Viết lại `p4-06-q02` (`AVG(status = 'error')`), `p4-06-q04` (`.astype(str)` tránh `AttributeError`), `p4-06-f02` (`.where` vs `dropna`), `p4-06-q07` (Parsons `if_exists="replace"` với 1 dòng `import sqlite3, pandas as pd` để đảm bảo thứ tự duy nhất) và `p4-02-q12` (`sort_values(..., ascending=False)`).

23. **Hai chỉnh sửa nhỏ ở `p4-04` và `p4-02`**
    - File đã sửa: `curriculum/phase-04-data/p4-04-matplotlib/lesson.{en,vi}.md`, `curriculum/phase-04-data/p4-02-pandas/quiz.yaml`.
    - Đã làm: Bổ sung ngoại lệ cho TIP sắp xếp bar chart khi nhóm có thứ tự tự nhiên (tháng, epoch, rating 1–5) và đổi tag `json` -> `pandas` trên `p4-02-q04`, `p4-02-f02`.

24. **Từ chối rating có phần thập phân ở `p4-03 ex02`**
    - File đã sửa: `curriculum/phase-04-data/p4-03-cleaning/exercises/ex02-clean-ratings/{prompt.en.md,prompt.vi.md,solution.py,alternatives/01_loop.py,test_exercise.py,exercise.yaml}`.
    - Đã làm: Thêm quy tắc rating phải là số nguyên (loại bỏ giá trị như `"4.5"`) vào prompt, thêm `test_drops_fractional_ratings` trong `test_exercise.py`, cập nhật `solution.py` (`out["rating"] % 1 == 0`), `01_loop.py` (`value % 1 != 0`) và Hint 2/3.

25. **Sửa nhánh `test` trong `apps/web/public/pyodide-worker.js`**
    - File đã sửa: `apps/web/public/pyodide-worker.js`.
    - Đã làm: Cập nhật nhánh `test` (dòng 178–181) để gọi `loadImports` và `usesMatplotlib` cho cả `msg.code` và `msg.tests`, giữ nguyên nhánh `run`/`trace` và định dạng message.

---

## 2. Danh sách toàn bộ file đã sửa (59 file)

- `apps/web/public/pyodide-worker.js`
- `curriculum/phase-04-data/p4-01-numpy/examples/01_sensor_readings.en.md`
- `curriculum/phase-04-data/p4-01-numpy/examples/01_sensor_readings.vi.md`
- `curriculum/phase-04-data/p4-01-numpy/exercises/ex01-min-max-scale/exercise.yaml`
- `curriculum/phase-04-data/p4-01-numpy/exercises/ex01-min-max-scale/prompt.en.md`
- `curriculum/phase-04-data/p4-01-numpy/exercises/ex01-min-max-scale/prompt.vi.md`
- `curriculum/phase-04-data/p4-01-numpy/exercises/ex01-min-max-scale/solution.py`
- `curriculum/phase-04-data/p4-01-numpy/exercises/ex01-min-max-scale/starter.py`
- `curriculum/phase-04-data/p4-01-numpy/exercises/ex02-predicted-labels/exercise.yaml`
- `curriculum/phase-04-data/p4-01-numpy/exercises/ex02-predicted-labels/solution.py`
- `curriculum/phase-04-data/p4-01-numpy/lesson.en.md`
- `curriculum/phase-04-data/p4-01-numpy/lesson.vi.md`
- `curriculum/phase-04-data/p4-02-pandas/examples/03_eval_by_model.en.md`
- `curriculum/phase-04-data/p4-02-pandas/examples/03_eval_by_model.vi.md`
- `curriculum/phase-04-data/p4-02-pandas/exercises/ex02-average-score-by-model/exercise.yaml`
- `curriculum/phase-04-data/p4-02-pandas/lesson.vi.md`
- `curriculum/phase-04-data/p4-02-pandas/quiz.yaml`
- `curriculum/phase-04-data/p4-03-cleaning/examples/01_survey_missing.en.md`
- `curriculum/phase-04-data/p4-03-cleaning/examples/01_survey_missing.vi.md`
- `curriculum/phase-04-data/p4-03-cleaning/examples/03_training_labels.en.md`
- `curriculum/phase-04-data/p4-03-cleaning/examples/03_training_labels.vi.md`
- `curriculum/phase-04-data/p4-03-cleaning/exercises/ex02-clean-ratings/alternatives/01_loop.py`
- `curriculum/phase-04-data/p4-03-cleaning/exercises/ex02-clean-ratings/exercise.yaml`
- `curriculum/phase-04-data/p4-03-cleaning/exercises/ex02-clean-ratings/prompt.en.md`
- `curriculum/phase-04-data/p4-03-cleaning/exercises/ex02-clean-ratings/prompt.vi.md`
- `curriculum/phase-04-data/p4-03-cleaning/exercises/ex02-clean-ratings/solution.py`
- `curriculum/phase-04-data/p4-03-cleaning/exercises/ex02-clean-ratings/test_exercise.py`
- `curriculum/phase-04-data/p4-03-cleaning/lesson.en.md`
- `curriculum/phase-04-data/p4-03-cleaning/lesson.vi.md`
- `curriculum/phase-04-data/p4-04-matplotlib/examples/02_cost_by_model.en.md`
- `curriculum/phase-04-data/p4-04-matplotlib/examples/02_cost_by_model.vi.md`
- `curriculum/phase-04-data/p4-04-matplotlib/examples/03_latency_scatter.en.md`
- `curriculum/phase-04-data/p4-04-matplotlib/examples/03_latency_scatter.vi.md`
- `curriculum/phase-04-data/p4-04-matplotlib/lesson.en.md`
- `curriculum/phase-04-data/p4-04-matplotlib/lesson.vi.md`
- `curriculum/phase-04-data/p4-04-matplotlib/quiz.yaml`
- `curriculum/phase-04-data/p4-05-sql/examples/01_chat_history.en.md`
- `curriculum/phase-04-data/p4-05-sql/examples/01_chat_history.vi.md`
- `curriculum/phase-04-data/p4-05-sql/examples/03_eval_to_pandas.en.md`
- `curriculum/phase-04-data/p4-05-sql/examples/03_eval_to_pandas.py`
- `curriculum/phase-04-data/p4-05-sql/examples/03_eval_to_pandas.vi.md`
- `curriculum/phase-04-data/p4-05-sql/exercises/ex01-top-models/exercise.yaml`
- `curriculum/phase-04-data/p4-05-sql/exercises/ex01-top-models/solution.py`
- `curriculum/phase-04-data/p4-05-sql/exercises/ex01-top-models/starter.py`
- `curriculum/phase-04-data/p4-05-sql/exercises/ex02-feedback-db/exercise.yaml`
- `curriculum/phase-04-data/p4-05-sql/lesson.en.md`
- `curriculum/phase-04-data/p4-05-sql/lesson.vi.md`
- `curriculum/phase-04-data/p4-05-sql/quiz.yaml`
- `curriculum/phase-04-data/p4-06-mini-project/examples/03_report_chart.en.md`
- `curriculum/phase-04-data/p4-06-mini-project/examples/03_report_chart.vi.md`
- `curriculum/phase-04-data/p4-06-mini-project/exercises/ex01-load-and-clean/exercise.yaml`
- `curriculum/phase-04-data/p4-06-mini-project/exercises/ex01-load-and-clean/prompt.en.md`
- `curriculum/phase-04-data/p4-06-mini-project/exercises/ex01-load-and-clean/prompt.vi.md`
- `curriculum/phase-04-data/p4-06-mini-project/exercises/ex02-model-report/alternatives/01_pandas_groupby.en.md`
- `curriculum/phase-04-data/p4-06-mini-project/exercises/ex02-model-report/alternatives/01_pandas_groupby.vi.md`
- `curriculum/phase-04-data/p4-06-mini-project/exercises/ex02-model-report/exercise.yaml`
- `curriculum/phase-04-data/p4-06-mini-project/lesson.en.md`
- `curriculum/phase-04-data/p4-06-mini-project/lesson.vi.md`
- `curriculum/phase-04-data/p4-06-mini-project/quiz.yaml`

Báo cáo mới tạo: `tasks/m3-p4-review-fixes.report.md`. Không có file nào bị xóa; không sửa file nào ngoài phạm vi cho phép (`apps/web/src/generated/` được tái tạo bởi `tools/build_content.py` và thuộc `.gitignore`).

---

## 3. Kết quả các lệnh kiểm tra (chạy sau lần sửa cuối cùng)

| Lệnh | Kết quả | Chi tiết |
| --- | --- | --- |
| `uv run python tools/validate.py --path curriculum/phase-04-data` | Pass (`exit 0`) | `OK: 0 error(s), 0 warning(s). Checked 6 lessons, 43 markdown pairs, 18 examples, 12 exercises, 7 alternatives, 96 questions.` |
| `uv run python tools/validate.py` | Pass (`exit 0`) | `OK: 0 error(s), 0 warning(s). Checked 30 lessons, 236 markdown pairs, 88 examples, 60 exercises, 58 alternatives, 562 questions, 5 exams, 1 portfolio, 1 glossary, 1 interview.` |
| `uv run python -m pytest curriculum` | Pass (`exit 0`) | `580 passed, 14 warnings in 1.49s` (các warning là `PyparsingDeprecationWarning` từ thư viện `matplotlib`). |
| `uv run ruff check curriculum` | Pass (`exit 0`) | `All checks passed!` |
| `pnpm.cmd --filter web typecheck` | Pass (`exit 0`) | Đã build content (`30 lessons, 5 exams, 180 flashcards, 483 questions -> apps\web\src\generated`) và chạy `tsc --noEmit` không lỗi. (Dùng `pnpm.cmd` do PowerShell chặn `pnpm.ps1`.) |
| `git grep -n "zip(\*" -- curriculum/phase-04-data` | Pass (0 match) | Không còn mẫu `zip(*` nào trong phase 4. |
| `git grep -n "UserWarning: No artists" -- curriculum/phase-04-data` | Pass (0 match) | Không còn tiền tố `UserWarning: No artists` nào trong phase 4. |
| `git grep -n -E 'ten_cot\|Hợp nhất cho\|ngoặc đơn `\[' -- curriculum/phase-04-data` | Pass (0 match) | Không còn các chuỗi lỗi tiếng Việt được liệt kê. |
| `uv run python tools/build_content.py` | Pass (`exit 0`) | `Built 30 lessons, 5 exams, 180 flashcards, 483 questions -> apps\web\src\generated` |
| `git status --short` & `git diff --stat` | Đạt | `59 files changed, 303 insertions(+), 240 deletions(-)`; toàn bộ nằm trong `curriculum/phase-04-data/p4-0*/` và `apps/web/public/pyodide-worker.js`, không có file bị xóa. |

---

## 4. Điều còn chưa chắc / cần lưu ý

- **Kiểm tra trình duyệt (Pyodide runtime):** Môi trường hiện tại không có trình duyệt nên chưa chạy kiểm thử end-to-end trong web app cho mục 25 (`apps/web/public/pyodide-worker.js` nhánh `test` khi bài test cần package/matplotlib không có trong code người học) cũng như việc render biểu đồ matplotlib 3.8.4 và thông điệp cảnh báo thực tế của `legend()` trong Pyodide wasm32. Boss cần kiểm tra trực tiếp trên trình duyệt trong app.
- **`pnpm --filter web build`:** Không chạy theo đúng ràng buộc trong spec vì dev server đang chạy.
- **Một điểm ghi chú ở `p4-06-q07`:** Để giữ `p4-06-q07` là câu `parsons` về `if_exists="replace"` mà vẫn có đúng một thứ tự thực thi hợp lệ theo `validate.py`, hai lệnh import được gộp thành một dòng `"import sqlite3, pandas as pd"` (prompt EN/VI điều chỉnh tương ứng).
