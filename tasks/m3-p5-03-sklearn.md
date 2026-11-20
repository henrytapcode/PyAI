# M3 bước 11: bài p5-03 scikit-learn workflow

## Mục tiêu
Viết bài `p5-03-sklearn` trong `curriculum/phase-05-ml/`, đúng `docs/CONTENT_GUIDE.md`, song ngữ EN/VI.
Người học đã xong phase 1–4, `p5-01-math-bridge` (MSE, gradient descent) và `p5-02-supervised` (feature/label, train/test split tự viết bằng `rng.permutation`, ngưỡng, accuracy, overfitting, data leakage khi scale). Bài này cho thấy **scikit-learn làm chính những việc đó với một API chung**: `fit` / `predict` / `score`, `train_test_split`, scaler, `Pipeline`, và so sánh hai mô hình công bằng.
Bài mẫu: `curriculum/phase-05-ml/p5-02-supervised/` (vừa duyệt) và `p5-01-math-bridge/`.

Boss đã đo (2026-11-13), scikit-learn 1.7.0, scipy 1.14.1 (local đã ghim cho khớp app): `train_test_split(random_state=...)`, `stratify`, `LogisticRegression`, `DecisionTreeClassifier(random_state=0)`, `KNeighborsClassifier`, `LinearRegression`, `StandardScaler`, `make_pipeline`, `load_iris`, `make_classification(random_state=0)` cho kết quả **giống hệt** giữa local và app (score, `predict(...).tolist()`, `coef_` làm tròn 3).

## File được phép sửa/tạo
- Thư mục mới `curriculum/phase-05-ml/p5-03-sklearn/` và mọi file bên trong.
- `curriculum/glossary.yaml`: chỉ **thêm** thuật ngữ mới (estimator, fit, predict, score, pipeline, feature scaling / StandardScaler, hyperparameter, random_state, stratify; bỏ qua cái đã có).

## Không được đụng
- `apps/`, `tools/`, `pyproject.toml`, `uv.lock`, `curriculum/syllabus.yaml`, `curriculum/topics.yaml`, các bài khác, `exams/`.
- Không xóa file, không `git commit`, **không chạy `pnpm --filter web build`**.

## Quy tắc output (bắt buộc; xem đầu `tasks/M3-PLAN.md`)
- Pyodide 32-bit: không in `dtype` của mảng NumPy số nguyên, không `astype(int)`/`dtype=int` (dùng `"int64"`), không `df.info()`. Không in list/dict chứa numpy scalar: kết quả `predict` in bằng `.tolist()`, hệ số bằng `np.round(m.coef_, 3).tolist()` hoặc `round(float(x), 3)`.
- `model.score(...)` trả `float` Python; vẫn **làm tròn** khi in (`round(..., 3)`).
- Ngẫu nhiên: `train_test_split(..., random_state=<số>)`, `DecisionTreeClassifier(random_state=0)`, dữ liệu tự sinh bằng `np.random.default_rng(seed)` hoặc `make_classification(random_state=...)`. Không `np.random.seed`, `np.random.rand`, module `random`.
- Dữ liệu: tự tạo, hoặc `load_iris` (có sẵn trong gói, không cần mạng). **Không** `fetch_*` / `fetch_openml` (cần mạng).
- **Không có warning nào** khi chạy (stderr phải sạch): `LogisticRegression` dùng `max_iter=1000` khi dữ liệu chưa scale; không truyền DataFrame lúc fit rồi mảng lúc predict (sinh warning "feature names"), chọn một kiểu và giữ nguyên.
- Lỗi minh họa (vd predict trước fit, X 1 chiều): bắt bằng `try/except` và in `type(e).__name__` (không in nguyên message dài).
- Mọi số thực in ra phải làm tròn. DataFrame in ra ≤ 4 cột, dòng < 60 ký tự.
- matplotlib (nếu dùng): example in thêm dòng tóm tắt; lesson ghi `# (shows ...)` / `# (hiện ...)` sau `plt.show()`; tự chạy ngoài validator thì đặt `MPLBACKEND=Agg`.
- Mọi `print(...)  # ...` trong lesson phải khớp output thật.
- Mỗi API sklearn mới phải được giới thiệu một câu ở lần dùng đầu (import từ đâu, làm gì).

## Nội dung bài (boss chốt dàn ý, worker viết)
Opening (không heading): ở p5-02 bạn tự viết chia train/test, tự chọn ngưỡng, tự tính accuracy. scikit-learn làm sẵn những việc đó, và **mọi mô hình dùng chung ba lệnh** `fit`, `predict`, `score`; đổi mô hình chỉ cần đổi một dòng. Đây là thư viện ML cổ điển mà team AI dùng hằng ngày (baseline trước khi gọi LLM, phân loại ticket, dự đoán độ trễ).

