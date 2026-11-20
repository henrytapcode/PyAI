# M3 bước 9: bài p5-01 Math bridge: vectors & gradients

## Mục tiêu
Viết bài đầu tiên của phase 5 (`p5-01-math-bridge`) trong thư mục mới `curriculum/phase-05-ml/` (tên thư mục theo `curriculum/syllabus.yaml`, khối `p5`), đúng `docs/CONTENT_GUIDE.md`, song ngữ EN/VI.
Đây là **"cầu nối toán bằng hình ảnh"** (docs/DESIGN.md §3): toán vừa đủ để hiểu ML, **không chứng minh, không ký hiệu đạo hàm**. Người học đã xong phase 1–4 (NumPy array, vectorised math, `axis`, mask, pandas, matplotlib `fig, ax`, SQL).
Bài mẫu về giọng văn/hình dạng: `curriculum/phase-04-data/p4-01-numpy/` và `p4-04-matplotlib/` (đã duyệt, đã sửa review).

## File được phép sửa/tạo
- Thư mục mới `curriculum/phase-05-ml/p5-01-math-bridge/` và mọi file bên trong. Nếu validator đòi file cấp phase cho `curriculum/phase-05-ml/` thì tạo đúng file đó, ghi rõ trong report. **Không** tạo `phase-test.yaml`.
- `curriculum/glossary.yaml`: chỉ **thêm** thuật ngữ mới (vector, dot product, loss / mean squared error, gradient, gradient descent, learning rate; bỏ qua cái đã có).

## Không được đụng
- `apps/`, `tools/`, `curriculum/syllabus.yaml`, `curriculum/topics.yaml`, phase 1–4, `exams/`.
- Không xóa file, không `git commit`, **không chạy `pnpm --filter web build`** (dev server đang chạy).

## Quy tắc output (bắt buộc; xem đầu `tasks/M3-PLAN.md`)
- App chạy Pyodide 32-bit: không in `dtype` của mảng NumPy số nguyên; không `astype(int)`/`dtype=int` (dùng `"int64"`); không `df.info()`. Không in list/tuple/dict chứa numpy scalar (dùng `.tolist()`, `float()`, `round(float(x), n)`).
- **Mọi số thực in ra phải làm tròn** (`round(float(x), 3)` hoặc `np.round(a, 3)`), vì vòng lặp gradient descent dễ cho chữ số cuối khác nhau.
- matplotlib: example vẽ biểu đồ phải in thêm dòng tóm tắt bằng chữ; trong lesson sau `plt.show()` ghi `# (shows ...)` / `# (hiện ...)`; chỉ API có ở 3.8.
- Mọi `print(...)  # ...` trong lesson phải khớp output thật; thông báo lỗi lấy từ lần chạy thật. Khi tự chạy code có matplotlib ngoài validator, đặt `MPLBACKEND=Agg`.
- Chỉ dùng thứ đã dạy ở phase 1–4. Thứ mới của bài này (`@`, `np.dot`, `np.linalg.norm`, `np.sqrt`, ý tưởng loss/gradient/learning rate) phải được giới thiệu bằng một câu ở lần dùng đầu tiên.

## Nội dung bài (boss chốt dàn ý, worker viết)
Opening (không heading): một mô hình ML chỉ là vài con số (weights) được chỉnh dần cho sai số nhỏ lại. Bài này cần đúng ba ý: vector, tích vô hướng, gradient. Không cần nhớ công thức đạo hàm.

