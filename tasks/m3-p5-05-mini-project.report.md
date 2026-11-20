# Báo cáo triển khai: `m3-p5-05-mini-project` (`p5-05-mini-project`)

## 1. Đã làm gì

- Thiết kế bộ sinh dữ liệu dùng chung `make_ticket_log(n=240, seed=21)` (nhất quán qua mọi khối code trong lesson và examples) thỏa cả 4 ràng buộc kết quả trên tập dữ liệu sạch `231` dòng (`173` train / `58` test, `57` ticket khẩn cấp tổng thể, `14` ticket khẩn cấp trong test):
  1. `DummyClassifier(strategy="most_frequent")` đạt accuracy trên test `0.759` nhưng F1 lớp khẩn cấp = `0.000` (CV F1 = `0.000 +/- 0.000`).
  2. Hai mô hình thật vượt rõ rệt baseline trên 5-fold CV (tập train): `logreg` đạt `0.709 +/- 0.092`, `tree` (`max_depth=3`) đạt `0.701 +/- 0.140`.
  3. Độ chênh giữa hai mô hình thật (`|0.709 - 0.701| = 0.008`) nhỏ hơn độ lệch chuẩn (`0.092` và `0.140`), làm cơ sở cho cảnh báo trung thực.
  4. Khi giữ cột target leakage `escalated_to_oncall`, CV F1 của `logreg` nhảy lên `0.978 +/- 0.027`.
- Viết bài học song ngữ (`lesson.en.md` và `lesson.vi.md`) đầy đủ các mục theo dàn ý: Opening, §1 Kế hoạch (sơ đồ mermaid `flowchart LR` 7 node + bảng 3 mảnh), §2 Nhìn dữ liệu thô (kèm picture in text), §3 Làm sạch & tạo feature (bảng problem/fix + lời mời bấm **Visualize**), §4 Baseline & chọn mô hình bằng CV (bảng kết quả mean/std), §5 Đánh giá một lần trên test (`cross_val_predict`, bảng dò ngưỡng trên train OOF, `confusion_matrix`), §6 Báo cáo trung thực (bảng honest/misleading + callout `[!TIP]`), §7 Lỗi thường gặp (3 lỗi chạy thật: target leakage, chỉnh ngưỡng trên test, bẫy accuracy), §8 Tóm tắt + Đi xa hơn.
- Tạo 3 ví dụ chạy được (`01_raw_ticket_log`, `02_model_selection_cv`, `03_honest_report`) kèm `.out`, `.en.md`, `.vi.md`.
- Tạo 2 bài tập `kind: project` (`difficulty: 3`):
  - `ex01-prepare-features`: hàm `prepare_features(raw)` với 9 test trong `test_exercise.py` và alternative `alternatives/01_boolean_encoding.py` (+ `.en.md`, `.vi.md`).
  - `ex02-evaluate-and-report`: hai hàm `evaluate_models(X, y, seed)` và `write_report(results, n_test)` với 9 hàm test (10 test case nhờ `@pytest.mark.parametrize`) trong `test_exercise.py` và alternative `alternatives/01_manual_folds.py` (+ `.en.md`, `.vi.md`).
- Tạo ngân hàng `quiz.yaml` gồm 16 câu hỏi (`3` dễ, `9` vừa, `4` khó; gồm `8` `mcq`, `3` `output`, `3` `fill`, `2` `parsons`) và 6 flashcard.
- Thêm 2 thuật ngữ mới vào `curriculum/glossary.yaml`: `target leakage` và `holdout set`.
- Chạy `uv run python tools/build_content.py` để cập nhật bundle dữ liệu cho app.
- **Sửa theo Feedback vòng 1 (vòng 2)**:
  1. Sửa khối `mini` đầu §3 trong `lesson.en.md` và `lesson.vi.md`: bỏ lời gọi `make_ticket_log()`, tạo trực tiếp `mini = pd.DataFrame({...})` gồm 5 dòng thô thật (`t003`, `t005`, `t012`, `t003`, `t042`) lấy từ bảng mẫu §2 kèm `hours_since_deploy`, giữ nguyên các bước làm sạch và output. Xác nhận qua `tools.pyrunner.tracer.trace`: chạy hết trong **18 bước** (`< 150`, `truncated=False`, `error=None`), bước cuối `mini` còn đúng 2 dòng (`t003`, `t042`).
  2. Thêm 1 câu ngay sau khối `make_ticket_log` đầu tiên (§2) trong cả `lesson.en.md` và `lesson.vi.md` giải thích rằng hàm này chỉ giả lập bảng log để bài chạy được trong trình duyệt và các khối sau chép lại y hệt để chạy độc lập.

