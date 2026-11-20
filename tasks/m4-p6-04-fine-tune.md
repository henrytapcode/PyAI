# M4 bước 8: p6-04 Mini-project: fine-tune nhỏ

## Mục tiêu
Viết mini-project cuối phase 6 (`p6-04-fine-tune`, `kind: project`, `runner: local`): **fine-tune BERT-Tiny để phân loại ticket hỗ trợ** của một sản phẩm AI, trên CPU, trong vài giây.
- Người học ghép những gì đã học ở phase 6:
  - tensor, autograd (p6-01);
  - vòng lặp training, `eval()` + `no_grad()`, chia train/validation/test (p6-02);
  - tokenizer, model, logits, `id2label` (p6-03).
- Câu chuyện nối từ p6-03: model sentiment có sẵn không hiểu ticket của bạn, nên bạn lấy một model nền nhỏ và dạy nó đúng việc mình cần.
- Ý mới được phép (mỗi ý giới thiệu bằng 1–2 câu):
  - classifier head mới được khởi tạo ngẫu nhiên, và LOAD REPORT nói gì;
  - `model(**batch, labels=y)` trả sẵn `out.loss`;
  - `torch.optim.AdamW` và learning rate nhỏ cho fine-tune;
  - đặt `id2label` / `label2id` khi nạp model;
  - lưu bằng `save_pretrained` vào thư mục tạm rồi nạp lại.
- Bài mẫu về hình dạng mini-project: `curriculum/phase-05-ml/p5-05-mini-project/` (opening, "The plan" có mermaid và bảng các mảnh, 2 bài tập `kind: project`, khoảng 8–9 test mỗi bài, có "Đi xa hơn"). Giọng văn: `curriculum/phase-06-deep-learning/p6-03-huggingface/`.

## Model
Chỉ dùng model `tiny-bert` đã ghim trong `tools/localrunner/models.py` (đã có trong cache):
```python
REPO = "google/bert_uncased_L-2_H-128_A-2"
REV = "30b0a37ccaaa32f332884b96992754e246e48c5f"
```
- Mọi `from_pretrained(...)` truyền `revision=REV, local_files_only=True`. Model phân loại thì thêm `num_labels`, `id2label`, `label2id`.
- **`torch.manual_seed(0)` ngay trước `from_pretrained` của model**: classifier head khởi tạo ngẫu nhiên, và dropout khi train cũng dùng số ngẫu nhiên.
- **LOAD REPORT:** khi nạp với `num_labels`, transformers in ra stderr một bảng UNEXPECTED (`cls.*`) / MISSING (`classifier.*`). Boss đã thử: `from transformers import logging as hf_logging; hf_logging.set_verbosity_error()` trước khi nạp thì stderr rỗng.
  - Bài phải **giải thích** bảng này một lần ở §1: lớp `classifier` mới được tạo ngẫu nhiên, nên phải fine-tune. Cho người học xem bảng dưới dạng fence `text` (chép rút gọn từ lần chạy thật), không in ra từ code.
  - Mọi khối code đều tắt nó bằng dòng trên, kèm comment ngắn.
- Boss đã đo trên máy này: import + nạp tokenizer + nạp model khoảng 3,9 s; 10 bước full-batch trên 40 câu khoảng 0,3 s; chạy hai lần ra cùng số; `-W error` sạch.

## File được phép sửa/tạo
- Thư mục mới `curriculum/phase-06-deep-learning/p6-04-fine-tune/` và mọi file bên trong. **Không** tạo `phase-test.yaml` (bước 9).
- `curriculum/glossary.yaml`: chỉ **thêm** thuật ngữ mới (fine-tuning, classification head, AdamW, overfitting nếu chưa có). Thuật ngữ nào đã có thì bỏ qua.
- `tasks/m4-p6-04-fine-tune.report.md`

## Không được đụng
- `apps/`, `tools/`, `curriculum/syllabus.yaml`, `curriculum/topics.yaml`, `curriculum/conftest.py`, các bài khác, `exams/`, `pyproject.toml`, `uv.lock`.
- Không xóa file, không `git commit`, **không chạy `pnpm --filter web build`**, không chạy server hay dev server ở foreground.
- `meta.yaml` **không** có trường `runner`.

## Quy tắc code (bắt buộc)
Giữ toàn bộ quy tắc phase 6 trong `tasks/m4-p6-01-tensors.md`, `tasks/m4-p6-02-training-loop.md`, `tasks/m4-p6-03-huggingface.md`: seed, không in tensor thô, không `tensor(` trong `.out`, chỉ CPU, `-W error` sạch, **stderr rỗng**, không gọi mạng (kiểm bằng proxy giả như p6-03), thông báo lỗi lấy từ lần chạy thật. Thêm:
- Mỗi khối code dưới 10 s. Lesson có tối đa 6 khối nạp model. Câu quiz có code **không** nạp model hay tokenizer: chỉ torch thuần hoặc Python thuần.
- Lưu file chỉ trong `tempfile.TemporaryDirectory()` (lesson, example) hoặc `tmp_path` (test).
- In accuracy và loss làm tròn 3 chữ số.

