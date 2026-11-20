# M3 bước 14: Phase test 5 (ML)

## Mục tiêu
Viết `curriculum/phase-05-ml/phase-test.yaml`: bài kiểm tra cuối phase 5, cùng định dạng với `curriculum/phase-04-data/phase-test.yaml` (schema `tools/schema/exam.schema.json`, `kind: phase_test`).
Boss đã chốt blueprint dưới đây; worker viết câu hỏi theo đúng blueprint.

## File được phép sửa/tạo
- File mới `curriculum/phase-05-ml/phase-test.yaml`. Chỉ file này.

## Không được đụng
- Mọi file khác (quiz các bài, `tools/`, `apps/`, glossary). Không xóa file, không `git commit`, **không chạy `pnpm --filter web build`**.

## Blueprint (boss chốt)
- `id: p5-phase-test`, `phase: p5`, title EN "Phase 5 test: Machine learning" / VI "Bài kiểm tra Phase 5: Machine learning", description nêu số câu và chủ đề.
- `duration_min: 25`, `pass_score: 0.7`.
- **18 câu**, id `p5-test-q01` … `p5-test-q18`, nhóm theo chủ đề bằng comment `# ---- math` như phase 4:

| Chủ đề (bài) | Số câu | Ý chính phải kiểm |
|---|---|---|
| Math bridge (p5-01) | 4 | dot product / weighted score, cosine similarity (độ dài vector không ảnh hưởng), MSE, một bước gradient descent (dấu và learning rate quá lớn) |
| Supervised (p5-02) | 3 | X vs y, regression vs classification, underfit/overfit qua train vs test score |
| sklearn workflow (p5-03) | 4 | `fit`/`predict`, `fit_transform` trên train và chỉ `transform` trên test, pipeline chặn rò rỉ scaling, `random_state`/`stratify` khi split |
| Evaluation (p5-04) | 4 | accuracy dễ đánh lừa khi lệch lớp (baseline `DummyClassifier`), precision vs recall theo bối cảnh, hạ threshold → recall tăng/precision giảm, cross-validation (mean ± std, `StratifiedKFold`) |
| Mini-project, tích hợp (p5-05) | 3 | quy trình đúng: làm sạch → split → chọn mô hình bằng CV trên train → chấm test **một lần**; target leakage (cột chỉ có sau khi biết kết quả); báo cáo trung thực (hai mô hình chênh < 1 std) |

- **Loại câu**: 8 `mcq`, 5 `output`, 3 `fill`, 2 `parsons` (rải đều; mỗi chủ đề ít nhất 2 loại khác nhau).
- **Độ khó**: 4 câu mức 1, 10 câu mức 2, 4 câu mức 3. Câu mức 3 nên là câu tích hợp hoặc bẫy phổ biến (leakage, chọn bằng test, accuracy lệch lớp).
- mcq: rải `answer` đều trên các vị trí 0–3 (đúng 2 câu mỗi vị trí); distractor là hiểu lầm thật; không "All of the above".
- **Câu mới hoàn toàn**: đọc hết 5 file `curriculum/phase-05-ml/p5-0*/quiz.yaml` trước; không chép hay đổi chút ít câu nào (trùng ý hoặc trùng code).
- Mỗi câu có `tags` có sẵn trong `curriculum/topics.yaml` (vd `ml-math`, `supervised-learning`, `sklearn`, `model-evaluation`, `data-prep`), và `explanation` song ngữ nói **vì sao**.
- parsons: `lines` theo thứ tự đúng, chạy được, mỗi dòng duy nhất, chỉ một thứ tự đúng (ràng buộc phụ thuộc hoặc kết quả in ra).
- Chỉ dùng kiến thức đã dạy trong phase 1–5.

## Quy tắc nội dung (bắt buộc, khớp phần sửa review phase 5)
- **Test chỉ dùng một lần**: chọn mô hình, hyperparameter, threshold bằng CV hoặc validation tách từ train. Không câu nào (kể cả đáp án hay explanation) ngụ ý chọn theo test score.
- **`zero_division`** (sklearn 1.7): chỉ precision cảnh báo khi TP+FP=0; F1/recall của dự đoán toàn 0 khi có dương thật trả 0.0 **không** cảnh báo. `zero_division=0` là giá trị dự phòng tường minh khi mẫu số bằng 0.
- Thuật ngữ VI thống nhất: accuracy = "tỉ lệ đoán đúng"; precision = "độ chuẩn khi báo dương"; recall = "độ nhạy, tức tỉ lệ bắt được". Không dùng "độ chính xác", "độ phủ".
- `load_breast_cancer`: nếu dùng thì `y = 1 - y` để lớp dương = ung thư. Tốt hơn: dùng dữ liệu nhỏ tự tạo bằng `np.random.default_rng(seed)`.
- Ngẫu nhiên chỉ qua `default_rng` và `random_state`. Không `fetch_*`, không mạng.

