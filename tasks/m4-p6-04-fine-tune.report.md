# Báo cáo thực hiện `m4-p6-04-fine-tune`

## 1. Đã làm gì

Đã implement đầy đủ mini-project **Fine-tuning BERT-Tiny cho phân loại ticket hỗ trợ (`bug` vs `billing`)** (`p6-04-fine-tune`, `kind: project`, `runner: local`) chạy hoàn toàn offline trên CPU theo đúng spec `tasks/m4-p6-04-fine-tune.md`:

- **Metadata (`meta.yaml`)**: `id: p6-04-fine-tune`, `phase: p6`, `order: 4`, `kind: project`, `tags: [huggingface, pytorch, dl]`, `prerequisites: [p6-03-huggingface]`, `duration_min: 30`, `review_by: "2027-05-01"`, không khai báo `runner` trong `meta.yaml`. Hai URL `further_reading` (`huggingface.co/learn/llm-course/chapter3/1` và `huggingface.co/google/bert_uncased_L-2_H-128_A-2`) đều kiểm tra HTTP `200`.
- **Glossary (`curriculum/glossary.yaml`)**: Bổ sung `classification head` và `AdamW` (còn `fine-tuning` và `overfitting` đã tồn tại sẵn trong file).
- **Bài học song ngữ (`lesson.en.md`, `lesson.vi.md`)**:
  - Mở đầu trực quan không phụ thuộc bài trước; §1 sơ đồ `flowchart LR` (8 node) + bảng ánh xạ tác vụ; §2 bộ dữ liệu `make_tickets()` gồm 80 ticket (`40` bug, `40` billing) chia `48 train / 16 val / 16 test` bằng `torch.Generator().manual_seed(27)`; §3 tải `google/bert_uncased_L-2_H-128_A-2` (`revision="30b0a37ccaaa32f332884b96992754e246e48c5f"`, `local_files_only=True`) cho thấy `4,386,178` tham số và `val_acc=0.5` trước khi fine-tune; §4 vòng lặp 10 epoch (`AdamW`, `lr=5e-4`, loss `0.712 -> 0.254`, `val_acc` `0.5 -> 1.0`) kèm khối Visualize (`22` bước tracer); §5 đánh giá 1 lần trên test (`0.562 -> 0.938`, 15/16, chỉ nhầm `"Timeout right when submitting receipt"`), bảng so sánh trước/sau và `[!WARNING]`; §6 lưu/tải lại qua `save_pretrained` vào `tempfile.TemporaryDirectory()` và dự đoán 4 ticket mới (`bug 0.807`, `billing 0.749`, `bug 0.787`, `billing 0.776`); §7 4 lỗi thường gặp (chạy 2 seed khác nhau trên 6 câu cho `0.333` vs `0.5`, `lr=1e-1` làm `val_acc=0.5`, thiếu `model.eval()` trên `nn.Dropout(0.5)`, nhìn trộm tập test); §8 hướng mở rộng & Recap.
  - Tổng cộng đúng **6** block load model Hugging Face trong bài học (mỗi block đều có `# no network needed` và chạy offline với `local_files_only=True`).
- **3 Ví dụ (`examples/01_*` .. `03_*`)**: Khớp `.py`, `.out`, `.en.md`, `.vi.md`, stderr rỗng dưới `-W error` và `HF_HUB_DISABLE_PROGRESS_BARS=1`.
- **2 Bài tập (`exercises/ex01-prepare-tickets`, `exercises/ex02-fine-tune-and-evaluate`)**:
  - `ex01`: 9 test (starter đạt `0/9`, solution và alternative `01_manual_slicing.py` đạt `9/9`).
  - `ex02`: 8 test (starter đạt `0/8`, solution và alternative `01_minibatch.py` đạt `8/8`, ngưỡng đánh giá `0.85`).
- **Quiz (`quiz.yaml`)**: 16 câu (`p6-04-q01`..`q16`: 6 `mcq`, 4 `output`, 3 `fill`, 3 `parsons`; 5 easy, 8 medium, 3 hard; 0 lần load model/tokenizer HF) và 6 flashcard (`p6-04-f01`..`f06`). Tất cả câu `parsons` (`p6-04-q05`, `p6-04-q10`, `p6-04-q16`) đều `<= 8` dòng (`PARSONS_MAX_LINES`) và có thứ tự duy nhất (được `validate.py --path` kiểm tra, `0` lỗi).

