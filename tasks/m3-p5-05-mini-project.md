# M3 bước 13: p5-05 Mini-project: ML classifier

## Mục tiêu
Viết mini-project cuối phase 5 (`p5-05-mini-project`, `kind: project`): **bộ phân loại ticket khẩn cấp** từ log thô đến một báo cáo kết quả **trung thực**.
Người học ghép những gì đã học: làm sạch bằng pandas (p4-03), feature/label và chia dữ liệu (p5-02), pipeline sklearn (p5-03), baseline, precision/recall/F1, ngưỡng, cross-validation (p5-04).
Gần như không có kiến thức mới. Một ý mới duy nhất được phép: **target leakage** (feature chỉ biết được *sau* khi có đáp án), dạy ở phần lỗi thường gặp.
Bài mẫu về hình dạng mini-project: `curriculum/phase-04-data/p4-06-mini-project/` (đã duyệt: opening, "The plan" có mermaid + bảng các mảnh, 2 bài tập `kind: project`, ~9 test mỗi bài, có "Đi xa hơn"). Giọng văn: `curriculum/phase-05-ml/p5-03-sklearn/`, `p5-04-evaluation/`.

## File được phép sửa/tạo
- Thư mục mới `curriculum/phase-05-ml/p5-05-mini-project/` và mọi file bên trong.
- `curriculum/glossary.yaml`: chỉ **thêm** thuật ngữ mới nếu thật sự có (vd target leakage, holdout set); có thể không thêm gì.

## Không được đụng
- `apps/`, `tools/`, `pyproject.toml`, `uv.lock`, `curriculum/syllabus.yaml`, `curriculum/topics.yaml`, các bài khác, `exams/`.
- Không xóa file, không `git commit`, **không chạy `pnpm --filter web build`**. Không tạo `phase-test.yaml` (bước 14).

## Quy tắc output (bắt buộc; xem đầu `tasks/M3-PLAN.md`)
- Pyodide 32-bit: không in `dtype` của mảng NumPy số nguyên, không `astype(int)`/`dtype=int` (dùng `"int64"`), không `df.info()`. Không in list/dict/tuple chứa numpy scalar (`.tolist()`, `int(...)`, `round(float(x), 3)`).
- Ngẫu nhiên: chỉ `np.random.default_rng(seed)` và `random_state=<số>` (`train_test_split`, `StratifiedKFold(shuffle=True, ...)`, `DecisionTreeClassifier`, ...). Không `np.random.seed`, `np.random.rand`, module `random`.
- Dữ liệu: tự sinh, không `fetch_*`, không đọc/ghi file.
- **Không có warning nào** (stderr sạch): `zero_division=0` ở mọi precision/F1 có thể chia 0; `LogisticRegression` đặt trong pipeline có scaler; không fit bằng DataFrame rồi predict bằng ndarray (hoặc ngược lại).
- DataFrame in ra ≤ 4 cột, dòng < 60 ký tự (rộng hơn thì in từng dòng bằng f-string). Mọi số thực in ra phải làm tròn.
- matplotlib (nếu dùng): example in thêm dòng tóm tắt; lesson ghi `# (shows ...)` / `# (hiện ...)` sau `plt.show()`; hàm vẽ trong bài tập trả `(fig, ax)`, không `plt.show()`.
- Mọi `print(...)  # ...` trong lesson phải khớp output thật.
- Mỗi khối python trong lesson phải chạy độc lập. Để không lặp dài, bộ sinh dữ liệu phải **ngắn** (≤ 15 dòng) và giống hệt nhau ở mọi khối dùng nó. Trong app toàn bộ CV của một khối phải chạy nhanh (≤ 300 dòng dữ liệu, ≤ 3 mô hình, 5 fold).

