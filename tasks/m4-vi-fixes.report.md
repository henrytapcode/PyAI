# Báo cáo sửa bản tiếng Việt phase 6–8 (M4 bước 27b)

Ngày thực hiện: 2026-11-18  
Spec: `tasks/m4-vi-fixes.md`  
Mẫu đọc tham chiếu: `tasks/m4-vi-sample-review.md`

---

## 1. Tóm tắt những gì đã làm

1. **Sửa 3 lỗi nặng** khớp với bản tiếng Anh:
   - `curriculum/phase-07-llm/p7-03-embeddings/lesson.vi.md` (l.310): đổi `"độ dài văn bản"` → `"độ dài vector"`.
   - `curriculum/phase-07-llm/p7-07-agents/lesson.vi.md` (l.332): bỏ câu `"Giới hạn là rất rõ:"` và phần `"(hoặc max_steps)"` làm ngược ý EN; viết lại đúng nghĩa rằng nếu bước 2 lặp lại đúng lời gọi lỗi với cùng tham số, phanh `repeat` ở §4 sẽ dừng vòng lặp ngay lập tức thay vì để agent quay vòng tới `max_steps`.
   - `curriculum/phase-06-deep-learning/p6-02-training-loop/lesson.vi.md` (l.436): bỏ cụm `"sai số dự đoán"`, thay bằng `"không làm đổi các con số dự đoán"`, và bổ sung ý `"cho tới khi một lượt validation lớn bị hết bộ nhớ vì PyTorch vẫn âm thầm dựng computation graph (requires_grad=True)"`.
2. **Sửa toàn bộ lỗi Vừa và Nhẹ** từ `tasks/m4-vi-sample-review.md` (chi tiết từng mục ở bảng mục 2).
3. **Sửa 4 lỗi lặp trên toàn phase 6–8**:
   - **Xưng hô (`ta`/`chúng ta`)**: đổi sang `"bạn"` hoặc câu không chủ ngữ trên tất cả các file `*.vi.md` và phần `vi:` của `*.yaml` (bao gồm cả trường hợp đứng sau dấu gạch dài `—ta` ở `p7-03` l.219). Chỉ giữ `"người ta"`.
   - **Từ `"accuracy"` đứng trần trong văn xuôi VI**: chuẩn hóa thành `"tỉ lệ đoán đúng (accuracy)"` ở lần xuất hiện đầu tiên trong mỗi file/câu hỏi và `"tỉ lệ đoán đúng"` ở các lần sau (giữ nguyên tên hàm, tên biến và output trong code block).
   - **Cụm `"độ chính xác"`**:
     - Đổi sang `"độ nhạy (recall — có thể sót vài kết quả gần nhất)"` ở các chỗ nói về ANN trong `p7-04-vector-db/lesson.vi.md` (l.498) và `p7-04-vector-db/quiz.yaml` (l.298, l.388).
     - **Quyết định đối với các chỗ khác ngoài ANN**:
       - `p6-01-tensors` (`lesson.vi.md:13`, `quiz.yaml:18, 20, 138, 347`): nói về độ chính xác số thực (`float32`/`float64`/`float16` precision) → **giữ nguyên** theo spec.
       - `p6-02-training-loop/exercises/ex01-fix-training-loop/exercise.yaml` (l.30, phần `vi:`): bản EN viết `"what type and precision losses records"` (chỉ việc ép về Python `float` và làm tròn 4 chữ số thập phân) → đây cũng là độ chính xác biểu diễn số học (`precision`), không phải `accuracy`/`recall` → **giữ nguyên**.
       - `p7-10-mini-project-agent/quiz.yaml` (l.199, `p7-10-q09`): đối chiếu với bản EN (`"Nothing else; scripted tests prove model accuracy"`) cho thấy câu này nói về **model accuracy** (không phải ANN recall). Vì vậy đổi `"độ chính xác"` → `"tỉ lệ đoán đúng (accuracy) của model"` (vừa khớp nghĩa EN, vừa đảm bảo `"độ chính xác"` chỉ còn ở chỗ nói precision số thực).
   - **Dịch sát thành ngữ**: xử lý toàn bộ `"nối dây"` (`lắp ráp`), `"đóng băng mẫu đầu tiên"` (`giữ cứng câu trả lời ngẫu nhiên đầu tiên`), `"thắng về"` (`cho tích vô hướng cao hơn`), `"nói thật"` (`nói rõ`), `"nhảy trước"` (`tua nhanh`), `"đụng hàng"` (`trùng`).

