# M4 bước 6: bài p6-02 The training loop

## Mục tiêu
Viết bài `p6-02-training-loop` trong `curriculum/phase-06-deep-learning/`, đúng `docs/CONTENT_GUIDE.md`, song ngữ EN/VI.
- Bài có `runner: local` trong syllabus. Trong app, code chạy bằng CPython qua runner cục bộ. Validate vẫn chạy mọi khối code như các bài khác.
- Người học vừa xong `p6-01-tensors`: tensor, `@`, `dim=`, `.item()` / `.tolist()`, `requires_grad`, `loss.backward()`, cập nhật trong `torch.no_grad()`, `w.grad.zero_()`. Ở phase 5 họ đã biết train/test split, accuracy, và quy tắc "test set chỉ dùng một lần".
- Bài này đi từ vòng lặp viết tay của p6-01 sang cách viết chuẩn của PyTorch: `nn.Module`, loss có sẵn, `torch.optim`, `DataLoader`, lưu và nạp model, đánh giá.
- Bài mẫu về giọng văn và hình dạng: `curriculum/phase-06-deep-learning/p6-01-tensors/` (đã duyệt, commit `8e210d4`).

## File được phép sửa/tạo
- Thư mục mới `curriculum/phase-06-deep-learning/p6-02-training-loop/` và mọi file bên trong. **Không** tạo `phase-test.yaml`.
- `curriculum/glossary.yaml`: chỉ **thêm** thuật ngữ mới (epoch, batch, optimizer, logits, state_dict). Thuật ngữ nào đã có thì bỏ qua.
- `tasks/m4-p6-02-training-loop.report.md`

## Không được đụng
- `apps/`, `tools/`, `curriculum/syllabus.yaml`, `curriculum/topics.yaml`, phase 0–5, `p6-01-tensors`, `exams/`, `pyproject.toml`, `uv.lock`.
- Không xóa file, không `git commit`, **không chạy `pnpm --filter web build`**, không chạy server hay dev server ở foreground.
- `meta.yaml` **không** có trường `runner`.

## Quy tắc code phase 6 (bắt buộc)
Giữ nguyên toàn bộ mục "Quy tắc code phase 6" trong `tasks/m4-p6-01-tensors.md`: seed, không in tensor thô, không chuỗi `tensor(` trong `.out`, in shape bằng `tuple(...)`, chỉ CPU, mỗi khối dưới 10 giây, `-W error` sạch, thông báo lỗi lấy từ lần chạy thật. Thêm:
- **`torch.manual_seed(0)` đặt trước khi tạo model**, vì `nn.Linear` khởi tạo trọng số ngẫu nhiên. Khối nào tạo model hoặc dữ liệu ngẫu nhiên đều phải có seed ở đầu khối.
- `DataLoader` luôn có `num_workers=0`. Nếu `shuffle=True` thì truyền `generator=torch.Generator().manual_seed(0)` để thứ tự lặp lại được.
- Lưu file chỉ trong `tempfile.TemporaryDirectory()`. Nạp bằng `torch.load(path, weights_only=True)`.
- Không in `model` hay `print(model.state_dict())` (repr có tensor). Muốn cho xem cấu trúc thì in tên và shape: `[(name, tuple(p.shape)) for name, p in model.named_parameters()]`.
- In loss bằng `round(loss.item(), 3)` (hoặc 4 chữ số nếu cần thấy thay đổi). Không in quá 6–8 dòng loss mỗi khối: in mỗi N epoch.
- Dữ liệu tổng hợp (synthetic) nhỏ, tạo bằng `torch.randn` có seed, tối đa vài trăm điểm, 2 feature.
- Test set chỉ dùng một lần ở cuối. Chọn learning rate hay số epoch thì dùng validation split cắt từ train.