## Dữ liệu dùng chung (worker thiết kế, boss duyệt qua output)
- Một hàm ngắn (≤ 15 dòng), giống hệt nhau ở mọi khối dùng nó, ví dụ `make_tickets()`. Hàm ghép chủ ngữ với vấn đề để sinh khoảng 60–90 ticket tiếng Anh ngắn, gồm hai nhãn `bug` và `billing`. Boss đã thử bản 60 câu: trước fine-tune accuracy 0.5, sau 10 bước full batch thì test 1.0.
- Để bài không "quá dễ", thêm:
  - vài ticket mơ hồ, có từ của cả hai lớp, vd "the app crashed during checkout and I was charged";
  - từ đồng nghĩa không có trong lúc train ở tập test.
- Mục tiêu: accuracy sau fine-tune cao rõ rệt so với trước (trước khoảng 0.5), nhưng không nhất thiết 1.0.
- Chia train / validation / test bằng `torch.randperm` với generator có seed. Chọn số epoch bằng validation. Test chỉ dùng **một lần** ở cuối.
- Worker chạy thật và chọn seed/tham số, **không bịa số**.

## Nội dung bài (boss chốt dàn ý, worker viết)
Opening (không heading): ở p6-03 model sentiment chấm sai ticket của bạn. Team hỗ trợ muốn tự động chuyển ticket về đúng nhóm (kỹ thuật hay thanh toán). Bạn sẽ dạy một model nền 4,4 triệu tham số làm việc đó trên CPU trong vài giây. Một câu: gần như không có gì mới, bạn ghép p6-01 tới p6-03.

1. **The plan** (VI: "Kế hoạch").
   - **Mermaid** `flowchart LR` (≤ 8 node): tickets → split → tokenizer → BERT-Tiny + head mới → training loop (chọn epoch bằng validation) → test một lần → lưu → dự đoán ticket mới.
   - **Bảng các mảnh** `| step | tool | from lesson |`.
2. **Dữ liệu ticket.** `make_tickets()`, đếm mỗi lớp, in 4 ticket mẫu, chia train/val/test, in kích thước. **Picture in text**: một ticket đi qua tokenizer thành ids rồi ra nhãn.
3. **Model nền và head mới.**
   - Nạp với `num_labels=2`, `id2label`, `label2id`.
   - Fence `text` chép LOAD REPORT rút gọn kèm giải thích: phần thân (encoder) đã học tiếng Anh; phần head `classifier` mới được tạo ngẫu nhiên.
   - Đo accuracy trên validation **trước** fine-tune: khoảng 0.5, đúng như đoán mò.
   - In số tham số.
4. **Fine-tune.**
   - Vòng lặp p6-02, khác ở hai chỗ:
     - `out = model(**batch, labels=y)` rồi dùng `out.loss`;
     - `AdamW` với lr nhỏ (vd `5e-4`; giải thích một câu vì sao fine-tune dùng lr nhỏ: không phá kiến thức có sẵn).
   - In train loss và val accuracy theo epoch.
   - **Trace table** `| epoch | train loss | val accuracy |`, số khớp output thật.
   - Chọn epoch tốt nhất bằng validation.
5. **Đánh giá một lần trên test.**
   - Accuracy trước / sau trên test.
   - In các ticket test bị đoán sai, nếu có. Nếu không có thì nói thẳng rằng test nhỏ nên con số này dao động mạnh.
   - **Bảng so sánh** `| | before fine-tune | after fine-tune |`.
   - Callout `[!WARNING]`: test có 15–20 câu thì mỗi câu sai là 5–7 điểm phần trăm. Đừng khoe "100%".
6. **Lưu, nạp lại, dự đoán ticket mới.**
   - `model.save_pretrained(tmp)` cùng `tokenizer.save_pretrained(tmp)`, rồi `from_pretrained(tmp)`; dự đoán 3–4 ticket mới viết tay. Có thể dùng `pipeline("text-classification", model=..., tokenizer=...)` từ object đã nạp.
   - In nhãn chữ nhờ `id2label`.
   - Một câu: thư mục này là thứ bạn sẽ đưa vào service ở phase 8.
