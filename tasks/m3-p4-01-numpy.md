# M3 bước 2: bài p4-01 NumPy arrays

## Mục tiêu
Viết bài đầu tiên của phase 4 (`p4-01-numpy`) đúng `docs/CONTENT_GUIDE.md`, song ngữ EN/VI, chạy được cả local và trong app (Pyodide tự tải numpy).
Người học đã xong phase 1–3 (list, dict, comprehension, hàm, dataclass, typing, pytest) nhưng **chưa biết NumPy**.

## File được phép sửa/tạo
- Thư mục mới `curriculum/phase-04-data/p4-01-numpy/` và mọi file bên trong (theo layout của CONTENT_GUIDE).
- Nếu validator đòi file cấp phase cho thư mục `curriculum/phase-04-data/` thì tạo đúng file đó, ghi rõ trong report. **Không** tạo `phase-test.yaml` (bước 8).
- `curriculum/glossary.yaml`: chỉ **thêm** thuật ngữ mới của bài (array, dtype, shape, vectorization, broadcasting, boolean mask, axis), đúng định dạng file.

## Không được đụng
- Mọi thứ trong `apps/`, `tools/`, `curriculum/syllabus.yaml`, `curriculum/topics.yaml`, các phase khác, `exams/`.
- Không xóa file, không `git commit`, **không chạy `pnpm --filter web build`** (dev server đang chạy).

## Nội dung bài (boss chốt dàn ý, worker viết)
Opening (không heading): vì sao AI engineer cần NumPy. Ví dụ: embedding là vector 384 số, một batch dự đoán là bảng số; tính trên list bằng vòng lặp vừa dài vừa chậm.