## Nội dung bài (boss chốt dàn ý, worker viết)
Opening (không heading): mọi model deep learning, từ mạng nhỏ trong bài này tới LLM, đều được train bằng cùng một vòng lặp năm dòng. Ở p6-01 bạn đã viết nó bằng tay cho một tham số `w`. Bài này dạy cách PyTorch đóng gói từng phần để vòng lặp đó chạy được cho model có hàng nghìn tham số.

1. **Model là một `nn.Module`.**
   - `nn.Linear(in_features, out_features)` là `x @ W.T + b` với trọng số tự tạo và tự `requires_grad`.
   - Viết một class `class TinyNet(nn.Module)` có `__init__` (gọi `super().__init__()`, tạo các layer) và `forward(self, x)`. Nhắc lại OOP ở phase 2 bằng một câu.
   - `nn.ReLU()` giới thiệu bằng một câu: giữ số dương, đổi số âm thành 0, để model học được đường cong chứ không chỉ đường thẳng.
   - In `named_parameters()` dạng tên + shape, và tổng số tham số bằng `sum(p.numel() for p in model.parameters())`.
   - **Picture in text** (fence `text`): luồng shape `(N, 2) → Linear(2, 8) → (N, 8) → ReLU → (N, 8) → Linear(8, 2) → (N, 2)`.
2. **Loss và optimizer có sẵn.**
   - `nn.CrossEntropyLoss()` nhận **logits** (điểm thô, chưa qua softmax) shape `(N, C)` và nhãn `int64` shape `(N,)`. Một câu: model trả logits, nhãn dự đoán là `logits.argmax(dim=1)`.
   - `torch.optim.SGD(model.parameters(), lr=...)`: `optimizer.zero_grad()` thay cho `w.grad.zero_()`, `optimizer.step()` thay cho `with torch.no_grad(): w -= lr * w.grad`.
   - **Bảng so sánh** `| p6-01 (by hand) | PyTorch way |`: `w.grad.zero_()` / `optimizer.zero_grad()`, `w -= lr * w.grad` trong `no_grad` / `optimizer.step()`, công thức MSE tự viết / `nn.MSELoss()` hoặc `nn.CrossEntropyLoss()`, `w * x + b` / `model(x)`.
   - Nhắc `torch.optim.Adam` trong một câu (thường hội tụ nhanh hơn, dùng ở p6-04).
3. **Vòng lặp training.**
   - Năm dòng chuẩn: `logits = model(xb)` → `loss = loss_fn(logits, yb)` → `optimizer.zero_grad()` → `loss.backward()` → `optimizer.step()`.
   - **Mermaid** `flowchart TD` (≤ 8 node): batch → forward → loss → zero_grad → backward → step → còn batch? → epoch tiếp.
   - Ví dụ đầu tiên chạy trên toàn bộ dữ liệu một lần mỗi epoch (chưa có DataLoader). Dữ liệu: hai đám điểm 2D, lớp 0 quanh `(-1, -1)`, lớp 1 quanh `(1, 1)`.
   - **Trace table** `| epoch | loss | accuracy |` cho 4–5 mốc, số khớp output thật.
   - Section mời bấm **Visualize**: một khối **riêng, ngắn** (model `nn.Linear(1, 1)`, 4 điểm, `torch.optim.SGD`, 3 epoch), dưới 600 step. Boss sẽ kiểm số step trong app; worker tự kiểm bằng `tools/pyrunner/tracer.py` (gọi `tracer.trace(code)`, xem `len(steps)` và `truncated`).
4. **Epoch, batch và `DataLoader`.**
   - **Epoch** là một lượt đi qua toàn bộ dữ liệu; **batch** là một nhóm nhỏ mẫu dùng cho một bước cập nhật.
   - `TensorDataset(X, y)` và `DataLoader(dataset, batch_size=16, shuffle=True, num_workers=0, generator=...)`.
   - In số batch mỗi epoch (`len(loader)`) và shape của batch đầu tiên.
   - Callout `[!TIP]`: `num_workers=0` giữ mọi thứ trong một process, đơn giản và dễ debug. Dữ liệu lớn mới cần nhiều worker.
