# Báo cáo sửa 38 điểm review Phase 5 (`m3-p5-review-fixes`)

Hoàn thành sửa toàn bộ **38 điểm review** (1 Blocker `B1`, 10 Major `M1–M10`, 27 Minor `1–27`) cho Phase 5 (`curriculum/phase-05-ml/p5-01`..`p5-05` và `curriculum/glossary.yaml`) theo đúng `tasks/m3-p5-review-fixes.md` và `tasks/m3-p5-review.md`, giữ song song EN/VI cho mọi thay đổi và chỉ chạm vào các file được phép.

---

## 1. Chi tiết từng mục đã xử lý

### Blocker
- **B1.** Thống nhất quy tắc "test chỉ chấm một lần ở cuối; chọn mô hình/ngưỡng bằng CV trên train hoặc tập validation tách từ train; so sánh trên 1 lần chia held-out ở p5-02/p5-03 chỉ là cái nhìn đầu tiên":
  - `p5-02-supervised/quiz.yaml`: cập nhật phương án đúng và giải thích EN/VI của `p5-02-q15` (so sánh một lần trên held-out chỉ là cái nhìn đầu tiên; CV và quy trình giữ test chấm 1 lần học ở `p5-04`/`p5-05`).
  - `p5-03-sklearn/lesson.{en,vi}.md`: sửa §6, dòng 3 bảng fair/unfair, callout `NOTE` và Recap (bỏ "selection strictly by test score" / "always pick the winner by test score"; giải thích chênh 1/45 mẫu nằm trong may rủi chia tập và dẫn sang CV ở `p5-04`, test chấm 1 lần ở `p5-05`).
  - `p5-03-sklearn/quiz.yaml`: viết lại `p5-03-q15` và flashcard `p5-03-f06` theo đúng quy tắc và nhắc CV ở `p5-04`.
  - `p5-03-sklearn/examples/03_compare_models.{en,vi}.md`: cập nhật `Notice` (chênh 1/45 mẫu nằm trong may rủi của 1 lần chia) và dẫn sang CV.
  - `p5-03-sklearn/exercises/ex02-compare-models/prompt.{en,vi}.md`: giữ `best_model`, bổ sung câu nêu rõ ở bài này hàm nhận điểm held-out để so sánh bước đầu và sang `p5-04` sẽ truyền điểm CV vào cùng hàm.
  - `p5-04-evaluation/lesson.{en,vi}.md`: giữ bảng quét ngưỡng trên test ở §5 làm minh họa đánh đổi, thêm `> [!WARNING]` cùng vị trí (EN/VI) lưu ý quét ngưỡng thật phải dùng validation hoặc xác suất out-of-fold trên train (`p5-05`), test chỉ chấm một lần.
  - `p5-04-evaluation/examples/02_threshold_tradeoff.{py,out,en.md,vi.md}`: sửa code tách tập validation từ phần train (`train_test_split(..., stratify=...)`), chọn ngưỡng trên tập validation rồi mới chấm `X_test` đúng một lần; chạy lại bằng Python `-W error::UserWarning`, cập nhật `.out` và `.md` (EN/VI).

### Major (`M1–M10`)
- **M1.** Sửa lý do `zero_division` khớp thực tế scikit-learn 1.7:
  - `p5-04-evaluation/lesson.{en,vi}.md`: sửa §3, Mistake 1 (gỡ `zero_division=0` thừa ở `recall_score` và giải thích đúng: trong các chỉ số này chỉ `precision_score` khi `TP + FP == 0` mới phát `UndefinedMetricWarning`; `recall`/`F1` khi dự đoán toàn `0` nhưng còn mẫu dương thật trả `0.0` không cảnh báo) và Recap.
  - `p5-05-mini-project/lesson.{en,vi}.md`: sửa mục "New in this lesson" và §4 (giữ `make_scorer(f1_score, zero_division=0)`, lý do là ghi rõ ý định trả `0.0` khi mẫu số bằng 0—ví dụ một fold không có dự đoán dương—thay vì dựa vào mặc định).
  - `p5-05-mini-project/examples/02_model_selection_cv.{en,vi}.md`: sửa bước 3 theo lý do mới (không nói chặn cảnh báo cho baseline).
  - `p5-05-mini-project/exercises/ex02-evaluate-and-report/prompt.{en,vi}.md`: sửa quy tắc dùng `make_scorer(f1_score, zero_division=0)` theo đúng lý do ghi rõ hành vi khi mẫu số bằng 0.
  - `p5-05-mini-project/quiz.yaml`: sửa `p5-05-q07`, `p5-05-q08` (prompt + `answer: [["0", "0.0"], "f1_safe"]`), và `p5-05-f04` cho đúng sự thật.
