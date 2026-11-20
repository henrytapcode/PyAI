# M3 bước 12: bài p5-04 Evaluating models

## Mục tiêu
Viết bài `p5-04-evaluation` trong `curriculum/phase-05-ml/`, đúng `docs/CONTENT_GUIDE.md`, song ngữ EN/VI.
Người học đã xong phase 1–4, `p5-01` (MSE), `p5-02` (accuracy tự viết, ngưỡng, train/test, overfitting) và `p5-03-sklearn` (`fit`/`predict`/`score`, `train_test_split` + `stratify`, `StandardScaler`, `make_pipeline`, so sánh hai mô hình trên một split; NOTE hẹn cross-validation ở bài này). Bài này dạy **đo cho đúng**: vì sao accuracy đánh lừa khi dữ liệu lệch lớp, confusion matrix, precision / recall / F1, đánh đổi theo ngưỡng, và cross-validation.
Bài mẫu: `curriculum/phase-05-ml/p5-03-sklearn/` (vừa duyệt) và `p5-02-supervised/`.

Boss đã đo (2026-11-14), scikit-learn 1.7.0, local và app cho kết quả **giống hệt**:
```
X, y = make_classification(n_samples=200, n_features=5, weights=[0.85], random_state=1)
Xa, Xb, ya, yb = train_test_split(X, y, test_size=0.3, random_state=0, stratify=y)
p = make_pipeline(StandardScaler(), LogisticRegression()).fit(Xa, ya)
confusion_matrix(yb, p.predict(Xb)).tolist()      -> [[51, 0], [7, 2]]
accuracy / precision / recall / f1 (round 3)      -> 0.883 1.0 0.222 0.364
ngưỡng 0.3 trên predict_proba[:, 1]               -> [[50, 1], [1, 8]], recall 0.889
cross_val_score(p, X, y, cv=5)                     -> [0.9, 0.9, 0.825, 0.925, 0.925], mean 0.895, std 0.037
StratifiedKFold(5, shuffle=True, random_state=0), DecisionTree(max_depth=3), scoring="f1" -> [0.8, 0.857, 0.727, 0.667, 0.8]
load_breast_cancer: (569, 30), bincount [212, 357]
classification_report(..., digits=3): chuỗi in ra giống hệt
```
Bộ dữ liệu trên là ví dụ rất tốt cho bài (accuracy 0.883 nhưng recall lớp hiếm chỉ 0.222; hạ ngưỡng lên recall 0.889). Worker **nên dùng lại** nó cho mạch chính.

## File được phép sửa/tạo
- Thư mục mới `curriculum/phase-05-ml/p5-04-evaluation/` và mọi file bên trong.
- `curriculum/glossary.yaml`: chỉ **thêm** thuật ngữ mới (confusion matrix, true/false positive/negative, precision, recall, F1 score, imbalanced data, decision threshold, cross-validation, fold, baseline; bỏ qua cái đã có).

## Không được đụng
- `apps/`, `tools/`, `pyproject.toml`, `uv.lock`, `curriculum/syllabus.yaml`, `curriculum/topics.yaml`, các bài khác, `exams/`.
- Không xóa file, không `git commit`, **không chạy `pnpm --filter web build`**.

