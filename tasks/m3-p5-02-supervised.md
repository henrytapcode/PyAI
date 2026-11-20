# M3 bước 10: bài p5-02 Supervised learning

## Mục tiêu
Viết bài `p5-02-supervised` trong `curriculum/phase-05-ml/`, đúng `docs/CONTENT_GUIDE.md`, song ngữ EN/VI.
Người học đã xong phase 1–4 và `p5-01-math-bridge` (vector, `@`, MSE, gradient descent, learning rate). **Chưa học scikit-learn** (để bài p5-03): bài này dạy **ý tưởng** bằng NumPy/pandas/matplotlib, không import `sklearn`.
Bài mẫu: `curriculum/phase-05-ml/p5-01-math-bridge/` (vừa duyệt) và các bài phase 4.

Boss đã đo (2026-11-13): `np.random.default_rng(seed)` (`permutation`, `normal`) và `np.polyfit` tới bậc 6 cho kết quả **giống hệt** giữa local và app (làm tròn 4 chữ số).

## File được phép sửa/tạo
- Thư mục mới `curriculum/phase-05-ml/p5-02-supervised/` và mọi file bên trong.
- `curriculum/glossary.yaml`: chỉ **thêm** thuật ngữ mới (supervised learning, feature, label, regression, classification, train/test split, overfitting, underfitting, accuracy, data leakage; bỏ qua cái đã có).

## Không được đụng
- `apps/`, `tools/`, `curriculum/syllabus.yaml`, `curriculum/topics.yaml`, các bài khác, `exams/`.
- Không xóa file, không `git commit`, **không chạy `pnpm --filter web build`**.

## Quy tắc output (bắt buộc; xem đầu `tasks/M3-PLAN.md`)
- Pyodide 32-bit: không in `dtype` của mảng NumPy số nguyên (vd kết quả `rng.permutation`), không `astype(int)`/`dtype=int` (dùng `"int64"`), không `df.info()`. Không in list/dict chứa numpy scalar (dùng `.tolist()`, `float()`, `round(float(x), n)`).
- Ngẫu nhiên: **luôn** `rng = np.random.default_rng(<seed>)`; không dùng `np.random.seed`, `np.random.rand`, `random` module.
- `np.polyfit`: tối đa bậc 6, x nằm trong `[0, 1]`; mọi hệ số/sai số in ra làm tròn ≤ 3 chữ số.
- Mọi số thực in ra phải làm tròn. DataFrame in ra ≤ 4 cột, dòng < 60 ký tự.
- matplotlib: example vẽ biểu đồ in thêm dòng tóm tắt; lesson ghi `# (shows ...)` / `# (hiện ...)` sau `plt.show()`; chỉ API có ở 3.8. Tự chạy code matplotlib ngoài validator thì đặt `MPLBACKEND=Agg`.
- Mọi `print(...)  # ...` trong lesson phải khớp output thật.
- Thứ mới của bài (`rng.permutation`, `np.polyfit`, `np.polyval`, slicing theo chỉ số đã xáo) phải được giới thiệu một câu ở lần dùng đầu.

## Nội dung bài (boss chốt dàn ý, worker viết)
Opening (không heading): "supervised" = học từ ví dụ **có sẵn đáp án**: lịch sử ticket đã gắn nhãn spam/không spam, request đã biết độ trễ. Mô hình học quy luật từ ví dụ cũ để đoán ví dụ mới.