5. **Đánh giá: `model.eval()` và `torch.no_grad()`.**
   - Chia train / validation / test từ đầu (vd 60/20/20 bằng `torch.randperm` có seed). Vòng lặp in train loss và validation accuracy mỗi N epoch.
   - `model.eval()` + `with torch.no_grad():` khi đánh giá. Giải thích: `no_grad` không dựng đồ thị nên nhanh và nhẹ; `eval()` báo cho các layer như dropout biết đang đánh giá (model này chưa có dropout nhưng nên tập thói quen). Quay lại `model.train()` trước khi train tiếp.
   - Test accuracy chỉ tính **một lần** ở cuối, sau khi đã chọn số epoch bằng validation.
6. **Lưu và nạp model.**
   - `torch.save(model.state_dict(), path)` trong `tempfile.TemporaryDirectory()`; tạo model mới cùng class, `load_state_dict(torch.load(path, weights_only=True))`, `eval()`.
   - In accuracy của model nạp lại bằng đúng accuracy của model gốc. In `True` cho phép so dự đoán: `torch.equal(pred_a, pred_b)`.
   - Một câu: `state_dict` chỉ lưu các con số (trọng số), không lưu code của class, nên phải có class để nạp lại.
7. **Lỗi thường gặp** (VI: `## 7. Lỗi thường gặp`), chạy thật để lấy đúng output:
   - Quên `optimizer.zero_grad()`: gradient cộng dồn, loss dao động hoặc giảm chậm. In loss vài epoch của bản sai và bản đúng cạnh nhau.
   - Nhãn sai kiểu cho `CrossEntropyLoss` (`float` thay cho `int64`, shape `(N, 1)`) → `RuntimeError`. Lấy dòng cuối thông báo thật, cắt bớt nếu dài.
   - Đánh giá mà quên `torch.no_grad()`: không sai số, nhưng `requires_grad` vẫn bật. In `preds.requires_grad` (`True`) rồi bản đúng (`False`).
   - Dùng test set để chọn số epoch: không có lỗi in ra, đây là lỗi tư duy. Giải thích ngắn và trỏ lại phase 5.
8. **Recap / Tóm tắt**: 4–6 gạch đầu dòng.

Thời lượng 15–20 phút. `review_by: "2027-11-01"`. `tags: [pytorch, dl]`. `prerequisites: [p6-01-tensors]`. `further_reading`: PyTorch tutorial "Build the Neural Network" và "Optimizing Model Parameters" (URL chính thức trên pytorch.org/tutorials, mở thử để chắc URL còn sống).

## Examples (3)
- `01_two_blobs`: hai đám điểm 2D (200 điểm), `TinyNet` 2 → 8 → 2, SGD, 30 epoch full batch. In loss mỗi 10 epoch và accuracy cuối trên train.
- `02_minibatch_loader`: cùng dữ liệu, có `DataLoader` batch 32, split train/val/test. In val accuracy mỗi 5 epoch, rồi test accuracy một lần ở cuối.
- `03_save_and_reload`: train ngắn, lưu `state_dict` vào thư mục tạm, nạp vào model mới, in hai accuracy bằng nhau và `same predictions: True`.

## Exercises (2)
- `ex01-fix-training-loop` (`kind: debug`): hàm `train(model, xs, ys, lr, epochs) -> list[float]` trả danh sách loss mỗi epoch (`float` Python, làm tròn 4 chữ số). Starter **chạy được** nhưng có 2 lỗi:
  - thiếu `optimizer.zero_grad()`;
  - ghi `losses.append(loss)` (tensor) thay cho `round(loss.item(), 4)`.
  - Test (4–5, dùng model `nn.Linear(1, 1)` tạo trong test, có `torch.manual_seed(0)`, dữ liệu `y = 2x + 1`):
    - độ dài danh sách bằng `epochs`;
    - mọi phần tử là `float` Python;
    - loss cuối nhỏ hơn loss đầu;
    - loss cuối dưới một ngưỡng chỉ đạt được khi đã sửa `zero_grad` (worker chạy thử bản lỗi để chọn ngưỡng; ghi số đo vào report);
    - weight của model sau khi train gần `2.0` (`pytest.approx`, `abs` phù hợp).
  - Prompt nói rõ "hàm chạy được nhưng kết quả sai; có 2 lỗi".