### Ghi chú hành vi `transformers 5.23.0` / `torch 2.15.0+cpu` đã quan sát
- Khi load `BertForSequenceClassification` với `num_labels=2`, `transformers 5.23.0` in `LOAD REPORT` ra stderr (`cls.*` là `UNEXPECTED`, `classifier.weight`/`classifier.bias` là `MISSING`); dùng `transformers.logging.set_verbosity_error()` sẽ ẩn báo cáo này.
- Thanh tiến độ `Loading weights:` (tqdm) cần `HF_HUB_DISABLE_PROGRESS_BARS=1` để giữ stderr rỗng (biến môi trường này đã được `tools/validate.py`, `curriculum/conftest.py` và `tools/localrunner/server.py` thiết lập sẵn).
- Toàn bộ thao tác `from_pretrained(..., local_files_only=True)` và `save_pretrained` / nạp lại từ `TemporaryDirectory` đều chạy thành công khi chặn mạng bằng fake proxy `127.0.0.1:9` mà không cần `HF_HUB_OFFLINE`.

---

## 2. File đã sửa / tạo mới

### File đã sửa
- `curriculum/glossary.yaml` (chỉ thêm 2 term `classification head` và `AdamW`)

### File đã tạo mới (32 file trong `curriculum/phase-06-deep-learning/p6-04-fine-tune/`)
- `curriculum/phase-06-deep-learning/p6-04-fine-tune/meta.yaml`
- `curriculum/phase-06-deep-learning/p6-04-fine-tune/lesson.en.md`
- `curriculum/phase-06-deep-learning/p6-04-fine-tune/lesson.vi.md`
- `curriculum/phase-06-deep-learning/p6-04-fine-tune/quiz.yaml`
- `curriculum/phase-06-deep-learning/p6-04-fine-tune/examples/01_ticket_dataset.{py,out,en.md,vi.md}` (4 file)
- `curriculum/phase-06-deep-learning/p6-04-fine-tune/examples/02_before_after.{py,out,en.md,vi.md}` (4 file)
- `curriculum/phase-06-deep-learning/p6-04-fine-tune/examples/03_save_and_predict.{py,out,en.md,vi.md}` (4 file)
- `curriculum/phase-06-deep-learning/p6-04-fine-tune/exercises/ex01-prepare-tickets/{exercise.yaml,prompt.en.md,prompt.vi.md,starter.py,solution.py,test_exercise.py}` (6 file)
- `curriculum/phase-06-deep-learning/p6-04-fine-tune/exercises/ex01-prepare-tickets/alternatives/01_manual_slicing.{py,en.md,vi.md}` (3 file)
- `curriculum/phase-06-deep-learning/p6-04-fine-tune/exercises/ex02-fine-tune-and-evaluate/{exercise.yaml,prompt.en.md,prompt.vi.md,starter.py,solution.py,test_exercise.py}` (6 file)
- `curriculum/phase-06-deep-learning/p6-04-fine-tune/exercises/ex02-fine-tune-and-evaluate/alternatives/01_minibatch.{py,en.md,vi.md}` (3 file)
- Báo cáo này: `tasks/m4-p6-04-fine-tune.report.md`

*(Không chạm tới `apps/`, `tools/`, `curriculum/syllabus.yaml`, `curriculum/topics.yaml`, `curriculum/conftest.py`, `exams/`, `pyproject.toml`, `uv.lock`, hay các bài học khác; không tạo `phase-test.yaml`.)*

---

## 3. Kết quả lệnh kiểm tra & đo đạc

### Các lệnh kiểm tra trong spec
| Lệnh kiểm tra | Kết quả |
| --- | --- |
| `uv run python tools/validate.py --path curriculum/phase-06-deep-learning/p6-04-fine-tune` | **PASS** — `OK: 0 error(s), 0 warning(s). Checked 1 lessons, 8 markdown pairs, 3 examples, 2 alternatives, 2 exercises, 16 questions.` (`ELAPSED=52.67s`, `RC=0`) |
| `uv run python tools/validate.py --fast` | **PASS** — `OK: 0 error(s), 0 warning(s). Checked 39 lessons, 301 markdown pairs, 115 examples, 78 exercises, 69 alternatives, 766 questions, 8 exams, 1 portfolio, 1 glossary, 1 interview.` |
| `uv run python -m pytest curriculum/phase-06-deep-learning` | **PASS** — `48 passed in 5.82s` |
| `uv run ruff check curriculum/phase-06-deep-learning` | **PASS** — `All checks passed!` |
| Regex kiểm tra mẫu cấm trong `p6-04-fine-tune` (`\.cuda\(|to\("cuda|astype\(int\)|dtype=int\b|\.info\(|print\(model\)|num_workers=[1-9]`) | **PASS** — `GREP1_HITS: 0 []` (kiểm tra bằng Python `re` vì `bash` trên Windows trỏ tới WSL chưa cài distro) |
| Regex kiểm tra `tensor(` trong `curriculum/phase-06-deep-learning/**/*.out` | **PASS** — `GREP2_HITS: 0 []` |
| `uv run python tools/build_content.py` | **PASS** — `Built 39 lessons, 8 exams, 234 flashcards, 627 questions -> apps\web\src\generated` |
| `git status --short` | `M curriculum/glossary.yaml`, `?? .hallmark/`, `?? curriculum/phase-06-deep-learning/p6-04-fine-tune/`, `?? tasks/` |

