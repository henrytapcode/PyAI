# Báo cáo: M4 bước 6 — bài `p6-02-training-loop`

## 1. Đã làm gì

- Tạo bài học song ngữ EN/VI `curriculum/phase-06-deep-learning/p6-02-training-loop/` theo đúng dàn ý và quy tắc code phase 6 trong `tasks/m4-p6-02-training-loop.md` và `docs/CONTENT_GUIDE.md`:
  - `meta.yaml`: `phase: p6`, `order: 2`, `tags: [pytorch, dl]`, `prerequisites: [p6-01-tensors]`, `duration_min: 18`, `review_by: "2027-11-01"`, `outcomes` khớp `curriculum/syllabus.yaml` (bổ sung ý DataLoader mini-batch), không có trường `runner`, `further_reading` trỏ tới hai trang chính thức trên `pytorch.org/tutorials` (đã kiểm HTTP 200 sau redirect qua `curl.exe`).
  - `lesson.en.md` và `lesson.vi.md`: mở đầu không heading, đủ 7 mục + Recap/Tóm tắt, có picture in text (fence `text`), bảng so sánh `p6-01` vs PyTorch, diagram Mermaid `flowchart TD` 8 node (9 dòng khớp nhau EN/VI), trace table 4 mốc khớp stdout thật, khối Visualize riêng (`nn.Linear(1, 1)`, 4 điểm, 3 epoch, **31 step**, `truncated: False`), callout `[!TIP]` về `num_workers=0`, phần `Common mistakes` / `Lỗi thường gặp` lấy nguyên văn thông báo `RuntimeError` thật từ PyTorch `2.15.0+cpu`. Toàn bộ 10 khối code trong bài chạy sạch với `python -W error`.
  - 3 ví dụ chạy độc lập trong `examples/`: `01_two_blobs`, `02_minibatch_loader`, `03_save_and_reload` kèm `.out` UTF-8 và `.en.md` / `.vi.md`.
  - 2 bài tập trong `exercises/`:
    - `ex01-fix-training-loop` (`kind: debug`): `train(model, xs, ys, lr, epochs) -> list[float]`, starter chạy được nhưng thiếu `optimizer.zero_grad()` và lưu `loss` (tensor) thay vì `round(loss.item(), 4)`. Số đo trên `nn.Linear(1, 1)`, `torch.manual_seed(0)`, `y = 2x + 1`, `lr=0.05`, `epochs=30`: bản lỗi cho `loss[0]=35.0928`, `loss[-1]=40.9991`, `weight=3.7648`; bản đúng cho `loss[0]=35.0928`, `loss[-1]=0.0027`, `weight=1.9575`. Ngưỡng kiểm tra `losses[-1] < 0.05` chỉ đạt được khi đã sửa `zero_grad()`.
    - `ex02-tiny-classifier` (`kind: code`): `TinyClassifier(in_features, hidden, classes)` và `accuracy(model, xs, ys)`, 6 test (kể cả kiểm tra `accuracy` gọi `model.eval()` và không tạo gradient), kèm `alternatives/01_sequential.py` + `.en.md` / `.vi.md`.
  - `quiz.yaml`: 16 câu hỏi (5 dễ, 8 vừa, 3 khó; 7 `mcq`, 4 `output`, 3 `fill`, 2 `parsons` đều có thứ tự duy nhất) và 6 flashcard (`p6-02-f01`..`p6-02-f06`).
- Bổ sung 5 thuật ngữ mới vào `curriculum/glossary.yaml`: `epoch`, `batch`, `optimizer`, `logits`, `state_dict` (kiểm tra trước không trùng với các mục đã có; tổng số mục hiện tại là 216).

## 2. File đã sửa / tạo

- Tạo mới `curriculum/phase-06-deep-learning/p6-02-training-loop/`:
  - `meta.yaml`, `lesson.en.md`, `lesson.vi.md`, `quiz.yaml`
  - `examples/01_two_blobs.{py,out,en.md,vi.md}`
  - `examples/02_minibatch_loader.{py,out,en.md,vi.md}`
  - `examples/03_save_and_reload.{py,out,en.md,vi.md}`
  - `exercises/ex01-fix-training-loop/{exercise.yaml,prompt.en.md,prompt.vi.md,starter.py,solution.py,test_exercise.py}`
  - `exercises/ex02-tiny-classifier/{exercise.yaml,prompt.en.md,prompt.vi.md,starter.py,solution.py,test_exercise.py}`
  - `exercises/ex02-tiny-classifier/alternatives/01_sequential.{py,en.md,vi.md}`
- Sửa `curriculum/glossary.yaml`: thêm 5 thuật ngữ mới ở cuối file.
- Tạo mới `tasks/m4-p6-02-training-loop.report.md` (file báo cáo này).
- Ghi chú artifact build: chạy `tools/build_content.py` cập nhật thư mục gitignored `apps/web/src/generated`.

## 3. Kết quả lệnh kiểm tra