## Quy tắc output (bắt buộc; xem đầu `tasks/M3-PLAN.md`)
- Pyodide 32-bit: không in `dtype` của mảng NumPy số nguyên, không `astype(int)`/`dtype=int` (dùng `"int64"`), không `df.info()`. Không in list/dict/tuple chứa numpy scalar: `confusion_matrix(...).tolist()`, `np.round(scores, 3).tolist()`, đếm bằng `int((...).sum())`, metric bằng `round(float(x), 3)`.
- Ngẫu nhiên: `random_state=<số>` cho `train_test_split`, `make_classification`, `StratifiedKFold(shuffle=True, ...)`, `DecisionTreeClassifier`; dữ liệu tự sinh bằng `np.random.default_rng(seed)`. Không `np.random.seed`, `np.random.rand`, module `random`.
- Dữ liệu: tự tạo, `make_classification`, `load_breast_cancer`, `load_iris` (có sẵn trong gói). **Không** `fetch_*`.
- **Không có warning nào** (stderr sạch). Đặc biệt `precision_score`/`f1_score` khi không có dự đoán dương sẽ sinh `UndefinedMetricWarning`: truyền `zero_division=0` ở những chỗ đó và giải thích một câu.
- Lỗi minh họa: `try/except`, in `type(e).__name__`.
- `classification_report(..., digits=3)` được in nguyên khối; trong lesson ghi output bằng các dòng comment `#` ngay dưới (giữ khoảng trắng như output thật) hoặc trong fence `text` ngay sau khối code (fence `text` phải giống hệt EN/VI). Các dòng trống trong report giữ nguyên.
- Mọi số thực in ra phải làm tròn. DataFrame in ra ≤ 4 cột, dòng < 60 ký tự.
- matplotlib (nếu dùng): example in thêm dòng tóm tắt; lesson ghi `# (shows ...)` / `# (hiện ...)` sau `plt.show()`; tự chạy ngoài validator thì `MPLBACKEND=Agg`.
- Mọi `print(...)  # ...` trong lesson phải khớp output thật.
- Mỗi API mới (`confusion_matrix`, `precision_score`, `recall_score`, `f1_score`, `classification_report`, `predict_proba`, `cross_val_score`, `StratifiedKFold`, `DummyClassifier` nếu dùng) giới thiệu một câu ở lần dùng đầu (import từ đâu, làm gì).

## Nội dung bài (boss chốt dàn ý, worker viết)
Opening (không heading): 85% ticket là bình thường, 15% khẩn cấp. Một "mô hình" luôn trả lời "bình thường" đạt accuracy 0.85 mà không bắt được ticket khẩn cấp nào. Đánh giá mô hình là chọn đúng con số cho đúng câu hỏi.

1. **Bẫy accuracy khi dữ liệu lệch lớp**: baseline luôn đoán lớp phổ biến (`np.zeros_like(y_test)` hoặc `DummyClassifier(strategy="most_frequent")`), in accuracy của baseline và của mô hình thật trên bộ dữ liệu boss đo (0.883 so với baseline ~0.85). Câu chốt: luôn so với baseline.
2. **Confusion matrix**: TP, FP, FN, TN bằng ví dụ ticket (khẩn cấp = positive). **Picture in text** (fence `text`): bố cục của `confusion_matrix(y_true, y_pred)` trong sklearn (hàng = thật, cột = đoán, `[[TN, FP], [FN, TP]]`). Đếm tay bằng NumPy boolean (`int(((y_true == 1) & (y_pred == 1)).sum())`) rồi đối chiếu `confusion_matrix(...).tolist()`. Bảng thuật ngữ `| cell | meaning | ticket example |`.
3. **Precision, recall, F1**: công thức bằng lời và bằng code (từ 4 ô), rồi `precision_score`/`recall_score`/`f1_score`. **Trace table** `| metric | formula | value |` trên bộ dữ liệu chính (precision 1.0, recall 0.222, F1 0.364). **Bảng so sánh** `| situation | care most about | why |` (lọc spam: precision; bắt ticket khẩn cấp / gian lận: recall; cần cân bằng: F1). Nhắc `zero_division=0`.
4. **Đọc `classification_report`**: in report `digits=3`, giải thích từng cột (precision, recall, f1-score, support) và hai dòng `macro avg` / `weighted avg` mỗi dòng một câu.
5. **Ngưỡng quyết định**: `predict_proba(X)[:, 1]` là xác suất lớp 1; `predict` dùng ngưỡng 0.5. Vòng `for t in [0.5, 0.3, 0.1]` in precision và recall (làm tròn 3) → **bảng** `| threshold | precision | recall |`. Nối với bộ phân loại theo ngưỡng ở p5-02. Đây là section mời bấm **Visualize** (khối nhỏ: vòng qua các ngưỡng, theo dõi `preds`, `recall`).
6. **Cross-validation**: một lần chia còn may rủi (nối NOTE p5-03). **Picture in text**: 5 fold, mỗi lượt một fold làm test (vd `[T][ ][ ][ ][ ]`, `[ ][T][ ][ ][ ]` ...). **Mermaid** `flowchart LR` (≤ 7 node): data → split into k folds → train on k-1 → score on 1 → repeat k times → mean ± std. `cross_val_score(pipe, X, y, cv=5)` in điểm từng fold, mean, std. `StratifiedKFold(n_splits=5, shuffle=True, random_state=0)` và `scoring="f1"`. So hai mô hình bằng mean CV (LogisticRegression pipeline vs DecisionTree). Callout `[!TIP]`: đặt scaler **trong** pipeline để mỗi fold tự fit scaler trên phần train của nó.
7. **Lỗi thường gặp** (3–4, chạy thật):
   - Chỉ nhìn accuracy trên dữ liệu lệch lớp (đã có ở §1 thì ở đây nhắc ngắn bằng ví dụ khác hoặc thay bằng lỗi khác).
   - Đảo thứ tự tham số `confusion_matrix(y_pred, y_true)` → ma trận bị chuyển vị, đọc nhầm FP/FN (in cả hai).
   - Scale toàn bộ X trước rồi mới `cross_val_score` (leakage) vs pipeline trong CV (in hai mean; nếu chênh lệch quá nhỏ không thấy được thì nói rõ là kết quả có thể trông giống nhau nhưng quy trình vẫn sai, đừng bịa số).
   - Báo cáo mean CV mà bỏ std / chọn mô hình theo một fold tốt nhất.