## 2. File đã sửa / tạo mới

### File đã sửa
- `curriculum/glossary.yaml` (thêm 2 thuật ngữ: `target leakage`, `holdout set`)

### Thư mục mới `curriculum/phase-05-ml/p5-05-mini-project/` (34 file)
- `curriculum/phase-05-ml/p5-05-mini-project/meta.yaml`
- `curriculum/phase-05-ml/p5-05-mini-project/lesson.en.md`
- `curriculum/phase-05-ml/p5-05-mini-project/lesson.vi.md`
- `curriculum/phase-05-ml/p5-05-mini-project/quiz.yaml`
- `curriculum/phase-05-ml/p5-05-mini-project/examples/01_raw_ticket_log.py`
- `curriculum/phase-05-ml/p5-05-mini-project/examples/01_raw_ticket_log.out`
- `curriculum/phase-05-ml/p5-05-mini-project/examples/01_raw_ticket_log.en.md`
- `curriculum/phase-05-ml/p5-05-mini-project/examples/01_raw_ticket_log.vi.md`
- `curriculum/phase-05-ml/p5-05-mini-project/examples/02_model_selection_cv.py`
- `curriculum/phase-05-ml/p5-05-mini-project/examples/02_model_selection_cv.out`
- `curriculum/phase-05-ml/p5-05-mini-project/examples/02_model_selection_cv.en.md`
- `curriculum/phase-05-ml/p5-05-mini-project/examples/02_model_selection_cv.vi.md`
- `curriculum/phase-05-ml/p5-05-mini-project/examples/03_honest_report.py`
- `curriculum/phase-05-ml/p5-05-mini-project/examples/03_honest_report.out`
- `curriculum/phase-05-ml/p5-05-mini-project/examples/03_honest_report.en.md`
- `curriculum/phase-05-ml/p5-05-mini-project/examples/03_honest_report.vi.md`
- `curriculum/phase-05-ml/p5-05-mini-project/exercises/ex01-prepare-features/exercise.yaml`
- `curriculum/phase-05-ml/p5-05-mini-project/exercises/ex01-prepare-features/prompt.en.md`
- `curriculum/phase-05-ml/p5-05-mini-project/exercises/ex01-prepare-features/prompt.vi.md`
- `curriculum/phase-05-ml/p5-05-mini-project/exercises/ex01-prepare-features/starter.py`
- `curriculum/phase-05-ml/p5-05-mini-project/exercises/ex01-prepare-features/solution.py`
- `curriculum/phase-05-ml/p5-05-mini-project/exercises/ex01-prepare-features/test_exercise.py`
- `curriculum/phase-05-ml/p5-05-mini-project/exercises/ex01-prepare-features/alternatives/01_boolean_encoding.py`
- `curriculum/phase-05-ml/p5-05-mini-project/exercises/ex01-prepare-features/alternatives/01_boolean_encoding.en.md`
- `curriculum/phase-05-ml/p5-05-mini-project/exercises/ex01-prepare-features/alternatives/01_boolean_encoding.vi.md`
- `curriculum/phase-05-ml/p5-05-mini-project/exercises/ex02-evaluate-and-report/exercise.yaml`
- `curriculum/phase-05-ml/p5-05-mini-project/exercises/ex02-evaluate-and-report/prompt.en.md`
- `curriculum/phase-05-ml/p5-05-mini-project/exercises/ex02-evaluate-and-report/prompt.vi.md`
- `curriculum/phase-05-ml/p5-05-mini-project/exercises/ex02-evaluate-and-report/starter.py`
- `curriculum/phase-05-ml/p5-05-mini-project/exercises/ex02-evaluate-and-report/solution.py`
- `curriculum/phase-05-ml/p5-05-mini-project/exercises/ex02-evaluate-and-report/test_exercise.py`
- `curriculum/phase-05-ml/p5-05-mini-project/exercises/ex02-evaluate-and-report/alternatives/01_manual_folds.py`
- `curriculum/phase-05-ml/p5-05-mini-project/exercises/ex02-evaluate-and-report/alternatives/01_manual_folds.en.md`
- `curriculum/phase-05-ml/p5-05-mini-project/exercises/ex02-evaluate-and-report/alternatives/01_manual_folds.vi.md`

