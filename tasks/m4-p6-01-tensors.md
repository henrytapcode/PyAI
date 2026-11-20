# M4 bước 5: bài p6-01 Tensors & autograd

## Mục tiêu
Viết bài đầu tiên của phase 6 (`p6-01-tensors`) trong thư mục mới `curriculum/phase-06-deep-learning/` (tên thư mục theo khối `p6` trong `curriculum/syllabus.yaml`), đúng `docs/CONTENT_GUIDE.md`, song ngữ EN/VI.
- Bài có `runner: local` trong syllabus. Trong app, code chạy bằng CPython qua runner cục bộ (`tools/localrunner/`), không chạy trong Pyodide. Validate vẫn chạy mọi khối code bằng CPython như các bài khác.
- Người học đã xong phase 1–5: NumPy (array, shape, `axis`, broadcasting, `@`), pandas, matplotlib, scikit-learn. Bài `p5-01-math-bridge` đã dạy vector, dot product, MSE loss, độ dốc ước lượng bằng số (`(loss(w + h) - loss(w - h)) / (2 * h)`) và gradient descent bằng tay. Bài này nối tiếp đúng chỗ đó: PyTorch làm y như vậy, nhưng tự tính gradient.
- Bài mẫu về giọng văn và hình dạng: `curriculum/phase-05-ml/p5-01-math-bridge/` (đã duyệt và đã sửa theo review).

## File được phép sửa/tạo
- Thư mục mới `curriculum/phase-06-deep-learning/p6-01-tensors/` và mọi file bên trong. Nếu validator đòi file cấp phase cho `curriculum/phase-06-deep-learning/` thì tạo đúng file đó và ghi rõ trong report. **Không** tạo `phase-test.yaml`.
- `curriculum/topics.yaml`: chỉ **thêm** một dòng tag `pytorch:      { en: "PyTorch", vi: "PyTorch" }` ngay sau dòng `dl:`.
- `curriculum/glossary.yaml`: chỉ **thêm** thuật ngữ mới (tensor, autograd, computation graph, backward pass, leaf tensor). Thuật ngữ nào đã có thì bỏ qua.
- `tasks/m4-p6-01-tensors.report.md`

## Không được đụng
- `apps/`, `tools/`, `curriculum/syllabus.yaml`, phase 0–5, `exams/`, `pyproject.toml`, `uv.lock`.
- Không xóa file, không `git commit`, **không chạy `pnpm --filter web build`**, không chạy server hay dev server ở foreground.
- `meta.yaml` **không** có trường `runner`; trường này chỉ nằm trong syllabus.

## Quy tắc code phase 6 (bắt buộc, xem CONTENT_GUIDE mục "phase 6+")
- Giữ mọi quy tắc "Data & ML code (phase 4+)".
- Khối nào có ngẫu nhiên (`torch.rand`, `torch.randn`) thì gọi `torch.manual_seed(0)` ở đầu khối.
- **Không in tensor thô.** Mọi output và `.out` không được chứa chuỗi `tensor(`.
  - Số đơn: `round(t.item(), 3)`.
  - Nhiều số: `[round(v, 3) for v in t.tolist()]`; với 2D thì làm tròn từng hàng.
  - Shape: in `tuple(t.shape)` → `(2, 3)`, không in `torch.Size([2, 3])`.
  - In `t.dtype` thì được (ra `torch.float32`, giống nhau trên mọi máy vì bài chạy CPython). Riêng mảng NumPy số nguyên vẫn không in dtype.
  - Duy nhất §3 được *nói* về repr của tensor (để giải thích vì sao không in thô), và đặt nó trong comment, không in ra.
- Chỉ CPU, không gọi `.cuda()` hay `.to("cuda")`. GPU chỉ nhắc một câu trong callout `[!NOTE]`.
- Mỗi khối code chạy dưới 10 giây (`import torch` mất khoảng 2 giây). Dữ liệu nhỏ, vòng lặp ngắn.
- Code chạy với `python -W error` không có cảnh báo.
- Thông báo lỗi trong "Lỗi thường gặp" lấy từ lần chạy thật bằng torch 2.15.0, chỉ giữ dòng cuối (`RuntimeError: ...`). Thông báo dài quá 100 ký tự thì được cắt bằng `...`, nhưng phần giữ lại phải đúng nguyên văn.
- Chỉ dùng thứ đã dạy ở phase 1–5. Thứ mới của PyTorch phải được giới thiệu bằng một câu ở lần dùng đầu tiên.