8. **Recap / Tóm tắt**.

Thời lượng 12–15 phút. `review_by: "2027-11-01"`. `further_reading` (URL chính thức): scikit-learn "Metrics and scoring: quantifying the quality of predictions", scikit-learn "Cross-validation: evaluating estimator performance", Google ML Crash Course "Classification: Accuracy, recall, precision, and related metrics".

## Examples (3)
- `01_ticket_metrics`: bộ dữ liệu lệch lớp (có thể là bộ boss đo), pipeline LogisticRegression, in baseline accuracy, confusion matrix (`.tolist()`), precision/recall/F1.
- `02_threshold_tradeoff`: cùng mô hình, thử 4–5 ngưỡng, in bảng ngưỡng / precision / recall / số ticket bị gắn khẩn cấp; chọn ngưỡng cao nhất đạt recall ≥ 0.8.
- `03_cross_validation`: `load_breast_cancer` (hoặc `make_classification`), 2–3 mô hình trong pipeline, `StratifiedKFold(5, shuffle=True, random_state=0)`, in mean ± std (làm tròn 3) từng mô hình và mô hình tốt nhất.

## Exercises (2)
- `ex01-confusion-counts` (`kind: fill`): `confusion_counts(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, int]` trả `{"tp": ..., "fp": ..., "fn": ..., "tn": ...}` bằng phép so sánh boolean NumPy, mọi giá trị là `int` Python. Các ô `___` trong thân hàm (vd điều kiện của từng ô, `int(...)`). Test: ví dụ cố định, kiểu `int` Python, tổng 4 ô = `len(y_true)`, khớp `confusion_matrix(...).ravel()` của sklearn (so bằng `.tolist()`), toàn 0 / toàn 1, không sửa đầu vào.
- `ex02-threshold-metrics` (`kind: code`): hai hàm
  - `precision_recall_f1(y_true: np.ndarray, y_pred: np.ndarray) -> tuple[float, float, float]`: tự tính từ 4 ô (không gọi `sklearn.metrics` trong lời giải chính), mỗi giá trị `float` Python làm tròn 3; mẫu số 0 → giá trị đó là `0.0` (F1 = 0.0 khi precision + recall = 0).
  - `threshold_for_recall(probs: np.ndarray, y_true: np.ndarray, thresholds: list[float], min_recall: float) -> float | None`: với mỗi ngưỡng `t` trong `thresholds` (đoán 1 khi `probs >= t`), trả ngưỡng **lớn nhất** có recall ≥ `min_recall`; không ngưỡng nào đạt → `None`.
  5–6 test (khớp `precision_score`/`recall_score`/`f1_score` của sklearn với `zero_division=0` trên vài trường hợp, kiểu trả về, mẫu số 0, chọn đúng ngưỡng lớn nhất, trả `None`, `thresholds` không theo thứ tự). Có `alternatives/01_sklearn_metrics.py` (dùng `precision_score`, `recall_score`, `f1_score` với `zero_division=0`) + `.md` so sánh (khi nào tự viết, khi nào dùng thư viện).
