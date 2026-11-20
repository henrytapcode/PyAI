# Báo cáo: M4 bước 5 — bài `p6-01-tensors` (Tensors & autograd)

## 1. Đã làm gì

- Tạo bài học đầu tiên của Phase 6 (`curriculum/phase-06-deep-learning/p6-01-tensors/`) bám sát `docs/CONTENT_GUIDE.md` (bao gồm mục "Data & ML code (phase 4+)" và "Deep learning, LLM & production code (phase 6+)") và spec `tasks/m4-p6-01-tensors.md`, song ngữ EN/VI.
- **Không** tạo `phase-test.yaml` và validator cũng **không** đòi thêm file cấp phase nào cho `curriculum/phase-06-deep-learning/`.
- `meta.yaml`: `id: p6-01-tensors`, `phase: p6`, `order: 1`, `kind: lesson`, `tags: [pytorch, dl]`, `prerequisites: [p5-01-math-bridge]`, `duration_min: 17`, `review_by: "2027-11-01"`, `outcomes` khớp syllabus (+1 dòng về `torch.no_grad()` và `.grad.zero_()`), **không** có trường `runner`, `further_reading` trỏ tới 2 bài tutorial chính thức trên `pytorch.org/tutorials` (đã kiểm tra HTTP `200` cho cả hai URL).
- `lesson.en.md` / `lesson.vi.md`:
  - Opening nối từ `p5-01-math-bridge`: PyTorch làm phép tính mảng giống NumPy và tự tính gradient.
  - §1 Tensor là array của PyTorch (`tuple(t.shape)`, `t.dtype` mặc định `float32`, `zeros`, `ones`, `arange`, `torch.rand` kèm `torch.manual_seed(0)`, `torch.from_numpy`/`t.numpy()`, picture in text shape `(2, 3)`).
  - §2 Phép tính giống NumPy (`+`, `*`, broadcasting, `@`, `dim=` thay `axis=`, bảng so sánh `| NumPy | PyTorch |`, ví dụ batch 3 request × 4 feature).
  - §3 In tensor cho dễ đọc (`.item()`, `.tolist()`, `round(..., 3)`, chỉ nói về repr thô trong `#` comment mà không in ra).
  - §4 Autograd: `requires_grad=True`, `loss.backward()`, `w.grad`, đối chiếu khớp với ước lượng độ dốc bằng số `h = 0.001` (`-15.0` == `-15.0`), sơ đồ Mermaid `flowchart LR` 8 node.
  - §5 Gradient descent với autograd: vòng lặp 4 bước (`torch.no_grad()` và `w.grad.zero_()`), trace table 4 bước khớp output thật, lời mời bấm **Visualize** (43 step trong tracer), callout `[!NOTE]` về `torch.optim` ở bài sau và nhắc một câu về GPU (không dùng `.cuda(` hay `to("cuda`).
  - §6 Lỗi thường gặp (4 lỗi, thông báo lỗi lấy từ lần chạy thật trên PyTorch `2.15.0+cpu`): quên `w.grad.zero_()`, cập nhật ngoài `torch.no_grad()`, `.item()` trên tensor nhiều phần tử, lệch shape `(3, 4) @ (3,)`.
  - §7 Tóm tắt (5 gạch đầu dòng).
- **Examples (3):** `01_batch_scores`, `02_autograd_check`, `03_fit_line_autograd` (kèm `.out`, `.en.md`, `.vi.md`), tất cả chạy trên CPU, dưới 2 giây, không in tensor thô, không lỗi trong `tracer.py`.
- **Exercises (2):**
  - `ex01-batch-scores` (`kind: fill`): `score_batch` với 5 test (giá trị, `list` gồm `float` Python, batch 1 dòng, `weights` lệch độ dài raise `RuntimeError`, không sửa tensor đầu vào) + hint 3 tầng EN/VI.
  - `ex02-autograd-descent` (`kind: code`): `slope_at` & `fit_slope` với 6 test (khớp công thức MSE, gọi 2 lần không cộng dồn, hội tụ gần `3.0`, `steps=0 -> 0.0`, bước 1 khớp đạo hàm chính xác, kiểu trả về `float` Python), hint 3 tầng EN/VI, và `alternatives/01_manual_gradient.py` (+ `.en.md`, `.vi.md`).
- **Quiz (`quiz.yaml`):** 16 câu hỏi (`6 mcq`, `4 output`, `3 fill`, `3 parsons`; `5` easy, `8` medium, `3` hard) + 6 flashcard (`p6-01-f01`..`f06`), có câu về `float32` và cộng dồn gradient (`zero_()`), không in tensor thô.
- **Shared curriculum files:** thêm tag `pytorch` vào `curriculum/topics.yaml` ngay sau `dl:`; thêm 5 thuật ngữ (`tensor`, `autograd`, `computation graph`, `backward pass`, `leaf tensor`) vào `curriculum/glossary.yaml`.