1. **Estimator: fit, predict, score**. Một mô hình là một object; `fit(X_train, y_train)` học, `predict(X_new)` đoán, `score(X, y)` chấm (classifier: accuracy; regressor: R², chỉ nói một câu "1.0 là khớp hoàn hảo"). **Picture in text** (fence `text`): vòng đời `LogisticRegression()` → `.fit` → `.predict` → `.score`. Bảng `| method | input | returns |`. Ví dụ nhỏ với dữ liệu ticket tự tạo (6–10 dòng, 2 feature).
2. **`train_test_split`**: thay cho `split_data` tự viết ở p5-02; `test_size`, `random_state`; `stratify=y` giữ tỉ lệ lớp (in đếm lớp của test bằng `np.bincount(...).tolist()` có và không có stratify). Nối lại lỗi "không xáo khi dữ liệu đã sắp xếp" của p5-02: `train_test_split` xáo sẵn.
3. **Ba mô hình, một API**: `LogisticRegression` (tên có "Regression" nhưng là classifier, nói rõ), `KNeighborsClassifier` (k hàng xóm gần nhất bỏ phiếu), `DecisionTreeClassifier` (chuỗi câu hỏi if/else). Vòng `for` fit cả ba trên cùng một split, in train/test score. **Bảng so sánh** `| model | idea in one line | key hyperparameter |`. Thêm `LinearRegression` cho regression: in `coef_`, `intercept_` (làm tròn), nối với đường thẳng học bằng gradient descent ở p5-01.
4. **Scale feature**: KNN dựa vào khoảng cách nên feature có thang đo lớn (vd `tokens` hàng nghìn so với `error_rate` 0–1) lấn át. `StandardScaler`: `fit` trên train, `transform` cả train và test (nối với data leakage p5-02). Dữ liệu phải được chọn sao cho **in ra thấy rõ** KNN có scale tốt hơn không scale trên test (worker tự sinh bằng `default_rng`, kiểm tra con số trước khi viết lời).
5. **Pipeline**: `make_pipeline(StandardScaler(), KNeighborsClassifier(...))`; một `fit` làm cả scale lẫn học, `predict`/`score` tự scale dữ liệu mới bằng thông số của train, nên không thể leak nhầm. In `list(pipe.named_steps)`. **Mermaid** `flowchart LR` (≤ 7 node): X_train → StandardScaler fit+transform → model fit; X_test → StandardScaler transform → model predict → score. Đây là section mời bấm **Visualize** (khối nhỏ: tạo pipeline, fit, score, dữ liệu 8–12 dòng; theo dõi biến `pipe`, `acc`).
6. **So sánh hai mô hình công bằng**: cùng split (cùng `random_state`), cùng tiền xử lý (cả hai trong pipeline), chỉ chấm trên test, chọn theo test score. Bảng `| fair | unfair |` (cùng split vs mỗi mô hình một split; scale trong pipeline vs scale toàn bộ dữ liệu trước; chọn theo test vs chọn theo train). Ví dụ chạy thật: so `LogisticRegression` vs `DecisionTreeClassifier(max_depth=...)` trên `load_iris` hoặc dữ liệu tự sinh, in bảng kết quả. Callout `[!NOTE]`: một lần chia còn may rủi; p5-04 học cross-validation để so chắc hơn.
7. **Lỗi thường gặp** (3–4, chạy thật):
   - `predict` trước `fit` → `NotFittedError` (in tên lỗi; sửa: gọi `fit` trước).
   - X một chiều `[1, 2, 3]` → `ValueError` (sklearn cần 2D: mỗi hàng một ví dụ); sửa bằng `.reshape(-1, 1)` hoặc `X[["col"]]`.
   - `fit_transform` trên test (scaler học lại từ test) → in hai kết quả khác nhau; sửa: chỉ `transform`, hoặc dùng pipeline.
   - Chọn mô hình theo train score (cây sâu được 1.0 trên train) → in train vs test.
8. **Recap / Tóm tắt**.

Thời lượng 12–15 phút. `review_by: "2027-11-01"`. `further_reading` (URL chính thức scikit-learn.org): "Getting Started", "Pipelines and composite estimators", "Common pitfalls and recommended practices".

## Examples (3)
- `01_ticket_classifier`: 20–30 ticket tự sinh (2 feature số, label 0/1), `train_test_split` có `stratify`, fit `LogisticRegression`, in test accuracy và dự đoán cho 3 ticket mới (`.tolist()`).
- `02_scaling_pipeline`: cùng một dữ liệu có hai feature lệch thang đo; KNN không scale vs `make_pipeline(StandardScaler(), KNN)`; in hai test score.
- `03_compare_models`: `load_iris`, một split cố định, 3 pipeline (LogisticRegression, KNN, DecisionTree), in bảng tên mô hình + train/test score (DataFrame ≤ 4 cột hoặc f-string), in mô hình tốt nhất theo test.

