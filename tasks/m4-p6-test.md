# M4 bước 9: Phase test 6 (Deep learning)

## Mục tiêu
Viết `curriculum/phase-06-deep-learning/phase-test.yaml`, bài kiểm tra cuối phase 6. File cùng định dạng với `curriculum/phase-05-ml/phase-test.yaml`: schema `tools/schema/exam.schema.json`, `kind: phase_test`.
Boss đã chốt blueprint dưới đây. Worker viết câu hỏi theo đúng blueprint.

## File được phép sửa/tạo
- Chỉ một file mới: `curriculum/phase-06-deep-learning/phase-test.yaml`.
- Báo cáo `tasks/m4-p6-test.report.md`.

## Không được đụng
- Mọi file khác: quiz các bài, `tools/`, `apps/`, glossary, topics.
- Không xóa file, không `git commit`, **không chạy `pnpm --filter web build`**.

## Blueprint (boss chốt)
- `id: p6-phase-test`, `phase: p6`.
  - Title EN: "Phase 6 test: Deep learning"
  - Title VI: "Bài kiểm tra Phase 6: Deep learning"
  - Description nêu số câu và chủ đề.
- `duration_min: 25`, `pass_score: 0.7`.
- **16 câu**, id `p6-test-q01` … `p6-test-q16`. Nhóm theo chủ đề bằng comment `# ---- tensors` như phase 5.

| Chủ đề (bài) | Số câu | Ý chính phải kiểm |
|---|---|---|
| Tensors & autograd (p6-01) | 4 | shape và broadcasting của tensor, `.item()` và `tolist()`, `requires_grad` cùng `backward()` cho ra gradient (tính được bằng tay), gradient cộng dồn nếu không xóa, cập nhật tham số trong `torch.no_grad()` |
| Training loop (p6-02) | 4 | thứ tự 5 bước (forward → loss → `zero_grad` → `backward` → `step`), `CrossEntropyLoss` nhận logits và nhãn `int64` shape `(N,)`, `model.train()`/`model.eval()` + `torch.no_grad()` khi đánh giá, `DataLoader` mini-batch (số batch mỗi epoch) |
| Hugging Face (p6-03) | 4 | tokenizer: subword `##`, `[CLS]`/`[SEP]`, padding và `attention_mask`; `model(**batch)` trả logits rồi softmax → xác suất, `id2label`; pipeline tiện nhưng là hộp đen; giới hạn của model 2 lớp |
| Fine-tune (p6-04, tích hợp) | 4 | base model + classification head mới (vì sao LOAD REPORT có `MISSING`); learning rate nhỏ với AdamW; chọn epoch bằng validation (val_acc, hòa thì val_loss), test chỉ dùng cho báo cáo cuối; seed làm kết quả lặp lại được; `save_pretrained`/`from_pretrained` giữ `id2label` |

- **Loại câu:** 7 `mcq`, 4 `output`, 3 `fill`, 2 `parsons`. Rải đều, mỗi chủ đề có ít nhất 2 loại khác nhau.
- **Độ khó:** 3 câu mức 1, 9 câu mức 2, 4 câu mức 3. Câu mức 3 nên là câu tích hợp hoặc bẫy phổ biến: quên `zero_grad`, quên `eval()`, chọn epoch theo test, nhãn sai dtype.
- **mcq:**
  - Rải `answer` qua vị trí 0–3 theo phân bổ 2/2/2/1.
  - Distractor là hiểu lầm thật. Không dùng "All of the above".
  - **Cân độ dài:** `len(đúng) <= 1.2 × trung bình len(distractor)` ở cả en và vi.
  - Đáp án đúng không kèm lý do ("because…", "so that…", "vì…", "để…"). Lý do để trong `explanation`.
  - Đáp án đúng là phương án dài nhất duy nhất ở tối đa 2/7 câu.
- **Câu mới hoàn toàn:** đọc hết 4 file `curriculum/phase-06-deep-learning/p6-0*/quiz.yaml` trước. Không chép hay chỉ sửa sơ một câu có sẵn, dù trùng ý hay trùng code.
- Mỗi câu có `tags` lấy trong `[dl, pytorch, huggingface, model-evaluation, data-prep]` (đã có trong topics.yaml), và `explanation` song ngữ nói **vì sao**.
- **parsons:** `lines` theo thứ tự đúng, chạy được, mỗi dòng duy nhất. Chỉ có một thứ tự đúng, nhờ ràng buộc phụ thuộc hoặc kết quả in ra. Gợi ý: sắp xếp vòng training (`zero_grad` / `backward` / `step`) và in loss.
- Chỉ dùng kiến thức đã dạy ở phase 1–6.

