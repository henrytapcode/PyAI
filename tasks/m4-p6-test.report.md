# Báo cáo M4 bước 9: Phase test 6 (Deep learning)

## 1. Đã làm gì
- Đọc spec `tasks/m4-p6-test.md`, `tools/schema/exam.schema.json`, `tools/schema/common.schema.json`, mẫu `curriculum/phase-05-ml/phase-test.yaml`, 4 file `quiz.yaml`, 4 file `lesson.en.md` của phase 6 và `curriculum/topics.yaml`.
- Tạo mới `curriculum/phase-06-deep-learning/phase-test.yaml` (`id: p6-phase-test`, `kind: phase_test`, `phase: p6`, `duration_min: 25`, `pass_score: 0.7`) gồm **16 câu hỏi** mới hoàn toàn (`p6-test-q01` … `p6-test-q16`), nhóm theo 4 chủ đề bằng comment `# ---- tensors`, `# ---- training-loop`, `# ---- huggingface`, `# ---- fine-tune`.
- Tuân thủ quy tắc code: không dùng `from_pretrained`, `pipeline(`, `cuda` hay `"độ chính xác"` (dùng `"tỉ lệ đoán đúng"`); câu về Hugging Face dùng dữ liệu literal và `SimpleNamespace`; không in tensor thô; mọi câu chạy được kiểm bằng `-W error` không phát warning/stderr.

### Ý chính từng câu kiểm tra (không trùng quiz 4 bài)
| ID | Chủ đề | Loại | Mức | Tags | Ý chính kiểm tra |
|---|---|---|---|---|---|
| `p6-test-q01` | `tensors` (`p6-01`) | `output` | 1 | `pytorch` | Broadcasting `(2, 3) + (2, 1)`, `tuple(shape)`, `.item()`, `.tolist()` |
| `p6-test-q02` | `tensors` (`p6-01`) | `output` | 2 | `pytorch`, `dl` | `requires_grad=True` trên hai leaf tensor `w`, `b` và `backward()` theo quy tắc dây chuyền |
| `p6-test-q03` | `tensors` (`p6-01`) | `fill` | 2 | `pytorch`, `dl` | Điền `requires_grad` và `no_grad` để bật autograd rồi cập nhật tại chỗ an toàn |
| `p6-test-q04` | `tensors` (`p6-01`) | `mcq` | 3 | `pytorch`, `dl` | Bẫy quên `w.grad.zero_()` trong vòng lặp 2 bước làm gradient cộng dồn (`8.0 + 4.0`) gây nhảy vọt qua đáy |
| `p6-test-q05` | `training-loop` (`p6-02`) | `parsons` | 2 | `pytorch`, `dl` | Sắp xếp đúng thứ tự 5 bước huấn luyện (`forward -> loss -> zero_grad -> backward -> step`) trên `Linear(2, 2)` + `CrossEntropyLoss` + `SGD` |
| `p6-test-q06` | `training-loop` (`p6-02`) | `mcq` | 3 | `pytorch`, `dl` | Bẫy `CrossEntropyLoss` nhận nhãn `float32` gây `RuntimeError`, cần `dtype=torch.int64` shape `(N,)` |
| `p6-test-q07` | `training-loop` (`p6-02`) | `output` | 1 | `pytorch`, `data-prep` | `DataLoader` chia 35 mẫu với `batch_size=12`: số batch (`3`) và kích thước từng batch (`[12, 12, 11]`) |
| `p6-test-q08` | `training-loop` (`p6-02`) | `fill` | 3 | `pytorch`, `model-evaluation` | Bẫy chuyển trạng thái `eval()` -> `torch.no_grad()` khi đánh giá và khôi phục `train()` cho epoch kế tiếp |
| `p6-test-q09` | `huggingface` (`p6-03`) | `mcq` | 1 | `huggingface`, `data-prep` | Đọc hiểu chuỗi token đã đệm (`[CLS]`, `[SEP]`, subword `##seen`, `[PAD]`) cùng hàng `attention_mask` (`0` ở vị trí đệm) |
| `p6-test-q10` | `huggingface` (`p6-03`) | `fill` | 2 | `huggingface`, `pytorch` | Unpack `**batch` vào `model(...)`, tính `torch.softmax(logits, dim=1)` và ánh xạ qua `id2label` |
| `p6-test-q11` | `huggingface` (`p6-03`) | `mcq` | 2 | `huggingface` | Vì sao `pipeline` là hộp đen (gói gọn tokenize, logits thô, softmax vào một lệnh nên không chỉnh hay fine-tune được) |
| `p6-test-q12` | `huggingface` (`p6-03`) | `mcq` | 2 | `huggingface`, `model-evaluation` | Giới hạn của model 2 lớp trên câu trung tính (thiếu lớp `NEUTRAL`, softmax cao chỉ phản ánh chênh lệch logit) |
| `p6-test-q13` | `fine-tune` (`p6-04`) | `mcq` | 2 | `huggingface`, `dl` | Ý nghĩa `MISSING` trên `classifier` trong `LOAD REPORT` và cách chọn `AdamW` với `lr` nhỏ (`5e-4`) |
| `p6-test-q14` | `fine-tune` (`p6-04`) | `output` | 2 | `dl`, `model-evaluation` | Chọn epoch tốt nhất theo `val_acc`, hòa thì xét `val_loss` thấp hơn |
| `p6-test-q15` | `fine-tune` (`p6-04`) | `parsons` | 2 | `pytorch`, `data-prep` | Chia chỉ số train/val/test `12/4/4` tái lập được bằng `torch.Generator().manual_seed(27)` và `torch.randperm` |
| `p6-test-q16` | `fine-tune` (`p6-04`) | `mcq` | 3 | `huggingface`, `model-evaluation` | Bẫy chọn epoch trên tập test vs chọn trên validation, kết hợp `save_pretrained` để giữ `id2label` khi nạp lại |

