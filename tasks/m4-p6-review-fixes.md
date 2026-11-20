# M4 bước 8b: sửa phase 6 theo review

## Mục tiêu
Sửa các lỗi reviewer (Opus) tìm ra trong 4 bài phase 6 (`curriculum/phase-06-deep-learning/`). Chỉ sửa nội dung, không thêm bài mới. Mọi sửa đổi làm ở cả EN và VI, giữ parity (code block giống nhau trừ `#` comment, text fence giống hệt, mermaid cùng số dòng).

## File được phép sửa/tạo
- Mọi file trong `curriculum/phase-06-deep-learning/**`
- `curriculum/glossary.yaml` (chỉ thêm term `dropout` nếu chưa có)
- `tasks/m4-p6-review-fixes.report.md`

## Không được đụng
- `tools/**`, `apps/**`, `curriculum/syllabus.yaml`, `curriculum/topics.yaml`, các phase khác, `docs/**`.

## Việc cần làm

### A. MCQ để lộ đáp án qua độ dài (cao), cả 4 `quiz.yaml`
Hiện 24/25 câu `mcq` có đáp án đúng là phương án dài nhất. Với **mọi** câu `mcq` ở phase 6:
- Đáp án đúng không được kèm lý do ("because…", "so that…", "vì…", "để…"). Chuyển lý do sang `explanation`.
- Bốn phương án có độ dài gần nhau: `len(correct) <= 1.2 × trung bình len(distractor)` ở **cả en và vi**. Kéo dài distractor bằng một hiểu lầm cụ thể, không thêm chữ độn.
- Đáp án đúng không được là phương án dài nhất duy nhất ở quá 1/3 số câu `mcq` của mỗi file.
- Giữ nguyên `answer` (index), id và số câu. Kiểm tra lại explanation vẫn khớp.
Kiểm bằng script ở mục Lệnh kiểm tra.

### B. Hint không leo thang (cao)
Áp dụng cho: p6-01-ex02, p6-02-ex01, p6-02-ex02, p6-03-ex01, p6-03-ex02, p6-04-ex01, p6-04-ex02 (`exercise.yaml`, en và vi).
- Hint 1: chỉ ra ý tưởng và mục trong bài, kèm kết quả cho một input cụ thể.
- Hint 2: các bước **bằng lời** (danh sách đánh số). **Không** có biểu thức Python hoàn chỉnh. Được nhắc tên hàm/method (`model.eval()`, `torch.no_grad()`), nhưng không viết nguyên dòng code.
- Hint 3: skeleton trong python fence. Còn 1–2 chỗ `...` ở đúng phần khó, và phần này hint 2 chưa nói thẳng. Hint 3 phải cho **nhiều** thông tin hơn hint 2, không phải ít hơn (p6-03-ex01 hint 3 hiện gần như chính là starter, cần sửa).
- Ghép hint 2 với hint 3 **không** được ra nguyên solution.

### C. p6-04 §4: chọn epoch (trung bình), `lesson.en.md` và `lesson.vi.md`
- Khối training loop: in thêm `val_loss` (lấy `model(**val_batch, labels=val_y).loss` trong `no_grad`, rồi `round(float(...), 3)`). Cập nhật các dòng `#` output và bảng epoch (thêm cột val loss) bằng số chạy thật.
- Khối Visualize `history`: các tuple là `(epoch, val_acc, val_loss)`. Luật chọn: `val_acc` cao nhất, hòa thì chọn `val_loss` thấp hơn. Bỏ hoàn toàn việc phá hòa bằng train loss. Sửa câu dẫn và câu kết.
- Nói rõ chỉ quét 1–10 epoch. Ở `## 8. Going further`, thêm một ý: val loss vẫn còn giảm ở epoch 10, nên có thể quét dài hơn.
- Thêm 1 câu ở §4: "AdamW = Adam + weight decay (decoupled), the common default for fine-tuning transformers." (VI tương ứng).

### D. p6-04 §5: "đánh giá test một lần" (trung bình)
Giữ hai con số trước/sau, nhưng sửa lời văn cho khỏi mâu thuẫn. Test set chỉ được dùng cho báo cáo cuối. Con số "before" chỉ để tham khảo, không dùng để ra quyết định nào, vì mọi quyết định (số epoch) đã chốt bằng validation. Sửa tiêu đề/câu "once" cho đúng ý đó.

### E. p6-04-ex02: thêm `pick_epoch` (trung bình)
- Thêm hàm `pick_epoch(history: list[tuple[int, float, float]]) -> int`, với mỗi tuple là `(epoch, val_acc, val_loss)`. Trả epoch có `val_acc` cao nhất. Hòa thì lấy `val_loss` thấp hơn. Vẫn hòa thì lấy epoch sớm nhất.
- Starter trả `None` và có docstring kèm ví dụ. Solution và `alternatives/01_minibatch.py` đều phải có hàm này.
- Thêm 3 test: chọn theo val_acc; hòa val_acc thì chọn theo val_loss; hòa cả hai thì chọn epoch sớm nhất. Test chỉ dùng list thuần, không load model.
- Cập nhật `prompt.*.md` (thêm phần, ví dụ, Rules) và hint.
- Starter phải fail mọi test (kể cả 3 test mới).