## 2. File đã sửa / tạo

**Đã sửa:**
- `curriculum/topics.yaml` (thêm dòng `pytorch: { en: "PyTorch", vi: "PyTorch" }`)
- `curriculum/glossary.yaml` (thêm 5 thuật ngữ mới)

**Đã tạo:**
- `curriculum/phase-06-deep-learning/p6-01-tensors/meta.yaml`
- `curriculum/phase-06-deep-learning/p6-01-tensors/lesson.en.md`
- `curriculum/phase-06-deep-learning/p6-01-tensors/lesson.vi.md`
- `curriculum/phase-06-deep-learning/p6-01-tensors/quiz.yaml`
- `curriculum/phase-06-deep-learning/p6-01-tensors/examples/01_batch_scores.py`, `.out`, `.en.md`, `.vi.md`
- `curriculum/phase-06-deep-learning/p6-01-tensors/examples/02_autograd_check.py`, `.out`, `.en.md`, `.vi.md`
- `curriculum/phase-06-deep-learning/p6-01-tensors/examples/03_fit_line_autograd.py`, `.out`, `.en.md`, `.vi.md`
- `curriculum/phase-06-deep-learning/p6-01-tensors/exercises/ex01-batch-scores/{exercise.yaml, prompt.en.md, prompt.vi.md, starter.py, solution.py, test_exercise.py}`
- `curriculum/phase-06-deep-learning/p6-01-tensors/exercises/ex02-autograd-descent/{exercise.yaml, prompt.en.md, prompt.vi.md, starter.py, solution.py, test_exercise.py}`
- `curriculum/phase-06-deep-learning/p6-01-tensors/exercises/ex02-autograd-descent/alternatives/{01_manual_gradient.py, 01_manual_gradient.en.md, 01_manual_gradient.vi.md}`
- `tasks/m4-p6-01-tensors.report.md`

*(Ghi chú: `uv run python tools/build_content.py` cập nhật output gitignored trong `apps/web/src/generated/`.)*

## 3. Kết quả lệnh kiểm tra

| Lệnh | Kết quả | Thời gian / Chi tiết |
|---|---|---|
| `uv run python tools/validate.py --path curriculum/phase-06-deep-learning/p6-01-tensors` | PASS (exit `0`) | **31.23s** — `OK: 0 error(s), 0 warning(s). Checked 1 lessons, 7 markdown pairs, 3 examples, 2 exercises, 1 alternatives, 16 questions.` |
| `uv run python tools/validate.py` | PASS (exit `0`) | **263.53s** — `OK: 0 error(s), 0 warning(s). Checked 36 lessons, 279 markdown pairs, 106 examples, 72 exercises, 65 alternatives, 718 questions, 8 exams, 1 portfolio, 1 glossary, 1 interview.` |
| `uv run python -m pytest curriculum/phase-06-deep-learning` | PASS (exit `0`) | `11 passed in 1.18s` (tổng 11 test của `ex01` và `ex02`) |
| `uv run ruff check curriculum/phase-06-deep-learning` | PASS (exit `0`) | `All checks passed!` |
| `python -W error` trên từng block trong `lesson.en.md` (9 block) & 3 file example & các block trong `quiz.yaml` | PASS (exit `0`, 0 cảnh báo) | Khối code chậm nhất trong bài: **Block 8 (`1.44s`)**; ví dụ chậm nhất: **`03_fit_line_autograd.py` (`1.72s`)**; khối Visualize (§5 Block 5) chạy **43 step** trong `tracer.py` (`truncated=False`). |
| Kiểm tra mẫu cấm `\.cuda\(|to\("cuda|astype\(int\)|dtype=int\b|\.info\(` và `tensor(` trong `*.out` | Rỗng (`0` kết quả) | `grep` không có trong PATH Windows nên đã chạy bằng `Select-String` của PowerShell và Python `re` trên toàn bộ `curriculum/phase-06-deep-learning` — đều trả về rỗng `[]`. |
| `uv run python tools/build_content.py` | PASS (exit `0`) | `Built 36 lessons, 8 exams, 216 flashcards, 579 questions -> apps\web\src\generated` |
| `git status --short` | Sạch phạm vi cho phép | `M curriculum/glossary.yaml`, `M curriculum/topics.yaml`, `?? curriculum/phase-06-deep-learning/`, `?? tasks/` (và thư mục có sẵn `?? .hallmark/`). |

