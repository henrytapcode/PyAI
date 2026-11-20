# M3 bước 13b: sửa 38 điểm review phase 5

## Mục tiêu
Subagent reviewer đã soát 5 bài `curriculum/phase-05-ml/` (1 blocker, 10 major, 27 minor); boss đã xác minh các điểm chính (B1, M1, M2, M7, M9). Danh sách đầy đủ, có file và dòng: **`tasks/m3-p5-review.md`** (đọc trước). Sửa **cả 38 điểm**, theo đúng quyết định boss chốt ở từng mục dưới đây. Không thêm nội dung ngoài các mục này.
Luật nội dung: `docs/CONTENT_GUIDE.md`; quy tắc output phase 4–5 ở đầu `tasks/M3-PLAN.md` và trong các spec `tasks/m3-p5-0*.md` (Pyodide 32-bit, không in dtype int, không in numpy scalar trong list, DataFrame ≤ 4 cột, **không warning**, mọi comment `# output` khớp output thật).

## File được phép sửa
- Mọi file trong `curriculum/phase-05-ml/p5-0*/` (lesson, examples, exercises, quiz, meta). **Không tạo bài mới, không xóa file.** Được thêm test vào `test_exercise.py` có sẵn.
- `curriculum/glossary.yaml`: **chỉ** các mục thuật ngữ của phase 5 (và thêm mục `R²` mới), theo M3 và minor 2, 5, 27.

## Không được đụng
- `apps/`, `tools/`, `pyproject.toml`, `uv.lock`, `curriculum/syllabus.yaml`, `curriculum/topics.yaml`, các phase khác, `exams/`.
- Không `git commit`, **không chạy `pnpm --filter web build`**.
- Mọi sửa trong `*.en.md` phải sửa tương ứng ở `*.vi.md` (và ngược lại): code giống hệt, số dòng mermaid bằng nhau, fence `text` giống hệt. Tương tự `en:`/`vi:` trong yaml.

## Quy tắc chung cho cả phase (dùng để giải B1, M1)
- **Test chỉ chấm một lần ở cuối.** Chọn mô hình/ngưỡng bằng cross-validation trên train (p5-04 trở đi) hoặc tập validation tách từ train. Trước khi học CV (p5-02, p5-03), so sánh trên **một** lần chia held-out được coi là **cách nhìn đầu tiên**, kèm một câu nói rõ giới hạn và hẹn CV ở p5-04 / quy trình đầy đủ ở p5-05.
- **`zero_division` chỉ liên quan khi mẫu số = 0** (đúng với sklearn 1.7, boss đã chạy): precision khi không có dự đoán dương nào (TP+FP=0, **chỉ cái này sinh `UndefinedMetricWarning`** trong ví dụ của bài); recall khi không có mẫu dương thật nào (TP+FN=0); F1 khi TP+FP+FN=0. Mô hình đoán toàn 0 trên dữ liệu có mẫu dương: F1 = 0.0 và recall = 0.0 **không** cảnh báo.

## Các điểm cần sửa (số theo `tasks/m3-p5-review.md`)

### Blocker
**B1.** Thống nhất theo quy tắc trên:
- `p5-03-sklearn/lesson.*` §6: bỏ "selection strictly by test score". Viết: mọi mô hình chấm trên **cùng** một phần held-out, không bao giờ chọn theo train score; một lần chia là cái nhìn đầu tiên, còn may rủi (1 mẫu trên 45 là chênh lệch nhỏ); chọn thật thì dùng CV trên train (p5-04) và giữ test để chấm một lần ở cuối (p5-05). Hàng thứ ba bảng fair/unfair đổi cho khớp. Callout NOTE hiện có giữ, có thể gộp ý. Recap sửa tương ứng (bỏ "always pick the winner by test score").
- `p5-03-sklearn/quiz.yaml` q15 + f06: viết lại để đáp án đúng khớp quy tắc (vd phương án đúng: "cùng một split, cùng pipeline, so trên phần held-out, không chọn theo train"; không có phương án nào khẳng định "chọn theo test là đúng quy trình cuối"). Explanation nhắc CV ở p5-04.
- `p5-03-sklearn/examples/03_compare_models.*`: "Notice" nói rõ chênh 1 mẫu/45 nằm trong may rủi, dẫn sang CV; Try `max_depth=None` giải thích ngắn kết quả thật (minor 10).
- `p5-03-sklearn/exercises/ex02-compare-models`: giữ `best_model`; prompt thêm một câu: điểm đưa vào là điểm held-out để so sánh; ở p5-04 bạn sẽ đưa điểm CV vào cùng hàm này.
- `p5-04-evaluation/lesson.*` §5: giữ bảng quét ngưỡng trên test làm **minh họa** đánh đổi, thêm `> [!WARNING]` (cả EN/VI, cùng vị trí): ở đây quét trên test chỉ để thấy đánh đổi; chọn ngưỡng thật thì dùng xác suất out-of-fold trên train (p5-05), test chỉ chấm một lần.
- `p5-04-evaluation/examples/02_threshold_tradeoff.*`: **đổi code** để chọn ngưỡng trên tập validation tách từ train (`train_test_split` lần hai trên phần train, `stratify`), rồi áp ngưỡng đã chọn lên test **một lần**; cập nhật `.out`, `.md` (EN/VI), line refs.
- `p5-02-supervised/quiz.yaml` q15: sửa explanation (và chữ trong phương án nếu cần) theo quy tắc: so trên held-out là cái nhìn đầu tiên, không chọn theo train; quy trình chọn chuẩn (CV, test một lần) ở p5-04/p5-05.

