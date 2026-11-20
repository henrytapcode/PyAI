# M3 bước 3: bài p4-02 Pandas DataFrames

## Mục tiêu
Viết bài `p4-02-pandas` đúng `docs/CONTENT_GUIDE.md`, song ngữ EN/VI, chạy được cả local và trong app (Pyodide tự tải pandas).
Người học đã xong phase 1–3 và bài `p4-01-numpy` (array, vectorised math, boolean mask, `axis`), nhưng **chưa biết pandas**.
Bài mẫu gần nhất về giọng văn và hình dạng: `curriculum/phase-04-data/p4-01-numpy/` (vừa được duyệt).

## File được phép sửa/tạo
- Thư mục mới `curriculum/phase-04-data/p4-02-pandas/` và mọi file bên trong.
- `curriculum/glossary.yaml`: chỉ **thêm** thuật ngữ mới (DataFrame, Series, index, groupby, aggregation; bỏ qua cái đã có).

## Không được đụng
- `apps/`, `tools/`, `curriculum/syllabus.yaml`, `curriculum/topics.yaml`, bài `p4-01-numpy`, các phase khác, `exams/`.
- Không xóa file, không `git commit`, **không chạy `pnpm --filter web build`** (dev server đang chạy).

## Nội dung bài (boss chốt dàn ý, worker viết)
Opening (không heading): dữ liệu AI thường là bảng: log hội thoại chatbot, kết quả eval của nhiều mô hình. pandas là "Excel trong Python", xây trên NumPy.

1. **Series và DataFrame**: tạo DataFrame từ dict các list; `shape`, `columns`, `dtypes`, `head()`, `len(df)`. Một cột là một `Series`. Bảng so sánh `| NumPy array | pandas DataFrame |` (nhãn cột, nhiều kiểu dữ liệu theo cột, index).
2. **Đọc CSV**: `pd.read_csv(io.StringIO(text))` với CSV viết ngay trong code (giới thiệu `io.StringIO` một câu: "giả làm file từ một chuỗi"). Một câu: dự án thật dùng `pd.read_csv("data.csv")`.
3. **Chọn dữ liệu**: `df["col"]`, `df[["a", "b"]]`, `df.loc[label]`, `df.iloc[i]`, `df.loc[rows, cols]`. **Picture in text** (fence `text`) vẽ bảng có index ở cột trái, chỉ ra `loc` dùng nhãn còn `iloc` dùng vị trí.
4. **Lọc và sắp xếp**: boolean mask (nối lại với p4-01), `&`/`|` có ngoặc, `isin`, `sort_values(..., ascending=False)`, `reset_index(drop=True)`.
5. **Cột mới**: phép tính vector hóa giữa các cột (`df["cost"] = df["tokens"] * price`), `round`. Đây là section mời bấm **Visualize** (khối nhỏ, 3–4 dòng gán).
6. **groupby**: `df.groupby("model")["score"].mean()`, `.agg(["mean", "count"])`, `value_counts()`. **Mermaid** `flowchart LR` cho split → apply → combine. **Trace table** cho một groupby nhỏ (`| group | rows | scores | mean |`).
7. **Lỗi thường gặp** (3–4): `KeyError` vì sai tên cột (hoa thường, dấu cách); gán qua chained indexing `df[df.x > 0]["y"] = 1` không đổi `df` (chạy thật để lấy đúng cảnh báo pandas 2.3 đưa ra, rồi sửa bằng `df.loc[mask, "y"] = 1`); nhầm `loc`/`iloc` sau khi lọc vì index giữ nhãn cũ (sửa bằng `reset_index(drop=True)`); dùng `and` thay `&`.
8. **Recap / Tóm tắt**.

Thời lượng 10–12 phút. `review_by: "2027-11-01"`. `further_reading`: "10 minutes to pandas" và trang "Group by: split-apply-combine" (URL chính thức pandas.pydata.org).

## Examples (3)
- `01_chat_logs`: DataFrame từ dict (người dùng, số tin nhắn, đánh giá), lọc phiên có đánh giá thấp, sắp xếp.
- `02_api_costs_csv`: đọc CSV từ `io.StringIO` (model, prompt_tokens, completion_tokens), thêm cột tổng token và chi phí, in 3 dòng đắt nhất.
- `03_eval_by_model`: kết quả eval (model, task, score), `groupby("model")` lấy trung bình và số lượng, tìm model tốt nhất.

