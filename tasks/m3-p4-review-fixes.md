# M3: sửa 25 điểm review phase 4

## Mục tiêu
Subagent reviewer đã soát 6 bài `curriculum/phase-04-data/` (0 blocker, 11 major, 14 minor); boss đã xác minh các điểm chính. Sửa **cả 25 điểm** dưới đây, theo đúng quyết định boss đã chốt ở từng mục. Không thêm nội dung ngoài các mục này.
Luật nội dung vẫn là `docs/CONTENT_GUIDE.md`; quy tắc output phase 4 ở đầu `tasks/M3-PLAN.md` (Pyodide 32-bit, SQLite 3.39, matplotlib 3.8.4, DataFrame in ra ≤ 4 cột, comment `# output` phải khớp output thật).

## File được phép sửa
- Mọi file trong `curriculum/phase-04-data/p4-0*/` (lesson, examples, exercises, quiz, meta). **Không tạo bài mới, không xóa file.**
- `apps/web/public/pyodide-worker.js`: **chỉ** mục 25.

## Không được đụng
- `tools/`, `curriculum/syllabus.yaml`, `curriculum/topics.yaml`, `curriculum/glossary.yaml`, các phase khác, `exams/`, mọi file khác trong `apps/`.
- Không `git commit`, **không chạy `pnpm --filter web build`** (dev server đang chạy).
- Mọi sửa trong `lesson.en.md` phải sửa tương ứng ở `lesson.vi.md` (và ngược lại với các mục chỉ sửa VI): code giống hệt, số dòng mermaid bằng nhau, fence `text` giống hệt. Tương tự với `*.en.md`/`*.vi.md` của examples, prompts, alternatives và `en:`/`vi:` trong yaml.

## Các điểm cần sửa (đánh số theo báo cáo review)

### Major
1. **Thứ tự làm sạch, p4-03 + p4-06.** Chốt một quy tắc cho cả phase: *lọc/che giá trị ngoài khoảng và bỏ dòng không hợp lệ **trước**, rồi mới `drop_duplicates`* (lý do: nếu bỏ trùng trước với `keep="last"`, dòng giữ lại có thể là dòng hỏng; lọc sau sẽ làm mất luôn dòng hợp lệ của key đó).
   - `p4-03-cleaning/lesson.*.md` §6: sửa câu liệt kê thứ tự và câu giải thích cho đúng quy tắc trên; mermaid đổi chỗ node "Drop duplicates" và "Validate ranges" (validate trước). Code §6 đã đúng thứ tự, giữ nguyên.
   - §5: đổi ví dụ để lọc `between(1, 5)` **trước** rồi `drop_duplicates(..., keep="last")`; cập nhật output và câu "Notice" cho khớp (chạy thật).
   - `p4-06-mini-project/lesson.*.md` Recap (dòng ~399): ghi đúng thứ tự mà §3 và lời giải p4-06 dùng; nếu §3 dedupe trước khi che rating, giải thích vì sao ở p4-06 không sao (che rating thành NaN chứ không bỏ dòng; `keep="first"` theo request đầu tiên) — xem thêm mục 12.
