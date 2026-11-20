# M3 bước 8: Phase test 4 (Data)

## Mục tiêu
Viết `curriculum/phase-04-data/phase-test.yaml`: bài kiểm tra cuối phase 4, cùng định dạng với `curriculum/phase-03-code-quality/phase-test.yaml` (schema `tools/schema/exam.schema.json`, `kind: phase_test`).
Boss đã chốt blueprint dưới đây; worker viết câu hỏi theo đúng blueprint.

## File được phép sửa/tạo
- File mới `curriculum/phase-04-data/phase-test.yaml`. Chỉ file này.

## Không được đụng
- Mọi file khác (kể cả quiz của các bài, `tools/`, `apps/`). Không xóa file, không `git commit`, **không chạy `pnpm --filter web build`**.

## Blueprint (boss chốt)
- `id: p4-phase-test`, `phase: p4`, title EN "Phase 4 test: Data" / VI "Bài kiểm tra Phase 4: Dữ liệu", description nêu số câu và chủ đề (NumPy, pandas, làm sạch, biểu đồ, SQL).
- `duration_min: 25`, `pass_score: 0.7`.
- **18 câu**, id `p4-test-q01` … `p4-test-q18`, nhóm theo chủ đề bằng comment `# ---- numpy` như phase 3:

| Chủ đề (bài) | Số câu | Ý chính phải kiểm |
|---|---|---|
| NumPy (p4-01) | 3 | vectorised math vs list, `axis=0`/`axis=1`, boolean mask với `&` và ngoặc |
| pandas (p4-02) | 3 | `loc` vs `iloc` sau khi lọc, `groupby(...).agg`/`mean`, cột mới vector hóa |
| Cleaning (p4-03) | 3 | `to_numeric(errors="coerce")`, quên gán lại sau `dropna`/`fillna`, thứ tự "lọc khoảng hợp lệ trước rồi mới `drop_duplicates`" |
| Plotting (p4-04) | 3 | chọn loại biểu đồ theo câu hỏi, `fig, ax` + `set_title`/`set_xlabel`, đọc thuộc tính qua `ax.get_title()` / `len(ax.lines)` |
| SQL (p4-05) | 3 | placeholder `?` và tuple một phần tử `(x,)`, `GROUP BY` + `HAVING` vs `WHERE`, `IS NULL` |
| Mini-project, tích hợp (p4-06) | 3 | pipeline nhiều bước: đọc CSV bẩn → làm sạch → tổng hợp; `AVG(status = 'error')`; chọn SQL hay pandas cho một việc |

- **Loại câu**: 8 `mcq`, 5 `output`, 3 `fill`, 2 `parsons` (rải đều các chủ đề; mỗi chủ đề ít nhất 2 loại khác nhau).
- **Độ khó**: 4 câu mức 1, 10 câu mức 2, 4 câu mức 3. Câu mức 3 nên là câu tích hợp hoặc bẫy phổ biến.
- **Câu mới hoàn toàn**: không chép hay đổi chút ít câu nào trong `quiz.yaml` của 6 bài p4 (đọc hết 6 file quiz trước để tránh trùng ý và trùng code).
- Mỗi câu có `tags` (tag có sẵn trong `curriculum/topics.yaml`, ví dụ `numpy`, `pandas`, `data-cleaning`, `plotting`, `sql`), và `explanation` song ngữ nói **vì sao**, không chỉ đáp án.
- mcq: distractor là hiểu lầm thật; không "All of the above"; nếu cần giữ thứ tự thì `shuffle_options: false`.
- parsons: `lines` theo thứ tự đúng, chạy được, mỗi dòng duy nhất, chỉ một thứ tự đúng.
- Chỉ dùng kiến thức đã dạy trong phase 1–4 (đã sửa review: `DISTINCT`, `.tolist()`, `.where`, `.astype(str)`, `to_sql` đều đã được dạy).