## Dữ liệu dùng chung (worker thiết kế, boss duyệt qua output)
Một hàm `make_ticket_log(n, seed)` sinh **DataFrame thô** khoảng 200–300 ticket hỗ trợ của một sản phẩm AI, khoảng 15–25% là khẩn cấp (`urgent` = 1), với:
- feature số có tín hiệu thật nhưng chồng lấn (vd `tokens`, `num_links`, `error_count`, `hours_since_deploy`), một cột phân loại `plan` (`free`/`pro`/`enterprise`) được ghi bẩn (`" Pro"`, `"PRO"`, `"enterprise "`),
- vết bẩn theo đúng p4-03: vài ô số thiếu, vài `ticket_id` trùng, một cột số bị đọc thành chuỗi (vd `"1,200"`) nếu làm được gọn,
- một cột **target leakage** `escalated_to_oncall` (gần như trùng với `urgent`, chỉ biết sau khi xử lý ticket) để dùng ở phần lỗi thường gặp; pipeline chính **phải bỏ** cột này.
Ràng buộc kết quả (worker chạy thật và chọn seed/tham số sao cho đúng, **không bịa số**):
1. Baseline `DummyClassifier(strategy="most_frequent")` có accuracy cao nhưng F1 lớp khẩn cấp = 0.
2. Ít nhất một mô hình thật có F1 (CV) rõ ràng hơn baseline.
3. Hai mô hình thật có F1 trung bình CV chênh nhau **ít hơn** độ lệch chuẩn, để phần báo cáo trung thực có cái để nói ("không thể khẳng định mô hình nào tốt hơn").
4. Có cột leakage thì F1 gần 1.0 (thấy rõ là "quá đẹp để là thật").

## Nội dung bài (boss chốt dàn ý, worker viết)
Opening (không heading): team hỗ trợ muốn tự động gắn cờ ticket khẩn cấp để chuyển cho người trực. Bạn sẽ đi từ log thô đến một con số mà team **tin được**. Một câu: "gần như không có gì mới, bạn ghép những gì đã học; điều quan trọng nhất là báo cáo trung thực".

1. **The plan / Kế hoạch**: **mermaid** `flowchart LR` (≤ 8 node): log thô → làm sạch → X, y → chia train/test (giữ test riêng) → CV trên train để chọn mô hình → đánh giá một lần trên test → báo cáo. **Bảng các mảnh** `| Piece | Input | Output |` cho `prepare_features`, `evaluate_models`, `write_report`; nói rõ Exercise 1 / Exercise 2 làm mảnh nào.
2. **Nhìn dữ liệu thô**: `shape`, `isna().sum()`, `value_counts()` của `plan` và của `urgent` (tỉ lệ lớp). **Picture in text** (fence `text`): vài dòng thô kèm chú thích vấn đề.
3. **Phần 1: làm sạch và tạo feature**: chuẩn hóa `plan`, bỏ trùng, xử lý ô thiếu (nêu rõ chọn bỏ dòng hay điền và vì sao), biến `plan` thành số (map tay sang 0/1/2 hoặc các cột 0/1 làm bằng `==`; không cần `get_dummies`), bỏ cột leakage, tạo `X` (ndarray float theo thứ tự cột cố định) và `y` (`"int64"`). Bảng `| problem | fix |`. Mời bấm **Visualize** ở một khối nhỏ trong phần này.
4. **Phần 2: baseline và chọn mô hình bằng CV**: `train_test_split(..., stratify=y, random_state=...)` giữ test riêng; trên **train**, `StratifiedKFold(5, shuffle=True, random_state=0)`, `cross_val_score(..., scoring="f1")` cho baseline, LogisticRegression pipeline, DecisionTree (hoặc KNN pipeline). **Bảng kết quả** `| model | CV F1 mean | CV F1 std |` khớp output.
5. **Phần 3: đánh giá một lần trên test**: fit mô hình đã chọn trên toàn bộ train, `confusion_matrix(...).tolist()`, precision/recall/F1 trên test; chọn ngưỡng bằng `predict_proba` **trên dữ liệu train/CV, không trên test** (vd `cross_val_predict(..., method="predict_proba")` trên train, giới thiệu một câu) để đạt recall mục tiêu, rồi áp ngưỡng đó cho test. Trace table nhỏ cho ngưỡng.
6. **Phần 4: báo cáo trung thực**: báo cáo vài dòng (in bằng f-string): kích thước test và số ticket khẩn cấp trong test, baseline, mô hình chọn với mean ± std CV, kết quả test, ngưỡng, và câu cảnh báo khi hai mô hình chênh ít hơn std. **Bảng so sánh** `| honest claim | misleading claim |` (vd "F1 0.71 ± 0.06 qua 5 fold" vs "độ chính xác 93%"; "trên 60 ticket test" vs không nói cỡ mẫu; "không chắc A tốt hơn B" vs "A tốt hơn B"). Callout `[!TIP]`: luôn ghi baseline và cỡ mẫu.
7. **Lỗi thường gặp** (3, chạy thật):
   - **Target leakage**: giữ `escalated_to_oncall` → CV F1 gần 1.0; giải thích vì sao feature này không có lúc dự đoán; sửa: bỏ cột.
   - Chọn ngưỡng (hoặc mô hình) bằng cách nhìn **test** rồi báo cáo điểm test đó → con số lạc quan; sửa: chọn trên train/CV, test chỉ dùng một lần.
   - Báo cáo accuracy thay cho F1/recall trên dữ liệu lệch lớp (in accuracy của baseline cạnh mô hình).
