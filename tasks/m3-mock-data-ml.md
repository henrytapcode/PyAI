# M3 bước 15: Mock exam Data & ML

## Mục tiêu
Viết `curriculum/exams/mock-data-ml.yaml`: bài thi thử kiểu phỏng vấn AI Engineer, phủ phase 4 (Data) và phase 5 (ML). Cùng định dạng với `curriculum/exams/mock-python-core.yaml` (schema `tools/schema/exam.schema.json`, `kind: mock`, không có trường `phase`).
Boss đã chốt blueprint **từng câu** dưới đây; worker viết đúng ý, loại câu và độ khó của từng dòng.

## File được phép sửa/tạo
- File mới `curriculum/exams/mock-data-ml.yaml`. Chỉ file này.

## Không được đụng
- Mọi file khác (quiz, phase test, `tools/`, `apps/`, glossary, topics). Không xóa file, không `git commit`, **không chạy `pnpm --filter web build`**.

## Thông tin chung
- `id: mock-data-ml`, `kind: mock`, title EN "Mock exam: Data & ML" / VI "Thi thử: Dữ liệu & ML".
- description EN "24 interview-style questions on NumPy, pandas, cleaning, plotting, SQL, and machine learning. Aim for 80% or more." (VI tương ứng, tự nhiên).
- `duration_min: 35`, `pass_score: 0.8`.
- 24 câu, id `mock2-q01` … `mock2-q24`, nhóm bằng comment `# ---- data` và `# ---- ml`.
- Giọng kiểu phỏng vấn: đặt câu hỏi trong bối cảnh thật (log chatbot, ticket hỗ trợ, đơn hàng, chi phí token, phát hiện gian lận...), không hỏi định nghĩa suông.

## Blueprint từng câu (boss chốt)

| # | Chủ đề / tag chính | Loại | Độ khó | Ý phải kiểm |
|---|---|---|---|---|
| 01 | numpy | output | 2 | broadcasting: mảng `(3, 1)` cộng mảng `(2,)` → in `.shape` và `.tolist()` |
| 02 | numpy | mcq | 3 | chuẩn hóa từng cột `(X - X.mean(axis=0)) / X.std(axis=0)`: hỏi chọn đúng `axis` và vì sao (cột = feature) |
| 03 | numpy | output | 3 | view vs copy: sửa một slice làm đổi mảng gốc, còn `.copy()` thì không (dùng đúng cách p4-01 dạy; nếu p4-01 không dạy view thì thay bằng boolean mask + `np.where` tạo mảng mới) |
| 04 | pandas | output | 2 | `groupby(...).agg(...)` hoặc `groupby(...)[col].mean()` trên dữ liệu chi phí token theo model, in kết quả gọn (`round`, `.to_dict()` hoặc `to_string()`) |
| 05 | pandas | output | 3 | cột mới vector hóa + `sort_values(..., ascending=False)` + `head(2)`: in tên 2 dòng đứng đầu (bẫy: quên `ascending=False`) |
| 06 | pandas, data-cleaning | fill | 2 | tỉ lệ từng nhãn = `df["label"].___() / len(df)` (blank: `value_counts`), in `.round(3).to_dict()` |
| 07 | data-cleaning | output | 2 | `pd.to_numeric(errors="coerce")` rồi `dropna(subset=...)`: in số dòng còn lại và trung bình |
| 08 | data-cleaning | mcq | 3 | trùng lặp ẩn: `" Alice"`, `"alice"`, `"ALICE "` — phải `str.strip().str.lower()` **trước** `drop_duplicates`; distractor: drop trước rồi mới chuẩn hóa, `drop_duplicates(keep=False)`, `dropna` |
| 09 | plotting | mcq | 2 | chọn biểu đồ cho 3 câu hỏi khác nhau (xu hướng theo thời gian → line, phân bố độ dài prompt → histogram, so sánh nhóm → bar) |
| 10 | plotting | output | 2 | `fig, axes = plt.subplots(1, 2)`; đặt title từng ax; in `len(axes)` và `axes[1].get_title()` (không `plt.show()`) |
| 11 | sql | output | 3 | `GROUP BY` + `HAVING COUNT(*) >= n` + `ORDER BY`, kèm một cột có `NULL` lọc bằng `WHERE ... IS NOT NULL` (không dùng JOIN, chưa dạy) |
| 12 | sql | parsons | 2 | `sqlite3.connect(":memory:")` → `CREATE TABLE` → `executemany` với `?` → `SELECT ... ORDER BY` → in kết quả |
| 13 | ml-math | fill | 2 | chuẩn hóa hai vector về độ dài 1 bằng `np.linalg.norm`, rồi dot = cosine similarity; blank là `np.linalg.norm` hoặc `@` |
| 14 | ml-math | output | 3 | vòng gradient descent 3 bước trên loss `(w - 3) ** 2`, in `w` sau mỗi bước (làm tròn) |
| 15 | supervised-learning, data-prep | mcq | 2 | phỏng vấn: vì sao phải chia train/test **trước** khi fit scaler (thống kê của test rò vào train) |
| 16 | sklearn | parsons | 3 | `make_classification` → `make_pipeline(StandardScaler(), LogisticRegression())` → `StratifiedKFold(shuffle=True, random_state=...)` → `cross_val_score` → in mean ± std làm tròn |
| 17 | sklearn, model-evaluation | fill | 2 | `proba = model.predict_proba(X)[:, ___]` và `preds = (proba >= t).astype("int64")`; blank là `1` (cột lớp dương) |
| 18 | model-evaluation | output | 2 | `confusion_matrix(y_true, y_pred).ravel()` → in `tn, fp, fn, tp` dạng `int` |
| 19 | model-evaluation | mcq | 3 | fraud 1%: mô hình 99% accuracy đoán toàn 0; hỏi nên báo cáo gì (recall/precision/F1 của lớp gian lận, so với baseline `DummyClassifier`) |
| 20 | model-evaluation | output | 2 | tính precision, recall, F1 bằng tay từ TP/FP/FN cho sẵn (Python thuần), in làm tròn |
| 21 | model-evaluation | mcq | 2 | vì sao dùng `StratifiedKFold` thay `KFold` khi lớp hiếm (fold có thể không có mẫu dương) |
| 22 | model-evaluation, data-prep | mcq | 3 | leakage: `StandardScaler().fit_transform(X)` trên toàn bộ dữ liệu rồi mới `cross_val_score` → điểm CV lạc quan; sửa bằng pipeline |
| 23 | supervised-learning | mcq | 2 | bảng `max_depth` 1..6 với train score và validation score (tách từ train hoặc CV); chọn depth theo **validation**, không theo train, không theo test |
| 24 | model-evaluation | parsons | 3 | quy trình trung thực: `train_test_split(stratify=y)` → `cross_val_score` trên **train** để kiểm mô hình → `fit` trên train → chấm test **một lần** → in |