### Major
- **M1.** Sửa lý do `zero_division` theo quy tắc trên ở: `p5-05-mini-project/lesson.*` (mục "New in this lesson", §4), `p5-05` quiz q07, q08 (prompt), f04, `exercises/ex02-evaluate-and-report/prompt.*`; `p5-04-evaluation/lesson.*` Mistake 1 (bỏ `zero_division=0` ở `recall_score` nếu không cần, hoặc nói đúng lý do) và Recap. `make_scorer(f1_score, zero_division=0)` ở p5-05 **được giữ** nhưng lý do mới là "ghi rõ ý định khi mẫu số bằng 0 (vd một fold không có dự đoán dương) thay vì dựa vào mặc định"; không nói nó chặn cảnh báo của baseline. Đáp án q07 phải đúng sự thật; câu `fill` q08 nhận cả `"0"` và `"0.0"` (minor 23).
- **M2.** `p5-04-evaluation/examples/03_cross_validation.*`: dùng `y = 1 - y` để **malignant = 1** (lớp dương), thêm 1 câu giải thích trong code comment và `.md`; chạy lại, cập nhật `.out`, Notice, Try (recall giờ là recall của ung thư).
- **M3.** Thuật ngữ VI, áp dụng cho **mọi** file VI của phase 5 (lesson, examples, prompts, hints, quiz `vi:`) và glossary:
  - accuracy → "**accuracy** (tỉ lệ đoán đúng)" lần đầu, sau đó "accuracy" hoặc "tỉ lệ đoán đúng". **Không** dùng "độ chính xác" cho accuracy.
  - precision → "**precision** (độ chuẩn khi báo dương)" lần đầu, sau đó "precision". **Không** dùng "độ chính xác" cho precision.
  - recall → "**recall** (độ nhạy, tức tỉ lệ bắt được)" lần đầu; **không** dùng "độ phủ".
  - Grep sau khi sửa: `grep -rn "độ chính xác\|độ phủ" curriculum/phase-05-ml` phải rỗng (nếu còn chỗ dùng đúng nghĩa khác, ghi lý do trong report). Glossary: các mục accuracy, precision, recall (vi) theo cách gọi trên.