## Quy tắc output (bắt buộc, app chạy Pyodide 32-bit)
- Không in `dtype` mảng NumPy số nguyên; không `astype(int)`/`dtype=int` (dùng `"int64"`); không `df.info()`.
- Không in numpy scalar hay list/dict chứa chúng: dùng `.tolist()`, `round(float(x), 3)`, `int()`.
- Không phát warning nào (validator chạy với cảnh báo; tránh `ConvergenceWarning`, `UndefinedMetricWarning`, FutureWarning).
- DataFrame in ra tối đa 4 cột, dòng dưới 60 ký tự. Số thực in ra phải làm tròn.
- Code ngắn (câu output/fill dưới ~15 dòng), chạy nhanh (mô hình nhỏ, dữ liệu vài chục mẫu).
- `output`/`fill`/`parsons` phải chạy được với validator (validator chạy code thật và so đáp án). Kết quả phải giống nhau với sklearn 1.7.0 / numpy 2.2.5 (app) và bản local.

## Tiêu chí hoàn thành (checklist)
1. [ ] Đúng blueprint: 18 câu, phân bổ chủ đề, loại câu, độ khó, vị trí đáp án mcq; ghi bảng đếm thực tế vào report.
2. [ ] Không trùng câu với quiz 5 bài (report liệt kê mỗi câu kiểm ý nào).
3. [ ] EN/VI đầy đủ, VI tự nhiên, code giống hệt giữa hai ngôn ngữ.
4. [ ] Tuân thủ "Quy tắc nội dung" và "Quy tắc output".
5. [ ] Lệnh kiểm tra xanh, chạy đúng như ghi.

## Lệnh kiểm tra
Từ gốc repo `D:\Proj\python-ai-platform`:
```
uv run python tools/validate.py --path curriculum/phase-05-ml
uv run python tools/validate.py
uv run python -m pytest curriculum
uv run python tools/build_content.py
grep -nE "astype\(int\)|dtype=int\b|\.info\(|fetch_|độ chính xác|độ phủ" curriculum/phase-05-ml/phase-test.yaml
git status --short
```
Mong đợi: validate 0 lỗi (đếm exams tăng 1); pytest exit 0; build_content in số exams tăng 1; grep rỗng; chỉ có một file mới `curriculum/phase-05-ml/phase-test.yaml` (ngoài `tasks/`, `.hallmark/` vốn untracked).

## Ghi chú cho worker
- Đọc mẫu `curriculum/phase-04-data/phase-test.yaml`, schema `tools/schema/exam.schema.json`, 5 file quiz phase 5 và lesson phase 5 để biết API nào đã dạy.
- Tự chạy code câu output bằng python để kiểm số, kèm `-W error` để chắc không có warning: `uv run python -W error snippet.py`.
- Dùng `uv run python -m pytest`, không dùng `uv run pytest`.

## Trạng thái
- Bước hiện tại: 5 (đạt sau vòng 2: vòng 1 đáp án mcq lộ vì dài nhất; boss duyệt 18/18 câu, chạy sạch -W error, xem và nộp bài thi trong app; đã commit `44d05fa`)
- Vòng: 2/3
- Số lần swap: 0
- Fallback: không
- Model: Gemini 4 Hydrogen (High)

## Feedback vòng 1
Boss đã duyệt 18/18 câu: đáp án đúng, phân bổ đúng blueprint, chạy sạch với `-W error`, hiển thị và chấm đúng trong app. Còn 2 lỗi:
1. **Đáp án đúng lộ vì dài nhất**: ở q02, q04, q07, q11, q13, q16, q17 lựa chọn đúng dài gấp đôi các lựa chọn sai và có giải thích trong ngoặc ("so the shuffle is reproducible", "minimize false bans", "too simple to fit even train", ...). Người học chọn câu dài nhất là đúng.
   Sửa: cân độ dài 4 lựa chọn của mỗi câu mcq (chênh không quá ~30%). Rút lý do ra khỏi lựa chọn đúng (lý do đã có trong `explanation`), hoặc cho distractor một lý do nghe hợp lý tương tự. Giữ nguyên ý đúng/sai, giữ `answer` và thứ tự lựa chọn; sửa đồng thời `en` và `vi`.
2. q06 VI lựa chọn thứ 2: "vì số phút là con số" → "vì số phút là số nguyên" (khớp EN "integers").
Chỉ sửa `curriculum/phase-05-ml/phase-test.yaml`. Chạy lại `uv run python tools/validate.py --path curriculum/phase-05-ml` và `uv run python tools/validate.py`. Ghi vào report bảng độ dài (số ký tự EN) 4 lựa chọn của từng câu mcq sau khi sửa.