## Nội dung bài (boss chốt dàn ý, worker viết)
Opening (không heading): mọi mạng neural, từ model nhận diện ảnh tới LLM, đều là tensor nhân với nhau. Ở p5-01 bạn tự tính độ dốc bằng số. PyTorch làm hai việc giúp bạn: tính toán như NumPy, và **tự tính gradient**.

1. **Tensor là array của PyTorch.**
   - `torch.tensor([...])`, `tuple(t.shape)`, `t.dtype`; số thực mặc định là `float32` (NumPy là `float64`). Nói một câu vì sao: deep learning dùng float32 để nhanh và nhẹ.
   - `torch.zeros`, `torch.ones`, `torch.arange`; `torch.rand` kèm `torch.manual_seed(0)`.
   - Chuyển qua lại với NumPy: `torch.from_numpy(a)` và `t.numpy()`.
   - **Picture in text** (fence `text`): tensor shape `(2, 3)` với chỉ số hàng/cột.
2. **Phép tính giống NumPy.**
   - Phép tính từng phần tử, broadcasting, `@` (nhân ma trận), `.sum()` / `.mean()` với `dim=` (giống `axis=` của NumPy).
   - **Bảng so sánh** `| NumPy | PyTorch |`: `np.array` / `torch.tensor`, `a.shape` / `t.shape`, `axis=0` / `dim=0`, `a @ b` / `t @ u`, `float(a.sum())` / `t.sum().item()`.
   - Ví dụ thực tế: batch 3 request × 4 feature nhân vector weights → 3 điểm (nối với `01_feature_scores` của p5-01).
3. **In tensor cho dễ đọc.** `.item()` cho một số, `.tolist()` cho nhiều số, rồi làm tròn. Vì sao: repr của tensor kèm `tensor(...)`, `requires_grad`, `grad_fn`, khó đọc, và chữ số cuối của float32 có thể lệch. `.item()` chỉ dùng được với tensor đúng một phần tử.
4. **Autograd: gradient tự động.**
   - `requires_grad=True` đánh dấu tensor cần gradient (gọi là leaf tensor). Tính loss, gọi `loss.backward()`, đọc `w.grad`.
   - So sánh với p5-01: cùng loss MSE của `y = w * x`, tính độ dốc bằng số (`h = 0.001`) và bằng autograd, in cả hai đã làm tròn 3 chữ số. Hai số phải khớp.
   - **Mermaid** `flowchart LR` (≤ 8 node): computation graph `w` và `x` → `w * x` → `- y` → `** 2` → `mean` → `loss`. Một câu: `backward()` đi ngược đồ thị này để tính gradient.
5. **Gradient descent với autograd.**
   - Vòng lặp đầy đủ: forward → loss → `loss.backward()` → `with torch.no_grad(): w -= lr * w.grad` → `w.grad.zero_()`.
   - Giải thích `torch.no_grad()` (bước cập nhật không được ghi vào đồ thị) và `zero_()` (PyTorch **cộng dồn** gradient sau mỗi lần `backward`).
   - **Trace table** `| step | w | loss | w.grad |` cho 3–4 bước, số khớp output thật.
   - Đây là section mời bấm **Visualize** (khối ngắn, 3 bước, dưới 600 step; boss đã thử tracer với khối kiểu này: khoảng 30 step, chạy 4 giây).
   - Callout `[!NOTE]`: trong bài sau, `torch.optim` làm sẵn hai dòng `no_grad` và `zero_()` này. GPU (`.cuda()`) chỉ nhắc ở đây và ở "Đọc thêm".
6. **Lỗi thường gặp** (VI: `## 6. Lỗi thường gặp`), chạy thật để lấy đúng output:
   - Quên `w.grad.zero_()`: gradient cộng dồn, in `w.grad` sau hai lần `backward` để thấy giá trị gấp đôi.
   - Cập nhật `w -= lr * w.grad` ngoài `torch.no_grad()` → `RuntimeError` về leaf Variable dùng trong in-place operation.
   - `.item()` trên tensor nhiều phần tử → `RuntimeError` (a Tensor with 3 elements cannot be converted to Scalar).
   - Nhân ma trận lệch shape (`(3, 4) @ (3,)`) → `RuntimeError` về shape. In `tuple(t.shape)` để tìm lỗi.
7. **Recap / Tóm tắt**: 4–6 gạch đầu dòng.

Thời lượng 15–18 phút. `review_by: "2027-11-01"`. `tags: [pytorch, dl]`. `prerequisites: [p5-01-math-bridge]`. `further_reading`: PyTorch tutorial "Tensors" và "Automatic Differentiation with torch.autograd" (URL chính thức trên pytorch.org/tutorials, mở thử để chắc URL còn sống).

