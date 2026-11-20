# Báo cáo: m3-p5-04-evaluation

## 1. Đã làm gì

Đã viết hoàn chỉnh bài `p5-04-evaluation` ("Evaluating models" / "Đánh giá mô hình") trong `curriculum/phase-05-ml/p5-04-evaluation/` và bổ sung các thuật ngữ đánh giá mô hình vào `curriculum/glossary.yaml` theo đúng spec `tasks/m3-p5-04-evaluation.md` và `docs/CONTENT_GUIDE.md`:

- **Metadata (`meta.yaml`)**: `id: p5-04-evaluation`, `phase: p5`, `order: 4`, `tags: [model-evaluation, sklearn, evaluation]`, `prerequisites: [p5-03-sklearn]`, `duration_min: 14`, `review_by: "2027-11-01"`, `outcomes` khớp syllabus (+2 dòng về ngưỡng quyết định và so sánh với baseline), `further_reading` gồm 3 link chính thức của scikit-learn và Google ML Crash Course.
- **Bài học song ngữ (`lesson.en.md`, `lesson.vi.md`)**:
  - Opening với tình huống ticket 85% bình thường / 15% khẩn cấp.
  - §1 Bẫy accuracy khi dữ liệu lệch lớp: `DummyClassifier(strategy="most_frequent")` vs `LogisticRegression` pipeline trên bộ dữ liệu chính (`0.85` vs `0.883`).
  - §2 Confusion matrix: sơ đồ text bố cục `[[TN, FP], [FN, TP]]`, đếm tay bằng NumPy boolean mask đối chiếu `confusion_matrix(...).tolist()` (`[[51, 0], [7, 2]]`), bảng thuật ngữ.
  - §3 Precision, recall và F1: công thức bằng lời và code, `precision_score` / `recall_score` / `f1_score`, `zero_division=0` cho baseline, trace table (`1.0`, `0.222`, `0.364`) và bảng so sánh tình huống.
  - §4 Đọc `classification_report(..., digits=3)`: giữ nguyên fence `text` output (kèm dòng trống), giải thích từng cột và `macro avg` / `weighted avg`.
  - §5 Ngưỡng quyết định & `predict_proba`: vòng lặp `for t in [0.5, 0.3, 0.1]` kèm lời mời bấm **Visualize**, bảng ngưỡng/precision/recall.
  - §6 Cross-validation: picture in text 5 fold, Mermaid `flowchart LR` (6 node, cùng số dòng EN/VI), `cross_val_score` 5-fold (`0.895 +/- 0.037`), `StratifiedKFold(n_splits=5, shuffle=True, random_state=0)` với `scoring="f1"` so `LogisticRegression` (`0.597 +/- 0.098`) và `DecisionTreeClassifier` (`0.77 +/- 0.066`), callout `[!TIP]` đặt `StandardScaler()` bên trong pipeline.
  - §7 Lỗi thường gặp (4 lỗi chạy thật): chỉ nhìn accuracy khi lệch 95/5, đảo `(y_pred, y_true)` trong `confusion_matrix`, scale toàn bộ `X` trước CV (ghi nhận trung thực kết quả đo `0.895` vs `0.895` trên tập giả lập nhỏ nhưng quy trình vẫn rò rỉ), và bỏ `std` / nhặt fold cao nhất.
  - §8 Recap / Tóm tắt.
- **3 Examples** (`01_ticket_metrics`, `02_threshold_tradeoff`, `03_cross_validation`), mỗi bài đủ `.py`, `.out`, `.en.md`, `.vi.md`.
- **2 Exercises**:
  - `ex01-confusion-counts` (`kind: fill`): điền khuyết đếm 4 ô trả về `dict[str, int]` Python thuần; 6 test đối chiếu `confusion_matrix(...).ravel().tolist()`, kiểu `int`, tổng bằng `len(y_true)`, toàn 0/toàn 1, không sửa đầu vào; 3 tầng hint EN/VI.
  - `ex02-threshold-metrics` (`kind: code`): tự cài đặt `precision_recall_f1` (không dùng `sklearn.metrics` trong `solution.py`, xử lý mẫu số 0, làm tròn 3 ở bước trả về) và `threshold_for_recall` (chọn ngưỡng lớn nhất đạt `min_recall` hoặc `None`); 6 test đối chiếu `sklearn.metrics` với `zero_division=0`, mẫu số 0, `thresholds` không theo thứ tự, `None`, không sửa đầu vào; `alternatives/01_sklearn_metrics.py` + `.en.md` / `.vi.md`; 3 tầng hint EN/VI.
