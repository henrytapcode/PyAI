# Báo cáo: `m3-p5-01-math-bridge`

## 1. Đã làm gì

- Tạo bài đầu tiên của phase 5 tại `curriculum/phase-05-ml/p5-01-math-bridge/` (không tạo file cấp phase nào thêm và không tạo `phase-test.yaml`, vì `tools/validate.py` và `tools/build_content.py` không yêu cầu file cấp phase riêng).
- Viết `meta.yaml`: `id: p5-01-math-bridge`, `phase: p5`, `order: 1`, `duration_min: 14`, `tags: [ml-math, numpy]`, `prerequisites: [p4-01-numpy, p4-04-matplotlib]`, `outcomes` khớp `curriculum/syllabus.yaml` (thêm 1 outcome về chọn learning rate), `review_by: "2027-11-01"`, và 2 mục `further_reading` (3Blue1Brown Dot products; Google ML Crash Course Gradient descent).
- Viết `lesson.en.md` và `lesson.vi.md` đúng dàn ý cầu nối toán trực quan (không chứng minh, không dùng ký hiệu đạo hàm `d/dw` hay `∂`):
  - Opening giải thích weights và 3 ý chính (vector, tích vô hướng, gradient).
  - §1 Vector & độ dài `np.linalg.norm` / `np.sqrt`, kèm picture-in-text (`text` fence) cho mũi tên `[3, 4]`.
  - §2 Tích vô hướng (`np.dot`, `@`), trace table `| i | a[i] | b[i] | a[i] * b[i] | running sum |`, ý nghĩa điểm có trọng số và cosine similarity (xem trước Phase 7).
  - §3 Đo sai số bằng MSE loss, quét giá trị `w` và vẽ đường cong chữ U (`ax.plot` + `# (shows ...)` / `# (hiện ...)`).
  - §4 Gradient = độ dốc ước lượng bằng số `(loss(w + h) - loss(w - h)) / (2 * h)` với `h = 0.001`, kèm bảng so sánh 3 trường hợp độ dốc.
  - §5 Gradient descent: Mermaid `flowchart TD` 7 node, khối vòng lặp 5 bước (`lr = 0.05`) kèm lời mời bấm **Visualize**, trace table 5 bước khớp output thật, mở rộng sang `(w, b)` với công thức gradient MSE bằng lời và biểu đồ loss giảm theo step.
  - §6 Learning rate: so sánh `lr = 0.002`, `0.05`, `0.15` sau 10 bước, bảng so sánh và callout `> [!TIP]`.
  - §7 Lỗi thường gặp (4 lỗi, output/traceback lấy từ lần chạy thật): `a * b` vs `a @ b`; `np.dot` lệch kích thước (`ValueError: shapes (3,) and (2,) not aligned: 3 (dim 0) != 2 (dim 0)`); bước `+ lr * slope` làm loss tăng; `lr` quá lớn làm loss phình to.
  - §8 Tóm tắt 5 gạch đầu dòng.
  - Tất cả 11 khối code Python trong lesson đã được chạy thực tế (`MPLBACKEND=Agg`), mọi số thực in ra đều làm tròn (`round(..., 3)`), comment output khớp từng dòng.
- Tạo 3 examples trong `examples/` (`.py`, `.out`, `.en.md`, `.vi.md`):
  - `01_feature_scores`: tính điểm 3 request bằng `@` và tìm request điểm cao nhất (`req-102`, `5.21`).
  - `02_embedding_similarity`: cosine similarity giữa query và 4 embedding 4D (`refund_policy`, `0.99`).
  - `03_fit_a_line`: fit đường thẳng `y = w * x + b` trên dữ liệu token–latency qua 50 bước, in `w=0.6, b=0.23`, `start=4.836, end=0.002`, vẽ scatter + đường fit (tracer chạy hết 422 bước không bị cắt).
- Tạo 2 exercises trong `exercises/`:
  - `ex01-weighted-score` (`kind: fill`): `weighted_score(features, weights, bias) -> float`, 4 test, hint 3 tầng (hint 3 chừa 3 dòng `...`), starter fail / solution pass.
  - `ex02-gradient-descent` (`kind: code`): `mse(w, b, xs, ys) -> float` và `fit_line(xs, ys, lr, steps) -> tuple[float, float]`, 6 test, hint 3 tầng (hint 3 chừa 3 dòng `...`), kèm `alternatives/01_numeric_slope.py` + `.en.md`/`.vi.md` dùng độ dốc ước lượng bằng số.