1. **Feature và label**: `X` (mỗi hàng một ví dụ, mỗi cột một feature) và `y` (đáp án). **Picture in text** (fence `text`): bảng nhỏ chia vùng X | y. Bảng thuật ngữ `| term | meaning | example |`.
2. **Regression và classification**: đoán số (độ trễ, giá) vs đoán nhóm (spam / không spam, ý định người dùng). **Bảng so sánh** `| | regression | classification |` (output, loss/metric hay dùng: MSE vs accuracy, ví dụ AI).
3. **Mô hình đơn giản nhất: một ngưỡng**: bộ phân loại "score ≥ t thì spam"; thử vài `t`, tính accuracy (`(pred == y).mean()`); **trace table** `| t | predictions | accuracy |`. Nối lại p5-01: regression = đường thẳng học bằng gradient descent; classification ở đây = chọn ngưỡng tốt nhất.
4. **Chia train/test**: ví dụ "học bài tập nhưng thi đề mới". Xáo bằng `rng = np.random.default_rng(42)`, `idx = rng.permutation(len(X))`, lấy 80% đầu làm train, 20% còn lại làm test. **Mermaid** `flowchart LR` (≤ 7 node): data → shuffle → split → fit on train → evaluate on test → report. Đây là section mời bấm **Visualize** (khối nhỏ: permutation + cắt 2 phần, 6–10 ví dụ).
5. **Overfitting nhìn bằng mắt**: 10–12 điểm nhiễu quanh một đường cong (x trong [0, 1], seed cố định), chia train/test, fit `np.polyfit` bậc 1, 3, 6 trên train; bảng `| degree | train MSE | test MSE |` (làm tròn 3) cho thấy bậc cao: train MSE rất nhỏ nhưng test MSE lớn. Biểu đồ: điểm train, điểm test, 3 đường fit (`np.polyval` trên `np.linspace(0, 1, 100)`).
6. **Underfit / vừa / overfit**: **bảng so sánh** `| | underfitting | good fit | overfitting |` (train error, test error, dấu hiệu, cách sửa: thêm dữ liệu, mô hình đơn giản hơn, ...). Callout `[!TIP]`: luôn so train và test error.
7. **Lỗi thường gặp** (3–4, chạy thật):
   - Đánh giá trên chính dữ liệu train → điểm đẹp giả (in accuracy train vs test).
   - **Data leakage**: tính min/max để chuẩn hóa trên **toàn bộ** dữ liệu trước khi chia (nối với `min_max_scale` của p4-01); sửa: tính trên train rồi áp cho test.
   - Không xáo khi dữ liệu đã sắp xếp theo label → test toàn một lớp (in đếm label của test).
   - Không đặt seed → mỗi lần chạy chia khác nhau, kết quả nhảy (giải thích bằng lời + sửa bằng `default_rng(seed)`; không cần in kết quả ngẫu nhiên không seed).
8. **Recap / Tóm tắt**.

Thời lượng 12–15 phút. `review_by: "2027-11-01"`. `further_reading`: Google ML Crash Course "Training and test sets" và "Overfitting" (URL chính thức), scikit-learn user guide "Cross-validation" (nhắc là sẽ học ở p5-04).

## Examples (3)
- `01_ticket_threshold`: 12 ticket (spam score, label 0/1), thử các ngưỡng, in ngưỡng tốt nhất và accuracy.
- `02_train_test_split`: DataFrame 10 request (tokens, latency); xáo bằng seed, chia 8/2, in id thuộc train/test (`.tolist()`), fit đường thẳng bằng gradient descent (như p5-01) trên train, in MSE train và test.
- `03_overfitting_curve`: dữ liệu nhiễu, polyfit bậc 1/3/6, in bảng train/test MSE, vẽ biểu đồ.

## Exercises (2)
- `ex01-split-data` (`kind: fill`): `split_data(X: np.ndarray, y: np.ndarray, test_ratio: float, seed: int) -> tuple` trả `(X_train, X_test, y_train, y_test)`: `idx = rng.permutation(len(X))`, `n_test = int(round(len(X) * test_ratio))`, test là `n_test` chỉ số **đầu tiên** của `idx`, train là phần còn lại. Các ô `___` trong thân hàm. Test: kích thước đúng, train ∪ test = toàn bộ (so bằng `sorted(...tolist())`), cùng seed → cùng kết quả, X và y vẫn khớp từng hàng sau khi xáo, không sửa mảng đầu vào.
- `ex02-best-threshold` (`kind: code`): hai hàm
  - `accuracy(preds: np.ndarray, labels: np.ndarray) -> float`: tỉ lệ đúng, `float` Python; mảng rỗng → `0.0`.
  - `best_threshold(scores: np.ndarray, labels: np.ndarray) -> tuple[float, float]`: thử mỗi giá trị **khác nhau** trong `scores` làm ngưỡng (đoán 1 nếu `score >= t`), trả `(t, acc)` có accuracy cao nhất; hòa thì chọn `t` **nhỏ nhất**; cả hai là `float` Python (acc làm tròn 3).
  5–6 test (dữ liệu tách rời hoàn hảo → acc 1.0; trường hợp hòa; kiểu trả về; không sửa đầu vào). Có `alternatives/01_sorted_scan.py` (duyệt ngưỡng đã sắp xếp bằng vòng lặp Python thuần) + `.md` so sánh.