## Exercises (2)
- `ex01-slow-requests` (`kind: debug`): hàm `slow_requests(df, limit_ms) -> pd.DataFrame` trả các request có `latency_ms` **lớn hơn hẳn** `limit_ms`, chỉ gồm cột `["endpoint", "latency_ms"]`, sắp xếp giảm dần theo `latency_ms`, index đánh lại từ 0. Starter **chạy được** nhưng có 3 bug thật: dùng `>=` thay `>`, sắp xếp tăng dần, quên `reset_index(drop=True)`. Test so bằng `.to_dict("list")` hoặc `.tolist()`.
- `ex02-average-score-by-model` (`kind: code`): hàm `average_score_by_model(df) -> dict[str, float]`: chỉ lấy dòng có `status == "ok"`, trung bình `score` theo `model`, làm tròn 2 chữ số, trả **dict Python** với giá trị `float` thuần (không phải `np.float64`). Model không có dòng "ok" thì không xuất hiện. 4–6 test (gồm DataFrame rỗng sau khi lọc → `{}`). Có `alternatives/01_loop.py` (duyệt `df.itertuples()` với dict cộng dồn) + `.md` nói vì sao `groupby` ngắn và nhanh hơn.

## Quiz
15–18 câu, mỗi loại `mcq`/`output`/`fill`/`parsons` ít nhất 2; khoảng 5 dễ, 7 vừa, 3 khó. 6 flashcard. Tag: `pandas` (chính), có thể thêm `numpy` hoặc tag có sẵn.

## Tiêu chí hoàn thành (checklist)
1. [ ] Đủ file theo layout CONTENT_GUIDE; `meta.yaml` có `phase: p4`, `order: 2`, `tags` gồm `pandas`, `prerequisites` khớp syllabus (`[p4-01-numpy, p1-09-files]`), `outcomes` khớp syllabus (có thể thêm 1–2 dòng).
2. [ ] Lesson đúng dàn ý trên, đủ: mermaid, trace table, picture in text, bảng so sánh, một lời mời Visualize, callout.
3. [ ] Code giữa `lesson.en.md` và `lesson.vi.md` giống hệt (trừ comment); số dòng mermaid bằng nhau; fence `text` giống hệt.
4. [ ] **In DataFrame ổn định giữa local và app**: mọi DataFrame được `print` (trong lesson, example, quiz `output`) có tối đa 4 cột và mỗi dòng in ra dưới 60 ký tự, để pandas không tự ngắt dòng theo độ rộng terminal. Cần in rộng hơn thì dùng `df.to_string()`.
5. [ ] **Không in numpy scalar trong list/tuple/dict** (numpy 2 in `np.float64(2.5)`): dùng `.tolist()`, `float()`, `int()`, `round(float(x), 2)` trước khi in.
6. [ ] **Comment output trong lesson đúng thật**: mọi `print(...)  # ...` trong khối python của `lesson.en.md` phải khớp output thật (boss sẽ chạy từng khối để đối chiếu; validator không kiểm phần này). Với DataFrame nhiều dòng, ghi output dưới dạng comment nhiều dòng như bài NumPy đã làm.
7. [ ] Exercise: starter fail, solution và alternative pass (pytest **và** browser runner); hint đủ 3 tầng mỗi ngôn ngữ; gợi ý tầng 3 chừa ít nhất 2 chỗ `...`, không gần như lời giải.
8. [ ] Bản VI tự nhiên, xưng "bạn", thuật ngữ giữ tiếng Anh kèm giải nghĩa lần đầu.
9. [ ] Lệnh kiểm tra xanh.
10. [ ] Xem bài trong app: chạy `uv run python tools/build_content.py` (an toàn khi dev server đang chạy), mở `http://localhost:3000/lesson/p4-02-pandas/`, bấm Run một khối có DataFrame và Visualize ở khối được mời, ghi kết quả vào report.

## Lệnh kiểm tra
Từ gốc repo `D:\Proj\python-ai-platform`:
```
uv run python tools/validate.py --path curriculum/phase-04-data/p4-02-pandas
uv run python tools/validate.py
uv run python -m pytest curriculum/phase-04-data
uv run ruff check curriculum/phase-04-data
git status --short
```
Mong đợi: validate 0 lỗi (bài lẻ và toàn bộ); pytest exit 0; ruff sạch; chỉ có file mới trong `curriculum/phase-04-data/p4-02-pandas/` (và `glossary.yaml` nếu thêm thuật ngữ).

## Ghi chú cho worker
- Đọc `docs/CONTENT_GUIDE.md`, rồi bài `curriculum/phase-04-data/p4-01-numpy/` để bắt chước giọng văn và hình dạng file.
- Local dùng pandas 2.3.3 / numpy 2.2.5, giống Pyodide trong app; `.out` phải khớp chính xác stdout.
- Test so DataFrame/Series bằng `.tolist()`, `.to_dict("list")` hoặc `list(df.columns)`; đừng `assert df1 == df2`.
- Dùng `uv run python -m pytest`, không dùng `uv run pytest` (lỗi launcher).

## Trạng thái
- Bước hiện tại: 5 (đạt sau vòng 1, chờ user duyệt commit)
- Vòng: 1/3
- Số lần swap: 0
- Fallback: không
- Model: Gemini 4 Hydrogen (High)