- **M2.** `p5-04-evaluation/examples/03_cross_validation.{py,out,en.md,vi.md}`: thêm `y = 1 - y` kèm comment giải thích để `1 = malignant` (ung thư ác tính), chạy lại cập nhật `.out`, `Notice` và `Try` (EN/VI).
- **M3.** Chuẩn hóa thuật ngữ tiếng Việt cho toàn bộ Phase 5 và `curriculum/glossary.yaml`: dùng `**accuracy** (tỉ lệ đoán đúng)`, `**precision** (độ chuẩn khi báo dương)`, `**recall** (độ nhạy, tức tỉ lệ bắt được)` ở lần đầu và không còn dùng `độ chính xác` hay `độ phủ` trong `p5-02`, `p5-03`, `p5-04`, `p5-05` và các mục `accuracy`, `precision`, `recall` trong `curriculum/glossary.yaml`.
- **M4.** `p5-05-mini-project/lesson.vi.md` (§2, bảng §3, §7, Tóm tắt) và `p5-05-mini-project/quiz.yaml` (`p5-05-q04`): thay `"chuyển ca trực"` thành `"ghi nhận ticket sau đó có bị chuyển lên kỹ sư trực (on-call) hay không, thông tin chỉ có sau khi ticket đã được xử lý"`, và thay `"cột hậu kiểm"` thành `"cột chỉ có sau khi biết kết quả"`.
- **M5.** Chuyển Hint 2 (EN+VI) sang kế hoạch bằng lời (không chứa biểu thức đáp án) và giữ Hint 3 ở dạng khung chừa nhiều dòng `...` thật: `p5-01-math-bridge/exercises/ex02-gradient-descent/exercise.yaml`, `p5-02-supervised/exercises/ex01-split-data/exercise.yaml`, `p5-02-supervised/exercises/ex02-best-threshold/exercise.yaml` (cùng sửa `starter.py` TODO của `accuracy` thành mô tả bằng lời).
- **M6.** `p5-05-mini-project/exercises/ex01-prepare-features/exercise.yaml`: viết lại Hint 3 (EN+VI) chỉ giữ comment từng bước với tối đa một dòng mở đầu chừa `...`, không chép nguyên văn các dòng làm sạch từ `solution.py`.
- **M7.** `p5-01-math-bridge/exercises/ex02-gradient-descent/test_exercise.py`: thêm `test_fit_line_one_step_matches_exact_mse_gradient` kiểm tra giá trị sau 1 bước (`fit_line(xs, ys, lr=0.05, steps=1) == pytest.approx((1.75, 0.6), abs=1e-6)`). Đã kiểm chứng trên bản mutant tạm trong scratch (đã xóa sau kiểm tra) bỏ hệ số `2 *` ở `grad_w`/`grad_b`: test mới fail (`(0.875, 0.3)` != `(1.75, 0.6)`, 1 failed / 6 passed).
- **M8.** `p5-04-evaluation/quiz.yaml`: sửa `p5-04-q09` còn 1 ô trống ngưỡng duy nhất, bỏ ô dtype và bỏ con số lộ đáp án trong prompt, đặt code in cả `precision_score` và `recall_score` (`1.0 1.0`), `answer: [["0.3", "0.35", "0.26", "0.27", "0.28", "0.29", "0.30", "0.31", "0.32", "0.33", "0.34"]]`.
- **M9.** `p5-03-sklearn/examples/01_ticket_classifier.{en,vi}.md`: đổi `Try` sang `[180.0, 1.0]` cho ticket thứ 3 để dự đoán thực sự lật từ `[0, 1, 0]` sang `[0, 1, 1]` và ghi đúng điểm accuracy với `test_size=0.3` (`0.875`).
- **M10.** `p5-05-mini-project/examples/03_honest_report.{py,out,en.md,vi.md}`: dùng biến `target_recall = 0.80`; khi không ngưỡng nào đạt mục tiêu thì giữ `chosen_t = None`, in `"no threshold reaches recall >= <target>"` và bỏ qua phần chấm test (không rơi về `0.5` im lặng); cập nhật `.md` (EN/VI), `Try` (`target_recall = 0.90` ở dòng 62) và line refs; output mặc định giữ nguyên như `.out` cũ.

