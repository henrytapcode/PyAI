# Báo cáo thực hiện `m3-p5-03-sklearn`

## 1. Đã làm gì

- Xây dựng hoàn chỉnh bài học `p5-03-sklearn` ("scikit-learn workflow" / "Quy trình scikit-learn") trong `curriculum/phase-05-ml/p5-03-sklearn/` theo đúng dàn ý trong `tasks/m3-p5-03-sklearn.md` và `docs/CONTENT_GUIDE.md`:
  - `meta.yaml`: `phase: p5`, `order: 3`, `duration_min: 14`, `tags: [sklearn, supervised-learning, ml]`, `prerequisites: [p5-02-supervised]`, `review_by: "2027-11-01"`, 5 outcome khớp `syllabus.yaml` và 3 link `further_reading` chính thức trên `scikit-learn.org`.
  - `lesson.en.md` và `lesson.vi.md`: giữ đồng bộ tuyệt đối về code block (chỉ khác comment `#`), số dòng Mermaid (7 node `flowchart LR`), picture-in-text (khối `text` vòng đời estimator), bảng so sánh, callout `[!NOTE]`, lời mời bấm **Visualize** ở §5 (`pipe`, `acc`), giới thiệu một câu cho mỗi API scikit-learn mới ở lần dùng đầu, 4 lỗi thường gặp có code chạy được (`NotFittedError`, mảng `X` 1D `ValueError`, `fit_transform` trên test, chọn theo train score), và recap.
  - 3 examples kèm `.out`, `.en.md`, `.vi.md`:
    - `01_ticket_classifier.py`: 24 ticket mô phỏng, `train_test_split(..., stratify=y, random_state=42)`, `LogisticRegression(max_iter=1000)`, in test accuracy (`0.833`) và dự đoán 3 ticket mới (`.tolist()`).
    - `02_scaling_pipeline.py`: dữ liệu lệch thang đo (`tokens` 200–4000 vs `error_rate` 0.0–0.45), so sánh KNN thô (`0.5`) với `make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=3))` (`1.0`).
    - `03_compare_models.py`: so sánh công bằng `LogisticRegression`, `KNeighborsClassifier`, `DecisionTreeClassifier` trong pipeline trên `load_iris` cùng một split (`DecisionTree` thắng `0.933` trên test).
  - 2 exercises (100% pass cho solution/alternative và fail cho starter cả trên browser runner lẫn pytest):
    - `ex01-fit-pipeline` (`kind: fill`): `train_and_score(X, y, seed)`, 5 test, 3 tầng hint.
    - `ex02-compare-models` (`kind: code`): `compare_models(X, y, models, seed)` dùng `sklearn.base.clone` và một lần split duy nhất + `best_model(scores)`, 6 test (kể cả kiểm tra `NotFittedError` trên object gốc, hòa theo chữ cái, dict rỗng), kèm `alternatives/01_dict_comprehension.py` (dùng `_test_score`, dict comprehension, `min(..., key=lambda kv: (-kv[1], kv[0]))`) và `.en.md`/`.vi.md`.
  - `quiz.yaml`: 16 câu hỏi (`6 mcq`, `4 output`, `3 fill`, `3 parsons`; độ khó: 5 mức 1, 7 mức 2, 4 mức 3) và 6 flashcard (`p5-03-f01`..`p5-03-f06`).