*(Ghi chú: lệnh `tools/build_content.py` ghi file sinh tự động vào `apps/web/src/generated`, đã được gitignore.)*

## 3. Kết quả lệnh kiểm tra

| Lệnh | Kết quả |
|---|---|
| `uv run python tools/validate.py --path curriculum/phase-05-ml/p5-05-mini-project` | `OK: 0 error(s), 0 warning(s). Checked 1 lessons, 8 markdown pairs, 3 examples, 2 alternatives, 2 exercises, 16 questions.` |
| `uv run python tools/validate.py` | `OK: 0 error(s), 0 warning(s). Checked 35 lessons, 272 markdown pairs, 103 examples, 70 exercises, 64 alternatives, 660 questions, 6 exams, 1 portfolio, 1 glossary, 1 interview.` |
| `uv run python -m pytest curriculum/phase-05-ml -W error::UserWarning -W error::FutureWarning` | `68 passed in 1.33s` (exit 0) |
| `uv run ruff check curriculum/phase-05-ml` | `All checks passed!` (exit 0) |
| Kiểm tra pattern cấm (`astype(int)`, `dtype=int`, `.info(`, `fetch_`, `np.random.seed/rand`, `import random`, `open(`) | `0` kết quả trùng (`Grep hits: 0`) |
| Kiểm tra `tools.pyrunner.tracer.trace` trên khối `mini` (§3) | `steps: 18` (`< 150`), `truncated: False`, `error: None`, bước cuối `mini` còn 2 dòng (`t003`, `t042`) |
| `uv run python tools/build_content.py` | `Built 35 lessons, 6 exams, 210 flashcards, 563 questions -> apps\web\src\generated` (exit 0) |
| Chạy 3 example + 9 khối Python trong `lesson.en.md` + 9 khối Python trong `lesson.vi.md` với `-W error::UserWarning -W error::FutureWarning` | Toàn bộ 21 lượt chạy exit 0, stderr rỗng, output khớp 100% comment `# ...`. Chậm nhất trong bài: `lesson.en.md#block4` và `lesson.en.md#block9` = `1.189s`; chậm nhất trong example: `02_model_selection_cv.py` = `1.263s` (đã gồm khởi động process Python + import sklearn). |
| `git status --short` | `M curriculum/glossary.yaml`, `?? curriculum/phase-05-ml/p5-05-mini-project/` (cùng thư mục có sẵn `.hallmark/`, `tasks/`) |

## 4. Điều còn chưa chắc

- **Trình duyệt / Pyodide thật (wasm32)**: Không mở trình duyệt để test trực tiếp giao diện web hay chạy trong Pyodide wasm32 thực tế. Tuy nhiên `tools/validate.py` đã chạy bộ test bài tập qua `tools/pyrunner/runner.py` (browser test runner) và step tracer `tools/pyrunner/tracer.py` đều xanh, đồng thời mọi ép kiểu số nguyên trong bài đều dùng `"int64"` tường minh và tránh in `dtype` mảng NumPy số nguyên hay `df.info()`.
- **Thời gian chạy trên Pyodide**: Trên CPython local, khối chậm nhất trong lesson (`lesson.en.md#block4` và `lesson.en.md#block9`, gồm khởi động tiến trình Python + import sklearn + 5-fold CV) mất `1.189s`, còn `02_model_selection_cv.py` mất `1.263s`. Trên Pyodide trong trình duyệt lần chạy đầu sau khi tải gói có thể mất thêm vài trăm mili-giây nhưng với 231 dòng sạch và 3 mô hình thì vẫn rất nhẹ.
