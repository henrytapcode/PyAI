# Báo cáo M3 bước 14: Phase test 5 (ML)

## 1. Đã làm gì
Hoàn thiện và chỉnh sửa `curriculum/phase-05-ml/phase-test.yaml` (`id: p5-phase-test`, `kind: phase_test`, `phase: p5`, `duration_min: 25`, `pass_score: 0.7`, 18 câu hỏi song ngữ EN/VI từ `p5-test-q01` đến `p5-test-q18`), bao gồm xử lý toàn bộ **Feedback vòng 1**:

1. **Cân độ dài 4 lựa chọn cho toàn bộ 8 câu MCQ (EN & VI)** để đáp án đúng không bị lộ do dài nhất, giữ nguyên `answer`, thứ tự lựa chọn, ý đúng/sai và thuật ngữ VI thống nhất:
   - Rút phần giải thích/lý do thừa trong ngoặc hoặc mệnh đề phụ ra khỏi đáp án đúng ở `p5-test-q02`, `p5-test-q04`, `p5-test-q07`, `p5-test-q11`, `p5-test-q13`, `p5-test-q16`, `p5-test-q17` (các lý do này vẫn được giải thích đầy đủ trong `explanation`).
   - Cân lại độ dài các distractor (bao gồm `p5-test-q06`) để tỷ lệ dài nhất / ngắn nhất của cả 4 lựa chọn nằm trong khoảng `1.03x`–`1.27x` (chênh lệch <= 27%), đồng thời tránh cụm từ `"cả hai"` trong phương án tiếng Việt để hợp lệ với quy tắc `POSITIONAL_OPTION` của `validate.py` khi xáo trộn đáp án.
2. **Sửa thuật ngữ `p5-test-q06` VI lựa chọn thứ 2**: đổi `"vì số phút là con số"` → `"vì số phút là số nguyên"` (khớp EN `"integers"`).

### Bảng đếm thực tế theo blueprint
- **Tổng số câu**: 18 (`p5-test-q01` .. `p5-test-q18`)
- **Phân bổ theo chủ đề**:
  - `# ---- math` (`p5-01`): 4 câu (`q01`–`q04`) — 3 loại (`output`, `mcq`, `fill`)
  - `# ---- supervised` (`p5-02`): 3 câu (`q05`–`q07`) — 2 loại (`parsons`, `mcq`)
  - `# ---- sklearn` (`p5-03`): 4 câu (`q08`–`q11`) — 4 loại (`output`, `fill`, `parsons`, `mcq`)
  - `# ---- evaluation` (`p5-04`): 4 câu (`q12`–`q15`) — 3 loại (`output`, `mcq`, `fill`)
  - `# ---- mini-project` (`p5-05`): 3 câu (`q16`–`q18`) — 2 loại (`mcq`, `output`)
- **Phân bổ theo loại câu**: `mcq`: 8, `output`: 5, `fill`: 3, `parsons`: 2 (tổng 18; mỗi chủ đề >= 2 loại khác nhau).
- **Phân bổ theo độ khó**: Mức 1: 4 (`q01, q05, q06, q08`), Mức 2: 10 (`q02, q03, q04, q07, q09, q11, q13, q14, q15, q18`), Mức 3: 4 (`q10, q12, q16, q17`).
- **Phân bổ vị trí đáp án `mcq`**:
  - `0`: 2 câu (`q06, q16`)
  - `1`: 2 câu (`q02, q13`)
  - `2`: 2 câu (`q04, q17`)
  - `3`: 2 câu (`q07, q11`)