- Starter import sạch. Hint 2 là kế hoạch **bằng lời** (không viết sẵn biểu thức là đáp án); hint 3 là khung code có 2–3 dòng thật sự để trống (`...`), không lộ lời giải.
- Docstring ví dụ trong starter/solution: con số phải chạy thật mới ghi.

## Quiz
15–18 câu, mỗi loại `mcq`/`output`/`fill`/`parsons` ít nhất 2; khoảng 5 dễ, 7 vừa, 3 khó. 6 flashcard. Tag: `model-evaluation` (chính), có thể thêm `sklearn`. Câu `output` dùng dữ liệu nhỏ viết tay (không `load_*` trong câu hỏi), chạy nhanh, không warning. Có ít nhất 2 câu tính precision/recall từ một confusion matrix cho sẵn. Đáp án mcq không phụ thuộc vị trí. Không lặp câu của p5-01…p5-03.

## Tiêu chí hoàn thành (checklist)
1. [ ] Đủ file theo layout CONTENT_GUIDE; `meta.yaml` có `phase: p5`, `order: 4`, `tags` gồm `model-evaluation`, `prerequisites: [p5-03-sklearn]`, `outcomes` khớp syllabus (có thể thêm 1–2 dòng).
2. [ ] Lesson đúng dàn ý, đủ: mermaid, hai picture in text, trace table, bảng so sánh, một lời mời Visualize, callout.
3. [ ] Code giữa `lesson.en.md` và `lesson.vi.md` giống hệt (trừ comment); số dòng mermaid bằng nhau; fence `text` giống hệt.
4. [ ] Tuân thủ "Quy tắc output" (kể cả không warning).
5. [ ] Exercise: starter fail, solution và alternative pass (pytest **và** browser runner); hint đủ 3 tầng; hint 2 bằng lời, hint 3 không lộ lời giải.
6. [ ] Bản VI tự nhiên, xưng "bạn", thuật ngữ giữ tiếng Anh kèm giải nghĩa lần đầu.
7. [ ] Lệnh kiểm tra xanh, chạy đúng như ghi.
8. [ ] Chạy `uv run python tools/build_content.py`. Không có trình duyệt thì ghi rõ trong report.

## Lệnh kiểm tra
Từ gốc repo `D:\Proj\python-ai-platform`:
```
uv run python tools/validate.py --path curriculum/phase-05-ml/p5-04-evaluation
uv run python tools/validate.py
uv run python -m pytest curriculum/phase-05-ml -W error::UserWarning -W error::FutureWarning
uv run ruff check curriculum/phase-05-ml
grep -rnE "astype\(int\)|dtype=int\b|\.info\(|fetch_|np\.random\.(seed|rand)|^import random" curriculum/phase-05-ml/p5-04-evaluation
git status --short
```
Mong đợi: validate 0 lỗi; pytest exit 0 (warning bị coi là lỗi; `UndefinedMetricWarning` là `UserWarning`); ruff sạch; grep rỗng; file mới chỉ trong `p5-04-evaluation/` (và `glossary.yaml`).
Thêm: chạy từng example và từng khối python của lesson bằng `uv run python` với `-W error::UserWarning`, xác nhận stderr rỗng và output khớp comment.

## Ghi chú cho worker
- Đọc `docs/CONTENT_GUIDE.md`, `curriculum/phase-05-ml/p5-03-sklearn/` (giọng văn, cấu trúc, cách viết hint đã được duyệt).
- Test chỉ dùng: assert, pytest.raises, pytest.approx, pytest.mark.parametrize, `@pytest.fixture` định nghĩa trong file test. Test được import `sklearn.metrics` để đối chiếu.
- Dùng `uv run python -m pytest`, không dùng `uv run pytest`.
- Con số trong test, docstring và comment lesson: chạy thật rồi mới ghi, đừng đoán.

## Trạng thái
- Bước hiện tại: 5 (đạt sau vòng 1; boss kiểm trong app: Visualize ngưỡng khớp số, ex02 8/8; chờ user duyệt commit)
- Vòng: 1/3
- Số lần swap: 0
- Fallback: không
- Model: Gemini 4 Hydrogen (High)