## Exercises (2)
- `ex01-fit-pipeline` (`kind: fill`): `train_and_score(X: np.ndarray, y: np.ndarray, seed: int) -> float`: `train_test_split(X, y, test_size=0.25, random_state=seed, stratify=y)`, `pipe = make_pipeline(StandardScaler(), LogisticRegression())`, fit trên train, trả `round(pipe.score(X_test, y_test), 3)` (`float` Python). Các ô `___` trong thân hàm (vd tên hàm chia, bước scale, lệnh fit, dữ liệu đưa vào score). Test: kiểu `float`, giá trị đúng với một dữ liệu cố định (tính sẵn, ghi số trong test), cùng seed → cùng kết quả, khác seed vẫn trong `[0, 1]`, không sửa mảng đầu vào.
- `ex02-compare-models` (`kind: code`): hai hàm
  - `compare_models(X: np.ndarray, y: np.ndarray, models: dict, seed: int) -> dict[str, float]`: **một** lần `train_test_split(X, y, test_size=0.3, random_state=seed, stratify=y)`, với mỗi `name, model` trong `models`: fit một **bản sao** (`sklearn.base.clone(model)`) trên train, ghi test accuracy làm tròn 3 (`float` Python). Không fit object người gọi truyền vào. Trả dict cùng thứ tự key với `models`.
  - `best_model(scores: dict[str, float]) -> str`: tên có score cao nhất; hòa thì tên xếp trước theo thứ tự chữ cái; dict rỗng → `ValueError`.
  5–6 test (giá trị đúng trên một dữ liệu cố định, kiểu trả về, mọi mô hình dùng cùng split (vd hai pipeline giống nhau ra cùng score), object truyền vào vẫn chưa fit (`pytest.raises(NotFittedError)` khi gọi `predict`), hòa, rỗng). Có `alternatives/01_dict_comprehension.py` (dict comprehension + hàm phụ `_test_score`, `best_model` bằng `min(..., key=lambda kv: (-kv[1], kv[0]))` hoặc tương đương) + `.md` so sánh.
- Starter import sạch (người học thấy từng test đỏ/xanh). Hint 3 là khung có 2–3 dòng thật sự để trống (`...`), **không** để lộ lời giải.

## Quiz
15–18 câu, mỗi loại `mcq`/`output`/`fill`/`parsons` ít nhất 2; khoảng 5 dễ, 7 vừa, 3 khó. 6 flashcard. Tag: `sklearn` (chính), có thể thêm `supervised-learning`. Câu `output` phải chạy nhanh (dữ liệu nhỏ, không `load_iris` trong mỗi câu) và không sinh warning. Đáp án mcq không phụ thuộc vị trí (app xáo lựa chọn theo id). Không lặp câu của p5-01, p5-02.

## Tiêu chí hoàn thành (checklist)
1. [ ] Đủ file theo layout CONTENT_GUIDE; `meta.yaml` có `phase: p5`, `order: 3`, `tags` gồm `sklearn`, `prerequisites: [p5-02-supervised]`, `outcomes` khớp syllabus (có thể thêm 1–2 dòng).
2. [ ] Lesson đúng dàn ý, đủ: mermaid, picture in text, các bảng so sánh, một lời mời Visualize, callout.
3. [ ] Code giữa `lesson.en.md` và `lesson.vi.md` giống hệt (trừ comment); số dòng mermaid bằng nhau; fence `text` giống hệt.
4. [ ] Tuân thủ "Quy tắc output" (kể cả không warning).
5. [ ] Exercise: starter fail, solution và alternative pass (pytest **và** browser runner); hint đủ 3 tầng; hint 3 không lộ lời giải.
6. [ ] Bản VI tự nhiên, xưng "bạn", thuật ngữ giữ tiếng Anh kèm giải nghĩa lần đầu.
7. [ ] Lệnh kiểm tra xanh, chạy đúng như ghi.
8. [ ] Chạy `uv run python tools/build_content.py`. Không có trình duyệt thì ghi rõ trong report.

## Lệnh kiểm tra
Từ gốc repo `D:\Proj\python-ai-platform`:
```
uv run python tools/validate.py --path curriculum/phase-05-ml/p5-03-sklearn
uv run python tools/validate.py
uv run python -m pytest curriculum/phase-05-ml -W error::UserWarning -W error::FutureWarning
uv run ruff check curriculum/phase-05-ml
grep -rnE "astype\(int\)|dtype=int\b|\.info\(|fetch_|np\.random\.(seed|rand)|^import random" curriculum/phase-05-ml/p5-03-sklearn
git status --short
```
Mong đợi: validate 0 lỗi; pytest exit 0 (kể cả khi warning bị coi là lỗi); ruff sạch; grep rỗng; file mới chỉ trong `p5-03-sklearn/` (và `glossary.yaml`).
Thêm: chạy từng example bằng `uv run python <file>` và xác nhận stderr rỗng.