- Bổ sung 9 thuật ngữ mới vào `curriculum/glossary.yaml`: `estimator`, `fit`, `predict`, `score`, `pipeline`, `feature scaling / StandardScaler`, `hyperparameter`, `random_state`, `stratify`.
- **Cập nhật theo `## Feedback vòng 1`:**
  - `exercises/ex01-fit-pipeline/exercise.yaml`: viết lại hint 2 (EN + VI) thành kế hoạch bằng lời (chia train/test có `stratify` bằng hàm ở §2, tạo pipeline gồm bước chuẩn hóa rồi mô hình logistic, huấn luyện trên train, chấm trên test), không ghi tên hàm/lớp là đáp án của ô trống; giữ nguyên hint 3.
  - `exercises/ex02-compare-models/exercise.yaml`: viết lại hint 2 (EN + VI) thành kế hoạch bằng lời (chia 70/30 một lần, nhân bản mô hình bằng hàm sao chép ở đề bài, huấn luyện trên train và ghi điểm test làm tròn, kiểm tra rỗng ném `ValueError`, giữ tên đứng trước theo chữ cái khi hòa), không lộ thân vòng lặp hay điều kiện `name < best_name`; giữ nguyên hint 3.
  - `lesson.en.md` và `lesson.vi.md` (Lỗi thường gặp 3 — `fit_transform` trên `X_test`): đảo thứ tự phần sai (`# Wrong:` / `# Sai:`) lên trước để in `fit_transform: 0.5 [0, 1]`, sau đó mới đến `# Fix:` / `# Sửa:` (fit lại `scaler` trên `X_train` rồi gọi `scaler.transform(X_test)`) để in `transform:     1.0 [1, 1]`; giữ code EN/VI giống hệt nhau trừ comment.

- **Cập nhật theo `## Feedback vòng 2`:**
  - `exercises/ex02-compare-models/starter.py` và `exercises/ex02-compare-models/solution.py`: sửa docstring `Example` của `compare_models` (vốn ghi `KNeighborsClassifier()` ra `0.833` là sai số) để ghi rõ bộ dữ liệu `make_classification(n_samples=60, n_features=4, n_informative=3, n_redundant=0, random_state=0)` và dùng đúng pipeline `make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=3))` khớp với `prompt`/`test_exercise.py`, cho output thật `{'knn': 0.833}` (đã chạy xác nhận bằng Python trước khi sửa; đồng thời kiểm tra `KNeighborsClassifier()` thô ra `{'knn': 0.722}` đúng như feedback nêu). Giữ docstring của `starter.py` và `solution.py` giống hệt nhau và tuân thủ giới hạn độ dài dòng ≤ 100 ký tự của `ruff`.

## 2. File đã sửa / tạo

- **Sửa ở vòng 3 (theo `## Feedback vòng 2`):**
  - `curriculum/phase-05-ml/p5-03-sklearn/exercises/ex02-compare-models/starter.py`
  - `curriculum/phase-05-ml/p5-03-sklearn/exercises/ex02-compare-models/solution.py`
  - `tasks/m3-p5-03-sklearn.report.md`
- **Sửa ở vòng 2 (theo `## Feedback vòng 1`):**
  - `curriculum/phase-05-ml/p5-03-sklearn/exercises/ex01-fit-pipeline/exercise.yaml`
  - `curriculum/phase-05-ml/p5-03-sklearn/exercises/ex02-compare-models/exercise.yaml`
  - `curriculum/phase-05-ml/p5-03-sklearn/lesson.en.md`
  - `curriculum/phase-05-ml/p5-03-sklearn/lesson.vi.md`
  - `tasks/m3-p5-03-sklearn.report.md`
- **Toàn bộ file thuộc bước này:**
  - **Sửa:** `curriculum/glossary.yaml` (chỉ thêm 9 thuật ngữ mới).
  - **Tạo mới thư mục `curriculum/phase-05-ml/p5-03-sklearn/`:**
    - `meta.yaml`, `lesson.en.md`, `lesson.vi.md`, `quiz.yaml`
    - `examples/01_ticket_classifier.{py,out,en.md,vi.md}`
    - `examples/02_scaling_pipeline.{py,out,en.md,vi.md}`
    - `examples/03_compare_models.{py,out,en.md,vi.md}`
    - `exercises/ex01-fit-pipeline/{exercise.yaml,prompt.en.md,prompt.vi.md,starter.py,solution.py,test_exercise.py}`
    - `exercises/ex02-compare-models/{exercise.yaml,prompt.en.md,prompt.vi.md,starter.py,solution.py,test_exercise.py}`
    - `exercises/ex02-compare-models/alternatives/01_dict_comprehension.{py,en.md,vi.md}`
  - **Generated (bởi `build_content.py`, gitignored):** `apps/web/src/generated`.
  - *(Lưu ý: `pyproject.toml`, `uv.lock`, `.hallmark/` đã có thay đổi sẵn trong workspace từ trước khi thực hiện bước này và không bị đụng tới.)*