### Minor (`1–27`)
1. `p5-04-evaluation/lesson.{en,vi}.md` (§5) và `examples/02_threshold_tradeoff.{en,vi}.md`: sửa `"precision stays at 0.889"` thành giảm nhẹ từ `1.0` xuống `0.889` (trên bảng minh họa bài học) / phản ánh đúng biến thiên trên tập validation trong `02_threshold_tradeoff`.
2. `p5-04-evaluation/lesson.{en,vi}.md` (§5) và `curriculum/glossary.yaml` (`decision threshold`): nêu rõ với `LogisticRegression` nhị phân, `.predict()` tương đương so sánh `predict_proba(X)[:, 1]` với `0.5`.
3. `p5-03-sklearn/lesson.{en,vi}.md` (§5 và Recap): giảm cách nói quá tuyệt đối (`"leakage impossible"` / `"zero data leakage"`) thành ngăn rò rỉ thống kê scaling giữa train và test.
4. `p5-03-sklearn/lesson.{en,vi}.md` (Recap): đồng bộ ý về scaling cho `LogisticRegression` với §1/§4 (cần scaling khi các feature lệch thang đo lớn).
5. `p5-03-sklearn/lesson.{en,vi}.md` (§1) và `curriculum/glossary.yaml`: giải thích `R²` (`1.0` khớp hoàn hảo, `0.0` không hơn đoán trung bình, có thể âm trên dữ liệu mới) và thêm mục `R²` vào `curriculum/glossary.yaml`.
6. `p5-04-evaluation/lesson.{en,vi}.md` (§6): viết lại câu về `StratifiedKFold` để rõ `scoring="f1"` là tham số của `cross_val_score`, không phải của `StratifiedKFold`.
7. `p5-04-evaluation/lesson.{en,vi}.md` (Mistake 3): cập nhật cấu hình dữ liệu thực (`make_classification` với `n_samples=40, weights=[0.8], random_state=5`, `KNeighborsClassifier(n_neighbors=3)`, `StratifiedKFold`) cho chênh lệch thật giữa leaked (`mean: 0.667`) và clean (`mean: 0.633`).
8. `p5-02-supervised/lesson.{en,vi}.md` (Mistake 2): thêm giải thích vì sao `clean test: [1.5, 4.5]` nằm ngoài `[0, 1]`.
9. `p5-02-supervised/examples/03_overfitting_curve.{en,vi}.md`: sửa `Notice` và `Try` để không gọi bậc 3 là "sweet spot" (dữ liệu sinh từ parabol nên bậc 2 đạt `test_mse = 0.011` thấp hơn bậc 3 `0.018`).
10. `p5-03-sklearn/examples/03_compare_models.{en,vi}.md`: cập nhật `Notice` (chênh 1/45 mẫu) và `Try` (`max_depth=None` học thuộc train `1.000`, đạt `0.978` = 44/45 trên lần chia này, minh họa dao động 1 lần chia so với CV).
11. Đếm lại line refs theo file `.py` thật và sửa mọi file `.en.md` / `.vi.md` có lệch ở toàn bộ example của Phase 5: `p5-01` (`03_fit_a_line`), `p5-04` (`01_ticket_metrics`, `02_threshold_tradeoff`, `03_cross_validation`), `p5-05` (`01_raw_ticket_log`, `02_model_selection_cv`, `03_honest_report`).
12. `p5-01-math-bridge/examples/03_fit_a_line.{en,vi}.md`: cập nhật `Try` nêu rõ `lr=0.1` vượt ngưỡng ổn định và phát nổ (`~1.7e14`), gợi ý thử `lr=0.06` để hội tụ nhanh hơn mà vẫn ổn định.
13. `p5-02-supervised/examples/02_train_test_split.en.md`: sửa lỗi diễn đạt ở `Try` (`"IDs stay small"` -> mô tả cách ID thay đổi trong khi `Test MSE` giữ nhỏ).
14. Bổ sung giới thiệu ngắn cho các API lần đầu xuất hiện: `np.argmin` (`p5-01` lesson §3), `rng.normal` (`p5-02` lesson §5), `np.unique` (`p5-02` ex02 Hint 2), `np.bincount`, `rng.integers`, `rng.uniform`, `np.concatenate`, `np.column_stack` (`p5-03` lesson §2 & §4), `sklearn.base.clone` (`p5-03` ex02 prompt).
15. `p5-02-supervised/lesson.{en,vi}.md` (§4): giữ nguyên code; thêm giải thích chọn phần đầu permutation làm train hay test đều tương đương miễn nhất quán, và `ex01` quy ước lấy `n_test` phần tử đầu làm test.
16. Cập nhật `meta.yaml` `duration_min` trung thực theo độ dài ở `p5-01` (`19`), `p5-02` (`18`), `p5-03` (`18`), `p5-04` (`20`); giữ nguyên `p5-05` (`48`) không cắt hay thêm nội dung.
17. `p5-01-math-bridge/exercises/ex01-weighted-score/exercise.yaml`: sửa Hint 3 (EN+VI) chừa trống nhiều hơn để không trùng hoàn toàn `starter.py`.
18. `p5-02-supervised/exercises/ex02-best-threshold/{prompt.{en,vi}.md,solution.py,test_exercise.py}`: quy định mảng rỗng trả `(0.0, 0.0)` thống nhất giữa `prompt`, `solution.py` và `alternatives/01_sorted_scan.py`; thêm test hòa với mảng chưa sắp và test mảng rỗng.
19. `p5-03-sklearn/exercises/ex02-compare-models/test_exercise.py`: đổi tên test `test_all_models_use_same_split` thành `test_identical_models_get_identical_scores` khớp hành vi kiểm tra thực tế.
20. `p5-04-evaluation/exercises/ex02-threshold-metrics/{exercise.yaml,prompt.en.md,test_exercise.py}`: bỏ biến chết `best` và chừa trống thêm ở Hint 3 (EN+VI); làm rõ câu về mẫu số bằng 0 ở `prompt.en.md`; sửa ngữ pháp comment (`both` -> `all`) ở `test_exercise.py`.
21. `p5-05-mini-project/exercises/ex02-evaluate-and-report/test_exercise.py`: dùng số biểu diễn nhị phân chính xác (`0.75 - 0.5 == 0.25` vs std `0.25`, `0.125`) cho test biên `<` và sửa comment.
22. `p5-05-mini-project/exercises/ex01-prepare-features/{prompt.{en,vi}.md,test_exercise.py}`: ghi rõ thứ tự trong Rules (khử trùng `keep="first"` trước khi bỏ dòng thiếu, khớp lesson §3) và thêm `test_deduplicates_before_dropping_missing_rows`.
23. Liệt kê đủ các đáp án `fill` hợp lệ đã chạy thử ở `p5-03-q08` (`[["fit", "fit_transform"], "transform"]`), `p5-04-q04` (`[["most_frequent", "prior"], ["0", "0.0"]]`), `p5-04-q09` (11 giá trị ngưỡng hợp lệ), `p5-05-q08` (`[["0", "0.0"], "f1_safe"]`), và ở `p5-05-q03` bỏ chữ `64-bit` làm lộ dtype trong đề + chấp nhận `["coerce", ["int64", "int32", "int"]]`.
24. Cập nhật độ khó: `p5-01-q14` -> `difficulty: 2`; `p5-05-q04` -> `difficulty: 1` (đạt phân bố `{1: 4, 2: 8, 3: 4}` trong `p5-05-mini-project/quiz.yaml`).
25. Sửa các chỗ tiếng Việt gượng: `"mặt phẳng"` -> `"phẳng ngang"` (`p5-01`), `"bảng vết"` -> `"bảng theo dõi từng bước"`/`"bảng theo dõi"` (`p5-01`, `p5-02`), `"lệch chuẩn"` -> `"phân bố lệch"` (`p5-04`), `"chuẩn hóa"` dòng 28 và đoạn Tóm tắt ở `p5-05/lesson.vi.md`, `"bộ phân loại hồi quy logistic"` -> `"bộ phân loại LogisticRegression"` (`p5-03` ex01 Hint 2 VI).
26. Dịch các header bảng còn tiếng Anh trong `lesson.vi.md` (`p5-02`, `p5-04`, `p5-05`) và chuẩn hóa nhãn trong tất cả 15 `examples/*.vi.md` của Phase 5 thành `**Ví dụ này cho thấy:**`, `**Từng bước**`, `**Để ý:**`, `**Tự thử:**`.
27. `curriculum/glossary.yaml`: cập nhật `data leakage` (bao gồm cả thông tin từ ngoài tập train và thông tin chưa tồn tại lúc dự đoán thật), `target leakage` (`"cao bất thường"` thay `"gần 1.0"`/`"near 1.0"`), `holdout set` (cùng nghĩa EN/VI: không dùng cho chọn mô hình, chỉnh feature, CV hay chọn ngưỡng), `decision threshold` (minor 2), và thêm mới mục `R²` (minor 5).