## 2. File đã sửa / tạo
- Tạo mới: `curriculum/phase-06-deep-learning/phase-test.yaml`
- Tạo mới: `tasks/m4-p6-test.report.md`
- Ghi chú: `tools/build_content.py` cập nhật thư mục generated (đã gitignore) `apps/web/src/generated`. Không sửa bất kỳ file nào khác.

## 3. Kết quả lệnh kiểm tra

### Bảng đếm blueprint thực tế
| Hạng mục | Yêu cầu spec | Thực tế |
|---|---|---|
| Tổng số câu | 16 (`p6-test-q01` … `p6-test-q16`) | 16 |
| Theo chủ đề | `tensors`: 4, `training-loop`: 4, `huggingface`: 4, `fine-tune`: 4 | 4 / 4 / 4 / 4 |
| Theo loại câu | 7 `mcq`, 4 `output`, 3 `fill`, 2 `parsons` | 7 `mcq`, 4 `output`, 3 `fill`, 2 `parsons` |
| Số loại khác nhau mỗi chủ đề | >= 2 | `tensors`: 3, `training-loop`: 4, `huggingface`: 2, `fine-tune`: 3 |
| Theo độ khó | Mức 1: 3, Mức 2: 9, Mức 3: 4 | Mức 1: 3, Mức 2: 9, Mức 3: 4 |
| Vị trí đáp án `mcq` (0–3) | 2 / 2 / 2 / 1 | `0`: 2 (`q04`, `q11`), `1`: 2 (`q13`, `q16`), `2`: 2 (`q06`, `q12`), `3`: 1 (`q09`) |
| Đáp án đúng dài nhất duy nhất (`mcq`) | <= 2/7 câu | EN: 2/7 (`q04`, `q09`), VI: 0/7 |