- **M4.** `p5-05-mini-project/lesson.vi.md` §2: thay câu "chuyển ca trực" bằng "ghi nhận ticket sau đó có bị chuyển lên kỹ sư trực (on-call) hay không, thông tin chỉ có sau khi ticket đã được xử lý". "cột hậu kiểm" ở mọi chỗ → "cột chỉ có sau khi biết kết quả".
- **M5.** Hint 2 (EN + VI) thành kế hoạch **bằng lời**, không có biểu thức là đáp án: `p5-01-math-bridge/ex02-gradient-descent`, `p5-02-supervised/ex01-split-data`, `p5-02-supervised/ex02-best-threshold`. Hint 3 của các bài này giữ dạng khung, chừa ≥ 2–3 dòng thật sự trống. Starter `p5-02 ex02`: TODO của `accuracy` chỉ mô tả bằng lời, không ghi sẵn thân hàm. Mẫu đúng: hint của p5-03/p5-04.
- **M6.** `p5-05-mini-project/ex01-prepare-features` hint 3: chỉ giữ comment theo bước, mỗi bước tối đa một dòng mở đầu chừa `...` (vd `df["tokens"] = pd.to_numeric(..., errors=...)`); không chép nguyên văn các dòng làm sạch.
- **M7.** `p5-01-math-bridge/ex02-gradient-descent/test_exercise.py`: thêm test giá trị chính xác sau 1 bước (và/hoặc 2 bước), vd `fit_line([1, 2, 3, 4], [3, 5, 7, 9], lr=0.05, steps=1)`, tính bằng solution rồi assert `pytest.approx(..., abs=1e-6)`. Xác nhận trong report: lời giải bỏ hệ số `2` trong `grad_w`/`grad_b` giờ **fail** (chạy mutant tạm trong thư mục scratch, không để lại file).
- **M8.** `p5-04-evaluation/quiz.yaml` q09: một ô trống duy nhất là ngưỡng; prompt không ghi số; mô tả mục tiêu (bắt cả hai mẫu dương, không bắt mẫu âm); `answer` liệt kê các giá trị hợp lệ (chạy thử để chắc từng giá trị ra đúng output); bỏ ô dtype.
- **M9.** `p5-03-sklearn/examples/01_ticket_classifier.*`: đổi Try sang thay đổi thật sự làm đổi dự đoán (vd tăng `tokens` của ticket thứ ba), chạy thử và mô tả đúng kết quả.
- **M10.** `p5-05-mini-project/examples/03_honest_report.py`: khi không ngưỡng nào đạt mục tiêu, `chosen_t = None` và in `"no threshold reaches recall >= <target>"` rồi dừng phần test (không im lặng dùng 0.5); dòng in ngưỡng dùng biến mục tiêu thay vì chữ cứng `0.80`. Cập nhật `.out` (output mặc định giữ như cũ nếu được), `.md`: Try mô tả đúng điều thấy được, line refs đúng.

### Minor (1–27)
Làm đúng đề xuất trong `tasks/m3-p5-review.md`, cộng các quyết định sau:
- **2.** Sửa câu thành "với `LogisticRegression` nhị phân, `.predict` tương đương so `predict_proba(X)[:, 1]` với 0.5"; glossary `decision threshold` tương ứng.
- **5.** Thêm mục glossary `R²` (EN/VI): 1.0 khớp hoàn hảo, 0 không hơn đoán trung bình, có thể âm trên dữ liệu mới.
- **7.** Mistake 3 p5-04: nếu tìm được cấu hình (dữ liệu nhỏ, lệch thang đo) cho thấy chênh lệch thật giữa leaked và clean thì dùng; nếu không thì chuyển thành `> [!NOTE]` nói rõ quy trình sai dù số trùng. Không bịa số.
- **11.** Line refs: đếm lại theo file `.py` **thật** cho **mọi** example `.md` của phase 5 (EN + VI), không chỉ các file reviewer nêu.
- **14.** API chưa giới thiệu: thêm một câu ở lần dùng đầu (lesson) hoặc một dòng trong prompt/hint/.md nơi nó xuất hiện.
- **15.** Không đổi code p5-02. Thêm một câu ở lesson §4 (hoặc prompt ex01): lấy phần đầu làm train hay làm test đều được miễn nhất quán; bài tập lấy phần đầu làm test.
- **16.** Không cắt bài. Đặt `duration_min` trung thực theo độ dài (lesson ~2000+ từ: 18–20; p5-05 giữ 45–50). Không thêm nội dung mới.
- **18.** Thêm test hòa với scores chưa sắp; quy định trong prompt kết quả khi `scores` rỗng và sửa solution/alternative cho **giống nhau** (chọn `(0.0, 0.0)`), có test.
- **19.** Đổi tên test thành điều nó thật sự kiểm (vd `test_identical_models_get_identical_scores`) hoặc thêm cách kiểm "split once"; chọn cách đơn giản, đúng.
- **20.** Hint 3 `threshold_for_recall`: chừa thêm chỗ trống, bỏ biến chết `best`; sửa câu prompt EN và comment test.
- **21.** Dùng mean 0.75 / 0.5, std 0.25 (biểu diễn chính xác) cho test biên; sửa comment.
- **22.** Ghi rõ thứ tự trong Rules của prompt (bỏ trùng trước, rồi bỏ dòng thiếu, như lesson §3) và thêm một test phân biệt (dòng trùng **đầu tiên** bị thiếu số → ticket đó biến mất hẳn).
- **23.** Mỗi câu fill nêu tên: `answer` liệt kê mọi đáp án hợp lệ đã chạy thử (validator dùng đáp án đầu tiên); p5-05 q03 bỏ chữ lộ dtype trong đề.
- **24.** p5-01 q14 → difficulty 2. p5-05: gắn lại độ khó trung thực sao cho có ≥ 4 câu dễ (chỉ gắn lại câu thật sự dễ; nếu không đủ, viết lại 1 câu cho dễ hơn, giữ id).
- **26.** Dịch header bảng còn tiếng Anh trong `lesson.vi.md` (mọi bài phase 5). Nhãn trong `examples/*.vi.md` của phase 5 thống nhất theo bài mẫu `curriculum/phase-01-python-core/p1-01-variables/examples/01_shop_receipt.vi.md`: `**Ví dụ này cho thấy:**`, `**Từng bước**`, `**Để ý:**`, `**Tự thử:**`.
- **27.** Glossary: sửa `data leakage` (thông tin lúc dự đoán thật không có, hoặc từ ngoài tập train), `target leakage` ("cao bất thường"), `holdout set` (EN/VI cùng nghĩa: không dùng cho chọn mô hình, chỉnh feature, CV, chọn ngưỡng).