Đếm kiểm: mcq 8 (02, 08, 09, 15, 19, 21, 22, 23), output 10, fill 3, parsons 3. Độ khó 3: 10 câu; độ khó 2: 14 câu.

## Yêu cầu chất lượng
- **Câu mới hoàn toàn**: đọc hết quiz của 11 bài p4/p5, `curriculum/phase-04-data/phase-test.yaml`, `curriculum/phase-05-ml/phase-test.yaml`; không chép hay đổi chút ít câu nào.
- mcq: `answer` rải đều (đúng 2 câu ở mỗi vị trí 0–3). **Độ dài 4 lựa chọn cân nhau** (dài nhất / ngắn nhất ≤ 1.3); không nhét lý do vào lựa chọn đúng (lý do để trong `explanation`). Distractor là hiểu lầm thật. Không "All of the above", không "cả hai"/"Both A and B" (validator chặn lựa chọn phụ thuộc vị trí).
- parsons: mỗi dòng duy nhất, chạy được theo thứ tự đúng, chỉ một thứ tự đúng (dòng sau phụ thuộc dòng trước).
- `explanation` song ngữ nói **vì sao**. `tags` có sẵn trong `curriculum/topics.yaml`.
- Chỉ dùng API đã dạy trong phase 1–5 (đọc lesson p4/p5 để chắc; JOIN và `merge` **chưa** dạy).

## Quy tắc nội dung (giữ như phase 5)
- **Test chỉ dùng một lần**: chọn mô hình, hyperparameter, threshold bằng CV hoặc validation tách từ train. Không câu nào ngụ ý chọn theo test score.
- **`zero_division`** (sklearn 1.7): chỉ precision cảnh báo khi TP+FP=0; F1/recall của dự đoán toàn 0 khi có dương thật trả 0.0 không cảnh báo.
- Thuật ngữ VI: accuracy = "tỉ lệ đoán đúng"; precision = "độ chuẩn khi báo dương"; recall = "độ nhạy, tức tỉ lệ bắt được". Không dùng "độ chính xác", "độ phủ".
- Ngẫu nhiên chỉ qua `np.random.default_rng(seed)` và `random_state`. Không `fetch_*`, `load_*` dataset, không mạng.

