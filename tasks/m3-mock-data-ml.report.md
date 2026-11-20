# Báo cáo M3 bước 15: Mock exam Data & ML

## 1. Đã làm gì
- Tạo mới đề thi thử `curriculum/exams/mock-data-ml.yaml` (`id: mock-data-ml`, `kind: mock`, không có trường `phase`, `duration_min: 35`, `pass_score: 0.8`, title/description song ngữ EN/VI).
- Viết đủ 24 câu hỏi mới (`mock2-q01`–`mock2-q24`) theo giọng phỏng vấn thực tế (độ trễ API, chi phí token, log chatbot, ticket hỗ trợ, phát hiện gian lận, review code), chia 2 nhóm `# ---- data` (12 câu) và `# ---- ml` (12 câu).
- Phân bố loại câu: 8 `mcq`, 10 `output`, 3 `fill`, 3 `parsons`. Phân bố độ khó: 14 câu độ khó `2`, 10 câu độ khó `3`.
- Không trùng lặp với 11 quiz bài học phase 4/5 và `phase-test.yaml` của phase 4/5; chỉ dùng API đã dạy trong phase 1–5 (không `JOIN`, không `merge()`).
- Tuân thủ quy tắc nội dung và Pyodide 32-bit: dùng `np.random.default_rng` / `random_state`, `"int64"`, `.tolist()`, `round(float(...), 3)`, thuật ngữ VI chuẩn (`tỉ lệ đoán đúng`, `độ chuẩn khi báo dương`, `độ nhạy, tức tỉ lệ bắt được`), không in `dtype` số nguyên, không `plt.show()`.

### Bảng kiểm tra từng câu theo blueprint

| id | loại | độ khó | ý kiểm |
|---|---|---|---|
| `mock2-q01` | output | 2 | Broadcasting `(3, 1)` + `(2,)` → in `.shape` và `.tolist()` |
| `mock2-q02` | mcq | 3 | Chuẩn hóa từng cột trên `(100, 4)`: chọn `axis=0` (cột = feature) |
| `mock2-q03` | output | 3 | View vs copy: sửa slice `tokens[1:3]` làm đổi gốc, `.copy()` thì không |
| `mock2-q04` | output | 2 | `groupby("model")["cost"].mean().round(3).to_dict()` chi phí token |
| `mock2-q05` | output | 3 | Cột mới vector hóa + `sort_values("total", ascending=False)` + `head(2)` |
| `mock2-q06` | fill | 2 | Tỉ lệ nhãn `(df["label"].___() / len(df)).round(3).to_dict()` (`value_counts`) |
| `mock2-q07` | output | 2 | `pd.to_numeric(..., errors="coerce")` + `dropna(subset=...)`, in số dòng và mean |
| `mock2-q08` | mcq | 3 | Trùng lặp ẩn `" Alice"`, `"alice"`, `"ALICE "`: `.str.strip().str.lower()` trước `drop_duplicates` |
| `mock2-q09` | mcq | 2 | Chọn biểu đồ cho 3 câu hỏi (thời gian → line, phân bố prompt → histogram, nhóm → bar) |
| `mock2-q10` | output | 2 | `fig, axes = plt.subplots(1, 2)`, đặt title, in `len(axes)` và `axes[1].get_title()` |
| `mock2-q11` | output | 3 | SQL `WHERE rating IS NOT NULL` + `GROUP BY` + `HAVING COUNT(*) >= 2` + `ORDER BY` |
| `mock2-q12` | parsons | 2 | `sqlite3.connect(":memory:")` → `CREATE TABLE` → `executemany` với `?` → `SELECT ... ORDER BY` → in |
| `mock2-q13` | fill | 2 | Chuẩn hóa 2 vector về độ dài 1 bằng `np.linalg.norm`, dot product = cosine similarity |
| `mock2-q14` | output | 3 | Vòng lặp gradient descent 3 bước trên `(w - 3) ** 2`, in `w` sau mỗi bước |
| `mock2-q15` | mcq | 2 | Phỏng vấn: vì sao phải `train_test_split` trước khi fit `StandardScaler` |
| `mock2-q16` | parsons | 3 | `make_classification` → `make_pipeline` + `StratifiedKFold` + `cross_val_score` → in `mean +/- std` |
| `mock2-q17` | fill | 2 | `predict_proba(...)[:, ___]` với blank `1` (cột lớp dương) và ngưỡng `t` |
| `mock2-q18` | output | 2 | `confusion_matrix(y_true, y_pred).ravel().tolist()` → in `tn, fp, fn, tp` dạng `int` |
| `mock2-q19` | mcq | 3 | Fraud 1% đoán toàn 0 được 99% tỉ lệ đoán đúng: báo cáo recall/precision/F1 lớp gian lận vs `DummyClassifier` |
| `mock2-q20` | output | 2 | Tính precision, recall, F1 bằng Python thuần từ `TP=18, FP=6, FN=2`, in làm tròn |
| `mock2-q21` | mcq | 2 | Vì sao dùng `StratifiedKFold` thay `KFold` khi lớp dương hiếm (5/100) |
| `mock2-q22` | mcq | 3 | Bug leakage `StandardScaler().fit_transform(X)` trước `cross_val_score` → lạc quan; sửa bằng `make_pipeline` |
| `mock2-q23` | mcq | 2 | Bảng `max_depth` 1..6 (`train_f1`, `val_f1`): chọn `max_depth=3` theo validation |
| `mock2-q24` | parsons | 3 | Quy trình trung thực: `train_test_split(stratify=y)` → CV F1 trên train → fit train → chấm F1 trên test một lần |