1. **Array là gì**: `np.array`, mọi phần tử cùng một kiểu; `shape`, `dtype`, `ndim`, `len`. So sánh list và array (bảng `| list | array |`).
2. **Tính vector hóa (vectorised math)**: `a * 2`, `a + b`, `a ** 2`, so với `[x * 2 for x in xs]`. Nhấn mạnh `list * 2` lặp list còn `array * 2` nhân từng số. Chỉ broadcasting với một số (scalar); nhắc tên "broadcasting" một câu, chi tiết để "Đọc thêm".
3. **Hàm tổng hợp**: `sum`, `mean`, `min`, `max`, `argmax`, `round`. Có **trace table** cho một ví dụ tính trung bình (vd `| step | value | running total |`) để nối với mẫu accumulator đã học.
4. **Mảng 2D**: hàng × cột, `shape == (rows, cols)`, `a[r, c]`, `a[1]`, `a[:, 0]`, `axis=0` (theo cột) và `axis=1` (theo hàng). Có **picture in text** (fence ```` ```text ````) minh họa index hàng/cột và hướng `axis`.
5. **Boolean mask**: `a > 3` ra mảng bool, `a[a > 3]`, kết hợp `&`, `|` có ngoặc, đếm bằng `(a > 3).sum()`. Có **mermaid** `flowchart LR` cho luồng: array → so sánh → mask → lọc → kết quả. Đây là section mời bấm **Visualize** (một khối nhỏ, biến đổi rõ ràng).
6. **Tạo mảng nhanh**: `np.arange`, `np.zeros`, `np.ones`, `np.linspace`, `reshape`.
7. **Lỗi thường gặp** (3–4): dùng `and` thay `&` (ValueError "truth value of an array ... is ambiguous"); quên ngoặc `a > 1 & a < 5`; gán số thực vào mảng int bị cắt (`a = np.array([1, 2, 3]); a[0] = 2.7` → 2); slice là view nên sửa slice làm đổi mảng gốc (sửa bằng `.copy()`).
8. **Recap / Tóm tắt**.

Thời lượng 10–12 phút. `review_by: "2027-11-01"`. `further_reading`: NumPy "absolute beginners" guide và trang broadcasting (URL chính thức numpy.org).

## Examples (3)
- `01_sensor_readings`: một mảng nhiệt độ, tính min/max/mean, lọc giá trị bất thường bằng mask.
- `02_score_matrix`: mảng 2D điểm (học viên × bài), trung bình theo `axis=0` và `axis=1`, ai cao nhất bằng `argmax`.
- `03_batch_predictions`: mảng 2D xác suất mô hình (mẫu × lớp), `argmax(axis=1)` ra nhãn dự đoán, đếm mẫu có độ tin cậy ≥ 0.8.

## Exercises (2)
- `ex01-min-max-scale` (`kind: fill`): hàm `min_max_scale(values: np.ndarray) -> np.ndarray` đưa giá trị về [0, 1] bằng `(a - a.min()) / (a.max() - a.min())`, có các ô `___` trong thân hàm. Test: kết quả khớp `pytest.approx`, min là 0, max là 1, giữ đúng `shape`, không sửa mảng đầu vào.
- `ex02-predicted-labels` (`kind: code`): hàm `predicted_labels(probs: np.ndarray, labels: list[str], threshold: float) -> list[str]` — với mỗi hàng của `probs` (mẫu × lớp) lấy lớp có xác suất cao nhất; nếu xác suất đó < `threshold` thì trả `"unsure"`. Trả **list Python** các chuỗi. 4–6 test (gồm hàng hòa điểm: `argmax` lấy chỉ số đầu tiên; ngưỡng đúng bằng xác suất thì vẫn nhận). Có `alternatives/01_loop.py` (vòng lặp từng hàng) + `.md` giải thích khi nào nên dùng.

## Quiz
15–18 câu, mỗi loại `mcq`/`output`/`fill`/`parsons` ít nhất 2; khoảng 5 dễ, 7 vừa, 3 khó. 6 flashcard. Tag dùng: `numpy` (chính), có thể thêm tag có sẵn trong `topics.yaml`.

## Tiêu chí hoàn thành (checklist)
1. [ ] Đủ file theo layout CONTENT_GUIDE; `meta.yaml` có `phase: p4`, `order: 1`, `tags` gồm `numpy`, `prerequisites` khớp syllabus (`[p2-01-comprehensions]`), `outcomes` khớp syllabus (có thể thêm 1–2 dòng).
2. [ ] Lesson theo đúng dàn ý trên, có đủ: mermaid, trace table, picture in text, bảng so sánh, một lời mời Visualize, callout.
3. [ ] Code giữa `lesson.en.md` và `lesson.vi.md` giống hệt (trừ comment); số dòng mermaid bằng nhau; fence `text` giống hệt.
4. [ ] **Output in ra không phụ thuộc kiểu numpy scalar**: numpy 2 in list chứa `np.float64` thành `[np.float64(2.5)]`. Trong mọi example/quiz `output`, chỉ `print` array, số đơn lẻ, hoặc `.tolist()`/`float()`/`int()`; không in list/tuple/dict chứa numpy scalar.
5. [ ] Exercise: starter fail, solution và alternative pass (pytest **và** browser runner, validator đã kiểm cả hai); hint đủ 3 tầng mỗi ngôn ngữ đúng guide.
6. [ ] Bản VI tự nhiên, xưng "bạn", thuật ngữ giữ tiếng Anh kèm giải nghĩa lần đầu.
7. [ ] Lệnh kiểm tra xanh.
8. [ ] Xem bài trong app (dev server đang chạy, HMR không áp dụng cho nội dung: cần `uv run python tools/build_content.py` để app thấy bài mới, lệnh này an toàn khi dev server đang chạy): `http://localhost:3000/lesson/p4-01-numpy/`, bấm Run một khối numpy và Visualize ở khối được mời, ghi kết quả vào report.

## Lệnh kiểm tra
Từ gốc repo `D:\Proj\python-ai-platform`:
```
uv run python tools/validate.py --path curriculum/phase-04-data/p4-01-numpy
uv run python tools/validate.py
uv run python -m pytest curriculum/phase-04-data
uv run ruff check curriculum/phase-04-data
git status --short
```
Mong đợi: validate 0 lỗi (cả bài lẻ và toàn bộ); pytest exit 0; ruff sạch; chỉ có file mới trong `curriculum/phase-04-data/` (và `glossary.yaml` nếu thêm thuật ngữ).

## Ghi chú cho worker
- Đọc `docs/CONTENT_GUIDE.md` và bài mẫu `curriculum/phase-01-python-core/p1-01-variables/`; tham khảo thêm `curriculum/phase-02-intermediate/p2-01-comprehensions/` (cùng cấp độ). Bắt chước giọng văn và hình dạng file.
- Local dùng numpy 2.2.5, giống Pyodide trong app; `.out` phải khớp chính xác stdout.
- Test trả về numpy array thì so bằng `.tolist()` hoặc `pytest.approx(list(...))`, đừng `assert a == b` trên array (ra mảng bool, gây lỗi).
- Dùng `uv run python -m pytest`, không dùng `uv run pytest` (lỗi launcher).

## Trạng thái
- Bước hiện tại: 5 (đạt sau vòng 1, chờ user duyệt commit)
- Vòng: 1/3
- Số lần swap: 0
- Fallback: không
- Model: Gemini 4 Hydrogen (High)
