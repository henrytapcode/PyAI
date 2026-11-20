# Báo cáo: m3-p5-02-supervised

## 1. Đã làm gì

Đã tạo hoàn chỉnh bài `p5-02-supervised` trong `curriculum/phase-05-ml/p5-02-supervised/` theo đúng `tasks/m3-p5-02-supervised.md` và `docs/CONTENT_GUIDE.md`, song ngữ EN/VI, không dùng `import sklearn`:

- **`meta.yaml`**: `id: p5-02-supervised`, `phase: p5`, `order: 2`, `duration_min: 14`, `tags: [supervised-learning, ml, numpy]`, `prerequisites: [p5-01-math-bridge, p4-02-pandas]`, `outcomes` khớp `syllabus.yaml` (bổ sung thêm mục chọn ngưỡng phân loại và tránh data leakage), `review_by: "2027-11-01"`, và 3 mục `further_reading` (Google ML Crash Course: Training and test sets & Overfitting, scikit-learn User Guide: Cross-validation ghi chú học ở `p5-04`).
- **`lesson.en.md` / `lesson.vi.md`**:
  - Phần mở đầu không heading giới thiệu học có giám sát (học từ ví dụ có sẵn đáp án: ticket spam, request có độ trễ).
  - §1 Feature và label: `X`, `y`, picture in text (`text` fence giống hệt EN/VI), bảng thuật ngữ, ví dụ Pandas DataFrame 3 cột chuyển sang `.to_numpy()`.
  - §2 Regression và classification: bảng so sánh + code tính MSE và accuracy.
  - §3 Mô hình đơn giản nhất: bộ phân loại một ngưỡng `score >= t`, tính accuracy bằng `(preds == y).mean()`, trace table qua 3 ngưỡng `0.3`, `0.5`, `0.7`, nối lại bài `p5-01-math-bridge`.
  - §4 Chia tập train/test: ví dụ bài tập ở nhà vs đề thi mới, sơ đồ Mermaid `flowchart LR` (6 node, 7 dòng ở cả EN/VI), giới thiệu `rng.permutation` và cắt chỉ số đã xáo, kèm lời mời bấm **Visualize** trên khối 8 ví dụ (đã kiểm tra qua `tools/pyrunner/tracer.py`: 15 bước, không lỗi, không bị cắt).
  - §5 Nhận ra overfitting bằng mắt: 12 điểm nhiễu (`x` trong `[0, 1]`, seed `14`), `np.polyfit` bậc `1`, `3`, `6` trên train, bảng `| degree | train MSE | test MSE |` (làm tròn 3 chữ số), biểu đồ Matplotlib gồm điểm train, điểm test và 3 đường `np.polyval` trên `np.linspace(0.0, 1.0, 100)`, có chú thích `# (shows ...)` / `# (hiện ...)` sau `plt.show()`.
  - §6 Underfitting, vừa khớp và overfitting: bảng so sánh 3 chế độ và callout `> [!TIP]`.
  - §7 Lỗi thường gặp (4 lỗi có code chạy được): đánh giá trên tập train, data leakage khi min/max trên toàn dữ liệu trước khi chia (nối với `min_max_scale` của `p4-01-numpy`), quên xáo dữ liệu đã sắp xếp theo label, và quên đặt random seed (giải thích + sửa bằng `np.random.default_rng(42)`).
  - §8 Recap / Tóm tắt.
  - Đã chạy kiểm tra toàn bộ 9 khối code Python trong lesson (`MPLBACKEND=Agg`) và đối chiếu khớp hoàn toàn các comment `# output`.
- **Examples (3)**:
  - `01_ticket_threshold.py` (+ `.out`, `.en.md`, `.vi.md`): 12 ticket với spam score và nhãn 0/1, thử 5 ngưỡng, in accuracy từng ngưỡng và ngưỡng tốt nhất (`0.55`, accuracy `0.917`).
  - `02_train_test_split.py` (+ `.out`, `.en.md`, `.vi.md`): DataFrame 10 request (`id`, `tokens`, `latency`), xáo bằng seed `42`, chia 8/2, in `Train IDs` và `Test IDs` bằng `.tolist()`, fit đường thẳng bằng gradient descent trên train, in `Train MSE=0.001, Test MSE=0.002`.
  - `03_overfitting_curve.py` (+ `.out`, `.en.md`, `.vi.md`): 12 điểm nhiễu với seed `27`, `np.polyfit` bậc 1/3/6, in bảng `train_mse` và `test_mse`, vẽ biểu đồ.