## Quiz
15–18 câu, mỗi loại `mcq`/`output`/`fill`/`parsons` ít nhất 2; khoảng 5 dễ, 7 vừa, 3 khó. 6 flashcard. Tag: `supervised-learning` (chính), có thể thêm `ml-math`, `numpy`. Đáp án mcq rải đều các vị trí. Không lặp câu của p5-01.

## Tiêu chí hoàn thành (checklist)
1. [ ] Đủ file theo layout CONTENT_GUIDE; `meta.yaml` có `phase: p5`, `order: 2`, `tags` gồm `supervised-learning`, `prerequisites: [p5-01-math-bridge, p4-02-pandas]`, `outcomes` khớp syllabus (có thể thêm 1–2 dòng).
2. [ ] Lesson đúng dàn ý, đủ: mermaid, trace table, picture in text, các bảng so sánh, một lời mời Visualize, callout. Không import `sklearn`.
3. [ ] Code giữa `lesson.en.md` và `lesson.vi.md` giống hệt (trừ comment); số dòng mermaid bằng nhau; fence `text` giống hệt.
4. [ ] Tuân thủ "Quy tắc output".
5. [ ] Exercise: starter fail, solution và alternative pass (pytest **và** browser runner); hint đủ 3 tầng; hint 3 để trống ít nhất 2–3 dòng thật sự.
6. [ ] Bản VI tự nhiên, xưng "bạn", thuật ngữ giữ tiếng Anh kèm giải nghĩa lần đầu.
7. [ ] Lệnh kiểm tra xanh, chạy đúng như ghi.
8. [ ] Chạy `uv run python tools/build_content.py`. Không có trình duyệt thì ghi rõ trong report.

## Lệnh kiểm tra
Từ gốc repo `D:\Proj\python-ai-platform`:
```
uv run python tools/validate.py --path curriculum/phase-05-ml/p5-02-supervised
uv run python tools/validate.py
uv run python -m pytest curriculum/phase-05-ml
uv run ruff check curriculum/phase-05-ml
grep -rnE "astype\(int\)|dtype=int\b|\.info\(|sklearn|np\.random\.(seed|rand)|^import random" curriculum/phase-05-ml/p5-02-supervised
git status --short
```
Mong đợi: validate 0 lỗi; pytest exit 0; ruff sạch; grep rỗng (riêng chữ "scikit-learn" trong câu văn/further_reading thì được, nhưng không `import sklearn`); file mới chỉ trong `p5-02-supervised/` (và `glossary.yaml`).

## Ghi chú cho worker
- Đọc `docs/CONTENT_GUIDE.md`, `curriculum/phase-05-ml/p5-01-math-bridge/`, và `curriculum/phase-04-data/p4-01-numpy/` (ex01 `min_max_scale`, dùng cho ví dụ leakage).
- Test chỉ dùng: assert, pytest.raises, pytest.approx, pytest.mark.parametrize, `@pytest.fixture` định nghĩa trong file test.
- Dùng `uv run python -m pytest`, không dùng `uv run pytest`.

## Trạng thái
- Bước hiện tại: 5 (đạt sau vòng 1; boss kiểm trong app: Visualize split + polyfit khớp số, ex02 6/6; chờ user duyệt commit)
- Vòng: 1/3
- Số lần swap: 0
- Fallback: không
- Model: Gemini 4 Hydrogen (High)