2. **`zip(*pairs)` chưa dạy, p4-04 §3 và mục lỗi "unsorted x".** Thay bằng pandas đã học: `s = pd.Series(costs, index=models).sort_values(ascending=False)` rồi `ax.bar(s.index.tolist(), s.tolist())`; với x chưa sắp xếp dùng `pd.Series(y, index=x).sort_index()` (hoặc `sorted(zip(x, y))` + comprehension `[p[0] for p in pairs]` nếu muốn giữ thuần Python). Cập nhật output/comment.
3. **`.astype(str)` chưa giải thích, p4-06.** Thêm một câu ở §3 trước lần dùng đầu (dòng ~153): khi cột không có chữ nào, pandas đọc thành số và `.str` báo `AttributeError: Can only use .str accessor with string values!` (lấy đúng thông báo khi chạy thật); `.astype(str)` giúp an toàn. Thêm một dòng tương ứng vào **Rules** của `ex01-load-and-clean/prompt.*.md`.
4. **`DISTINCT` chưa dạy, p4-05.** Thêm `SELECT DISTINCT` vào §3 của lesson với một ví dụ ngắn có `ORDER BY` (comment output khớp thật). Giữ lời giải và hint ex02 dùng `DISTINCT`.
5. **p4-06 "almost nothing new".** Thay câu ở dòng ~3 bằng một mục ngắn "New in this lesson" / "Mới trong bài này": `df.to_sql(..., if_exists=...)`, `Series.where` ("giữ giá trị ở chỗ điều kiện True, chỗ khác thành NaN"), `.astype(str)`, `AVG(status = 'error')`, `iterrows()`, định dạng `:<7` trong f-string — mỗi cái một dòng giải thích. `.where` phải được giải thích **trước** lần dùng đầu.
6. **Hint tầng 3 lộ lời giải.** Sửa hint 3 (EN + VI) của: `p4-03-cleaning/ex02-clean-ratings`, `p4-05-sql/ex02-feedback-db`, `p4-06-mini-project/ex01-load-and-clean`, `p4-06-mini-project/ex02-model-report`. Giữ khung cấu trúc nhưng **để trống cả dòng** ở những chỗ cần suy nghĩ (thứ tự lọc/bỏ trùng, mệnh đề `GROUP BY`/`ORDER BY`, lời gọi `to_sql`, câu `WHERE` có placeholder) bằng `...` hoặc comment `# your code`. Mỗi hint 3 còn ít nhất 2–3 dòng trống thật sự.
7. **VI `p4-02-pandas/lesson.vi.md:101`**: "ngoặc đơn `["score"]`" → "ngoặc vuông đơn `["score"]`"; "ngoặc kép lồng `[[...]]`" → "ngoặc vuông kép `[["model", "score"]]`". Rà cả bài VI p4-01…p4-06 cho cùng lỗi này.
8. **VI `p4-02-pandas/lesson.vi.md:57`**: "Hợp nhất cho …" → "Phù hợp nhất cho …" (cả hai ô).
9. **"Try it yourself" sai** (EN + VI):
   - `p4-01-numpy/examples/01_sensor_readings.*.md`: đổi thành "đổi giới hạn dưới `10` thành `20` ở dòng 9 và 12" và nói kết quả đúng (chạy thử để lấy số: clean mean đổi từ 22.26 thành bao nhiêu, normal count bao nhiêu).
   - `p4-02-pandas/examples/03_eval_by_model.*.md`: đổi thành "hạ điểm `code` của claude từ `0.94` xuống `0.80`" và nói đúng thứ hạng mới (chạy thử để kiểm).
10. **Cảnh báo legend không phải `UserWarning`** (boss đã đo: trong app, matplotlib 3.8.4 chỉ log dòng "No artists with labels found to put in legend. …", `warnings` rỗng; local 3.9.2 là `UserWarning`). Sửa `p4-04-matplotlib/lesson.*.md` (~dòng 251): bỏ tiền tố `UserWarning:`, viết "matplotlib prints a warning: No artists with labels found to put in legend…" / VI tương ứng. Sửa explanation của `p4-04-q11` (EN + VI) cho trung tính ("matplotlib warns …").
11. **VI recap p4-06 (dòng ~399)**: "lọc giá trị ngoài khoảng" → "biến giá trị ngoài khoảng thành `NaN`" (khớp EN "mask" và câu q08). Kết hợp với mục 1.