## Examples (3)
- `01_batch_scores`: batch 4 request × 3 feature (tokens nghìn, latency giây, số tin nhắn) là một tensor `(4, 3)`; weights `(3,)` và bias; điểm từng request bằng `@`; in shape, điểm đã làm tròn, và index request điểm cao nhất (`.argmax().item()`).
- `02_autograd_check`: một loss nhỏ hai tham số `w`, `b` (MSE của `w * x + b` trên 5 điểm); in gradient của autograd và gradient tính bằng số cho cả `w` và `b`, cùng một dòng "match: True" (so bằng `abs(a - b) < 1e-3`).
- `03_fit_line_autograd`: làm lại `03_fit_a_line` của p5-01 (dữ liệu tokens → latency gần thẳng hàng) bằng autograd. In loss mỗi 20 step và `w`, `b` cuối, làm tròn 3 chữ số. Không vẽ hình.

## Exercises (2)
- `ex01-batch-scores` (`kind: fill`): `score_batch(features: torch.Tensor, weights: torch.Tensor, bias: float) -> list[float]` trả `[round(v, 3) for v in (features @ weights + bias).tolist()]`. Các ô `___` nằm trong thân hàm. 4–5 test:
  - giá trị đúng (`pytest.approx`);
  - trả `list` gồm `float` Python;
  - batch 1 dòng trả list 1 phần tử;
  - weights sai độ dài → `pytest.raises(RuntimeError)`.
- `ex02-autograd-descent` (`kind: code`): hai hàm.
  - `slope_at(w_value: float, xs: torch.Tensor, ys: torch.Tensor) -> float`: gradient của `mean((w * xs - ys) ** 2)` theo `w` tại `w_value`, dùng autograd, trả `round(..., 3)` kiểu `float`.
  - `fit_slope(xs, ys, lr: float, steps: int) -> float`: bắt đầu `w = 0.0`, gradient descent bằng autograd `steps` lần, trả `round(w, 3)` kiểu `float`.
  - 5–6 test:
    - `slope_at` khớp công thức `mean(2 * (w * xs - ys) * xs)` (`pytest.approx`);
    - gọi `slope_at` hai lần cùng giá trị ra cùng kết quả (bắt lỗi cộng dồn nếu học viên dùng chung tensor);
    - `fit_slope` với `ys = 3 * xs` hội tụ gần `3.0` (`pytest.approx(..., abs=0.05)`);
    - `steps=0` → `0.0`;
    - kiểu trả về là `float` Python, không phải tensor.
  - Chọn `lr` và `steps` trong test để hội tụ chắc chắn mà mỗi test chạy dưới 0,5 giây.
  - Có `alternatives/01_manual_gradient.py`: tính gradient bằng công thức viết tay với tensor, không dùng autograd. File `.md` đi kèm nói khi nào cách này ổn (model nhỏ, biết công thức) và vì sao autograd thắng khi model có hàng triệu tham số.
- Hint 3 tầng đúng CONTENT_GUIDE. Hint 3 để trống ít nhất 2–3 dòng thật sự.

## Quiz
- 15–18 câu, mỗi loại `mcq`, `output`, `fill`, `parsons` ít nhất 2; khoảng 5 dễ, 7 vừa, 3 khó. 6 flashcard.
- Tag: `pytorch` (chính), có thể thêm `dl`.
- Câu `output` in số đã làm tròn, không in tensor thô.
- Phải có ít nhất một câu về việc gradient cộng dồn và một câu về `float32`.

## Tiêu chí hoàn thành (checklist)
1. [ ] Đủ file theo layout CONTENT_GUIDE. `meta.yaml` có `phase: p6`, `order: 1`, `tags` gồm `pytorch`, `prerequisites: [p5-01-math-bridge]`, `outcomes` khớp syllabus (có thể thêm 1–2 dòng), không có `runner`.
2. [ ] Lesson đúng dàn ý, đủ: mermaid, trace table, picture in text, bảng so sánh, một lời mời Visualize, callout.
3. [ ] Code giữa `lesson.en.md` và `lesson.vi.md` giống hệt, chỉ khác comment; số dòng mermaid bằng nhau; fence `text` giống hệt.
4. [ ] Tuân thủ "Quy tắc code phase 6". Lệnh grep bên dưới phải rỗng.
5. [ ] Exercise: starter fail; solution và alternative pass (pytest **và** browser runner trong validate).
6. [ ] Bản VI tự nhiên, xưng "bạn", thuật ngữ giữ tiếng Anh kèm giải nghĩa lần đầu, vd "tensor (mảng nhiều chiều của PyTorch)".
7. [ ] Report ghi thời gian chạy của khối code chậm nhất và của `uv run python tools/validate.py --path ...`.
8. [ ] Lệnh kiểm tra xanh, chạy đúng như ghi. Chạy `uv run python tools/build_content.py`.