---

## 2. Bảng file đã sửa và số chỗ sửa theo nhóm (28 file)

> Ghi chú đếm: Một vài vị trí thuộc đồng thời 2 nhóm (ví dụ: `p7-03` l.33 vừa là mục *Vừa* vừa là *Thành ngữ* `"nói thật"`; `p8-03` l.448 vừa là *Vừa* vừa là *Thành ngữ* `"đóng băng mẫu đầu tiên"`; `p8-05` l.682 vừa là *Vừa* vừa là *Thành ngữ* `"nối dây"`). Các cột dưới đây đếm số chỗ theo từng tiêu chí áp dụng.

| File | Nặng | Vừa | Nhẹ | Xưng hô | Accuracy | Độ chính xác | Thành ngữ | Ghi chú chi tiết |
|---|---|---|---|---|---|---|---|---|
| `curriculum/phase-06-deep-learning/p6-02-training-loop/lesson.vi.md` | 1 | 1 | 2 | 3 | 2 | 0 | 0 | Nặng l.436; Vừa l.59; Nhẹ l.1, l.203; Xưng hô l.7, l.311, l.371; Accuracy l.371, l.459 |
| `curriculum/phase-06-deep-learning/p6-02-training-loop/examples/02_minibatch_loader.vi.md` | 0 | 0 | 1 | 0 | 3 | 0 | 0 | Nhẹ l.8 (`suy đoán`→`suy luận`); Accuracy l.3, l.9, l.14 |
| `curriculum/phase-06-deep-learning/p6-02-training-loop/examples/03_save_and_reload.vi.md` | 0 | 0 | 0 | 1 | 3 | 0 | 0 | Xưng hô l.12; Accuracy l.7, l.10, l.12 |
| `curriculum/phase-06-deep-learning/p6-02-training-loop/exercises/ex02-tiny-classifier/prompt.vi.md` | 0 | 0 | 2 | 0 | 0 | 0 | 0 | Nhẹ l.4, l.21 (`suy luận`, chế độ đánh giá) |
| `curriculum/phase-06-deep-learning/p6-02-training-loop/quiz.yaml` | 0 | 0 | 1 | 0 | 2 | 0 | 0 | Nhẹ l.282 (`suy luận`); Accuracy q13 l.276, q15 l.327 |
| `curriculum/phase-06-deep-learning/p6-03-huggingface/lesson.vi.md` | 0 | 0 | 0 | 1 | 0 | 0 | 0 | Xưng hô l.170 |
| `curriculum/phase-06-deep-learning/p6-04-fine-tune/lesson.vi.md` | 0 | 0 | 0 | 3 | 6 | 0 | 0 | Xưng hô l.167, l.273, l.277; Accuracy l.167, l.243, l.245, l.365, l.453, l.577 |
| `curriculum/phase-06-deep-learning/p6-04-fine-tune/examples/02_before_after.vi.md` | 0 | 0 | 0 | 0 | 2 | 0 | 0 | Accuracy l.1, l.12 |
| `curriculum/phase-06-deep-learning/p6-04-fine-tune/quiz.yaml` | 0 | 0 | 0 | 1 | 7 | 0 | 0 | Xưng hô l.84; Accuracy l.16, l.222, l.288–290, l.328, l.399 |
| `curriculum/phase-06-deep-learning/phase-test.yaml` | 0 | 0 | 0 | 1 | 0 | 0 | 0 | Xưng hô l.52 |
| `curriculum/phase-07-llm/p7-01-llm-api/lesson.vi.md` | 0 | 0 | 0 | 1 | 0 | 0 | 0 | Xưng hô l.194 |
| `curriculum/phase-07-llm/p7-02-structured-output/quiz.yaml` | 0 | 0 | 0 | 1 | 0 | 0 | 0 | Xưng hô l.16 |
| `curriculum/phase-07-llm/p7-03-embeddings/lesson.vi.md` | 1 | 4 | 2 | 5 | 0 | 0 | 2 | Nặng l.310; Vừa l.33, l.145, l.291, l.336; Nhẹ l.129, l.223; Xưng hô l.1, l.30, l.37, l.90, l.219; Thành ngữ l.33, l.291 |
| `curriculum/phase-07-llm/p7-03-embeddings/exercises/ex02-top-k/prompt.vi.md` | 0 | 1 | 0 | 0 | 0 | 0 | 0 | Vừa l.20 (`score < min_score`, bằng ngưỡng thì giữ) |
| `curriculum/phase-07-llm/p7-04-vector-db/lesson.vi.md` | 0 | 0 | 0 | 1 | 0 | 1 | 0 | Xưng hô l.38; Độ chính xác l.498 (→ `độ nhạy (recall)`) |
| `curriculum/phase-07-llm/p7-04-vector-db/quiz.yaml` | 0 | 0 | 0 | 0 | 0 | 2 | 0 | Độ chính xác l.298, l.388 (→ `độ nhạy (recall)`) |
| `curriculum/phase-07-llm/p7-05-rag/lesson.vi.md` | 0 | 0 | 0 | 2 | 0 | 0 | 1 | Xưng hô l.219, l.259; Thành ngữ l.176 (`Nói thật`→`Nói rõ`) |
| `curriculum/phase-07-llm/p7-05-rag/quiz.yaml` | 0 | 0 | 0 | 1 | 0 | 0 | 0 | Xưng hô l.38 |
| `curriculum/phase-07-llm/p7-06-tool-use/lesson.vi.md` | 0 | 0 | 0 | 2 | 0 | 0 | 0 | Xưng hô l.101, l.226 |
| `curriculum/phase-07-llm/p7-07-agents/lesson.vi.md` | 1 | 1 | 0 | 1 | 0 | 0 | 0 | Nặng l.332; Vừa l.5; Xưng hô l.241 |
| `curriculum/phase-07-llm/p7-08-evals/lesson.vi.md` | 0 | 0 | 0 | 3 | 0 | 0 | 0 | Xưng hô l.174, l.176, l.356 |
| `curriculum/phase-07-llm/p7-08-evals/quiz.yaml` | 0 | 0 | 0 | 1 | 0 | 0 | 0 | Xưng hô l.133 |
| `curriculum/phase-07-llm/p7-10-mini-project-agent/exercises/ex01-toolbox/alternatives/01_dataclass_registry.vi.md` | 0 | 0 | 0 | 1 | 0 | 0 | 0 | Xưng hô l.3 |
| `curriculum/phase-07-llm/p7-10-mini-project-agent/lesson.vi.md` | 0 | 0 | 0 | 2 | 0 | 0 | 0 | Xưng hô l.234, l.722 |
| `curriculum/phase-07-llm/p7-10-mini-project-agent/quiz.yaml` | 0 | 0 | 0 | 0 | 0 | 1 | 0 | Độ chính xác l.199 (→ `tỉ lệ đoán đúng (accuracy) của model`) |
| `curriculum/phase-08-production/p8-03-caching/lesson.vi.md` | 0 | 1 | 2 | 0 | 0 | 0 | 3 | Vừa l.448; Nhẹ l.206, l.326; Thành ngữ l.206, l.448, l.496 |
| `curriculum/phase-08-production/p8-04-monitoring/lesson.vi.md` | 0 | 0 | 0 | 4 | 0 | 0 | 0 | Xưng hô l.7, l.94, l.124, l.139 (2 chỗ) |
| `curriculum/phase-08-production/p8-05-mini-project/lesson.vi.md` | 0 | 2 | 2 | 2 | 0 | 0 | 2 | Vừa l.368, l.682; Nhẹ l.22, l.254; Xưng hô l.43, l.254; Thành ngữ l.254, l.682 |