## Quy tắc output (bắt buộc, app chạy Pyodide 32-bit)
- Không in `dtype` của mảng NumPy số nguyên; không `astype(int)`/`dtype=int` (dùng `"int64"`); không `df.info()`. Không in list/dict chứa numpy scalar (dùng `.tolist()`, `float()`, `int()`).
- SQLite: chỉ `sqlite3.connect(":memory:")`, không tính năng mới hơn 3.39, `SELECT` nhiều dòng phải có `ORDER BY`, không in object Connection.
- matplotlib: câu `output` chỉ in chữ (`print(ax.get_title())`, ...), không gọi `plt.show()`; không dùng API mới hơn 3.8.
- DataFrame in ra tối đa 4 cột, dòng dưới 60 ký tự. Số thực in ra phải làm tròn.
- `output`/`fill`/`parsons` phải chạy được với validator (validator chạy code thật và so đáp án).

## Tiêu chí hoàn thành (checklist)
1. [ ] Đúng blueprint: 18 câu, phân bổ chủ đề, loại câu và độ khó như bảng; ghi bảng đếm thực tế vào report.
2. [ ] Không trùng câu với quiz của 6 bài (report liệt kê, mỗi câu kiểm ý nào).
3. [ ] EN/VI đầy đủ, VI tự nhiên, code giống hệt giữa hai ngôn ngữ.
4. [ ] Tuân thủ "Quy tắc output".
5. [ ] Lệnh kiểm tra xanh, chạy đúng như ghi.

## Lệnh kiểm tra
Từ gốc repo `D:\Proj\python-ai-platform`:
```
uv run python tools/validate.py --path curriculum/phase-04-data
uv run python tools/validate.py
uv run python -m pytest curriculum
uv run python tools/build_content.py
grep -nE "astype\(int\)|dtype=int\b|\.info\(|sqlite_version|plt\.show" curriculum/phase-04-data/phase-test.yaml
git status --short
```
Mong đợi: validate 0 lỗi (đếm exams tăng 1); pytest exit 0; build_content in số exams tăng 1; grep rỗng; chỉ có một file mới `curriculum/phase-04-data/phase-test.yaml`.

## Ghi chú cho worker
- Đọc mẫu `curriculum/phase-03-code-quality/phase-test.yaml`, schema `tools/schema/exam.schema.json`, và 6 file `curriculum/phase-04-data/p4-0*/quiz.yaml`.
- Tự chạy code của câu có matplotlib bằng python ngoài validator thì đặt `MPLBACKEND=Agg`.
- Dùng `uv run python -m pytest`, không dùng `uv run pytest`.

## Trạng thái
- Bước hiện tại: 5 (đạt sau vòng 2: vòng 1 vị trí đáp án mcq lệch về A; boss duyệt 18/18 câu, xem bài thi trong app; chờ user duyệt commit)
- Vòng: 2/3
- Số lần swap: 0
- Fallback: không
- Model: Gemini 4 Hydrogen (High)

## Feedback vòng 1
Nội dung 18 câu đạt (boss đã duyệt từng câu: đáp án, phân bổ chủ đề/loại/độ khó đúng blueprint). Chỉ còn một lỗi:
- **Vị trí đáp án mcq lệch**: app hiện **không xáo trộn lựa chọn mcq** (chỉ xáo dòng parsons, xem `apps/web/src/components/question.tsx`), nên thứ tự trong yaml chính là thứ tự người học thấy. Hiện `answer` của 8 câu mcq là `0,1,0,0,2,0,0,1` (5/8 là A).
- Sửa: đổi **thứ tự options** (và `answer` cho khớp) của các câu mcq để đáp án đúng rải đều: đúng 2 câu ở mỗi vị trí 0, 1, 2, 3. Đổi thứ tự **giống hệt** ở `en.options` và `vi.options`. Không đổi nội dung option, prompt hay explanation (trừ khi explanation nhắc tới vị trí, vd "option A").
- Chỉ sửa `curriculum/phase-04-data/phase-test.yaml`. Chạy lại `uv run python tools/validate.py --path curriculum/phase-04-data` và `uv run python tools/validate.py`; ghi vào report bảng `id → answer` mới.