## Quy tắc code (bắt buộc)
- Trong app, câu hỏi bài thi chỉ hiển thị code. Validator chạy code ở máy với timeout **15 s** và so đáp án. Vì vậy:
  - Được dùng `torch` (CPU) với tensor nhỏ.
  - **Không** nạp model hay tokenizer Hugging Face (`from_pretrained`, `pipeline`) trong code của câu nào. Câu về tokenizer/model viết dạng mcq hoặc fill, và đưa sẵn dữ liệu (vd list token, `input_ids`, logits) dưới dạng literal.
- `torch.manual_seed(0)` ở đầu mọi đoạn có ngẫu nhiên. Tốt nhất là tránh ngẫu nhiên, dùng số cố định cho dễ tính tay.
- Không in tensor thô (`tensor(...)` không được xuất hiện trong output). Dùng `.item()`, `.tolist()`, `round(x.item(), 3)`, `tuple(t.shape)`.
- Không in dtype số nguyên của NumPy. Torch dtype in được nếu cần (`torch.int64` in ra giống nhau ở mọi máy), nhưng ưu tiên không in.
- Không phát warning nào. Kiểm bằng `uv run python -W error snippet.py`.
- Code ngắn (câu output/fill dưới ~15 dòng) và chạy nhanh.
- Thuật ngữ VI: accuracy là "tỉ lệ đoán đúng". Không dùng "độ chính xác".

## Tiêu chí hoàn thành (checklist)
1. [ ] Đúng blueprint: 16 câu, đúng phân bổ chủ đề, loại câu, độ khó và vị trí đáp án mcq. Ghi bảng đếm thực tế vào report.
2. [ ] Không trùng câu với quiz 4 bài. Report liệt kê mỗi câu kiểm ý nào.
3. [ ] EN/VI đầy đủ, bản VI tự nhiên, code giống hệt giữa hai ngôn ngữ.
4. [ ] Script độ dài mcq bên dưới in `violations: 0`. Report ghi bảng độ dài 4 phương án (EN) của từng câu mcq.
5. [ ] Tuân thủ "Quy tắc code". Mọi câu output/fill/parsons chạy với `-W error` không có stderr.
6. [ ] Lệnh kiểm tra xanh, chạy đúng như ghi.

## Lệnh kiểm tra
Từ gốc repo `D:\Proj\python-ai-platform`:
```
uv run python tools/validate.py --path curriculum/phase-06-deep-learning
uv run python tools/build_content.py
grep -nE "from_pretrained|pipeline\(|cuda|độ chính xác" curriculum/phase-06-deep-learning/phase-test.yaml
git status --short
```
Kiểm độ dài mcq (phải in `violations: 0`):
```
uv run python -c "
import yaml
bad=0
for q in yaml.safe_load(open('curriculum/phase-06-deep-learning/phase-test.yaml',encoding='utf-8'))['questions']:
    if q['type']!='mcq': continue
    for lang in ('en','vi'):
        o=q[lang]['options']; L=[len(x) for x in o]; a=q['answer']
        d=[l for i,l in enumerate(L) if i!=a]
        if L[a] > 1.2*sum(d)/len(d): bad+=1; print(q['id'],lang,L)
print('violations:',bad)
"
```
Kết quả mong đợi:
- validate 0 lỗi, số exams tăng 1.
- build_content in số exams tăng 1.
- grep rỗng.
- Chỉ có một file mới là `phase-test.yaml` (ngoài `tasks/` và `.hallmark/`, vốn đã untracked).

## Ghi chú cho worker
- Đọc mẫu `curriculum/phase-05-ml/phase-test.yaml`, 4 file quiz phase 6 và các lesson phase 6 để biết API nào đã dạy.
- Đặt `HF_HUB_OFFLINE=1` khi chạy validate.
- Dùng `uv run python -m pytest`, không dùng `uv run pytest`.
- Không chạy server hay dev server.

## Trạng thái
- Bước hiện tại: 5 (đạt vòng 1; boss duyệt 16/16 câu, validate phase 6 0 lỗi, MCQ 0 vi phạm, build 62 trang, đề hiện và chạy trong app; phát hiện Visualize trong bài thi chạy Pyodide nên báo thiếu torch, là lỗi app ngoài phạm vi; đã commit `81df246`)
- Vòng: 1/3
- Số lần swap: 0
- Fallback: không
- Model: Gemini 4 Hydrogen (High)