*(Tổng: 28 file sửa, 89 dòng thêm / 89 dòng xóa theo `git diff --stat`.)*

---

## 3. Kết quả lệnh kiểm tra

### 3.1. `tools/validate.py` cho phase 6–8
- `uv run python tools/validate.py --path curriculum/phase-06-deep-learning` (exit 0):
  `OK: 0 error(s), 0 warning(s). Checked 4 lessons, 29 markdown pairs, 12 examples, 8 exercises, 5 alternatives, 80 questions, 1 exams.`
- `uv run python tools/validate.py --path curriculum/phase-07-llm` (exit 0):
  `OK: 0 error(s), 0 warning(s). Checked 10 lessons, 72 markdown pairs, 30 examples, 20 exercises, 12 alternatives, 179 questions, 1 exams.`
- `uv run python tools/validate.py --path curriculum/phase-08-production` (exit 0):
  `OK: 0 error(s), 0 warning(s). Checked 5 lessons, 36 markdown pairs, 15 examples, 10 exercises, 6 alternatives, 96 questions, 1 exams.`

### 3.2. Kiểm tra quy tắc lặp và phạm vi diff
- Quét `ta`/`chúng ta` theo regex `"(^|[ .:(\"'])(Ta|ta|Chúng ta|chúng ta) "` (bỏ `"người ta"`) và quét ranh giới từ `(?<![\wÀ-ỹ])(Ta|ta|Chúng ta|chúng ta)(?![\wÀ-ỹ])` trên toàn `*.vi.md` và phần `vi:` của `*.yaml` trong phase 6–8: **0 dòng**.
- Quét `"độ chính xác"` trên toàn phase 6–8: chỉ còn **6 dòng**, đều nói về độ chính xác số học của số thực (`p6-01-tensors/lesson.vi.md:13`, `p6-01-tensors/quiz.yaml:18, 20, 138, 347`, và `p6-02-training-loop/exercises/ex01-fix-training-loop/exercise.yaml:30`).
- Quét cụm thành ngữ (`"nối dây"`, `"đóng băng mẫu"`, `"thắng về"`, `"nói thật"`, `"nhảy trước"`, `"đụng hàng"`): **0 dòng**.
- `git diff --name-only | Select-String -Pattern "\.en\.md$|\.py$|\.out$|meta\.yaml$"` : **trống** (0 file `.en.md`, `.py`, `.out`, `meta.yaml` bị sửa). Kiểm tra diff từng dòng YAML xác nhận chỉ sửa bên trong phần `vi:`.