1. **Vector là danh sách số có ý nghĩa**: feature của một request (tokens, latency, số tin nhắn) → `np.array`; độ dài vector `np.linalg.norm` (giới thiệu một câu: "khoảng cách từ gốc tới đầu mũi tên", ví dụ `[3, 4]` → `5.0`). **Picture in text** (fence `text`): mũi tên `[3, 4]` trên lưới nhỏ.
2. **Tích vô hướng (dot product)**: nhân từng cặp rồi cộng; `np.dot(a, b)` và `a @ b`. Ý nghĩa 1: **điểm có trọng số** — `prediction = weights @ features + bias`. Ý nghĩa 2 (một đoạn ngắn, xem trước phase 7): hai embedding cùng hướng thì dot lớn; cosine similarity = `a @ b / (norm(a) * norm(b))`. **Trace table** `| i | a[i] | b[i] | a[i]*b[i] | running sum |`.
3. **Đo sai số bằng loss**: mô hình đường thẳng `y = w * x + b`; mean squared error `np.mean((pred - y) ** 2)` (giải thích bằng lời: bình phương để sai âm/dương không triệt tiêu và phạt sai lớn nặng hơn). Tính loss cho vài giá trị `w` rồi vẽ **loss theo w** (biểu đồ hình chữ U, `ax.plot`), in `w` có loss nhỏ nhất trong lưới thử.
4. **Gradient = độ dốc = hướng xuống dốc**: ước lượng độ dốc bằng số, **không đạo hàm**: `slope = (loss(w + h) - loss(w - h)) / (2 * h)` với `h = 0.001`. Dốc dương → giảm `w`, dốc âm → tăng `w`. **Bảng so sánh** `| slope | what it means | which way to move w |`.
5. **Gradient descent**: vòng lặp `w = w - lr * slope` (rồi thêm `b` với công thức gradient MSE cho sẵn, giải thích bằng lời: "trung bình của 2 × sai số × x"). **Mermaid** `flowchart TD` (≤ 7 node): start w, b → predict → loss → slope → step opposite → repeat? → done. **Trace table** 4–5 bước `| step | w | loss |` (số làm tròn, khớp output thật). Đây là section mời bấm **Visualize** (khối vòng lặp nhỏ, 4–5 bước). Thêm biểu đồ loss giảm theo step.
6. **Learning rate**: chạy cùng dữ liệu với `lr` nhỏ / vừa / quá lớn, in loss sau N bước (lớn quá thì loss tăng vọt). **Bảng so sánh** `| learning rate | what happens |`. Callout `[!TIP]` chọn lr.
7. **Lỗi thường gặp** (3–4, chạy thật để lấy đúng output/thông báo):
   - Dùng `a * b` (nhân từng phần tử, ra mảng) thay vì `a @ b` (ra một số).
   - Hai vector khác độ dài: `np.dot(a, b)` → `ValueError: shapes (3,) and (2,) not aligned: 3 (dim 0) != 2 (dim 0)` (boss đã đo; dùng `np.dot` trong ví dụ lỗi vì thông báo của `@` khó đọc).
   - Bước **cùng chiều** gradient (`w = w + lr * slope`) → loss tăng.
   - Learning rate quá lớn → loss dao động/phình to (in vài giá trị đã làm tròn; nếu ra `inf`/`nan` thì in đúng như vậy).
8. **Recap / Tóm tắt**.

Thời lượng 12–15 phút. `review_by: "2027-11-01"`. `further_reading`: 3Blue1Brown "Essence of linear algebra" (chương dot product) và Google ML Crash Course "Reducing loss: gradient descent" (URL chính thức).

## Examples (3)
- `01_feature_scores`: 3 request là 3 vector feature, một vector weights; tính điểm từng request bằng `@`, in request điểm cao nhất.
- `02_embedding_similarity`: 3–4 "embedding" nhỏ 4 chiều (số tự đặt), cosine similarity giữa câu hỏi và từng tài liệu, in tài liệu gần nhất (làm tròn 3 chữ số).
- `03_fit_a_line`: dữ liệu `x` (tokens, nghìn) và `y` (độ trễ) gần thẳng hàng; gradient descent tìm `w`, `b`; in `w`, `b` (làm tròn 2) và loss đầu/cuối; vẽ dữ liệu + đường fit.