### F. Test thiếu `no_grad` và `train()` (trung bình)
- p6-02-ex02 `test_accuracy_sets_eval_mode_and_creates_no_gradients` và p6-04-ex02 `test_accuracy_matches_seeded_baseline_and_creates_no_gradients`: kiểm `p.grad is None` là vô nghĩa. Thay bằng một model thăm dò định nghĩa trong test file: lớp con `nn.Module` có `forward` ghi lại `torch.is_grad_enabled()` vào một list, rồi trả logits hợp lệ.
  - p6-04: model thăm dò nhận `**batch` và trả object có `.logits`, ví dụ `types.SimpleNamespace(logits=...)`.
  - Assert mọi giá trị ghi lại là `False`, kèm message dễ hiểu ("wrap the forward pass in `torch.no_grad()`").
  - Có thể tách thành test riêng. Đặt tên test như một câu.
- p6-04-ex02: thêm test gọi `model.eval()`, rồi `fine_tune(..., epochs=1 hoặc 2)`, rồi `assert model.training`, message: "call `model.train()` before training steps". Giữ test nhanh.
- Mọi test chỉ dùng tập con được phép (assert, pytest.raises/approx/mark.parametrize/fail, fixture trong file). Import `types`, `torch`, `torch.nn` thì được.

### G. Sửa lặt vặt (trung bình/thấp)
1. p6-03-ex02: prompt có Rule "do not call `transformers.pipeline`", nhưng `alternatives/01_pipeline.py` lại dùng pipeline. Giữ Rule. Trong `alternatives/01_pipeline.en/vi.md`, ghi rõ đây là cách ngắn để **đối chiếu**, không đạt Rule "tự làm từng bước" của đề.
2. Adam/AdamW: p6-02 §2 hiện nói `torch.optim.Adam` "you will use when fine-tuning in p6-04". Sửa thành nhắc biến thể `AdamW` sẽ dùng ở p6-04.
3. p6-04-ex01 `prompt.en/vi.md`: shape `(2, 6)` → `(2, 5)` (hãy chạy thử để chắc chắn).
4. p6-04-ex02 docstring trong starter và solution: thay `-> [0.6913, 0.6512, 0.6104]` bằng "-> a list of 3 floats, e.g. decreasing losses". Bỏ biến `texts` không được định nghĩa, hoặc ghi rõ đó là gì.
5. p6-04-q04 (fill): chấp nhận `["0.0005", "5e-4"]`. p6-03-q14: nếu blank là `dim` thì chấp nhận thêm `"-1"` (chỉ khi code vẫn chạy đúng và cho cùng output).
6. Dropout: thêm 1–2 câu định nghĩa ở p6-02 §5, chỗ nhắc dropout lần đầu ("randomly zeroes some activations during training to fight overfitting; off in `eval()` mode"). Thêm term `dropout` vào glossary nếu chưa có.
7. p6-02-ex01 test: thêm assert kiểm tra loss đã được làm tròn 4 chữ số đúng như Rule (`losses == [round(v, 4) for v in losses]`), có message.
8. p6-03-ex02: thêm test biên `score == threshold` phải được giữ lại (`>=`). Dùng monkeypatch hoặc text có score biết trước. Starter vẫn phải fail.
9. p6-02 §5 và `examples/02_minibatch_loader.py`: `train_loss` thực ra là loss của batch cuối. Đổi thành trung bình các batch, hoặc đổi tên biến/nhãn in ra cho đúng. Thêm 1 câu giải thích vì sao `val_acc` ở epoch 1 thấp hơn đoán bừa (trọng số khởi tạo ngẫu nhiên, mới đi vài bước). Cập nhật `.out` và comment.
10. p6-02 Mistake 2: "passing float32 labels raises RuntimeError" → thêm "with shape `(N,)`".
11. Style: p6-04 thống nhất với p6-01/02, tức `.to(torch.float32)` thay `.float()` và `round(x.item(), 3)` thay `round(float(x.item()), 3)`, ở cả lesson, examples và solution. Không đổi output.
12. p6-04 LOAD REPORT: ghi "(abridged)" / "(rút gọn)" cạnh bảng. Kiểm tra bằng cách chạy các khối p6-04 **không** đặt `HF_HUB_DISABLE_PROGRESS_BARS`. Nếu stderr có thanh tiến trình "Loading weights", thêm `hf_logging.disable_progress_bar()` ngay sau `set_verbosity_error()` ở mọi khối, example và file exercise của p6-04 có load model.
13. `p6-04-ex01/alternatives/01_manual_slicing.*.md`: ghi rõ `collections.Counter` là xem trước một công cụ chưa học, kèm một câu giải thích.
14. Bản VI:
    - p6-02 `lesson.vi.md` §5: "độ chính xác trên validation" → "tỉ lệ đoán đúng (accuracy) trên validation".
    - p6-01 `lesson.vi.md` §1 và Tóm tắt: "tốn ít bộ nhớ hơn một nửa" → "chỉ tốn một nửa bộ nhớ".
    - p6-01 quiz q01 explanation VI: bỏ cụm "nhẹ bộ nhớ gấp đôi".
    - p6-04 `lesson.vi.md` §8: precision/recall phải có gloss theo CONTENT_GUIDE ("độ chuẩn khi báo dương", "độ nhạy, tức tỉ lệ bắt được").