### Minor
12. **p4-03 vs p4-06 hai cách xử lý khác nhau**: thêm 1–2 câu ở p4-06 §3: bỏ dòng khi trường hỏng là dữ liệu chính của dòng (như rating trong bảng rating ở p4-03); che thành NaN khi các cột khác vẫn có ích (như log request); `keep="first"` vì request được ghi đầu tiên là bản gốc, còn ở p4-03 `keep="last"` vì đánh giá mới nhất thay thế đánh giá cũ.
13. **`.tolist()`**: thêm một câu giới thiệu ở p4-01 (§5 hoặc §6, trước lần dùng đầu trong lesson; nếu quiz/test dùng trước đó thì đặt ở §1–§2): "`a.tolist()` đổi mảng thành list Python thường".
14. **API dùng mà chưa dạy**: thêm chú thích một dòng ở chỗ xuất hiện đầu tiên, hoặc đổi sang dạng đã dạy:
    - `.nunique()` (p4-03-q05): thêm một câu ở p4-03 §1 cạnh `.unique()`.
    - `Series.items()` (p4-02 ex02 hint 3, p4-04 example 02): chú thích một dòng trong hint/example `.md` ("`.items()` cho từng cặp (nhãn, giá trị)").
    - `groupby(as_index=False)` (p4-05 example 03): đổi thành `groupby(...)[...].mean().reset_index()` hoặc giải thích một dòng trong `.md`.
    - `SELECT *` (p4-05-q08, f05): thêm một dòng ở lesson p4-05 §3 ("`SELECT *` lấy mọi cột").
    - `INSERT INTO t VALUES (?, ?)` không liệt kê cột (p4-05-q13/q16, p4-06-q09/q16): đổi các câu đó sang dạng có danh sách cột như lesson đã dạy.
    - `zip(..., strict=True)` (p4-01 ex02 solution, p4-03 ex02 alternative): bỏ `strict=True` và thêm `# noqa: B905` nếu ruff báo, hoặc thêm comment một dòng giải thích.
    - `np.corrcoef` (p4-04 example 03): chú thích trong `.md` ("hệ số tương quan từ -1 đến 1; gần 1 = tăng cùng nhau").
15. **p4-01 ex02 hint 1** trỏ sai mục: sửa để trỏ tới example `03_batch_predictions` (nơi có `argmax(axis=1)`), và thêm một dòng ở lesson §4 cho thấy `max(axis=1)`/`argmax(axis=1)` (comment output khớp thật).
16. **p4-01 ex01 repr sai** `array([0.0, 0.5, 1.0])` trong prompt, docstring starter/solution và hint 1: đổi thành repr thật `array([0. , 0.5, 1. ])` hoặc viết dạng list `[0.0, 0.5, 1.0]` kèm "(as a list: `.tolist()`)".
17. **Số dòng lệch trong phần giải thích example** (EN + VI): sửa theo số dòng **thật** của file `.py` (đếm lại, đừng chép số từ đây): `p4-03-cleaning/examples/01_survey_missing`, `03_training_labels`; `p4-05-sql/examples/01_chat_history`, `03_eval_to_pandas`. Rà luôn mọi example `.md` khác của phase 4 có nhắc số dòng.
18. **"Try it" mơ hồ**: `p4-05-sql/examples/01_chat_history.*.md` → "đổi tham số `("an",)` thành `("binh",)`"; `p4-06-mini-project/examples/03_report_chart.*.md` → thêm hướng dẫn thêm `ROUND(AVG(latency_ms), 1) AS avg_latency` vào SELECT trước khi vẽ.
19. **Alternative p4-06 ex02 phá luật SQL**: giữ file `alternatives/01_pandas_groupby.py`, sửa `.md` (EN + VI) để nói rõ: cách này cố ý không dùng SQL để so sánh, và giới thiệu named aggregation `agg(new_col=("col", "func"))` (một câu giải thích).
20. **p4-05 ex01 ba bộ dữ liệu ví dụ khác nhau**: dùng bộ dữ liệu của `prompt.*.md` cho cả docstring starter/solution và hint 1 (số lần chạy, kết quả phải khớp nhau).
21. **VI p4-02 lesson**: dòng ~60 "được chống lưng bởi mảng NumPy" → "được xây trên mảng NumPy"; "chạy trực tiếp ngay lập tức" → "chạy được ngay"; dòng ~194 `calls["ten_cot"]` → `calls["new_col"]` (code không dịch).
22. **Câu quiz trùng giữa các bài**: viết lại (giữ id, type, độ khó tương đương) các câu bản sao ở **p4-06** — `p4-06-q04`, `p4-06-q07`, `p4-06-f02` (đang hỏi `IntCastingNaNError`), `p4-06-q02` (strip/lower rồi đếm) — sang ý của chính mini-project: `.where` khác `dropna` thế nào, vì sao cần `.astype(str)`, `AVG(status = 'error')` ra gì, `if_exists="replace"`. Viết lại `p4-02-q12` (fill `&` trùng p4-01-q13) sang một ý pandas khác (vd `isin` hoặc `sort_values(ascending=False)`). Câu `output`/`fill`/`parsons` mới phải qua validator.
23. **Nhỏ**: `p4-04-matplotlib/lesson.*.md` TIP "Always sort bar chart values" → thêm "trừ khi các nhóm có thứ tự tự nhiên (tháng, epoch, rating 1–5)"; `p4-02-q04`, `p4-02-f02` đổi tag `json` → `pandas`.
24. **p4-03 ex02 rating số lẻ**: thêm một dòng Rules trong `prompt.*.md`: "rating là số nguyên; giá trị có phần thập phân như `"4.5"` bị coi là không hợp lệ và bị bỏ" **và** một test tương ứng; sửa solution + alternative để qua (vd lọc thêm `rating == rating.round()` hoặc `% 1 == 0`), hint cập nhật nếu cần.
25. **`apps/web/public/pyodide-worker.js`, nhánh `test`**: tải gói và phát hiện matplotlib theo **cả** code người học **và** file test: `await loadImports(msg.code + "\n" + msg.tests)` và `usesMatplotlib(msg.code + "\n" + msg.tests)` (hoặc gọi hai lần). Không đổi nhánh `run`/`trace`, không đổi message.