- `ex02-tiny-classifier` (`kind: code`):
  - `class TinyClassifier(nn.Module)`: `__init__(self, in_features: int, hidden: int, classes: int)` tạo `Linear → ReLU → Linear`; `forward(self, x)` trả logits.
  - `accuracy(model: nn.Module, xs: torch.Tensor, ys: torch.Tensor) -> float`: dùng `model.eval()` và `torch.no_grad()`, trả tỉ lệ đúng làm tròn 3 chữ số, kiểu `float`.
  - Test 5–6:
    - output shape `(N, classes)`;
    - số tham số đúng với `in_features=2, hidden=8, classes=3` (`2*8 + 8 + 8*3 + 3 = 51`);
    - `accuracy` trên một model có trọng số đặt tay cho kết quả biết trước (đặt trọng số bằng `torch.no_grad()` trong test, hoặc một model giả viết trong file test);
    - `accuracy` trả `float` trong `[0, 1]`;
    - sau khi gọi `accuracy`, gradient không được tạo (`p.grad is None` cho mọi tham số);
    - train ngắn trên hai đám điểm thì accuracy ≥ 0.9.
  - Starter: skeleton class và hàm có docstring, `# TODO`, `pass` / `return None`. Starter phải import được và fail mọi test, kèm thông báo dễ hiểu khi trả `None` (như vòng 2 của p6-01).
  - `alternatives/01_sequential.py`: dựng model bằng `nn.Sequential` bên trong class. `.md` giải thích khi nào `Sequential` đủ, khi nào cần `forward` tự viết.
- Hint 3 tầng đúng CONTENT_GUIDE. Hint 3 để trống ít nhất 2–3 dòng thật sự.
- Mọi test chạy dưới 1 giây mỗi cái.

## Quiz
- 15–18 câu, mỗi loại `mcq`, `output`, `fill`, `parsons` ít nhất 2; khoảng 5 dễ, 7 vừa, 3 khó. 6 flashcard.
- Tag: `pytorch` (chính), có thể thêm `dl`.
- Phải có: một câu về thứ tự `zero_grad → backward → step`, một câu về logits và `argmax(dim=1)`, một câu về `eval()` + `no_grad()`, một câu về test set chỉ dùng một lần.
- Parsons về vòng lặp training phải chỉ có một thứ tự đúng (ràng buộc bằng biến hoặc bằng output in ra).

## Tiêu chí hoàn thành (checklist)
1. [ ] Đủ file theo layout CONTENT_GUIDE. `meta.yaml` có `phase: p6`, `order: 2`, `tags` gồm `pytorch`, `prerequisites: [p6-01-tensors]`, `outcomes` khớp syllabus (có thể thêm 1–2 dòng), không có `runner`.
2. [ ] Lesson đúng dàn ý, đủ: mermaid, trace table, picture in text, bảng so sánh, một lời mời Visualize (khối dưới 600 step), callout.
3. [ ] Code giữa `lesson.en.md` và `lesson.vi.md` giống hệt, chỉ khác comment; số dòng mermaid bằng nhau; fence `text` giống hệt.
4. [ ] Tuân thủ quy tắc code phase 6. Các lệnh grep bên dưới đều rỗng.
5. [ ] Exercise: starter fail **mọi** test (ghi số test pass với starter vào report: phải là 0); solution và alternative pass (pytest **và** browser runner trong validate).
6. [ ] Bản VI tự nhiên, xưng "bạn", thuật ngữ giữ tiếng Anh kèm giải nghĩa lần đầu, vd "epoch (một lượt qua toàn bộ dữ liệu)".
7. [ ] Report ghi: thời gian khối code chậm nhất, số step của khối Visualize, thời gian `validate.py --path`.
8. [ ] Lệnh kiểm tra xanh, chạy đúng như ghi.