### Sửa theo Feedback vòng 1 (vòng 2)
- `mock2-q13`: Bỏ tên hàm `np.linalg.norm` khỏi prompt EN/VI, thay bằng mô tả "the NumPy function that returns a vector's length" / "hàm NumPy trả về độ dài của vector"; giữ nguyên code và `answer`.
- `mock2-q17`: Viết lại prompt EN/VI để hỏi chỉ số cột chứa xác suất ticket khẩn cấp (nhãn `1`) kèm giải thích `predict_proba` trả về mỗi lớp một cột theo thứ tự `model.classes_`; giữ nguyên code và `answer`.
- `mock2-q24`: Đổi dòng test sang đo cùng thước đo F1 (`metrics.f1_score(y_te, linear_model.LogisticRegression().fit(X_tr, y_tr).predict(X_te))`, thêm `metrics` vào dòng import), chỉnh `random_state=2` ở `make_classification` để điểm test thực tế (`0.889` thay vì `1.0`), cập nhật prompt và explanation EN/VI thành "F1 on `X_te`", giữ đúng một thứ tự in `cv` trước `test` sau.
  - Output mới của `mock2-q24` khi chạy với `-W error`:
    ```text
    cv 0.903
    test 0.889
    ```

### Bảng MCQ (`id -> answer`, độ dài EN 4 lựa chọn, tỉ lệ max/min)

| id | answer | độ dài EN 4 lựa chọn (ký tự) | tỉ lệ max/min |
|---|---|---|---|
| `mock2-q02` | `1` | `[52, 52, 52, 57]` | `1.10` |
| `mock2-q08` | `2` | `[78, 83, 71, 76]` | `1.17` |
| `mock2-q09` | `0` | `[44, 47, 47, 44]` | `1.07` |
| `mock2-q15` | `3` | `[65, 64, 65, 60]` | `1.08` |
| `mock2-q19` | `1` | `[56, 68, 58, 56]` | `1.21` |
| `mock2-q21` | `0` | `[56, 58, 56, 58]` | `1.04` |
| `mock2-q22` | `2` | `[65, 66, 69, 69]` | `1.06` |
| `mock2-q23` | `3` | `[57, 58, 56, 55]` | `1.05` |

Phân bố `answer`: `0` (2 câu), `1` (2 câu), `2` (2 câu), `3` (2 câu). Tất cả tỉ lệ dài/ngắn ≤ `1.21` (đạt ngưỡng ≤ `1.3`).

## 2. File đã sửa / tạo
- Tạo mới: `curriculum/exams/mock-data-ml.yaml`
- Tạo mới: `tasks/m3-mock-data-ml.report.md` (báo cáo theo yêu cầu)
- Không chỉnh sửa bất kỳ file nào khác trong repo (chỉ chạy `build_content.py` sinh output vào `apps/web/src/generated` vốn gitignored).

## 3. Kết quả lệnh kiểm tra (sau khi sửa Feedback vòng 1)
- Chạy lại `mock2-q24` trực tiếp với `uv run python -W error`:
  - Exit code `0`, không warning, output:
    ```text
    cv 0.903
    test 0.889
    ```
- (Từ vòng 1, 15/16 câu `output`/`fill`/`parsons` khác giữ nguyên code và đã chạy sạch với `-W error`, riêng `mock2-q10` sạch khi lọc 2 `PyparsingDeprecationWarning` nội bộ lúc `import matplotlib.pyplot` trong `.venv`.)
- `uv run python tools/validate.py`:
  - Exit code `0`: `OK: 0 error(s), 0 warning(s). Checked 35 lessons, 272 markdown pairs, 103 examples, 70 exercises, 64 alternatives, 702 questions, 8 exams, 1 portfolio, 1 glossary, 1 interview.`
- `uv run python -m pytest curriculum`:
  - Exit code `0`: `652 passed, 14 warnings in 2.38s` (14 warning đều là `PyparsingDeprecationWarning` từ `matplotlib._fontconfig_pattern` / `matplotlib._mathtext` trong `.venv`).
- `uv run python tools/build_content.py`:
  - Exit code `0`: `Built 35 lessons, 8 exams, 210 flashcards, 563 questions -> apps\web\src\generated`.
- Kiểm tra regex từ khóa cấm (`astype\(int\)|dtype=int\b|\.info\(|fetch_|load_|plt\.show|JOIN|merge\(|độ chính xác|độ phủ`) trên `curriculum/exams/mock-data-ml.yaml`:
  - `Matches: []` (rỗng, 0 vi phạm).
- `git status --short`:
  - Chỉ có `?? .hallmark/`, `?? curriculum/exams/mock-data-ml.yaml`, `?? tasks/` (chứa `tasks/m3-mock-data-ml.md` và `tasks/m3-mock-data-ml.report.md`).

## 4. Điều còn chưa chắc
- Môi trường chạy thực tế trên trình duyệt dùng Pyodide 32-bit (`numpy 2.2.5`, `pandas 2.3.3`, `sklearn 1.7.0`, `matplotlib 3.8.4`) và bản build web (`pnpm --filter web build`) chưa được chạy trực tiếp trong phiên này (spec yêu cầu không chạy `pnpm --filter web build`); kết quả trên Pyodide 32-bit được suy ra là tương thích vì không dùng `dtype=int`/`astype(int)` hay scalar NumPy khi in, và không dùng API matplotlib > 3.8.
- Do không có lệnh `grep` dạng POSIX sẵn hay cần chạy Python regex trên PowerShell, phép kiểm tra regex từ cấm được thực hiện bằng Python `re.compile` với cùng pattern trong spec (cho kết quả 0 khớp).