## Tiêu chí hoàn thành (checklist)
1. [ ] Cả 25 mục đã sửa đúng quyết định trên; report liệt kê từng mục: file đã sửa + một câu đã làm gì. Mục nào không làm được hoặc làm khác, nói rõ lý do.
2. [ ] Mọi output/comment/thông báo lỗi mới lấy từ lần chạy thật (đặt `MPLBACKEND=Agg` khi tự chạy code có matplotlib bằng python ngoài validator, để không mở cửa sổ).
3. [ ] EN/VI song song cho mọi thay đổi.
4. [ ] Lệnh kiểm tra xanh, chạy đúng như ghi.

## Lệnh kiểm tra
Từ gốc repo `D:\Proj\python-ai-platform`:
```
uv run python tools/validate.py --path curriculum/phase-04-data
uv run python tools/validate.py
uv run python -m pytest curriculum
uv run ruff check curriculum
pnpm --filter web typecheck
grep -rn "zip(\*" curriculum/phase-04-data
grep -rn "UserWarning: No artists" curriculum/phase-04-data
grep -rn "ten_cot\|Hợp nhất cho\|ngoặc đơn \`\[" curriculum/phase-04-data
git status --short
git diff --stat
```
Mong đợi: validate 0 lỗi; pytest exit 0; ruff sạch; typecheck 0 lỗi; ba grep rỗng; chỉ file trong `curriculum/phase-04-data/` và `apps/web/public/pyodide-worker.js` bị sửa; không file nào bị xóa.
Sau đó chạy `uv run python tools/build_content.py` (an toàn khi dev server chạy).

## Ghi chú cho worker
- Dùng `uv run python -m pytest`, không dùng `uv run pytest`.
- Không có trình duyệt thì ghi rõ trong report; boss tự kiểm tra trong app.

## Trạng thái
- Bước hiện tại: 5 (đạt sau vòng 1; boss xác minh từng mục + mục 25 trong app; chờ user duyệt commit)
- Vòng: 1/3
- Số lần swap: 0
- Fallback: không
- Model: Gemini 4 Hydrogen (High)