### Bảng độ dài 4 lựa chọn của từng câu MCQ sau khi sửa
| Câu | `answer` | Độ dài EN `[0, 1, 2, 3]` (ký tự) | Tỷ lệ max/min EN | Độ dài VI `[0, 1, 2, 3]` (ký tự) | Tỷ lệ max/min VI |
|---|---|---|---|---|---|
| `p5-test-q02` | `1` | `[74, 77, 77, 76]` | `1.04` | `[73, 73, 73, 70]` | `1.04` |
| `p5-test-q04` | `2` | `[85, 82, 82, 80]` | `1.06` | `[74, 76, 80, 73]` | `1.10` |
| `p5-test-q06` | `0` | `[85, 104, 89, 82]` | `1.27` | `[86, 97, 83, 82]` | `1.18` |
| `p5-test-q07` | `3` | `[65, 65, 69, 66]` | `1.06` | `[68, 68, 64, 69]` | `1.08` |
| `p5-test-q11` | `3` | `[76, 73, 75, 72]` | `1.06` | `[76, 74, 75, 69]` | `1.10` |
| `p5-test-q13` | `1` | `[67, 67, 69, 70]` | `1.04` | `[67, 67, 65, 67]` | `1.03` |
| `p5-test-q16` | `0` | `[126, 127, 123, 128]` | `1.04` | `[135, 132, 126, 129]` | `1.07` |
| `p5-test-q17` | `2` | `[66, 69, 68, 71]` | `1.08` | `[72, 71, 69, 70]` | `1.04` |

### Danh sách 18 câu và ý kiểm tra
| ID | Chủ đề | Loại | Mức | Đáp án | Ý chính kiểm tra (mới so với quiz 5 bài) |
|---|---|---|---|---|---|
| `p5-test-q01` | Math (`p5-01`) | `output` | 1 | `"4.5"` | Tính weighted score `w @ x + bias` với bias khác 0 |
| `p5-test-q02` | Math (`p5-01`) | `mcq` | 2 | `1` | Nhân vector với `10.0`: dot product tăng `10x` còn cosine similarity giữ nguyên |
| `p5-test-q03` | Math (`p5-01`) | `fill` | 2 | `["mean"]` | Điền `np.mean` để tính MSE (`4.333`) thay vì `np.sum` |
| `p5-test-q04` | Math (`p5-01`) | `mcq` | 2 | `2` | Một bước gradient descent khi `slope = -6.0`: `lr=0.2` tới `3.2` còn `lr=2.0` vọt qua `5.0` tới `14.0` |
| `p5-test-q05` | Supervised (`p5-02`) | `parsons` | 1 | `4 2 (4,)` | Tách `X` (2D) và `y` (1D) từ DataFrame, kiểm tra số hàng/cột và `y.shape` |
| `p5-test-q06` | Supervised (`p5-02`) | `mcq` | 1 | `0` | Phân biệt regression (số phút chờ) và classification (nhóm hỗ trợ) |
| `p5-test-q07` | Supervised (`p5-02`) | `mcq` | 2 | `3` | Chẩn đoán underfitting (cả train và test `R^2` thấp) vs overfitting (train `R^2` rất cao, test tụt mạnh) |
| `p5-test-q08` | sklearn (`p5-03`) | `output` | 1 | `"10.0"` | `LinearRegression().fit(X_tr, y_tr).predict(...)` với 2 feature |
| `p5-test-q09` | sklearn (`p5-03`) | `fill` | 2 | `["fit_transform", "transform"]` | `StandardScaler`: `fit_transform` trên `X_train` và chỉ `transform` trên `X_test` |
| `p5-test-q10` | sklearn (`p5-03`) | `parsons` | 3 | `0.6` | Chia `train_test_split` trước rồi bọc `StandardScaler` + `KNeighborsClassifier` trong `make_pipeline` |
| `p5-test-q11` | sklearn (`p5-03`) | `mcq` | 2 | `3` | Dùng `random_state` cố định và `stratify=y` khi chia tập dữ liệu lệch lớp |
| `p5-test-q12` | Evaluation (`p5-04`) | `output` | 3 | `"0.9 0.0 0.0"` | `DummyClassifier(strategy="most_frequent")` trên dữ liệu 90/10: accuracy `0.9`, precision `0.0` (`zero_division=0`), recall `0.0` |
| `p5-test-q13` | Evaluation (`p5-04`) | `mcq` | 2 | `1` | Chọn precision (khóa nhầm tài khoản tự động) vs recall (bỏ sót cảnh báo xâm nhập bảo mật) theo bối cảnh |
| `p5-test-q14` | Evaluation (`p5-04`) | `output` | 2 | `0.7 1.0 0.333\n0.3 0.75 1.0` | Hạ threshold từ `0.7` xuống `0.3` làm recall tăng (`0.333 -> 1.0`) và precision giảm (`1.0 -> 0.75`) |
| `p5-test-q15` | Evaluation (`p5-04`) | `fill` | 2 | `["cross_val_score", "std"]` | Chạy `cross_val_score` với `StratifiedKFold` và tính `mean +/- std` |
| `p5-test-q16` | Mini-project (`p5-05`) | `mcq` | 3 | `0` | Quy trình đúng: làm sạch -> `train_test_split` -> chọn mô hình & threshold bằng CV trên `X_train` -> fit trên `X_train` và chấm `X_test` một lần |
| `p5-test-q17` | Mini-project (`p5-05`) | `mcq` | 3 | `2` | Bẫy target leakage với cột `refund_issued_at` chỉ được ghi nhận sau kết quả |
| `p5-test-q18` | Mini-project (`p5-05`) | `output` | 2 | `"0.01 0.057 True"` | So sánh trung thực hai mô hình khi chênh lệch mean (`0.01`) nhỏ hơn một độ lệch chuẩn (`0.057`) |