- **Exercises (2)**:
  - `ex01-split-data` (`kind: fill`): `split_data(X, y, test_ratio, seed)` lấy `n_test` chỉ số đầu của `rng.permutation(len(X))` làm test và phần còn lại làm train; 5 test (kích thước, phủ toàn bộ không trùng, cùng seed cho cùng kết quả, khớp hàng X/y, không sửa đầu vào); 3 tầng hint (hint 3 có 3 chỗ trống `...`).
  - `ex02-best-threshold` (`kind: code`): `accuracy(preds, labels)` và `best_threshold(scores, labels)` (hòa chọn `t` nhỏ nhất, trả về Python `float`, `acc` làm tròn 3 chữ số); 6 test; kèm `alternatives/01_sorted_scan.py` (quét một lượt sau khi sắp xếp bằng vòng lặp Python thuần) + `.en.md`/`.vi.md`.
- **`quiz.yaml`**: 16 câu hỏi (`6 mcq`, `4 output`, `3 fill`, `3 parsons`; độ khó: `5` mức 1, `8` mức 2, `3` mức 3; đáp án `mcq` rải qua vị trí `0, 1, 2, 3`) và 6 flashcard (`p5-02-f01`..`p5-02-f06`).
- **`curriculum/glossary.yaml`**: thêm 6 thuật ngữ mới còn thiếu (`supervised learning`, `underfitting`, `regression`, `classification`, `accuracy`, `data leakage`), bỏ qua 4 thuật ngữ đã có (`feature`, `label`, `train/test split`, `overfitting`).

## 2. File đã sửa / tạo

- Sửa:
  - `curriculum/glossary.yaml`
- Tạo mới:
  - `curriculum/phase-05-ml/p5-02-supervised/meta.yaml`
  - `curriculum/phase-05-ml/p5-02-supervised/lesson.en.md`
  - `curriculum/phase-05-ml/p5-02-supervised/lesson.vi.md`
  - `curriculum/phase-05-ml/p5-02-supervised/quiz.yaml`
  - `curriculum/phase-05-ml/p5-02-supervised/examples/01_ticket_threshold.py`
  - `curriculum/phase-05-ml/p5-02-supervised/examples/01_ticket_threshold.out`
  - `curriculum/phase-05-ml/p5-02-supervised/examples/01_ticket_threshold.en.md`
  - `curriculum/phase-05-ml/p5-02-supervised/examples/01_ticket_threshold.vi.md`
  - `curriculum/phase-05-ml/p5-02-supervised/examples/02_train_test_split.py`
  - `curriculum/phase-05-ml/p5-02-supervised/examples/02_train_test_split.out`
  - `curriculum/phase-05-ml/p5-02-supervised/examples/02_train_test_split.en.md`
  - `curriculum/phase-05-ml/p5-02-supervised/examples/02_train_test_split.vi.md`
  - `curriculum/phase-05-ml/p5-02-supervised/examples/03_overfitting_curve.py`
  - `curriculum/phase-05-ml/p5-02-supervised/examples/03_overfitting_curve.out`
  - `curriculum/phase-05-ml/p5-02-supervised/examples/03_overfitting_curve.en.md`
  - `curriculum/phase-05-ml/p5-02-supervised/examples/03_overfitting_curve.vi.md`
  - `curriculum/phase-05-ml/p5-02-supervised/exercises/ex01-split-data/exercise.yaml`
  - `curriculum/phase-05-ml/p5-02-supervised/exercises/ex01-split-data/prompt.en.md`
  - `curriculum/phase-05-ml/p5-02-supervised/exercises/ex01-split-data/prompt.vi.md`
  - `curriculum/phase-05-ml/p5-02-supervised/exercises/ex01-split-data/starter.py`
  - `curriculum/phase-05-ml/p5-02-supervised/exercises/ex01-split-data/solution.py`
  - `curriculum/phase-05-ml/p5-02-supervised/exercises/ex01-split-data/test_exercise.py`
  - `curriculum/phase-05-ml/p5-02-supervised/exercises/ex02-best-threshold/exercise.yaml`
  - `curriculum/phase-05-ml/p5-02-supervised/exercises/ex02-best-threshold/prompt.en.md`
  - `curriculum/phase-05-ml/p5-02-supervised/exercises/ex02-best-threshold/prompt.vi.md`
  - `curriculum/phase-05-ml/p5-02-supervised/exercises/ex02-best-threshold/starter.py`
  - `curriculum/phase-05-ml/p5-02-supervised/exercises/ex02-best-threshold/solution.py`
  - `curriculum/phase-05-ml/p5-02-supervised/exercises/ex02-best-threshold/test_exercise.py`
  - `curriculum/phase-05-ml/p5-02-supervised/exercises/ex02-best-threshold/alternatives/01_sorted_scan.py`
  - `curriculum/phase-05-ml/p5-02-supervised/exercises/ex02-best-threshold/alternatives/01_sorted_scan.en.md`
  - `curriculum/phase-05-ml/p5-02-supervised/exercises/ex02-best-threshold/alternatives/01_sorted_scan.vi.md`
  - `tasks/m3-p5-02-supervised.report.md` (file báo cáo này)