## Quy tắc output (bắt buộc, app chạy Pyodide 32-bit)
- Không in `dtype` mảng NumPy số nguyên; không `astype(int)`/`dtype=int` (dùng `"int64"`); không `df.info()`.
- Không in numpy scalar hay list/dict chứa chúng: dùng `.tolist()`, `round(float(x), 3)`, `int()`.
- Không phát warning nào (kể cả `ConvergenceWarning`, `UndefinedMetricWarning`, FutureWarning, matplotlib).
- DataFrame in ra tối đa 4 cột, dòng dưới 60 ký tự. Số thực in ra phải làm tròn.
- SQLite: chỉ `":memory:"`, `SELECT` nhiều dòng phải có `ORDER BY`. matplotlib: chỉ in chữ, không `plt.show()`, không API mới hơn 3.8.
- Code ngắn (output/fill dưới ~15 dòng), dữ liệu nhỏ, chạy nhanh. Kết quả giống nhau ở bản app (numpy 2.2.5, pandas 2.3.3, sklearn 1.7.0, matplotlib 3.8.4) và local.

## Tiêu chí hoàn thành (checklist)
1. [ ] Đúng blueprint từng câu (report: bảng `id | loại | độ khó | ý kiểm`).
2. [ ] mcq: bảng `id → answer` và độ dài (ký tự EN) 4 lựa chọn.
3. [ ] Không trùng câu với quiz p4/p5 và hai phase test.
4. [ ] EN/VI đầy đủ, VI tự nhiên, code giống hệt giữa hai ngôn ngữ.
5. [ ] Tuân thủ "Quy tắc nội dung" và "Quy tắc output"; mọi câu output/fill/parsons chạy sạch với `-W error`.
6. [ ] Lệnh kiểm tra xanh.

## Lệnh kiểm tra
Từ gốc repo `D:\Proj\python-ai-platform`:
```
uv run python tools/validate.py
uv run python -m pytest curriculum
uv run python tools/build_content.py
grep -nE "astype\(int\)|dtype=int\b|\.info\(|fetch_|load_|plt\.show|JOIN|merge\(|độ chính xác|độ phủ" curriculum/exams/mock-data-ml.yaml
git status --short
```
Mong đợi: validate 0 lỗi (exams từ 7 lên 8); pytest exit 0; build_content in 8 exams; grep rỗng; chỉ có file mới `curriculum/exams/mock-data-ml.yaml` (ngoài `tasks/`, `.hallmark/` vốn untracked).

## Ghi chú cho worker
- Đọc mẫu `curriculum/exams/mock-python-core.yaml` và `curriculum/phase-05-ml/phase-test.yaml` (mẫu gần nhất về độ dài lựa chọn cân nhau).
- Tự chạy từng đoạn code bằng `uv run python -W error snippet.py` (matplotlib: đặt `MPLBACKEND=Agg`).
- Dùng `uv run python -m pytest`, không dùng `uv run pytest`.

## Trạng thái
- Bước hiện tại: 5 (đạt sau vòng 2; boss duyệt 24/24 câu, chạy lại mọi câu, nộp thử trong app; đã commit `d9b7437`)
- Vòng: 2/3
- Số lần swap: 0
- Fallback: không
- Model: Gemini 4 Hydrogen (High)

## Feedback vòng 1
Boss đã duyệt 24/24 câu: đúng blueprint, đáp án đúng, mcq cân độ dài và rải đều vị trí, mọi câu chạy được đều in đúng đáp án. Còn 3 lỗi (chỉ sửa `curriculum/exams/mock-data-ml.yaml`):
1. **q13 lộ đáp án trong đề**: prompt EN/VI ghi thẳng "(`np.linalg.norm`)". Bỏ tên hàm khỏi prompt; nói "the NumPy function that returns a vector's length" / "hàm NumPy trả về độ dài của vector". Giữ code và `answer`.
2. **q17 gợi ý quá rõ**: "positive class (`1`)" gần như cho luôn chỉ số cột. Viết lại prompt: "fill in the column index that holds the probability of an urgent ticket (label `1`); `predict_proba` returns one column per class in the order of `model.classes_`" (VI tương ứng). Giữ code và `answer`.
3. **q24 so hai thước đo khác nhau**: CV in F1, còn test in accuracy (`.score`) và ra `1.0`. Một quy trình "trung thực" phải dùng cùng thước đo. Sửa dòng test để in **F1** trên test (vd `metrics.f1_score(y_te, linear_model.LogisticRegression().fit(X_tr, y_tr).predict(X_te))`, thêm `metrics` vào dòng import), và đổi `random_state`/`n_samples` nếu cần để điểm test không phải `1.0` (một con số thực tế hơn, ví dụ 0.8–0.95). Giữ đúng một thứ tự (prompt vẫn nói in cv trước, test sau). Cập nhật prompt và explanation cho khớp ("F1 on `X_te`").
Chạy lại `uv run python tools/validate.py` và tự chạy q24 với `-W error`; ghi output mới của q24 vào report.