## Tiêu chí hoàn thành (checklist)
1. [ ] Cả 38 mục đã sửa đúng quyết định; report liệt kê **từng mục** (B1, M1–M10, minor 1–27): file đã sửa + một câu đã làm gì. Mục nào không làm được hoặc làm khác, nói rõ lý do.
2. [ ] Mọi output, comment, `.out`, số trong `.md`/quiz/test lấy từ lần chạy thật (`MPLBACKEND=Agg` khi tự chạy code có matplotlib).
3. [ ] EN/VI song song cho mọi thay đổi.
4. [ ] Không warning khi chạy lesson/example/test phase 5.
5. [ ] Lệnh kiểm tra xanh, chạy đúng như ghi.

## Lệnh kiểm tra
Từ gốc repo `D:\Proj\python-ai-platform`:
```
uv run python tools/validate.py --path curriculum/phase-05-ml
uv run python tools/validate.py
uv run python -m pytest curriculum
uv run python -m pytest curriculum/phase-05-ml -W error::UserWarning -W error::FutureWarning
uv run ruff check curriculum
grep -rn "độ chính xác\|độ phủ\|chuyển ca trực\|hậu kiểm" curriculum/phase-05-ml
grep -rn "selection strictly by test\|pick the winner by \*\*test score" curriculum/phase-05-ml
grep -rnE "astype\(int\)|dtype=int\b|\.info\(|fetch_|np\.random\.(seed|rand)|^import random" curriculum/phase-05-ml
git status --short
git diff --stat
```
Mong đợi: validate 0 lỗi; pytest exit 0 (cả lần coi warning là lỗi); ruff sạch; ba grep rỗng; chỉ file trong `curriculum/phase-05-ml/` và `curriculum/glossary.yaml` bị sửa; không file nào bị xóa.
Thêm: chạy mọi khối python trong `lesson.en.md` của 5 bài và mọi example bằng `uv run python -W error::UserWarning`, xác nhận stderr rỗng và output khớp comment/`.out`. Sau đó `uv run python tools/build_content.py`.

## Ghi chú cho worker
- Dùng `uv run python -m pytest`, không dùng `uv run pytest`.
- Test chỉ dùng: assert, pytest.raises, pytest.approx, pytest.mark.parametrize, `@pytest.fixture` định nghĩa trong file test.
- Đây là việc lớn: làm theo từng bài (p5-01 → p5-05) rồi glossary, chạy `validate --path` của bài đó sau mỗi bài để lỗi lộ sớm.
- Không có trình duyệt thì ghi rõ trong report; boss tự kiểm tra trong app.

## Trạng thái
- Bước hiện tại: 5 (đạt sau vòng 1; boss xác minh B1, M1, M2, M7 (mutant giờ fail), M8, M9, M10, thuật ngữ VI; trong app p5-01 ex02 7/7, callout WARNING p5-04; đã commit `e0a633b`)
- Vòng: 1/3
- Số lần swap: 0
- Fallback: không
- Model: Gemini 4 Hydrogen (High)