### Đo thời gian & kiểm tra offline chi tiết
- **Chạy toàn bộ 9 block Python trong `lesson.en.md` với fake proxy (`HTTPS_PROXY=http://127.0.0.1:9`, `HTTP_PROXY=http://127.0.0.1:9`, bỏ `HF_HUB_OFFLINE`/`TRANSFORMERS_OFFLINE`, bật `HF_HUB_DISABLE_PROGRESS_BARS=1`, `-W error`)**:
  - Block 1 (§2 data, `hf=False`): `rc=0`, `1.41s`, `stderr_len=0`
  - Block 2 (§3 load model #1, `hf=True`): `rc=0`, `3.80s`, `stderr_len=0`
  - Block 3 (§4 training loop #2, `hf=True`): `rc=0`, `4.05s`, `stderr_len=0`
  - Block 4 (§4 Visualize, `hf=False`): `rc=0`, `0.04s`, `stderr_len=0` — `tracer.trace` ghi nhận `22` bước (`truncated=False`, `error=None`)
  - Block 5 (§5 one-time test #3, `hf=True`): `rc=0`, `4.15s`, `stderr_len=0`
  - Block 6 (§6 save & predict #4, `hf=True`): `rc=0`, `4.36s`, `stderr_len=0`
  - Block 7 (§7.1 seed variance #5, `hf=True`): `rc=0`, `4.10s`, `stderr_len=0` (`seed=0: val_acc=0.333`, `seed=1: val_acc=0.5`)
  - Block 8 (§7.2 lr quá lớn #6, `hf=True`): `rc=0`, `4.19s`, `stderr_len=0`
  - Block 9 (§7.3 `eval()`/`train()` dropout, `hf=False`): `rc=0`, `1.54s`, `stderr_len=0`
- **3 Ví dụ (`01`..`03`) với fake proxy `127.0.0.1:9`, `-W error`, `HF_HUB_DISABLE_PROGRESS_BARS=1`**: đều `rc=0`, `stderr` rỗng, khớp file `.out`.
- **Bài tập `ex01` và `ex02` qua `tools/pyrunner/runner.py` (`run_tests`)**:
  - `ex01`: `starter` `ok=False` (`0/9`, `2.23s`), `solution` `ok=True` (`9/9`, `0.01s`), `alternatives/01_manual_slicing.py` `ok=True` (`9/9`, `0.01s`).
  - `ex02`: `starter` `ok=False` (`0/8`, `1.93s`), `solution` `ok=True` (`8/8`, `1.42s`), `alternatives/01_minibatch.py` `ok=True` (`8/8`, `3.31s`).
- **Đo riêng `ex02` với `pytest` và kiểm tra ngưỡng `0.85`**:
  - `uv run python -m pytest curriculum/phase-06-deep-learning/p6-04-fine-tune/exercises/ex02-fine-tune-and-evaluate/test_exercise.py`: `8 passed in 4.39s` (tổng thời gian process `5.62s`, dưới 30s).
  - So sánh hàm `fine_tune` lỗi (bỏ `optimizer.step()`): `acc_before = 0.5`, `acc_broken_no_step = 0.5` (< ngưỡng `0.85`), sau `fine_tune` đúng đạt `1.0` (>= `0.85`).

---

## 4. Điều còn chưa chắc

1. **Giao diện Web & Local Runner thực tế**: Theo ràng buộc không chạy server/dev server và không chạy `pnpm --filter web build`, nên chưa kiểm tra trực tiếp bài học, sơ đồ Mermaid và `ex02` chạy end-to-end qua web UI + `tools/localrunner/server.py` (dù đã kiểm tra qua `validate.py --path`, `pytest` và `build_content.py`).
2. **Thư mục `.hallmark/` trong `git status`**: Thư mục untracked `.hallmark/` đã có sẵn trong working tree từ trước, không phải do tác vụ này tạo ra và không bị tác vụ xóa/sửa.
3. **Lệnh `grep` POSIX trên Windows**: Lệnh `bash -lc "grep ..."` gọi WSL chưa cài distro trên máy này; kiểm tra đã được thực hiện tương đương bằng Python `re` trên đúng tập file và mẫu regex trong spec.