## Ghi chú cho worker
- Đọc `docs/CONTENT_GUIDE.md`, `curriculum/phase-05-ml/p5-02-supervised/` (giọng văn, cấu trúc, ex01 `split_data`, ví dụ leakage).
- Test chỉ dùng: assert, pytest.raises, pytest.approx, pytest.mark.parametrize, `@pytest.fixture` định nghĩa trong file test. Test được import từ sklearn (`NotFittedError`, các model).
- Dùng `uv run python -m pytest`, không dùng `uv run pytest`.
- Con số trong test và comment lesson: chạy thật rồi mới ghi, đừng đoán.

## Trạng thái
- Bước hiện tại: 5 (đạt sau vòng 3; boss kiểm trong app: Visualize pipeline khớp số, ex02 6/6; chờ user duyệt commit)
- Vòng: 3/3
- Số lần swap: 0
- Fallback: không
- Model: Gemini 4 Hydrogen (High)

## Feedback vòng 1
Boss đã chạy lại: validate 0 lỗi, pytest 614 passed, ruff sạch, grep rỗng; 11 khối code lesson khớp comment, stderr sạch. Chỉ còn 2 việc:
1. **Hint 2 lộ lời giải** (CONTENT_GUIDE: hint 2 là kế hoạch bằng lời, hint 3 mới là khung code có chỗ trống).
   - `exercises/ex01-fit-pipeline/exercise.yaml` hint 2 (EN + VI): bốn bước đang là đúng 4 dòng lời giải (`train_test_split(X, y, test_size=0.25, ...)`, `make_pipeline(StandardScaler(), LogisticRegression())`, `pipe.fit(X_train, y_train)`, `round(float(pipe.score(X_test, y_test)), 3)`). Viết lại bằng lời: chia dữ liệu bằng hàm ở §2 với stratify, tạo pipeline gồm bước chuẩn hóa rồi mô hình, huấn luyện trên phần train, chấm trên phần test. Không ghi tên hàm/lớp là đáp án của ô trống.
   - `exercises/ex02-compare-models/exercise.yaml` hint 2 (EN + VI): bước 2 đang viết sẵn cả thân vòng lặp (`fitted = clone(model)`, fit, `round(float(fitted.score(...)), 3)`), bước 4 viết sẵn điều kiện hòa `name < best_name`, trong khi hint 3 để trống đúng những chỗ đó. Viết lại bằng lời (vd "nhân bản mô hình bằng hàm ở §… / ghi chú đề", "khi điểm bằng nhau, giữ tên đứng trước theo thứ tự chữ cái"); giữ hint 3 như hiện tại.
2. **Lỗi thường gặp 3** (`lesson.en.md` + `lesson.vi.md`, khối `fit_transform`): đang in cách đúng trước rồi mới in cách sai. Đổi thứ tự như các lỗi khác: phần sai (`# Wrong: ...`, `fit_transform` trên test) trước, rồi `# Fix: ...` (`transform`). Cập nhật comment output cho khớp, code EN/VI vẫn giống hệt.
Chạy lại toàn bộ "Lệnh kiểm tra" và `uv run python tools/build_content.py`, cập nhật report.

## Feedback vòng 2
Vòng 1 đã sửa đúng; boss chạy lại cổng xanh (validate 0 lỗi, pytest 614, build 53 trang), Visualize pipeline và ex02 6/6 trong app. Còn đúng một lỗi:
- `exercises/ex02-compare-models/starter.py` và `solution.py` dòng 14, docstring `Example: compare_models(X, y, {"knn": KNeighborsClassifier()}, seed=42) -> {"knn": 0.833}` **sai số**: boss chạy với dữ liệu của test (`make_classification(n_samples=60, n_features=4, n_informative=3, n_redundant=0, random_state=0)`) và `KNeighborsClassifier()` mặc định (k=5) ra `{'knn': 0.722}`. Sửa ví dụ cho đúng output thật, nên ghi rõ dữ liệu (vd dùng đúng mô hình như prompt: `make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=3))` → `0.833`, hoặc giữ `KNeighborsClassifier()` → `0.722`). Chạy thật để xác nhận số, giữ starter và solution cùng docstring. Không sửa gì khác.
Chạy lại pytest phase 5 + validate `--path`, cập nhật report.