## 3. Kết quả lệnh kiểm tra

- `uv run python tools/validate.py --path curriculum/phase-05-ml/p5-02-supervised`:
  - Exit code `0`: `OK: 0 error(s), 0 warning(s). Checked 1 lessons, 7 markdown pairs, 3 examples, 2 exercises, 1 alternatives, 16 questions.`
- `uv run python tools/validate.py`:
  - Exit code `0`: `OK: 0 error(s), 0 warning(s). Checked 32 lessons, 250 markdown pairs, 94 examples, 64 exercises, 60 alternatives, 612 questions, 6 exams, 1 portfolio, 1 glossary, 1 interview.`
- `uv run python -m pytest curriculum/phase-05-ml`:
  - Exit code `0`: `21 passed in 0.11s`
- `uv run ruff check curriculum/phase-05-ml`:
  - Exit code `0`: `All checks passed!`
- Kiểm tra regex mẫu cấm (`astype\(int\)|dtype=int\b|\.info\(|sklearn|np\.random\.(seed|rand)|^import random`) trên `curriculum/phase-05-ml/p5-02-supervised`:
  - Kết quả rỗng (0 dòng khớp).
- `uv run python tools/build_content.py`:
  - Exit code `0`: `Built 32 lessons, 6 exams, 192 flashcards, 515 questions -> apps\web\src\generated`
- Chạy kiểm tra bổ sung toàn bộ 9 khối Python trong `lesson.en.md` (với `MPLBACKEND=Agg`) + `tracer.trace` trên khối Visualize (§4):
  - Tất cả 9 khối chạy exit `0`, output khớp comment; khối Visualize trace được `15 steps, error= None, truncated= False`.
- `git status --short`:
  - Chỉ có `M curriculum/glossary.yaml`, `?? curriculum/phase-05-ml/p5-02-supervised/` (cùng thư mục `tasks/` và `.hallmark/` có sẵn trước đó). Không đụng `apps/`, `tools/`, `syllabus.yaml`, `topics.yaml`, `exams/` hay các bài khác; không chạy `pnpm --filter web build`; không commit.

## 4. Điều còn chưa chắc

- **Chạy thực tế trên trình duyệt (Pyodide wasm32)**: môi trường CLI không có trình duyệt để mở web app kiểm tra trực quan biểu đồ Matplotlib, giao diện Visualize/Mermaid, và output thực tế trong Pyodide 32-bit. Dù vậy, toàn bộ bài tập đã qua browser runner (`tools/pyrunner/runner.py`) trong `validate.py`, tracer đã qua `tools/pyrunner/tracer.py`, và code đã tuân thủ toàn bộ quy tắc 32-bit (không in `dtype` mảng nguyên, không dùng `astype(int)`/`dtype=int`, dùng `.tolist()`/`float()`/`round(..., 3)`).
- **URL ngoài (`further_reading`)**: các đường dẫn Google ML Crash Course (`dividing-the-original-dataset`, `overfitting/overfitting`) và scikit-learn (`cross_validation.html`) được xác nhận qua kết quả tìm kiếm web, chưa gửi HTTP request trực tiếp để kiểm tra mã trạng thái trả về.