7. **Lỗi thường gặp** (VI: `## 7. Lỗi thường gặp`):
   - Quên `torch.manual_seed(0)` trước khi nạp: accuracy trước fine-tune đổi mỗi lần chạy. Cho thấy bằng hai seed khác nhau ra hai số khác nhau.
   - lr quá lớn (vd `1e-1`): loss không giảm hoặc nhảy loạn, accuracy kẹt ở một lớp. In số thật.
   - Đánh giá mà quên `model.eval()`: dropout vẫn bật, nên hai lần đánh giá cùng dữ liệu ra logits khác nhau. In `True` / `False` khi so bằng `torch.equal`.
   - Chọn epoch bằng test: lỗi tư duy, trỏ lại p6-02 §5.
8. **Đi xa hơn** (VI: "Đi xa hơn"), 3–4 gạch đầu dòng, không code:
   - thêm lớp thứ ba (`feature request`);
   - nhiều dữ liệu thật hơn và đo precision/recall theo lớp (p5-04);
   - model lớn hơn hoặc GPU;
   - LoRA (chỉ nhắc tên, để "Đọc thêm").
9. **Recap / Tóm tắt**: 4–6 gạch đầu dòng.

- Một lời mời **Visualize** cho một khối ngắn **không nạp model** (vd hàm tính accuracy trên logits tự đặt, hoặc vòng chọn epoch tốt nhất từ list val accuracy), dưới 600 step; worker tự kiểm bằng `tracer.trace`.
- Thời lượng 25–35 phút. `review_by: "2027-05-01"`. `tags: [huggingface, pytorch]` (có thể thêm `dl`). `prerequisites: [p6-03-huggingface]`. `further_reading`: Hugging Face LLM Course chương 3 "Fine-tuning a pretrained model" và model card BERT-Tiny của google trên huggingface.co (mở thử để chắc URL còn sống).

## Examples (3)
- `01_ticket_dataset`: sinh dữ liệu, chia, in số câu mỗi lớp ở mỗi tập, và số token dài nhất (cần tokenizer, không cần model).
- `02_before_after`: nạp, đo test trước, fine-tune với số epoch đã chọn, đo test sau. In hai con số và độ chênh.
- `03_save_and_predict`: fine-tune ngắn, `save_pretrained` vào thư mục tạm, nạp lại, dự đoán 4 ticket mới; in `label  text`.

## Exercises (2, `kind: project`)
Starter của cả hai bài import được, đã nạp sẵn tokenizer ở mức module (dùng đúng `REPO`/`REV`/`local_files_only=True`, kèm `hf_logging.set_verbosity_error()`), và fail **mọi** test với thông báo dễ hiểu khi trả `None`.
- `ex01-prepare-tickets`, 8–9 test, **không** nạp model (nhanh):
  - `split_data(texts, labels, val_frac, test_frac, seed) -> tuple[list[str], list[int], list[str], list[int], list[str], list[int]]`. Xáo bằng `torch.randperm` với generator có seed; giữ đúng cặp text–label; ba tập không trùng nhau; kích thước đúng; cùng seed ra cùng kết quả.
  - `encode(texts, max_length) -> dict[str, torch.Tensor]` có `input_ids` và `attention_mask`, dùng padding và truncation, `return_tensors="pt"`. Test kiểm shape `(N, ≤ max_length)` và giá trị của mask.
  - `class_counts(labels) -> dict[int, int]`.
  - `alternatives/01_manual_slicing.py`: chia bằng chỉ số tự tính, không cắt list trực tiếp (hoặc một cách khác thật sự khác); kèm `.md`.
- `ex02-fine-tune-and-evaluate`, 8–9 test:
  - Starter cung cấp sẵn `load_model()`: seed rồi nạp `tiny-bert` với `num_labels=2`, `id2label={0: "bug", 1: "billing"}`. Người học không viết phần nạp.
  - `accuracy(model, texts, labels) -> float`: `eval()`, `no_grad()`, làm tròn 3 chữ số, kiểu `float`.
  - `fine_tune(model, texts, labels, lr, epochs) -> list[float]`: full batch, AdamW, `model.train()`, trả train loss mỗi epoch (`float`, làm tròn 4).
  - `predict(model, texts) -> list[str]`: nhãn chữ qua `id2label`.
  - Test, dùng dữ liệu nhỏ viết sẵn trong file test, 20–30 câu:
    - độ dài và kiểu của list loss;
    - loss cuối nhỏ hơn loss đầu;
    - accuracy sau fine-tune ≥ một ngưỡng mà bản lỗi không đạt; worker đo và ghi vào report;
    - accuracy là `float` trong `[0, 1]`;
    - `accuracy` không tạo gradient (`p.grad is None` với model vừa nạp);
    - `accuracy` gọi hai lần ra cùng số (bắt lỗi quên `eval()`);
    - `predict` trả nhãn chữ trong `{"bug", "billing"}` và đúng trên 2 câu rõ ràng sau khi fine-tune;
    - `epochs=0` trả `[]` và không đổi trọng số.
  - Toàn bộ test của ex02 chạy dưới 30 s (đo bằng `runner.run_tests` gọi trực tiếp và bằng pytest; ghi vào report).
  - `alternatives/01_minibatch.py`: `fine_tune` dùng `DataLoader` batch 8, `num_workers=0`, generator có seed; kèm `.md`.