## 2. File đã sửa / tạo
- Đã sửa: `curriculum/phase-05-ml/phase-test.yaml`
- Đã cập nhật báo cáo: `tasks/m3-p5-test.report.md`
- Không sửa bất kỳ file nào khác trong `curriculum/`, `tools/`, `apps/`, hay glossary; không chạy `pnpm --filter web build`. (`uv run python tools/build_content.py` sinh dữ liệu vào `apps/web/src/generated` thuộc `.gitignore`.)

## 3. Kết quả lệnh kiểm tra
Tất cả chạy tại `D:\Proj\python-ai-platform` sau lần sửa cuối cùng của `curriculum/phase-05-ml/phase-test.yaml`:

1. `uv run python tools/validate.py --path curriculum/phase-05-ml`:
   - Exit code `0`: `OK: 0 error(s), 0 warning(s). Checked 5 lessons, 36 markdown pairs, 15 examples, 10 exercises, 6 alternatives, 98 questions, 1 exams.`
2. `uv run python tools/validate.py`:
   - Exit code `0`: `OK: 0 error(s), 0 warning(s). Checked 35 lessons, 272 markdown pairs, 103 examples, 70 exercises, 64 alternatives, 678 questions, 7 exams, 1 portfolio, 1 glossary, 1 interview.`
3. `uv run python -m pytest curriculum`:
   - Exit code `0`: `652 passed, 14 warnings in 2.49s` (các warning đều là `PyparsingDeprecationWarning` từ nội bộ `matplotlib`).
4. `uv run python tools/build_content.py`:
   - Exit code `0`: `Built 35 lessons, 7 exams, 210 flashcards, 563 questions -> apps\web\src\generated`
5. Kiểm tra pattern cấm trên `curriculum/phase-05-ml/phase-test.yaml` (`astype\(int\)|dtype=int\b|\.info\(|fetch_|độ chính xác|độ phủ`):
   - `matches: []` (0 kết quả).
6. `git status --short`:
   - Chỉ có `?? .hallmark/`, `?? curriculum/phase-05-ml/phase-test.yaml`, `?? tasks/`.

## 4. Điều còn chưa chắc
- Sau khi chỉnh các lựa chọn MCQ ở vòng 2 (chỉ sửa văn bản `options` và `explanation` trên `mcq`, không đụng code của 10 câu `output`/`fill`/`parsons`), mọi lệnh `validate.py`, `pytest curriculum`, và `build_content.py` đều đã chạy lại và đạt 0 lỗi; riêng chạy độc lập từng đoạn code với `python -W error` không chạy lại ở vòng này vì code của các câu `output`/`fill`/`parsons` giữ nguyên không đổi từ vòng 1 (validator cũng đã thực thi và kiểm tra tất cả câu chạy được).
- Môi trường chạy kiểm tra là Python cục bộ trên Windows, chưa chạy lại trực tiếp trong runtime Pyodide 32-bit trên trình duyệt sau vòng sửa 2 (tuy nhiên các sửa đổi vòng 2 chỉ là chuỗi văn bản của lựa chọn MCQ).