15. p6-01 EN §4: "Both methods produce -15.0, except autograd…" → "…, but autograd…".

## Tiêu chí hoàn thành (checklist)
- [ ] A: script độ dài MCQ báo 0 vi phạm cho cả en và vi
- [ ] B: 7 bài tập có hint leo thang đúng luật
- [ ] C, D: p6-04 §4/§5 sửa, số in ra là số chạy thật
- [ ] E: `pick_epoch` có trong starter/solution/alternative/prompt/hint, 3 test mới
- [ ] F: test thăm dò `no_grad` ở p6-02-ex02 và p6-04-ex02; test `model.train()` ở p6-04-ex02
- [ ] G1–G15 xong
- [ ] Mọi starter fail mọi test; solution và alternatives pass
- [ ] Validate phase 6 0 lỗi, pytest phase 6 xanh, mọi khối python chạy với `-W error` và stderr rỗng
- [ ] Không file nào ngoài phạm vi bị sửa

## Lệnh kiểm tra
```bash
uv run python tools/validate.py --path curriculum/phase-06-deep-learning
uv run python -m pytest curriculum/phase-06-deep-learning -q
```
Kiểm độ dài MCQ (phải in `violations: 0`):
```bash
uv run python -c "
import yaml,glob
bad=0
for f in sorted(glob.glob('curriculum/phase-06-deep-learning/*/quiz.yaml')):
    for q in yaml.safe_load(open(f,encoding='utf-8'))['questions']:
        if q['type']!='mcq': continue
        for lang in ('en','vi'):
            o=q[lang]['options']; L=[len(x) for x in o]; a=q['answer']
            d=[l for i,l in enumerate(L) if i!=a]
            if L[a] > 1.2*sum(d)/len(d): bad+=1; print(q['id'],lang,L)
print('violations:',bad)
"
```
Starter phải fail: chạy pytest từng bài tập với starter (copy starter thành `exercise.py` trong thư mục tạm, như các bước trước). Báo số test fail/tổng.

## Ghi chú cho worker
- Các bài `runner: local` dùng model đã cache. Đặt `HF_HUB_OFFLINE=1` khi chạy tay.
- Không chạy server hay dev server.
- Mọi số trong lesson, `.out` và comment phải là số chạy thật, không ước đoán.
- Quy tắc code phase 6 vẫn áp dụng: `torch.manual_seed(0)`, không in tensor thô, CPU, mỗi khối < 10 s, `-W error` sạch.

## Trạng thái
- Bước hiện tại: 5 (đạt vòng 2; boss kiểm: pytest phase 6 54/54, MCQ 0 vi phạm, typecheck + build xanh; validate toàn bộ 0 lỗi; đã commit `5cc30a0`)
- Vòng: 2/3
- Số lần swap: 0
- Fallback: không
- Model: Gemini 4 Hydrogen (High)

## Feedback vòng 2
Boss đã kiểm: pytest phase 6 54/54, script MCQ 0 vi phạm, §4/§5 p6-04 đạt, test probe đạt. Còn 2 việc nhỏ:
1. `p6-04-fine-tune/exercises/ex02-fine-tune-and-evaluate/exercise.yaml` hint 3 (en + vi): `accuracy` và `predict` đang được viết đầy đủ, nên ghép hint 2 và hint 3 gần như ra nguyên solution. Mỗi hàm chỉ được còn đúng một `...` ở dòng cốt lõi:
   - `accuracy`: giữ `model.eval()`, dòng tokenize và `with torch.no_grad():`, nhưng dòng `preds = ...` để `...`.
   - `predict`: dòng `return ...` (tra `id2label`) để `...`.
   - `fine_tune` và `pick_epoch`: giữ như hiện tại.
   - Thêm một câu nhắc sau skeleton nếu cần, nhưng không viết lại code đã bỏ.
2. `p6-03-huggingface/quiz.yaml` p6-03-q15 vi: "khi suy đoán" → "khi suy luận (inference)". Giữ độ dài trong giới hạn của script MCQ.
Chạy lại: pytest phase 6, script độ dài MCQ, `validate.py --path curriculum/phase-06-deep-learning`. Ghi kết quả vào cuối report, dưới mục "Vòng 2".