## 3. Kết quả lệnh kiểm tra (chạy lại sau khi sửa theo Feedback vòng 2)

1. `uv run python tools/validate.py --path curriculum/phase-05-ml/p5-03-sklearn`
   - Kết quả: **PASS** — `OK: 0 error(s), 0 warning(s). Checked 1 lessons, 7 markdown pairs, 3 examples, 2 exercises, 1 alternatives, 16 questions.`
2. `uv run python tools/validate.py`
   - Kết quả: **PASS** — `OK: 0 error(s), 0 warning(s). Checked 33 lessons, 257 markdown pairs, 97 examples, 66 exercises, 61 alternatives, 628 questions, 6 exams, 1 portfolio, 1 glossary, 1 interview.`
3. `uv run python -m pytest curriculum/phase-05-ml -W error::UserWarning -W error::FutureWarning`
   - Kết quả: **PASS** — `34 passed in 1.18s`.
4. `uv run ruff check curriculum/phase-05-ml`
   - Kết quả: **PASS** — `All checks passed!`.
5. Kiểm tra mẫu cấm (`astype(int)|dtype=int\b|\.info\(|fetch_|np\.random\.(seed|rand)|^import random`) trên `curriculum/phase-05-ml/p5-03-sklearn` (chạy bằng `re` trong Python do môi trường Windows không có `grep` trong PATH):
   - Kết quả: **PASS** — `HITS: []` (rỗng).
6. Chạy xác nhận docstring `ex02-compare-models` và từng file example:
   - `compare_models` với `make_classification(n_samples=60, n_features=4, n_informative=3, n_redundant=0, random_state=0)` và `seed=42`: `KNeighborsClassifier()` thô → `{'knn': 0.722}`; `make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=3))` → `{'knn': 0.833}` (`rc=0`).
   - `01_ticket_classifier.py`: `rc=0`, stdout `Test accuracy: 0.833` / `New ticket predictions: [0, 1, 0]`, stderr rỗng.
   - `02_scaling_pipeline.py`: `rc=0`, stdout `KNN without scaling: 0.5` / `Pipeline with StandardScaler: 1.0`, stderr rỗng.
   - `03_compare_models.py`: `rc=0`, stdout bảng `LogisticRegression` (`0.981` / `0.911`), `KNeighbors` (`0.981` / `0.911`), `DecisionTree` (`0.981` / `0.933`), `Best on test: DecisionTree (0.933)`, stderr rỗng.
7. `uv run python tools/build_content.py`
   - Kết quả: **PASS** — `Built 33 lessons, 6 exams, 198 flashcards, 531 questions -> apps\web\src\generated`.
8. `git status --short`:
   - `M curriculum/glossary.yaml`, `?? curriculum/phase-05-ml/p5-03-sklearn/`, `?? tasks/` (cùng các file sẵn có từ trước: `M pyproject.toml`, `M uv.lock`, `?? .hallmark/`).

## 4. Điều còn chưa chắc

- **Chưa chạy kiểm tra trên trình duyệt / Pyodide thật** (không mở web UI và không chạy `pnpm --filter web build` theo yêu cầu spec); hành vi chạy in-browser của lesson, Visualize, và Pyodide wasm32 được kiểm chứng gián tiếp qua `tools/validate.py` và các quy tắc chống khác biệt 32/64-bit.
- Lệnh `grep` trực tiếp trong PowerShell không chạy được do máy không cài `rg`/`grep`, đã kiểm tra thay bằng script Python dùng đúng biểu thức regex trên toàn bộ file trong `curriculum/phase-05-ml/p5-03-sklearn/`.
