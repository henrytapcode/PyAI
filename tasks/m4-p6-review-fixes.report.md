# Báo cáo thực hiện `tasks/m4-p6-review-fixes.md`

## 1. Đã làm gì theo từng mục (A–G)

### Mục A — Chống lộ đáp án MCQ qua độ dài (4 `quiz.yaml`)
- Viết lại các phương án MCQ ở cả `en` và `vi` trong [p6-01-tensors/quiz.yaml](file:///D:/Proj/python-ai-platform/curriculum/phase-06-deep-learning/p6-01-tensors/quiz.yaml), [p6-02-training-loop/quiz.yaml](file:///D:/Proj/python-ai-platform/curriculum/phase-06-deep-learning/p6-02-training-loop/quiz.yaml), [p6-03-huggingface/quiz.yaml](file:///D:/Proj/python-ai-platform/curriculum/phase-06-deep-learning/p6-03-huggingface/quiz.yaml) và [p6-04-fine-tune/quiz.yaml](file:///D:/Proj/python-ai-platform/curriculum/phase-06-deep-learning/p6-04-fine-tune/quiz.yaml):
  - Bỏ cụm giải thích lý do trong đáp án đúng, chuyển sang `explanation` nếu cần.
  - Mở rộng các distractor theo hiểu lầm cụ thể để `len(correct) <= 1.2 * mean(distractors)` và số câu có đáp án đúng là phương án dài nhất duy nhất không vượt quá 1/3 số câu MCQ mỗi file.
  - Giữ nguyên `id`, số câu, `answer` index và kiểm tra lại tính nhất quán của `explanation`.

### Mục B — Sửa hint không leo thang (7 `exercise.yaml`, cả EN và VI)
- Cập nhật `hints.en` và `hints.vi` cho `p6-01-ex02`, `p6-02-ex01`, `p6-02-ex02`, `p6-03-ex01`, `p6-03-ex02`, `p6-04-ex01`, `p6-04-ex02`:
  - **Hint 1**: nêu ý tưởng, mục tương ứng trong bài và kết quả trên một input cụ thể.
  - **Hint 2**: các bước bằng lời dạng danh sách đánh số, chỉ nhắc tên hàm/method khi cần, không chứa biểu thức Python hoàn chỉnh.
  - **Hint 3**: skeleton trong code block `python` có 1–2 chỗ `...` ngay phần khó mà Hint 2 chưa nói thẳng (đặc biệt `p6-03-ex01` tách khỏi dạng starter Comprehension sang vòng lặp có chú thích phần còn thiếu), cho nhiều thông tin hơn Hint 2 và starter nhưng ghép Hint 2 + Hint 3 vẫn chưa ra full solution.

### Mục C — `p6-04` §4 chọn epoch ([lesson.en.md](file:///D:/Proj/python-ai-platform/curriculum/phase-06-deep-learning/p6-04-fine-tune/lesson.en.md), [lesson.vi.md](file:///D:/Proj/python-ai-platform/curriculum/phase-06-deep-learning/p6-04-fine-tune/lesson.vi.md))
- Thêm câu giới thiệu `AdamW` (`Adam + weight decay (decoupled)`).
- Tính và in thêm `val_loss` trong `torch.no_grad()` (`model(**val_batch, labels=val_y).loss`, làm tròn 3 chữ số) cùng số chạy thật (`val_loss`: `0.667, 0.654, 0.537, 0.387, 0.28, 0.211`), bổ sung cột `val loss` vào bảng tóm tắt.
- Cập nhật khối Visualize `history` sang tuple `(epoch, val_acc, val_loss)`, bỏ phá hòa bằng train loss và đổi sang chọn `val_acc` cao nhất, hòa thì chọn `val_loss` thấp hơn (`best epoch: 10 (val_acc=1.0, val_loss=0.211)`).
- Nêu rõ chỉ quét `1–10` epoch và thêm một ý ở `## 8. Going further` / `## 8. Đi xa hơn` về việc `val_loss` vẫn đang giảm ở epoch `10` (`0.211`) nên có thể quét dài hơn.

### Mục D — `p6-04` §5 đánh giá test ([lesson.en.md](file:///D:/Proj/python-ai-platform/curriculum/phase-06-deep-learning/p6-04-fine-tune/lesson.en.md), [lesson.vi.md](file:///D:/Proj/python-ai-platform/curriculum/phase-06-deep-learning/p6-04-fine-tune/lesson.vi.md))
- Đổi tiêu đề mục 5 thành `## 5. Final evaluation on test` / `## 5. Đánh giá cuối cùng trên tập test`.
- Giữ nguyên hai con số trước/sau (`0.562` và `0.938`) nhưng sửa lời văn: mốc `before` (`0.562`) chỉ để tham khảo baseline chưa tune, không dùng để ra bất kỳ quyết định chọn hyperparameter nào vì số epoch (`10`) đã chốt hoàn toàn bằng validation.

### Mục E — Thêm `pick_epoch` cho `p6-04-ex02`
- Bổ sung `pick_epoch(history: list[tuple[int, float, float]]) -> int` (trả `None` và có docstring + ví dụ trong [starter.py](file:///D:/Proj/python-ai-platform/curriculum/phase-06-deep-learning/p6-04-fine-tune/exercises/ex02-fine-tune-and-evaluate/starter.py), cài đặt đầy đủ trong [solution.py](file:///D:/Proj/python-ai-platform/curriculum/phase-06-deep-learning/p6-04-fine-tune/exercises/ex02-fine-tune-and-evaluate/solution.py) và [01_minibatch.py](file:///D:/Proj/python-ai-platform/curriculum/phase-06-deep-learning/p6-04-fine-tune/exercises/ex02-fine-tune-and-evaluate/alternatives/01_minibatch.py)): chọn `val_acc` cao nhất, hòa thì lấy `val_loss` thấp hơn, vẫn hòa thì lấy `epoch` sớm nhất.
- Cập nhật [prompt.en.md](file:///D:/Proj/python-ai-platform/curriculum/phase-06-deep-learning/p6-04-fine-tune/exercises/ex02-fine-tune-and-evaluate/prompt.en.md), [prompt.vi.md](file:///D:/Proj/python-ai-platform/curriculum/phase-06-deep-learning/p6-04-fine-tune/exercises/ex02-fine-tune-and-evaluate/prompt.vi.md) và `exercise.yaml`.
- Thêm 3 test thuần list trong [test_exercise.py](file:///D:/Proj/python-ai-platform/curriculum/phase-06-deep-learning/p6-04-fine-tune/exercises/ex02-fine-tune-and-evaluate/test_exercise.py) (`test_pick_epoch_selects_highest_val_acc`, `test_pick_epoch_breaks_val_acc_tie_with_lower_val_loss`, `test_pick_epoch_keeps_earliest_epoch_when_both_metrics_tie`).

### Mục F — Test `no_grad()` và `model.train()`
- Ở `p6-02-ex02` ([test_exercise.py](file:///D:/Proj/python-ai-platform/curriculum/phase-06-deep-learning/p6-02-training-loop/exercises/ex02-tiny-classifier/test_exercise.py)) và `p6-04-ex02` ([test_exercise.py](file:///D:/Proj/python-ai-platform/curriculum/phase-06-deep-learning/p6-04-fine-tune/exercises/ex02-fine-tune-and-evaluate/test_exercise.py)): thay kiểm tra `p.grad is None` bằng lớp con `nn.Module` thăm dò (`_GradProbe`, bên `p6-04` trả về `types.SimpleNamespace(logits=...)`) ghi lại `torch.is_grad_enabled()` và assert tất cả là `False` với thông báo `"wrap the forward pass in \`torch.no_grad()\`"`.
- Ở `p6-04-ex02`: thêm `test_fine_tune_switches_to_train_mode_before_steps` gọi `model.eval()`, chạy `fine_tune(..., epochs=1)`, và assert `model.training` với thông báo `"call \`model.train()\` before training steps"`.

### Mục G (G1–G15)
- **G1**: Ghi rõ trong `p6-03-ex02/alternatives/01_pipeline.{en,vi}.md` đây là cách đối chiếu tham khảo, không đạt Rule cấm gọi `transformers.pipeline`.
- **G2**: Sửa `p6-02` §2 EN/VI từ `torch.optim.Adam` dùng ở `p6-04` thành nhắc biến thể tách rời weight decay `AdamW` dùng ở `p6-04`.
- **G3**: Sửa shape `(2, 6)` -> `(2, 5)` trong `p6-04-ex01/prompt.{en,vi}.md` (đã xác nhận trực tiếp khi chạy `encode(["App crashes", "Card charged twice"], max_length=16)`).
- **G4**: Sửa docstring `fine_tune` trong `p6-04-ex02/{starter,solution}.py` bỏ biến `texts`/`labels` chưa định nghĩa và dùng ví dụ `["Bug A", "Bill B"], [0, 1]` -> `a list of 3 floats, e.g. decreasing losses`.
- **G5**: Cập nhật `p6-04-q04` thành `["AdamW", ["0.0005", "5e-4"]]` và `p6-03-q14` thành `[["1", "-1"], ["1", "-1"]]` (đã chạy kiểm tra `dim=-1` cho cùng output `[('POSITIVE', 0.982)]`).
- **G6**: Thêm định nghĩa `dropout` tại `p6-02` §5 EN/VI và thêm term `dropout` vào [glossary.yaml](file:///D:/Proj/python-ai-platform/curriculum/glossary.yaml).
- **G7**: Thêm assert `losses == [round(v, 4) for v in losses]` vào `p6-02-ex01/test_exercise.py`.
- **G8**: Thêm `test_negatives_keeps_exact_threshold_match` (dùng `monkeypatch`) kiểm tra biên `score == threshold` (`>=`) vào `p6-03-ex02/test_exercise.py`.
- **G9**: Đổi `last_loss` trong `p6-02` §5 EN/VI thành trung bình các batch (`total_loss / len(loader)`), cập nhật số chạy thật (`0.8, 0.68, 0.586, 0.519, 0.465`) và thêm câu giải thích vì sao `val_acc` ở epoch 1 là `0.1` (`examples/02_minibatch_loader.py` không in `train_loss` nên không cần đổi).
- **G10**: Sửa Mistake 2 ở `p6-02` EN/VI thành truyền nhãn `float32` có shape `(N,)`.
- **G11**: Thống nhất `.to(torch.float32)` và `round(x.item(), ...)` bỏ bọc `float(...)` ở `p6-04` lesson, `examples/02_before_after.py`, `p6-04-ex02/solution.py`, `p6-04-ex02/alternatives/01_minibatch.py`.
- **G12**: Ghi `(abridged)` / `(rút gọn)` cạnh bảng LOAD REPORT và thêm `hf_logging.disable_progress_bar()` sau `hf_logging.set_verbosity_error()` ở tất cả 6 khối load model của `p6-04/lesson.{en,vi}.md`, `examples/02_before_after.py`, `examples/03_save_and_predict.py` và `p6-04-ex02/{starter,solution,alternatives/01_minibatch}.py`.
- **G13**: Cập nhật `p6-04-ex01/alternatives/01_manual_slicing.{en,vi}.md` giải thích rõ `collections.Counter` là xem trước một công cụ thư viện chuẩn chưa học.
- **G14**: Chuẩn hóa bản VI (`"tỉ lệ đoán đúng (accuracy) trên validation"` ở `p6-02` §5; `"chỉ tốn một nửa bộ nhớ"` ở `p6-01` §1 và flashcard `p6-01-f01`; bỏ `"nhẹ bộ nhớ gấp đôi"` ở `p6-01-q01`; thêm gloss cho `precision` và `recall` ở `p6-04` §8).
- **G15**: Sửa `"except autograd…"` -> `"but autograd…"` ở `p6-01/lesson.en.md` §4.

## 2. Danh sách file đã sửa / tạo (36 file)

- `curriculum/glossary.yaml`
- `curriculum/phase-06-deep-learning/p6-01-tensors/lesson.en.md`
- `curriculum/phase-06-deep-learning/p6-01-tensors/lesson.vi.md`
- `curriculum/phase-06-deep-learning/p6-01-tensors/quiz.yaml`
- `curriculum/phase-06-deep-learning/p6-01-tensors/exercises/ex02-autograd-descent/exercise.yaml`
- `curriculum/phase-06-deep-learning/p6-02-training-loop/lesson.en.md`
- `curriculum/phase-06-deep-learning/p6-02-training-loop/lesson.vi.md`
- `curriculum/phase-06-deep-learning/p6-02-training-loop/quiz.yaml`
- `curriculum/phase-06-deep-learning/p6-02-training-loop/exercises/ex01-fix-training-loop/exercise.yaml`
- `curriculum/phase-06-deep-learning/p6-02-training-loop/exercises/ex01-fix-training-loop/test_exercise.py`
- `curriculum/phase-06-deep-learning/p6-02-training-loop/exercises/ex02-tiny-classifier/exercise.yaml`
- `curriculum/phase-06-deep-learning/p6-02-training-loop/exercises/ex02-tiny-classifier/test_exercise.py`
- `curriculum/phase-06-deep-learning/p6-03-huggingface/quiz.yaml`
- `curriculum/phase-06-deep-learning/p6-03-huggingface/exercises/ex01-count-tokens/exercise.yaml`
- `curriculum/phase-06-deep-learning/p6-03-huggingface/exercises/ex02-triage-feedback/exercise.yaml`
- `curriculum/phase-06-deep-learning/p6-03-huggingface/exercises/ex02-triage-feedback/test_exercise.py`
- `curriculum/phase-06-deep-learning/p6-03-huggingface/exercises/ex02-triage-feedback/alternatives/01_pipeline.en.md`
- `curriculum/phase-06-deep-learning/p6-03-huggingface/exercises/ex02-triage-feedback/alternatives/01_pipeline.vi.md`
- `curriculum/phase-06-deep-learning/p6-04-fine-tune/lesson.en.md`
- `curriculum/phase-06-deep-learning/p6-04-fine-tune/lesson.vi.md`
- `curriculum/phase-06-deep-learning/p6-04-fine-tune/quiz.yaml`
- `curriculum/phase-06-deep-learning/p6-04-fine-tune/examples/02_before_after.py`
- `curriculum/phase-06-deep-learning/p6-04-fine-tune/examples/03_save_and_predict.py`
- `curriculum/phase-06-deep-learning/p6-04-fine-tune/exercises/ex01-prepare-tickets/exercise.yaml`
- `curriculum/phase-06-deep-learning/p6-04-fine-tune/exercises/ex01-prepare-tickets/prompt.en.md`
- `curriculum/phase-06-deep-learning/p6-04-fine-tune/exercises/ex01-prepare-tickets/prompt.vi.md`
- `curriculum/phase-06-deep-learning/p6-04-fine-tune/exercises/ex01-prepare-tickets/alternatives/01_manual_slicing.en.md`
- `curriculum/phase-06-deep-learning/p6-04-fine-tune/exercises/ex01-prepare-tickets/alternatives/01_manual_slicing.vi.md`
- `curriculum/phase-06-deep-learning/p6-04-fine-tune/exercises/ex02-fine-tune-and-evaluate/exercise.yaml`
- `curriculum/phase-06-deep-learning/p6-04-fine-tune/exercises/ex02-fine-tune-and-evaluate/prompt.en.md`
- `curriculum/phase-06-deep-learning/p6-04-fine-tune/exercises/ex02-fine-tune-and-evaluate/prompt.vi.md`
- `curriculum/phase-06-deep-learning/p6-04-fine-tune/exercises/ex02-fine-tune-and-evaluate/solution.py`
- `curriculum/phase-06-deep-learning/p6-04-fine-tune/exercises/ex02-fine-tune-and-evaluate/starter.py`
- `curriculum/phase-06-deep-learning/p6-04-fine-tune/exercises/ex02-fine-tune-and-evaluate/test_exercise.py`
- `curriculum/phase-06-deep-learning/p6-04-fine-tune/exercises/ex02-fine-tune-and-evaluate/alternatives/01_minibatch.py`
- `tasks/m4-p6-review-fixes.report.md` (mới tạo)

## 3. Kết quả lệnh kiểm tra (sau lần sửa cuối)

### `uv run python tools/validate.py --path curriculum/phase-06-deep-learning` (với `HF_HUB_OFFLINE=1`)
```text
OK: 0 error(s), 0 warning(s). Checked 4 lessons, 29 markdown pairs, 12 examples, 8 exercises, 5 alternatives, 64 questions.
```

### `uv run python -m pytest curriculum/phase-06-deep-learning -q` (với `HF_HUB_OFFLINE=1`)
- Kết quả: `54 passed` (`0` failed).

### Script kiểm tra độ dài MCQ (chạy đúng script trong spec)
```text
violations: 0
```
Thống kê thêm số câu đáp án đúng là phương án dài nhất duy nhất (`unique_longest` / tổng MCQ, giới hạn `<= 1/3`):
- `p6-01-tensors/quiz.yaml`: `en: 0/6`, `vi: 0/6` (giới hạn `2.0`)
- `p6-02-training-loop/quiz.yaml`: `en: 1/7`, `vi: 0/7` (giới hạn `2.33`)
- `p6-03-huggingface/quiz.yaml`: `en: 0/6`, `vi: 0/6` (giới hạn `2.0`)
- `p6-04-fine-tune/quiz.yaml`: `en: 0/6`, `vi: 0/6` (giới hạn `2.0`)

### Kiểm tra starter fail từng bài tập (copy `starter.py` thành `exercise.py` trong thư mục tạm, chạy với `-W error` và `HF_HUB_OFFLINE=1`, không đặt `HF_HUB_DISABLE_PROGRESS_BARS`)
| Bài tập | Số test fail / tổng | `stderr` |
|---|---:|---|
| `p6-01-tensors/exercises/ex01-batch-scores` | `5/5` | rỗng (`0`) |
| `p6-01-tensors/exercises/ex02-autograd-descent` | `6/6` | rỗng (`0`) |
| `p6-02-training-loop/exercises/ex01-fix-training-loop` | `4/4` | rỗng (`0`) |
| `p6-02-training-loop/exercises/ex02-tiny-classifier` | `6/6` | rỗng (`0`) |
| `p6-03-huggingface/exercises/ex01-count-tokens` | `5/5` | rỗng (`0`) |
| `p6-03-huggingface/exercises/ex02-triage-feedback` | `6/6` | rỗng (`0`) |
| `p6-04-fine-tune/exercises/ex01-prepare-tickets` | `9/9` | rỗng (`0`) |
| `p6-04-fine-tune/exercises/ex02-fine-tune-and-evaluate` | `13/13` | rỗng (`0`) |
| **Tổng** | **`54/54` fail** | rỗng |

Tất cả 5 file `alternatives/*.py` cũng đã chạy riêng qua pytest với `-W error` và pass toàn bộ (`6/6`, `6/6`, `6/6`, `9/9`, `13/13`), `stderr` rỗng.

### Kiểm tra khối code Python trong bài học & `examples/` với `-W error` (không đặt `HF_HUB_DISABLE_PROGRESS_BARS`, `HF_HUB_OFFLINE=1`)
- `72` khối Python trong `lesson.{en,vi}.md` của cả 4 bài:
  - Toàn bộ khối ở `p6-01`, `p6-02` và `p6-04` đều `rc=0` và `stderr` rỗng (cả 9 khối trong `p6-04/lesson.en.md` và các khối `#3, #4, #6, #9` trong `p6-02/lesson.en.md` khớp hoàn toàn các dòng `# ` output; khối `#1` ở `p6-02` dùng comment nội dòng cho 2 dòng cuối).
  - Riêng 5 khối tải `distilbert` ở `p6-03-huggingface/lesson.{en,vi}.md` (khối #1, #4, #5, #6, #8 — tổng 10 khối EN+VI) chạy `rc=0` nhưng vẫn in progress bar `Loading weights: ...` ra `stderr`; tương tự với `p6-03-huggingface/examples/01_feedback_triage.py` và `03_logits_by_hand.py` (`stderr` dài `191` ký tự). Tất cả `examples/*.py` của `p6-01`, `p6-02` và `p6-04` đều `rc=0` và `stderr` rỗng.

### Kiểm tra `curriculum/glossary.yaml`
- Validate trực tiếp bằng `Draft202012Validator` với `tools/schema/glossary.schema.json` và registry thư mục `tools/schema/`: hợp lệ (`225` terms, term cuối `dropout`).

## 4. Điều còn chưa chắc / Lưu ý
- `p6-03-huggingface` không gọi `hf_logging.disable_progress_bar()` trong 5 khối lesson và 2 file example có nạp model, nên nếu chạy tay mà không đặt `HF_HUB_DISABLE_PROGRESS_BARS` sẽ còn thanh tiến trình `Loading weights` trên `stderr` (mục G12 chỉ yêu cầu áp dụng cho `p6-04`, nên giữ nguyên `p6-03`).
- `tools/validate.py` chỉ chạy với `--path curriculum/phase-06-deep-learning` theo phạm vi task (chưa chạy toàn bộ phase 1–5); riêng `curriculum/glossary.yaml` đã được kiểm tra schema trực tiếp ở trên.
- Trong `p6-02-q01` bản VI, phương án đúng `"Khởi tạo bộ theo dõi của nn.Module để ghi nhận các tầng"` dùng chữ `"để"` như phép dịch sát của `"to register layers"` (mô tả hành vi trực tiếp của lệnh chứ không thêm lý do giải thích phía sau), nhưng nếu kiểm tra bằng từ khóa cứng `"để"` thì vẫn sẽ khớp chuỗi này.

## Vòng 2

### 1. Sửa theo `## Feedback vòng 2`
- [p6-04-fine-tune/exercises/ex02-fine-tune-and-evaluate/exercise.yaml](file:///D:/Proj/python-ai-platform/curriculum/phase-06-deep-learning/p6-04-fine-tune/exercises/ex02-fine-tune-and-evaluate/exercise.yaml) (`hints.en` và `hints.vi`, hint 3):
  - Trong `accuracy`: giữ `model.eval()`, dòng tokenize và `with torch.no_grad():`, thay phần RHS của `preds` thành `preds = ...`.
  - Trong `predict`: giữ `model.eval()`, dòng tokenize, `with torch.no_grad():` và tính `pred_ids`, thay phần return thành `return ...`.
  - Giữ nguyên `fine_tune` và `pick_epoch` như trước, đồng thời thêm một câu nhắc ngắn sau skeleton (không viết lại code đã bỏ) cho cả bản EN và VI.
- [p6-03-huggingface/quiz.yaml](file:///D:/Proj/python-ai-platform/curriculum/phase-06-deep-learning/p6-03-huggingface/quiz.yaml) (`p6-03-q15`, bản `vi`):
  - Đổi `"khi suy đoán"` thành `"khi suy luận (inference)"` ở phương án 3 (distractor). Độ dài các phương án `vi` của `p6-03-q15` là `[83, 81, 77, 91]` (`ans_len=77 <= 1.2 * 85.0 = 102.0`).

### 2. Kết quả lệnh kiểm tra sau sửa vòng 2
- `uv run python tools/validate.py --path curriculum/phase-06-deep-learning` (với `HF_HUB_OFFLINE=1`):
  ```text
  OK: 0 error(s), 0 warning(s). Checked 4 lessons, 29 markdown pairs, 12 examples, 8 exercises, 5 alternatives, 64 questions.
  ```
- `uv run python -m pytest curriculum/phase-06-deep-learning -q` (với `HF_HUB_OFFLINE=1`):
  - Exit code `0`, output: `......................................................                   [100%]` (`54/54` test pass).
- Script kiểm tra độ dài MCQ (toàn phase 6):
  ```text
  violations: 0
  ```