8. **Recap / Tóm tắt** + đoạn "Đi xa hơn" (2–3 gợi ý: thử thêm feature, `class_weight="balanced"`, vẽ precision/recall theo ngưỡng).

`duration_min: 45–50`. `review_by: "2027-11-01"`. `further_reading`: scikit-learn "Common pitfalls and recommended practices" (mục data leakage), scikit-learn "Tuning the decision threshold for class prediction" (URL chính thức).

## Examples (3)
- `01_raw_ticket_log`: sinh log thô, in dấu hiệu bẩn (ô thiếu theo cột, biến thể `plan`, số id trùng, tỉ lệ khẩn cấp).
- `02_model_selection_cv`: làm sạch gọn, CV F1 của baseline và 2 mô hình trên train, in bảng mean ± std, in mô hình được chọn.
- `03_honest_report`: chọn ngưỡng trên train bằng `cross_val_predict`, đánh giá một lần trên test, in báo cáo trung thực nhiều dòng.

## Exercises (2, đều `kind: project`, difficulty 3)
- `ex01-prepare-features`: `prepare_features(raw: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]` làm đúng các bước Phần 1: chuẩn hóa `plan`, bỏ `ticket_id` trùng (giữ lần đầu), xử lý ô thiếu đúng như bài dạy, **bỏ** cột leakage, trả `X` (float, cột theo thứ tự cố định ghi trong prompt) và `y` (`"int64"`). Không sửa `raw`. **8–10 test** (mỗi quy tắc một test, cộng: thứ tự cột/shape, `y` chỉ 0/1, cột leakage không lọt vào X (vd số cột), DataFrame nhỏ viết tay trong test). Starter: khung hàm có `# TODO` từng bước, `return None`.
- `ex02-evaluate-and-report`: hai hàm
  - `evaluate_models(X: np.ndarray, y: np.ndarray, seed: int) -> dict[str, tuple[float, float]]`: trên **toàn bộ** X, y đưa vào (người gọi đã giữ test riêng), `StratifiedKFold(n_splits=5, shuffle=True, random_state=seed)`, `cross_val_score(..., scoring="f1")` cho đúng ba mô hình có tên cố định `"baseline"` (`DummyClassifier(strategy="most_frequent")`), `"logreg"` (`make_pipeline(StandardScaler(), LogisticRegression())`), `"tree"` (`DecisionTreeClassifier(max_depth=3, random_state=0)`); trả `{name: (mean, std)}` làm tròn 3, `float` Python. Baseline F1 = 0.0 không được sinh warning (cần `zero_division` qua `make_scorer(f1_score, zero_division=0)`, giới thiệu trong prompt, hoặc cách tương đương đã chạy thử sạch warning).
  - `write_report(results: dict[str, tuple[float, float]], n_test: int) -> list[str]`: các dòng báo cáo theo **định dạng cố định ghi trong prompt** (vd `"baseline F1: 0.000 +/- 0.000"`, một dòng cho mỗi mô hình theo thứ tự `results`, dòng `"best: <name>"` là mô hình không phải baseline có mean cao nhất (hòa → tên theo chữ cái), dòng `"test size: <n_test>"`, và dòng cảnh báo `"warning: <a> and <b> differ by less than one std"` khi mean của hai mô hình tốt nhất (không tính baseline) chênh nhỏ hơn std lớn hơn của chúng). Không có mô hình nào ngoài baseline → `ValueError`.
  **8–10 test** (giá trị CV đúng trên dữ liệu cố định sinh trong test bằng `default_rng`, kiểu trả về, baseline 0.0 và không warning (`pytest` chạy với `-W error::UserWarning` trong lệnh kiểm tra), định dạng từng dòng, có/không có dòng cảnh báo, hòa, `ValueError`).
  Có `alternatives/01_manual_folds.py`: `evaluate_models` tự lặp `skf.split(X, y)`, `clone`, fit, `f1_score(..., zero_division=0)` thay cho `cross_val_score` + `.md` so sánh. Alternative phải qua **cùng** bộ test (kết quả phải trùng tới 3 chữ số).