- **Thời gian khối code chậm nhất trong lesson**: khối `#2` (`§2`) mất **3.658s** khi chạy riêng từng khối bằng `uv run python -W error -c ...` (các khối còn lại từ `1.605s` đến `3.176s`, đều dưới 10s và thoát mã 0, không có cảnh báo).
- **Khối Visualize (`§3`)**: đo bằng `tools/pyrunner/tracer.py` (`tracer.trace`) ra **31 step**, `truncated: False`, `error: None`.
- **`uv run python tools/validate.py --path curriculum/phase-06-deep-learning/p6-02-training-loop`**: **55.24s**, thoát mã 0 — `OK: 0 error(s), 0 warning(s). Checked 1 lessons, 7 markdown pairs, 3 examples, 2 exercises, 1 alternatives, 16 questions.`
- **Kiểm tra starter / solution / alternative**:
  - Qua browser runner (`tools/pyrunner/runner.py`):
    - `ex01-fix-training-loop`: `starter` pass **0/4** (`ok=False`), `solution` pass **4/4** (`ok=True`).
    - `ex02-tiny-classifier`: `starter` pass **0/6** (`ok=False`), `solution` pass **6/6** (`ok=True`), `01_sequential` pass **6/6** (`ok=True`).
  - Qua `uv run python -m pytest` với `EXERCISE_TARGET=starter` trên hai file test của `p6-02-training-loop`: **10 failed, 0 passed** (`0` warnings) với thông báo lỗi rõ ràng.
- **`uv run python -m pytest curriculum/phase-06-deep-learning`**: `21 passed in 2.41s`, thoát mã 0 (bao gồm 11 test của `p6-01-tensors` và 10 test của `p6-02-training-loop`).
- **`uv run ruff check curriculum/phase-06-deep-learning`**: `All checks passed!`, thoát mã 0.
- **Hai lệnh `grep`** (chạy qua Git Bash `C:\Program Files\Git\bin\bash.exe` vì Windows PowerShell mặc định không có `grep` trong PATH):
  - `grep -rnE "\.cuda\(|to\(\"cuda|astype\(int\)|dtype=int\b|\.info\(|print\(model\)|num_workers=[1-9]" curriculum/phase-06-deep-learning/p6-02-training-loop` -> rỗng (exit 1).
  - `grep -rln "tensor(" curriculum/phase-06-deep-learning --include=*.out` -> rỗng (exit 1).
- **Schema `curriculum/glossary.yaml`**: kiểm tra riêng với `tools/schema/glossary.schema.json` -> `0` lỗi schema, `0` thuật ngữ trùng lặp.
- **`uv run python tools/build_content.py`**: thoát mã 0 — `Built 37 lessons, 8 exams, 222 flashcards, 595 questions -> apps\web\src\generated`.
- **`git status --short`**: chỉ thay đổi `M curriculum/glossary.yaml`, thêm mới `curriculum/phase-06-deep-learning/p6-02-training-loop/` và `tasks/` (cùng `.hallmark/` có sẵn từ trước).

## 4. Điều còn chưa chắc

- Chưa chạy `uv run python tools/validate.py` trên toàn bộ `curriculum/` (chỉ chạy `--path curriculum/phase-06-deep-learning/p6-02-training-loop` theo đúng spec, và kiểm tra riêng schema + tính duy nhất cho `curriculum/glossary.yaml`).
- Chưa chạy thử giao diện web hoặc local runner server trực tiếp trên trình duyệt (do quy tắc không chạy server/build web); hành vi Run/Visualize/chấm bài tập mới được xác minh gián tiếp qua `tools/validate.py`, `tools/pyrunner/tracer.py` và `tools/pyrunner/runner.py`.
- Đã kiểm tra URL `further_reading` trả HTTP 200 (sau redirect sang `docs.pytorch.org`) qua `curl.exe`, chưa đọc toàn bộ nội dung HTML của hai trang tutorial bên ngoài.

## Vòng 2

- **Đã sửa theo `## Feedback vòng 1`:**
  - Trong `lesson.en.md` và `lesson.vi.md` (§6): đổi tên biến từ `X_eval`, `y_eval` thành `X_train`, `y_train`; bổ sung 1 câu song ngữ EN/VI ngay sau khối code giải thích rằng ở đây đo accuracy trên `X_train` chỉ để đối chiếu model gốc với model nạp lại, còn đánh giá chất lượng tổng quát vẫn dùng tập validation/test như ở §5.
  - Trong `examples/03_save_and_reload.py` (trước đó dùng `X`, `y` cho cả train và kiểm tra): đổi tên thành `X_train`, `y_train`, đồng thời bổ sung câu giải thích tương ứng vào `examples/03_save_and_reload.en.md` và `examples/03_save_and_reload.vi.md`.
- **Kết quả kiểm tra lại (sau khi sửa):**
  - Chạy riêng khối §6 và `examples/03_save_and_reload.py` với `uv run python -W error`: thoát mã 0, không cảnh báo; output giữ nguyên (`acc original: 0.962 reloaded: 0.962` / `same predictions: True` cho §6; `original accuracy: 0.958` / `reloaded accuracy: 0.958` / `same predictions: True` khớp `examples/03_save_and_reload.out`).
  - `uv run python tools/validate.py --path curriculum/phase-06-deep-learning/p6-02-training-loop`: thoát mã 0 — `OK: 0 error(s), 0 warning(s). Checked 1 lessons, 7 markdown pairs, 3 examples, 2 exercises, 1 alternatives, 16 questions.`
  - `uv run python -m pytest curriculum/phase-06-deep-learning`: `21 passed in 3.35s`, thoát mã 0.
  - `uv run ruff check curriculum/phase-06-deep-learning`: `All checks passed!`, thoát mã 0.
  - Hai lệnh `grep` qua Git Bash (`C:\Program Files\Git\bin\bash.exe`): đều rỗng (`exit1=1`, `exit2=1`).
  - `uv run python tools/build_content.py`: thoát mã 0 — `Built 37 lessons, 8 exams, 222 flashcards, 595 questions -> apps\web\src\generated`.
  - `git status --short`: `M curriculum/glossary.yaml`, `?? .hallmark/`, `?? curriculum/phase-06-deep-learning/p6-02-training-loop/`, `?? tasks/`.