## Exercises (2)
- `ex01-weighted-score` (`kind: fill`): `weighted_score(features: np.ndarray, weights: np.ndarray, bias: float) -> float` = `float(features @ weights + bias)`, các ô `___` trong thân hàm. 3–5 test: kết quả đúng (`pytest.approx`), trả `float` Python (`type(result) is float`), bias âm, mọi weight bằng 0 → trả bias.
- `ex02-gradient-descent` (`kind: code`): hai hàm
  - `mse(w: float, b: float, xs: np.ndarray, ys: np.ndarray) -> float`: mean squared error của `w * xs + b`, trả `float`.
  - `fit_line(xs: np.ndarray, ys: np.ndarray, lr: float, steps: int) -> tuple[float, float]`: bắt đầu `w = b = 0.0`, lặp `steps` lần với gradient MSE **cho sẵn trong prompt** (`grad_w = mean(2 * (pred - ys) * xs)`, `grad_b = mean(2 * (pred - ys))`), trả `(round(w, 3), round(b, 3))` là `float` Python.
  5–6 test: `mse` = 0 khi đường đi qua mọi điểm; `fit_line` với dữ liệu sạch `y = 2x + 1` hội tụ gần `(2.0, 1.0)` (`pytest.approx(..., abs=0.05)`); `steps=0` → `(0.0, 0.0)`; loss sau khi fit nhỏ hơn loss ban đầu; kiểu trả về là tuple 2 `float`. Chọn `lr`/`steps` trong test sao cho hội tụ chắc chắn mà vẫn nhanh (< 0.5 giây). Có `alternatives/01_numeric_slope.py` dùng độ dốc ước lượng bằng số như §4 + `.md` so sánh (chậm hơn, nhưng không cần công thức).

## Quiz
15–18 câu, mỗi loại `mcq`/`output`/`fill`/`parsons` ít nhất 2; khoảng 5 dễ, 7 vừa, 3 khó. 6 flashcard. Tag: `ml-math` (chính), có thể thêm `numpy`. Đáp án mcq rải đều các vị trí (app xáo theo id, nhưng vẫn giữ thói quen tốt). Câu `output` phải in số đã làm tròn.

## Tiêu chí hoàn thành (checklist)
1. [ ] Đủ file theo layout CONTENT_GUIDE; `meta.yaml` có `phase: p5`, `order: 1`, `tags` gồm `ml-math`, `prerequisites: [p4-01-numpy, p4-04-matplotlib]`, `outcomes` khớp syllabus (có thể thêm 1–2 dòng).
2. [ ] Lesson đúng dàn ý, đủ: mermaid, trace table (2 cái), picture in text, bảng so sánh, một lời mời Visualize, callout. Không có ký hiệu đạo hàm (`d/dw`, `∂`) hay chứng minh.
3. [ ] Code giữa `lesson.en.md` và `lesson.vi.md` giống hệt (trừ comment); số dòng mermaid bằng nhau; fence `text` giống hệt.
4. [ ] Tuân thủ "Quy tắc output".
5. [ ] Exercise: starter fail, solution và alternative pass (pytest **và** browser runner); hint đủ 3 tầng; hint 3 để trống ít nhất 2–3 dòng thật sự (không gần như lời giải).
6. [ ] Bản VI tự nhiên, xưng "bạn", thuật ngữ giữ tiếng Anh kèm giải nghĩa lần đầu (vd "tích vô hướng (dot product)").
7. [ ] Lệnh kiểm tra xanh, chạy đúng như ghi.
8. [ ] Chạy `uv run python tools/build_content.py`. Không có trình duyệt thì ghi rõ trong report.

## Lệnh kiểm tra
Từ gốc repo `D:\Proj\python-ai-platform`:
```
uv run python tools/validate.py --path curriculum/phase-05-ml/p5-01-math-bridge
uv run python tools/validate.py
uv run python -m pytest curriculum/phase-05-ml
uv run ruff check curriculum/phase-05-ml
grep -rnE "astype\(int\)|dtype=int\b|\.info\(|∂|d/dw" curriculum/phase-05-ml
git status --short
```
Mong đợi: validate 0 lỗi; pytest exit 0; ruff sạch; grep rỗng; file mới chỉ trong `curriculum/phase-05-ml/` (và `glossary.yaml`).

## Ghi chú cho worker
- Đọc `docs/CONTENT_GUIDE.md`, `docs/DESIGN.md` §3 (cầu nối toán), rồi `curriculum/phase-04-data/p4-01-numpy/` và `p4-04-matplotlib/`.
- Test chỉ dùng: assert, pytest.raises, pytest.approx, pytest.mark.parametrize, `@pytest.fixture` định nghĩa trong file test.
- Dùng `uv run python -m pytest`, không dùng `uv run pytest`.

## Trạng thái
- Bước hiện tại: 5 (đạt sau vòng 1; boss kiểm trong app: Visualize khớp số, ex02 6/6 trên Pyodide; chờ user duyệt commit)
- Vòng: 1/3
- Số lần swap: 0
- Fallback: không
- Model: Gemini 4 Hydrogen (High)