- Tạo `quiz.yaml`: 16 câu (5 `mcq`, 4 `output`, 4 `fill`, 3 `parsons`; độ khó: 5 mức 1, 8 mức 2, 3 mức 3) và 6 flashcard (`p5-01-f01`..`p5-01-f06`).
- Cập nhật `curriculum/glossary.yaml`: thêm 5 thuật ngữ mới (`dot product`, `loss / mean squared error`, `gradient`, `gradient descent`, `learning rate`); giữ nguyên `vector` vì đã có sẵn.
- Chạy `uv run python tools/build_content.py` để cập nhật JSON sinh ra trong `apps/web/src/generated/` (đã gitignore).

## 2. File đã sửa / tạo

- Sửa:
  - `curriculum/glossary.yaml`
- Tạo mới trong `curriculum/phase-05-ml/p5-01-math-bridge/`:
  - `meta.yaml`
  - `lesson.en.md`, `lesson.vi.md`
  - `quiz.yaml`
  - `examples/01_feature_scores.{py,out,en.md,vi.md}`
  - `examples/02_embedding_similarity.{py,out,en.md,vi.md}`
  - `examples/03_fit_a_line.{py,out,en.md,vi.md}`
  - `exercises/ex01-weighted-score/{exercise.yaml,prompt.en.md,prompt.vi.md,starter.py,solution.py,test_exercise.py}`
  - `exercises/ex02-gradient-descent/{exercise.yaml,prompt.en.md,prompt.vi.md,starter.py,solution.py,test_exercise.py}`
  - `exercises/ex02-gradient-descent/alternatives/01_numeric_slope.{py,en.md,vi.md}`
- Tạo mới báo cáo này:
  - `tasks/m3-p5-01-math-bridge.report.md`

## 3. Kết quả lệnh kiểm tra

Chạy sau lần chỉnh sửa cuối cùng:

| Lệnh | Kết quả | Chi tiết |
|---|---|---|
| `uv run python tools/validate.py --path curriculum/phase-05-ml/p5-01-math-bridge` | Exit 0 | `OK: 0 error(s), 0 warning(s). Checked 1 lessons, 7 markdown pairs, 3 examples, 2 exercises, 1 alternatives, 16 questions.` |
| `uv run python tools/validate.py` | Exit 0 | `OK: 0 error(s), 0 warning(s). Checked 31 lessons, 243 markdown pairs, 91 examples, 62 exercises, 59 alternatives, 596 questions, 6 exams, 1 portfolio, 1 glossary, 1 interview.` |
| `uv run python -m pytest curriculum/phase-05-ml` | Exit 0 | `10 passed in 0.08s` |
| `uv run ruff check curriculum/phase-05-ml` | Exit 0 | `All checks passed!` |
| Kiểm tra pattern cấm (`astype(int)`, `dtype=int`, `.info(`, `∂`, `d/dw`) trong `curriculum/phase-05-ml` | Exit 0 | `Forbidden pattern matches: 0` |
| `uv run python tools/build_content.py` | Exit 0 | `Built 31 lessons, 6 exams, 186 flashcards, 499 questions -> apps\web\src\generated` |
| `git status --short` (trước khi ghi file report) | Exit 0 | `M curriculum/glossary.yaml`, `?? .hallmark/`, `?? curriculum/phase-05-ml/`, `?? tasks/` (`.hallmark/` và `tasks/` có sẵn từ trước) |

Ngoài ra đã chạy riêng toàn bộ 11 khối Python trong `lesson.en.md` (`MPLBACKEND=Agg`) và `tracer.trace(...)` cho 3 example (`25`, `31`, `422` bước; `truncated: False`, `error: None`).

## 4. Điều còn chưa chắc

- **Chưa chạy kiểm tra trực tiếp trên trình duyệt (Pyodide wasm32 / UI Next.js):** không mở trình duyệt trong phiên này nên chưa quan sát trực tiếp biểu đồ matplotlib render trên canvas của web app hay bấm chạy quiz/exercise trong Pyodide thật. Tuy nhiên toàn bộ quy tắc 32-bit/output đã được tuân thủ và `tools/validate.py` đã kiểm tra cả `tools/pyrunner/runner.py` lẫn `tools/pyrunner/tracer.py` trên CPython.
- **Lệnh kiểm tra pattern:** trên Windows PowerShell không có `grep`, đã chạy script Python tương đương với regex `astype\(int\)|dtype=int\b|\.info\(|∂|d/dw` trên toàn bộ file trong `curriculum/phase-05-ml` (0 kết quả khớp).