### Bảng độ dài 4 phương án `mcq` (EN và đối chiếu VI)
| ID | `answer` | Độ dài 4 phương án EN `[0, 1, 2, 3]` | Đúng (EN) | TB sai (EN) | Tỉ lệ EN | Độ dài 4 phương án VI `[0, 1, 2, 3]` | Đúng (VI) | TB sai (VI) | Tỉ lệ VI |
|---|---|---|---|---|---|---|---|---|---|
| `p6-test-q04` | 0 | `[76, 68, 66, 71]` | 76 | 68.3 | 1.11 | `[70, 68, 64, 71]` | 70 | 67.7 | 1.03 |
| `p6-test-q06` | 2 | `[58, 60, 57, 54]` | 57 | 57.3 | 0.99 | `[65, 64, 60, 61]` | 60 | 63.3 | 0.95 |
| `p6-test-q09` | 3 | `[66, 71, 66, 72]` | 72 | 67.7 | 1.06 | `[67, 68, 69, 67]` | 67 | 68.0 | 0.99 |
| `p6-test-q11` | 0 | `[72, 71, 71, 73]` | 72 | 71.7 | 1.00 | `[68, 68, 66, 69]` | 68 | 67.7 | 1.00 |
| `p6-test-q12` | 2 | `[69, 68, 71, 73]` | 71 | 70.0 | 1.01 | `[67, 68, 68, 72]` | 68 | 69.0 | 0.99 |
| `p6-test-q13` | 1 | `[62, 65, 71, 66]` | 65 | 66.3 | 0.98 | `[65, 55, 68, 69]` | 55 | 67.3 | 0.82 |
| `p6-test-q16` | 1 | `[103, 101, 98, 95]` | 101 | 98.7 | 1.02 | `[104, 95, 94, 92]` | 95 | 96.7 | 0.98 |

### Kết quả chạy các lệnh kiểm tra
1. `HF_HUB_OFFLINE=1 uv run python tools/validate.py --path curriculum/phase-06-deep-learning`:
   - Mã thoát `0`: `OK: 0 error(s), 0 warning(s). Checked 4 lessons, 29 markdown pairs, 12 examples, 8 exercises, 5 alternatives, 80 questions, 1 exams.` (tăng từ 0 lên 1 exam trong phase 6).
2. `uv run python tools/build_content.py`:
   - Mã thoát `0`: `Built 39 lessons, 9 exams, 234 flashcards, 627 questions -> apps\web\src\generated`
3. Kiểm tra pattern cấm (`from_pretrained|pipeline\(|cuda|độ chính xác`) trên `curriculum/phase-06-deep-learning/phase-test.yaml`:
   - Rỗng (`matches: []`).
4. Kiểm tra độ dài `mcq`:
   - `violations: 0`.
5. Chạy từng đoạn code (`q01`, `q02`, `q03`, `q04`, `q05`, `q07`, `q08`, `q10`, `q14`, `q15`) với `python -W error`:
   - Toàn bộ 10/10 đoạn mã thoát `0`, `stderr` rỗng, output khớp đáp án (`q01`: `(2, 3) 25.0 [12.0, 14.0, 16.0]`, `q02`: `-18.0 -6.0`, `q03`: `2.5`, `q04`: `0.0`, `q05`: `0.764`, `q07`: `3 [12, 12, 11]`, `q08`: `False False True`, `q10`: `['NEGATIVE', 'POSITIVE'] 0.5`, `q14`: `3 0.938 0.315`, `q15`: `12 4 4`).
6. `git status --short`:
   - Chỉ có `?? .hallmark/`, `?? curriculum/phase-06-deep-learning/phase-test.yaml`, `?? tasks/`.

## 4. Điều còn chưa chắc
- Không chạy `pnpm --filter web build` và không chạy test suite UI theo ràng buộc của spec, nên chưa kiểm tra hiển thị trực quan của `p6-phase-test` trên giao diện web.
- Trong `p6-test-q05` (`parsons`), dòng `opt.zero_grad()` đặt giữa `loss = ...` và `loss.backward()` là theo quy ước 5 bước chuẩn đã dạy ở `p6-02` (và được nêu rõ trong đề bài); về mặt thực thi Python thuần túy, đặt `opt.zero_grad()` trước `logits = ...` cũng cho cùng giá trị `loss` cuối.