- Hint 2 là kế hoạch **bằng lời**; hint 3 là khung code chừa ít nhất 2–3 chỗ `...` thật sự, không lộ lời giải.
- Docstring ví dụ trong starter/solution: số phải chạy thật mới ghi.

## Quiz
15–18 câu, mỗi loại `mcq`/`output`/`fill`/`parsons` ít nhất 2; nghiêng về khó vừa (vd 3 dễ, 9 vừa, 4 khó) vì là project. 6 flashcard. Tag: `model-evaluation`, `sklearn`, `data-cleaning` (có sẵn). Câu hỏi xoay quanh quyết định trong pipeline (thứ tự bước, test chỉ dùng một lần, nhận ra leakage, câu báo cáo nào trung thực); câu `output` dùng dữ liệu nhỏ viết tay, chạy nhanh, không warning. Không lặp câu các bài trước. Đáp án mcq không phụ thuộc vị trí.

## Tiêu chí hoàn thành (checklist)
1. [ ] Đủ file theo layout CONTENT_GUIDE; `meta.yaml` có `phase: p5`, `order: 5`, `kind: project`, `prerequisites: [p5-04-evaluation, p4-03-cleaning]`, `outcomes` khớp syllabus (có thể thêm 2–3 dòng như p4-06), `tags` từ danh sách trên.
2. [ ] Lesson đúng dàn ý, đủ: mermaid, bảng các mảnh, picture in text, bảng problem/fix, bảng kết quả, trace table ngưỡng, bảng honest/misleading, một lời mời Visualize, callout.
3. [ ] Dữ liệu thỏa 4 ràng buộc kết quả ở trên (nêu số thật trong report).
4. [ ] Code giữa `lesson.en.md` và `lesson.vi.md` giống hệt (trừ comment); số dòng mermaid bằng nhau; fence `text` giống hệt.
5. [ ] Tuân thủ "Quy tắc output" (kể cả không warning).
6. [ ] Exercise: starter fail, solution và alternative pass (pytest **và** browser runner); hint đủ 3 tầng.
7. [ ] Bản VI tự nhiên, xưng "bạn", thuật ngữ giữ tiếng Anh kèm giải nghĩa lần đầu.
8. [ ] Lệnh kiểm tra xanh, chạy đúng như ghi.
9. [ ] Chạy `uv run python tools/build_content.py`. Không có trình duyệt thì ghi rõ trong report.