## 4. Điều còn chưa chắc

- Chưa khởi động web app hay `localrunner` để kiểm tra giao diện hiển thị bài học, bảng Markdown và nút **Run / Visualize** trực tiếp trên trình duyệt (theo đúng quy tắc không chạy server/dev server và không chạy `pnpm --filter web build`).
- Trên máy Windows này không có lệnh `grep` trong PATH nên hai lệnh `grep` ở mục kiểm tra được xác minh tương đương bằng PowerShell `Select-String` và script Python `re` với kết quả rỗng.
- Phát hiện bên lề khi thử nghiệm `tools/pyrunner/tracer.py`: nếu một ví dụ dùng `with torch.no_grad():` chạm ngưỡng `MAX_STEPS = 600` (`_TooManySteps`) ngay bên trong khối `with`, trong cùng tiến trình Python đó `torch.is_grad_enabled()` có thể bị kẹt ở `False` sau khi `trace()` trả về. Đã giữ `03_fit_line_autograd.py` ở `41` bước (`463` step trong tracer, `truncated=False`) nên `validate.py` không gặp hiện tượng này, nhưng nên lưu ý khi viết các bài Phase 6 tiếp theo (chưa sửa `tools/` vì nằm ngoài phạm vi).

## Vòng 2

### Đã sửa theo Feedback vòng 1
1. **§5 (`lesson.en.md`, `lesson.vi.md`):** Sửa `"five moves"` → `"four moves"` và `"năm thao tác"` → `"bốn thao tác"` cho khớp với 4 bước được liệt kê.
2. **§3 (`lesson.en.md`, `lesson.vi.md`):** Viết lại lý do làm tròn với `float32`: thay vì nói kết quả lệch giữa các lần chạy, giải thích rằng chữ số thập phân cuối của `float32` có thể khác nhau giữa các phiên bản PyTorch hoặc các máy, nên làm tròn để output luôn ổn định.
3. **Exercise tests (`ex02-autograd-descent/test_exercise.py`, `ex01-batch-scores/test_exercise.py`):**
   - Trong `ex02`: thêm `assert first == pytest.approx(-18.667)` trước `assert first == second` ở `test_slope_at_does_not_accumulate_across_calls` để starter không pass được test nào; thêm `assert result is not None, "slope_at returned None: did you forget to return the value?"` (và tương tự cho `fit_slope`) trước các phép so sánh/kiểm tra kết quả để lỗi khi hàm chưa có `return` dễ hiểu hơn với người mới.
   - Trong `ex01`: giữ `starter.py` với `___` (nếu thay `___` bằng `None` thì `scores.None()` gây `SyntaxError` khi import); đồng thời kiểm thử trường hợp `score_batch` trả về `None` cho thấy trước đây `test_does_not_modify_input_tensors` vẫn pass (1/5) và 2 test kia báo `TypeError: object of type 'NoneType' has no len()`. Đã thêm `assert result is not None, "score_batch returned None: did you forget to return the value?"` ở 3 test tương ứng (`test_computes_scores_for_multi_row_batch`, `test_single_row_batch_returns_one_element_list`, `test_does_not_modify_input_tensors`) để trường hợp trả `None` fail cả 5/5 với thông báo rõ ràng.

### Kết quả kiểm tra Vòng 2

| Lệnh | Kết quả | Thời gian / Chi tiết |
|---|---|---|
| `uv run python tools/validate.py --path curriculum/phase-06-deep-learning/p6-01-tensors` | PASS (exit `0`) | **31.82s** — `OK: 0 error(s), 0 warning(s). Checked 1 lessons, 7 markdown pairs, 3 examples, 2 exercises, 1 alternatives, 16 questions.` |
| `uv run python -m pytest curriculum/phase-06-deep-learning -v` | PASS (exit `0`) | `11 passed in 1.27s` |
| Kiểm tra `ex02` với `starter.py` | FAIL đúng kỳ vọng | `6 failed in 1.30s` (pass **0/6** test) |
| Kiểm tra `ex01` khi `score_batch` trả `None` | FAIL đúng kỳ vọng | `5 failed in 1.23s` (pass **0/5** test) |
| `uv run ruff check curriculum/phase-06-deep-learning` | PASS (exit `0`) | `All checks passed!` |
| `uv run python tools/build_content.py` | PASS (exit `0`) | `Built 36 lessons, 8 exams, 216 flashcards, 579 questions -> apps\web\src\generated` |
| `git status --short` | Sạch phạm vi | `M curriculum/glossary.yaml`, `M curriculum/topics.yaml`, `?? .hallmark/`, `?? curriculum/phase-06-deep-learning/`, `?? tasks/` |