- **Quiz (`quiz.yaml`)**: 16 câu hỏi (`7 mcq`, `4 output`, `3 fill`, `2 parsons`; độ khó `5` dễ / `8` vừa / `3` khó; tag `model-evaluation` và `sklearn`) + 6 flashcards (`p5-04-f01`..`p5-04-f06`).
- **Glossary (`curriculum/glossary.yaml`)**: thêm 13 mục thuật ngữ mới (`baseline`, `imbalanced data`, `confusion matrix`, `true positive`, `false positive`, `true negative`, `false negative`, `precision`, `recall`, `F1 score`, `decision threshold`, `cross-validation`, `fold`).

## 2. File đã sửa / tạo

- Tạo mới `curriculum/phase-05-ml/p5-04-evaluation/`:
  - `meta.yaml`, `lesson.en.md`, `lesson.vi.md`, `quiz.yaml`
  - `examples/01_ticket_metrics.{py,out,en.md,vi.md}`
  - `examples/02_threshold_tradeoff.{py,out,en.md,vi.md}`
  - `examples/03_cross_validation.{py,out,en.md,vi.md}`
  - `exercises/ex01-confusion-counts/{exercise.yaml,prompt.en.md,prompt.vi.md,starter.py,solution.py,test_exercise.py}`
  - `exercises/ex02-threshold-metrics/{exercise.yaml,prompt.en.md,prompt.vi.md,starter.py,solution.py,test_exercise.py}`
  - `exercises/ex02-threshold-metrics/alternatives/01_sklearn_metrics.{py,en.md,vi.md}`
- Chỉnh sửa: `curriculum/glossary.yaml` (chỉ thêm 13 thuật ngữ mới).
- Tạo báo cáo: `tasks/m3-p5-04-evaluation.report.md`.
- Chạy `tools/build_content.py` sinh JSON vào thư mục gitignored `apps/web/src/generated/`.

## 3. Kết quả lệnh kiểm tra

| Lệnh | Kết quả | Ghi chú |
|---|---|---|
| `uv run python tools/validate.py --path curriculum/phase-05-ml/p5-04-evaluation` | Exit `0` — `OK: 0 error(s), 0 warning(s)` | Checked 1 lesson, 7 markdown pairs, 3 examples, 2 exercises, 1 alternative, 16 questions |
| `uv run python tools/validate.py` | Exit `0` — `OK: 0 error(s), 0 warning(s)` | Checked 34 lessons, 264 markdown pairs, 100 examples, 68 exercises, 62 alternatives, 644 questions, 6 exams, 1 portfolio, 1 glossary, 1 interview |
| `uv run python -m pytest curriculum/phase-05-ml -W error::UserWarning -W error::FutureWarning` | Exit `0` — `49 passed in 1.18s` | Không warning nào |
| `uv run ruff check curriculum/phase-05-ml` | Exit `0` — `All checks passed!` | Sạch lint |
| Grep rule check (`astype(int)`, `dtype=int`, `.info(`, `fetch_`, `np.random.seed/rand`, `import random`) | `0` kết quả | Sạch |
| Chạy từng khối Python trong `lesson.en.md` và `lesson.vi.md` với `-W error::UserWarning` | `10/10` khối mỗi bản exit `0`, `stderr=''` | Output khớp comment trong bài |
| Chạy 3 example bằng `uv run python -W error::UserWarning` | `3/3` exit `0`, `stderr=''` | Output khớp các file `.out` |
| Kiểm tra import `starter.py` và `tracer.py` trên khối Visualize | Import sạch cả 2 bài tập; `tracer` trả `error: None` (`31` bước) | |
| `uv run python tools/build_content.py` | Exit `0` — `Built 34 lessons, 6 exams, 204 flashcards, 547 questions -> apps\web\src\generated` | Không chạy `pnpm --filter web build` theo spec |
| `git status --short` | Chỉ có `curriculum/glossary.yaml`, `curriculum/phase-05-ml/p5-04-evaluation/`, `tasks/` (cùng `.hallmark/` có sẵn trước) | Không sửa file cấm |

## 4. Điều còn chưa chắc

- **Môi trường trình duyệt / Pyodide wasm32 thực tế**: Không mở trình duyệt để chạy app web trực tiếp; tuy nhiên `tools/validate.py` đã chạy bộ `tools/pyrunner/runner.py` và `tools/pyrunner/tracer.py` giống hệt app, và toàn bộ code đã tránh các khác biệt 32-bit đã biết (`"int64"` tường minh, không in `dtype` số nguyên, không in scalar NumPy trong list/tuple/dict).