## Lệnh kiểm tra
Từ gốc repo `D:\Proj\python-ai-platform`:
```
uv run python tools/validate.py --path curriculum/phase-05-ml/p5-05-mini-project
uv run python tools/validate.py
uv run python -m pytest curriculum/phase-05-ml -W error::UserWarning -W error::FutureWarning
uv run ruff check curriculum/phase-05-ml
grep -rnE "astype\(int\)|dtype=int\b|\.info\(|fetch_|np\.random\.(seed|rand)|^import random|open\(" curriculum/phase-05-ml/p5-05-mini-project
git status --short
```
Mong đợi: validate 0 lỗi; pytest exit 0; ruff sạch; grep rỗng; file mới chỉ trong `p5-05-mini-project/` (và `glossary.yaml` nếu thêm).
Thêm: chạy từng example và từng khối python của lesson bằng `uv run python -W error::UserWarning`, xác nhận stderr rỗng, output khớp comment, và ghi thời gian chạy khối chậm nhất vào report.

## Ghi chú cho worker
- Đọc `docs/CONTENT_GUIDE.md`, `curriculum/phase-04-data/p4-06-mini-project/` (hình dạng project), `curriculum/phase-05-ml/p5-04-evaluation/` (giọng văn, cách viết hint đã được duyệt).
- Test chỉ dùng: assert, pytest.raises, pytest.approx, pytest.mark.parametrize, `@pytest.fixture` định nghĩa trong file test. Test được import sklearn.
- Dùng `uv run python -m pytest`, không dùng `uv run pytest`.
- Con số trong test, docstring, bảng và comment lesson: chạy thật rồi mới ghi.

## Trạng thái
- Bước hiện tại: 5 (đạt sau vòng 2; boss kiểm trong app: Visualize mini 18 bước, ex02 10/10; chờ user duyệt commit)
- Vòng: 2/3
- Số lần swap: 0
- Fallback: không
- Model: Gemini 4 Hydrogen (High)

## Feedback vòng 1
Boss đã chạy lại: validate 0 lỗi, pytest 648 passed (phase 5 sạch warning), ruff sạch, grep rỗng; 9 khối lesson khớp comment; bảng `text` khớp dữ liệu thật; build 55 trang; trong app ex02 qua 10/10 (≈4 giây). Còn 2 việc:
1. **Visualize hỏng ở khối làm sạch `mini`** (`lesson.en.md` + `lesson.vi.md`, §3 khối đầu): trong app trace dừng ở "Trace stopped after 600 steps" khi vẫn còn **bên trong** `make_ticket_log` (các list comprehension 240 phần tử ăn hết `MAX_STEPS = 600` của `tools/pyrunner/tracer.py`), nên người học không bao giờ thấy `mini` co từ 5 xuống 2 dòng như câu mời hứa. Sửa: khối này **không gọi** `make_ticket_log`; tạo `mini` trực tiếp bằng `pd.DataFrame({...})` viết tay đúng 5 dòng thô t003, t005, t012, t003 (bản trùng), t042 với giá trị thật (đã có trong fence `text` ở §2; thêm cột `hours_since_deploy` lấy từ dữ liệu thật). Giữ nguyên các bước làm sạch và output. Xác nhận bằng `uv run python -c "from tools.pyrunner.tracer import trace; ..."` (hoặc cách tương đương) rằng khối chạy hết trong < 150 bước và bước cuối có `mini` 2 dòng; ghi số bước vào report.
2. Ngay sau khối `make_ticket_log` đầu tiên (§2), thêm 1 câu (EN + VI): hàm này chỉ **giả lập** log để bài chạy được trong trình duyệt, bạn không cần hiểu từng dòng của nó; các khối sau chép lại y hệt hàm này để mỗi khối chạy độc lập.
Chạy lại toàn bộ "Lệnh kiểm tra" và `uv run python tools/build_content.py`, cập nhật report.