## Lệnh kiểm tra
Từ gốc repo `D:\Proj\python-ai-platform`:
```
uv run python tools/validate.py --path curriculum/phase-06-deep-learning/p6-01-tensors
uv run python tools/validate.py
uv run python -m pytest curriculum/phase-06-deep-learning
uv run ruff check curriculum/phase-06-deep-learning
grep -rnE "\.cuda\(|to\(\"cuda|astype\(int\)|dtype=int\b|\.info\(" curriculum/phase-06-deep-learning
grep -rln "tensor(" curriculum/phase-06-deep-learning --include=*.out
uv run python tools/build_content.py
git status --short
```
Mong đợi: validate 0 lỗi; pytest exit 0; ruff sạch; hai lệnh grep rỗng; file mới chỉ nằm trong `curriculum/phase-06-deep-learning/`, cộng `topics.yaml` và `glossary.yaml`.

## Ghi chú cho worker
- Đọc `docs/CONTENT_GUIDE.md` (nhất là mục "phase 6+"), rồi `curriculum/phase-05-ml/p5-01-math-bridge/`.
- Test chỉ dùng: assert, pytest.raises, pytest.approx, pytest.mark.parametrize, và `@pytest.fixture` định nghĩa trong file test.
- Dùng `uv run python -m pytest`, không dùng `uv run pytest`.
- Validate toàn bộ mất khoảng 5–6 phút; mọi lệnh đều tự kết thúc. Không chạy server ở foreground.
- Kiểm cảnh báo bằng `uv run python -W error <file>`.

## Trạng thái
- Bước hiện tại: 5 (đạt vòng 2; boss kiểm: validate toàn bộ 0 lỗi, 11 test, ruff sạch, typecheck + build xanh; trong app qua runner cục bộ: Run §5 đúng, Visualize 43 bước, starter ex02 0/6 với thông báo rõ; đã commit `8e210d4`)
- Vòng: 2/3
- Số lần swap: 0
- Fallback: không
- Model: Gemini 4 Hydrogen (High)

## Feedback vòng 1
Boss đã kiểm: mọi khối code trong lesson chạy với `-W error` và khớp comment; 11 test pass; ruff sạch; grep rỗng. Trong app (runner cục bộ): Run khối §5 ra đúng 4 dòng, Visualize 43 bước, chấm ex02 với starter ra 1/6. Bài tốt. Sửa 3 điểm nhỏ:

1. **§5 nói "five moves" / "năm thao tác" nhưng chỉ liệt kê bốn.** Sửa thành "four moves" / "bốn thao tác" ở cả `lesson.en.md` và `lesson.vi.md`.
2. **§3 nói chữ số cuối của float32 "drift slightly across runs" / "có thể lệch nhẹ".** Trên cùng máy, cùng phiên bản, kết quả không đổi giữa các lần chạy. Viết lại: chữ số cuối có thể khác nhau giữa các phiên bản PyTorch hoặc các máy, nên làm tròn để output ổn định. Sửa cả EN và VI.
3. **ex02: `test_slope_at_does_not_accumulate_across_calls` pass với starter** (`None == None`), nên người học thấy một test xanh dù chưa viết gì.
   - Thêm `assert first == pytest.approx(-18.667)` (với `xs = [1, 2, 3]`, `ys = [3, 6, 9]`, `w = 1.0`: `mean(-4 * xs ** 2)`) trước khi so `first == second`.
   - Các test so bằng `pytest.approx` đang ra `TypeError: unsupported operand type(s) for -: 'NoneType' and 'float'` khi hàm trả `None`, khó hiểu với người mới. Ở đầu mỗi test đó, thêm `assert result is not None, "slope_at returned None: did you forget to return the value?"` (tương tự cho `fit_slope`).
   - Làm tương tự cho ex01 nếu ex01 có test bị lỗi như vậy khi starter đã được điền sai (kiểm bằng cách chạy test với starter đã điền `___` bằng `None`; nếu không áp dụng được thì bỏ qua).
   - Sau khi sửa: starter phải pass **0** test của ex02.

Chạy lại lệnh kiểm tra (validate cho bài và pytest là đủ, không cần validate toàn bộ) và thêm mục "Vòng 2" vào report.