---

## 2. Danh sách 76 file đã sửa (`git diff --name-only`)

- `curriculum/glossary.yaml`
- `curriculum/phase-05-ml/p5-01-math-bridge/`: `lesson.en.md`, `lesson.vi.md`, `meta.yaml`, `quiz.yaml`, `examples/01_feature_scores.vi.md`, `examples/02_embedding_similarity.vi.md`, `examples/03_fit_a_line.en.md`, `examples/03_fit_a_line.vi.md`, `exercises/ex01-weighted-score/exercise.yaml`, `exercises/ex02-gradient-descent/exercise.yaml`, `exercises/ex02-gradient-descent/test_exercise.py`
- `curriculum/phase-05-ml/p5-02-supervised/`: `lesson.en.md`, `lesson.vi.md`, `meta.yaml`, `quiz.yaml`, `examples/01_ticket_threshold.vi.md`, `examples/02_train_test_split.en.md`, `examples/02_train_test_split.vi.md`, `examples/03_overfitting_curve.en.md`, `examples/03_overfitting_curve.vi.md`, `exercises/ex01-split-data/exercise.yaml`, `exercises/ex02-best-threshold/{exercise.yaml,prompt.en.md,prompt.vi.md,solution.py,starter.py,test_exercise.py}`
- `curriculum/phase-05-ml/p5-03-sklearn/`: `lesson.en.md`, `lesson.vi.md`, `meta.yaml`, `quiz.yaml`, `examples/01_ticket_classifier.{en,vi}.md`, `examples/02_scaling_pipeline.vi.md`, `examples/03_compare_models.{en,vi}.md`, `exercises/ex01-fit-pipeline/exercise.yaml`, `exercises/ex02-compare-models/{exercise.yaml,prompt.en.md,prompt.vi.md,test_exercise.py}`
- `curriculum/phase-05-ml/p5-04-evaluation/`: `lesson.en.md`, `lesson.vi.md`, `meta.yaml`, `quiz.yaml`, `examples/01_ticket_metrics.{en,vi}.md`, `examples/02_threshold_tradeoff.{py,out,en.md,vi.md}`, `examples/03_cross_validation.{py,out,en.md,vi.md}`, `exercises/ex02-threshold-metrics/{exercise.yaml,prompt.en.md,test_exercise.py}`
- `curriculum/phase-05-ml/p5-05-mini-project/`: `lesson.en.md`, `lesson.vi.md`, `quiz.yaml`, `examples/01_raw_ticket_log.{en,vi}.md`, `examples/02_model_selection_cv.{en,vi}.md`, `examples/03_honest_report.{py,en.md,vi.md}`, `exercises/ex01-prepare-features/{exercise.yaml,prompt.en.md,prompt.vi.md,test_exercise.py}`, `exercises/ex02-evaluate-and-report/{prompt.en.md,prompt.vi.md,test_exercise.py}`