## Lệnh kiểm tra
Từ gốc repo `D:\Proj\python-ai-platform`:
```
uv run python tools/validate.py --path curriculum/phase-06-deep-learning/p6-02-training-loop
uv run python -m pytest curriculum/phase-06-deep-learning
uv run ruff check curriculum/phase-06-deep-learning
grep -rnE "\.cuda\(|to\(\"cuda|astype\(int\)|dtype=int\b|\.info\(|print\(model\)|num_workers=[1-9]" curriculum/phase-06-deep-learning/p6-02-training-loop
grep -rln "tensor(" curriculum/phase-06-deep-learning --include=*.out
uv run python tools/build_content.py
git status --short
```
Mong đợi: validate 0 lỗi; pytest exit 0; ruff sạch; hai lệnh grep rỗng; file mới chỉ nằm trong `curriculum/phase-06-deep-learning/p6-02-training-loop/`, cộng `glossary.yaml`. Không cần chạy validate toàn bộ (boss sẽ chạy).

## Ghi chú cho worker
- Đọc `docs/CONTENT_GUIDE.md` (mục "phase 6+"), `tasks/m4-p6-01-tensors.md` (quy tắc), rồi bài `curriculum/phase-06-deep-learning/p6-01-tensors/`.
- Test chỉ dùng: assert, pytest.raises, pytest.approx, pytest.mark.parametrize, `tmp_path`, và `@pytest.fixture` định nghĩa trong file test.
- Dùng `uv run python -m pytest`, không dùng `uv run pytest`. Trên Windows có thể không có `grep` trong PATH; dùng Git Bash hoặc tương đương, và ghi rõ trong report.
- Mọi lệnh phải tự kết thúc. Không chạy server ở foreground.
- Kiểm cảnh báo bằng `uv run python -W error <file>`.

## Trạng thái
- Bước hiện tại: 5 (đạt vòng 2; boss kiểm: validate toàn bộ 0 lỗi, 21 test, ruff sạch, typecheck + build xanh; trong app qua runner cục bộ: Visualize 31 bước, starter ex01 0/4; đã commit `6e192a8`)
- Vòng: 2/3
- Số lần swap: 0
- Fallback: không
- Model: Gemini 4 Hydrogen (High)

## Feedback vòng 1
Boss đã kiểm: mọi khối code chạy với `-W error` và khớp comment; 21 test pass; ruff sạch; grep rỗng. Trong app (runner cục bộ): Visualize khối `nn.Linear(1, 1)` 31 bước đúng số; starter ex01 0/4 với thông báo rõ. Bài tốt. Sửa 1 điểm:

1. **§6 và `examples/03_save_and_reload.py` (nếu cũng vậy): model được train trên chính `X_eval` / `y_eval` rồi đo accuracy trên cùng dữ liệu đó.** Bài vừa dạy ở §5 rằng phải tách train / validation / test, nên tên `X_eval` cho dữ liệu dùng để train dễ làm người học hiểu sai.
   - Đổi tên thành `X_train` / `y_train`.
   - Thêm một câu (EN và VI, cùng vị trí) sau khối code: ở đây ta đo trên dữ liệu train chỉ để so model gốc với model nạp lại; muốn biết model tốt đến đâu thì vẫn dùng validation/test như §5.
   - Output không đổi; chạy lại để chắc. Sửa cả `.out` và `.en.md` / `.vi.md` của example nếu có nhắc tên biến.

Chạy lại `validate --path`, pytest, ruff cho bài này và thêm mục "Vòng 2" vào report.