- Hint 3 tầng đúng CONTENT_GUIDE. Hint 3 để trống ít nhất 2–3 dòng thật sự.

## Quiz
- 15–18 câu, mỗi loại `mcq`, `output`, `fill`, `parsons` ít nhất 2; khoảng 5 dễ, 7 vừa, 3 khó. 6 flashcard. Tag: `huggingface` (chính), có thể thêm `pytorch`.
- Code trong quiz không nạp model hay tokenizer.
- Phải có câu về: vì sao head mới cho accuracy khoảng 0.5; vì sao lr nhỏ; `labels=` trả `out.loss`; chọn epoch bằng validation; `eval()` và dropout; test nhỏ thì accuracy dao động.

## Tiêu chí hoàn thành (checklist)
1. [ ] Đủ file theo layout CONTENT_GUIDE. `meta.yaml` có `phase: p6`, `order: 4`, `kind: project`, `tags` gồm `huggingface`, `prerequisites: [p6-03-huggingface]`, `outcomes` khớp syllabus (có thể thêm 1–2 dòng), không có `runner`.
2. [ ] Lesson đúng dàn ý, đủ: mermaid, bảng các mảnh, trace table, picture in text, bảng so sánh, một lời mời Visualize, callout, "Đi xa hơn".
3. [ ] Code giữa `lesson.en.md` và `lesson.vi.md` giống hệt, chỉ khác comment; số dòng mermaid bằng nhau; fence `text` giống hệt.
4. [ ] Tuân thủ quy tắc code: stderr rỗng, không gọi mạng (kiểm bằng proxy giả), mỗi khối dưới 10 s. Các lệnh grep bên dưới rỗng.
5. [ ] Số liệu thật: accuracy trước khoảng 0.5, sau cao rõ rệt; chạy hai lần ra cùng số.
6. [ ] Exercise: starter fail **mọi** test (ghi số test pass với starter vào report: phải là 0); solution và alternative pass (pytest **và** browser runner trong validate).
7. [ ] Bản VI tự nhiên, xưng "bạn", thuật ngữ giữ tiếng Anh kèm giải nghĩa lần đầu, vd "fine-tune (huấn luyện tiếp trên dữ liệu của bạn)".
8. [ ] Report ghi: thời gian từng khối nạp model, thời gian test ex02, thời gian `validate.py --path`, số step của khối Visualize.
9. [ ] Lệnh kiểm tra xanh, chạy đúng như ghi.

## Lệnh kiểm tra
Từ gốc repo `D:\Proj\python-ai-platform`:
```
uv run python tools/validate.py --path curriculum/phase-06-deep-learning/p6-04-fine-tune
uv run python tools/validate.py --fast
uv run python -m pytest curriculum/phase-06-deep-learning
uv run ruff check curriculum/phase-06-deep-learning
grep -rnE "\.cuda\(|to\(\"cuda|astype\(int\)|dtype=int\b|\.info\(|print\(model\)|num_workers=[1-9]" curriculum/phase-06-deep-learning/p6-04-fine-tune
grep -rln "tensor(" curriculum/phase-06-deep-learning --include=*.out
uv run python tools/build_content.py
git status --short
```
Mong đợi: validate 0 lỗi; pytest exit 0; ruff sạch; hai lệnh grep rỗng; thay đổi chỉ nằm trong `curriculum/phase-06-deep-learning/p6-04-fine-tune/` và `glossary.yaml`.

## Ghi chú cho worker
- Đọc `docs/CONTENT_GUIDE.md` (mục "phase 6+"), ba spec p6 trước (quy tắc), `curriculum/phase-05-ml/p5-05-mini-project/` (hình dạng mini-project), rồi bài `p6-03-huggingface`.
- transformers 5.23.0: API có thể khác trí nhớ của bạn. Đọc `help()` hoặc source trong `.venv` khi không chắc, và ghi vào report những gì khác.
- Test chỉ dùng: assert, pytest.raises, pytest.approx, pytest.mark.parametrize, `tmp_path`, và `@pytest.fixture` định nghĩa trong file test.
- Dùng `uv run python -m pytest`, không dùng `uv run pytest`. Trên Windows dùng Git Bash cho `grep`.
- Mọi lệnh phải tự kết thúc. Không chạy server ở foreground.

## Trạng thái
- Bước hiện tại: xong (đã commit `9f4a819`)
- Vòng: 1/3
- Số lần swap: 0
- Fallback: không
- Model: Gemini 4 Hydrogen (High)