Không có file nào thuộc `apps/` (trừ output build gitignored trong `apps/web/src/generated`), `tools/`, `pyproject.toml`, `uv.lock`, `syllabus.yaml`, `topics.yaml`, các phase khác hoặc `exams/` bị sửa hoặc xóa.

---

## 3. Kết quả các lệnh kiểm tra sau lần sửa cuối

| Lệnh kiểm tra | Kết quả |
|---|---|
| `uv run python tools/validate.py --path curriculum/phase-05-ml` | `OK: 0 error(s), 0 warning(s). Checked 5 lessons, 36 markdown pairs, 15 examples, 10 exercises, 6 alternatives, 80 questions.` |
| `uv run python tools/validate.py` | `OK: 0 error(s), 0 warning(s). Checked 35 lessons, 272 markdown pairs, 103 examples, 70 exercises, 64 alternatives, 660 questions, 6 exams, 1 portfolio, 1 glossary, 1 interview.` |
| `uv run python -m pytest curriculum` | `652 passed, 14 warnings in 2.48s` (14 `PyparsingDeprecationWarning` từ `matplotlib._fontconfig_pattern` / `_mathtext` ở các test phase khác) |
| `uv run python -m pytest curriculum/phase-05-ml -W error::UserWarning -W error::FutureWarning` | `72 passed in 1.32s` (0 warning, exit code 0) |
| `uv run ruff check curriculum` | `All checks passed!` |
| Regex check 1 (`độ chính xác\|độ phủ\|chuyển ca trực\|hậu kiểm` trên `curriculum/phase-05-ml`) | `0 hits` |
| Regex check 2 (`selection strictly by test\|pick the winner by \*\*test score` trên `curriculum/phase-05-ml`) | `0 hits` |
| Regex check 3 (`astype\(int\)\|dtype=int\b\|\.info\(\|fetch_\|np\.random\.(seed\|rand)\|^import random` trên `curriculum/phase-05-ml`) | `0 hits` |
| Chạy 50 khối Python trong 5 `lesson.en.md` + 15 file `examples/*.py` (`MPLBACKEND=Agg`, `-W error::UserWarning`) | 47/50 khối và 13/15 ví dụ chạy sạch với stderr rỗng và `.out` khớp hoàn toàn; 5 mục dùng `matplotlib` (block 3 & 6 ở `p5-01`, block 5 ở `p5-02`, `03_fit_a_line.py`, `03_overfitting_curve.py`) chạy `OK=True`, `rc=0`, `.out` khớp sau khi bỏ qua `PyparsingDeprecationWarning` nội bộ `matplotlib` khi import và `FigureCanvasAgg is non-interactive` khi gọi `plt.show()` dưới `Agg`. |
| Kiểm tra song song EN/VI (`lesson.en.md` vs `lesson.vi.md`) cả 5 bài | Số lượng và nội dung khối `python` (trừ `#` comment), `text`, và số dòng `mermaid` khớp 100%. |
| `uv run python tools/build_content.py` | `Built 35 lessons, 6 exams, 210 flashcards, 563 questions -> apps\web\src\generated` (exit code 0) |

---

## 4. Điều còn chưa chắc / cần kiểm tra thủ công

- **Chưa kiểm tra trong trình duyệt:** Môi trường hiện tại không có trình duyệt và không chạy `pnpm --filter web build` (theo spec), nên việc hiển thị UI của các thay đổi mới (bảng biểu, callout `WARNING`, mục glossary `R²`, trình chạy quiz/exercise trên Pyodide 32-bit WebAssembly) chưa được kiểm chứng trực tiếp trên web app — cần kiểm tra thủ công trong app.
- **Matplotlib trên CLI `Agg`:** Khi chạy trực tiếp qua `python -W error::UserWarning`, 5 khối/ví dụ có `import matplotlib.pyplot` chạm `PyparsingDeprecationWarning` nội bộ của `matplotlib 3.8.4` + `pyparsing` trong `.venv` (lỗi từ thư viện bên thứ ba lúc import) và cảnh báo `FigureCanvasAgg` của `plt.show()`; trên Pyodide / trình duyệt thực tế, `plt.show()` dùng backend canvas tương tác khác nên sẽ không gặp cảnh báo `Agg`.