---

## 4. Điều còn chưa chắc

- Ở `curriculum/phase-06-deep-learning/p6-02-training-loop/exercises/ex01-fix-training-loop/exercise.yaml:30`, cụm `"độ chính xác"` dịch từ `"what type and precision losses records"` (độ chính xác số thập phân khi làm tròn `float`). Đã giữ lại vì đúng nghĩa numeric precision theo tinh thần mục 3, nhưng nếu người đọc lướt checklist máy móc theo chữ `"float32 precision, p6-01"` có thể cân nhắc đổi thành `"độ chính xác số thập phân"` hoặc `"số chữ số thập phân"` cho tường minh hơn nữa.
- Ở `curriculum/phase-07-llm/p7-10-mini-project-agent/quiz.yaml:199` (`p7-10-q09`), bản EN ghi `"scripted tests prove model accuracy"` (phương án nhiễu về năng lực chọn tool của agent LLM, không phải ANN). Đã đổi sang `"tỉ lệ đoán đúng (accuracy) của model"` thay vì `"độ nhạy (recall)"` như ví dụ trong spec vốn liệt kê nhầm dòng này vào nhóm ANN; nhờ reviewer xác nhận lại cách diễn đạt này.
- Các bài ngoài mẫu (~75% còn lại của phase 6–8) mới được rà soát tự động theo 4 lỗi lặp trong spec, chưa đọc mẫu toàn văn từng dòng như phần 25% đầu.
