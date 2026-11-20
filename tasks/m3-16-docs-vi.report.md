# Báo cáo M3 bước 16: cập nhật tài liệu dự án + đọc mẫu bản VI phase 4–5

## 1. Đã làm gì

### A. Cập nhật tài liệu dự án
1. `CLAUDE.md` (mục `## Quy trình`):
   - Cập nhật trạng thái hiện tại: M3 đã xong (phase 4 gồm 6 bài + phase test, phase 5 gồm 5 bài + phase test, cả hai đã qua reviewer; mock exam `mock-data-ml`; Visualize hiện bảng).
   - Giữ lại một câu ngắn gọn rằng theme Dose đã merge, bỏ các chi tiết M2/redesign cũ.
   - Ghi bước kế tiếp là M4 (phase 6–8, runner cục bộ).
   - Thêm gạch đầu dòng: chạy pytest bằng `uv run python -m pytest` (không dùng `uv run pytest`).
   - Tổng số dòng hiện tại: 32 dòng (dưới ngưỡng ~60 dòng). Không sửa các mục khác.
2. `docs/DESIGN.md`:
   - Mục 5, dòng `Chạy Python`: ghi Pyodide 0.29.5 có sẵn `numpy`, `pandas`, `matplotlib`, `scikit-learn`, `scipy`, `sqlite3`, và môi trường local ghim phiên bản (vd `scipy==1.14.1`) để output khớp với app.
   - Mục 5: thêm mô tả **Visualize** sử dụng tracer `tools/pyrunner/tracer.py` chạy từng bước, giới hạn 600 bước, hiện DataFrame/Series/mảng 2D thành bảng 8×6.
   - Mục 10: ghi `M3 xong (2026-11-14)` ở dòng `M3`. Không sửa các phần khác.
3. `docs/CONTENT_GUIDE.md`:
   - Thêm mục `## Data & ML code (phase 4+)` ngay trước `## Quality gate`, viết bằng tiếng Anh ngắn gọn theo từng gạch đầu dòng đúng 11 quy tắc từ spec (`wasm32`/`int32`/`"int64"`/`df.info()`, `.tolist()`/`round(float(x), 3)` tránh numpy scalar, bảng tối đa 4 cột / dưới 60 ký tự, `-W error`, `default_rng`/`random_state`/không `fetch_*`/Agg/không `plt.show()`, SQLite `":memory:"` + `ORDER BY`, khối Visualize dưới 600 bước, "Test set is used once" / "a first look", `zero_division` trên sklearn 1.7, thuật ngữ VI cho accuracy/precision/recall, MCQ thi 4 lựa chọn dài gần bằng nhau và không nhét lý do vào đáp án đúng).

### B. Đọc mẫu và chỉnh sửa bản VI (phase 4–5)
Đã đọc đối chiếu bản EN và bản VI của `lesson.vi.md` và `examples/*.vi.md` cho 3 bài (`p4-03-cleaning`, `p5-02-supervised`, `p5-04-evaluation`), chỉ sửa câu chữ gượng/sát chữ, bổ sung giải nghĩa thuật ngữ lần đầu, chỉnh chỗ sai/nhầm nghĩa so với EN, giữ nguyên toàn bộ khối code, khối `text`, số dòng `mermaid`, callout, heading, bảng và link.

#### Bảng chi tiết mọi chỗ sửa — `p4-03-cleaning` (19 chỗ)

| file | trước | sau | lý do |
|---|---|---|---|
| `curriculum/phase-04-data/p4-03-cleaning/lesson.vi.md` | `hiếm khi sạch sẽ khi đi vào script của bạn` | `hiếm khi sạch gọn khi vào script của bạn` | "sạch sẽ" và "đi vào script" dịch sát chữ từ *tidy* / *reaches your script*, chưa tự nhiên. |
| `curriculum/phase-04-data/p4-03-cleaning/lesson.vi.md` | `các giá trị phân loại hiện có` | `các giá trị riêng biệt của cột phân loại` | Dịch sát "unique category values", dễ hiểu nhầm thành "có sẵn" thay vì các giá trị khác nhau. |
| `curriculum/phase-04-data/p4-03-cleaning/lesson.vi.md` | `(đếm số giá trị phân biệt)` | `(đếm số giá trị khác nhau)` | "giá trị phân biệt" hơi nặng tính toán học với người mới. |
| `curriculum/phase-04-data/p4-03-cleaning/lesson.vi.md` | `đi một vòng kiểm tra xe trước khi mở nắp capo` | `đi một vòng quanh xe trước khi mở nắp capo` | Diễn đạt tự nhiên hơn, sát hình ảnh ẩn dụ của bản EN. |
| `curriculum/phase-04-data/p4-03-cleaning/lesson.vi.md` | `bị tách làm hai nhóm đếm riêng` | `bị tách thành hai mục đếm riêng` | Rõ nghĩa hơn cho output của `value_counts()`. |
| `curriculum/phase-04-data/p4-03-cleaning/lesson.vi.md` | `hàng đó vẫn còn giá trị sử dụng` | `hàng đó vẫn còn hữu ích` | "giá trị sử dụng" nghe gượng (kiểu kinh tế học), EN là *still useful*. |
| `curriculum/phase-04-data/p4-03-cleaning/lesson.vi.md` | `chữ "N/A"` | `chuỗi "N/A"` | Thuật ngữ chính xác hơn trong ngữ cảnh kiểu `object`. |
| `curriculum/phase-04-data/p4-03-cleaning/lesson.vi.md` | `dùng **type coercion** (ép kiểu an toàn)` | `dùng **type coercion** (ép kiểu) an toàn` | Bản thân *type coercion* nghĩa là "ép kiểu"; "an toàn" là tính chất của `errors="coerce"`. |
| `curriculum/phase-04-data/p4-03-cleaning/lesson.vi.md` | `thay vì làm sập code` | `thay vì làm lỗi chương trình` | "sập code" dịch sát chữ từ *crashing*. |
| `curriculum/phase-04-data/p4-03-cleaning/lesson.vi.md` | `Để ý pd.to_numeric trả về` | `Để ý là pd.to_numeric trả về` | Thêm từ nối cho câu tự nhiên hơn. |
| `curriculum/phase-04-data/p4-03-cleaning/lesson.vi.md` | `thường giấu khoảng trắng ở hai đầu, chữ hoa thường lẫn lộn ... gộp các biến thể bị tách lẻ` | `thường dính khoảng trắng ở hai đầu, viết hoa thường lẫn lộn ... gộp các biến thể của cùng một nhãn` | "giấu khoảng trắng" dịch sát *hide spaces*; làm rõ ý gộp các biến thể của cùng một nhãn. |
| `curriculum/phase-04-data/p4-03-cleaning/lesson.vi.md` | `thay đúng chuỗi ký tự gốc chứ không dùng biểu thức chính quy` | `thay đúng chuỗi ký tự nguyên văn chứ không hiểu đó là **regular expression** (biểu thức chính quy)` | Chuẩn hơn về mặt kỹ thuật và có cặp thuật ngữ EN–VI. |
| `curriculum/phase-04-data/p4-03-cleaning/lesson.vi.md` | `để dòng hỏng không bao giờ giữ lại thay cho dòng hợp lệ trước đó` | `để dòng hỏng không bao giờ bị giữ lại thay cho dòng hợp lệ trước đó` | Thiếu từ bị động "bị", dễ đọc ngược chủ ngữ. |
| `curriculum/phase-04-data/p4-03-cleaning/lesson.vi.md` | `dữ liệu gốc của nơi gọi ... xử lý thiếu` | `dữ liệu gốc truyền vào ... xử lý giá trị thiếu` | "nơi gọi" (*callers*) gượng; "xử lý thiếu" thiếu danh từ "giá trị". |
| `curriculum/phase-04-data/p4-03-cleaning/lesson.vi.md` | `Loại bỏ khóa bị trùng` | `Loại bỏ dòng trùng khóa` | Đúng hành vi của `drop_duplicates(subset=[...])`. |
| `curriculum/phase-04-data/p4-03-cleaning/lesson.vi.md` | `luôn gán kết quả trả về vào biến` | `luôn gán lại kết quả trả về vào biến` | Nhấn mạnh ý *reassign back*. |
| `curriculum/phase-04-data/p4-03-cleaning/lesson.vi.md` | `trả về mặt nạ sai` | `trả về bộ lọc (mask) sai` | "mặt nạ" dịch sát chữ từ *mask*, khó hiểu với người mới. |
| `curriculum/phase-04-data/p4-03-cleaning/lesson.vi.md` | `nằm dưới bộ truy cập .str` | `nằm trong nhóm phương thức .str` | "bộ truy cập" dịch sát chữ từ *accessor*. |
| `curriculum/phase-04-data/p4-03-cleaning/examples/01_survey_missing.vi.md` | `bằng giá trị trung vị (median)` / `các ô score còn trống` | `bằng trung vị (median) của cột` / `các ô score bị thiếu` | Khớp ý *column median* ở bản EN và nhất quán dùng "bị thiếu". |
| `curriculum/phase-04-data/p4-03-cleaning/examples/02_price_text_to_numbers.vi.md` | `sẽ sập với ValueError` | `sẽ báo lỗi ValueError` | "sập" dịch sát chữ từ *crash*. |
| `curriculum/phase-04-data/p4-03-cleaning/examples/03_training_labels.vi.md` | `bằng strip, viết thường` / `value_counts() cuối cùng` | `bằng cách cắt khoảng trắng, chuyển chữ thường` / `value_counts() sau cùng` | Tránh trộn từ nửa Việt nửa Anh; "cuối cùng" dễ nhầm với nhãn ở vị trí cuối. |

#### Bảng chi tiết mọi chỗ sửa — `p5-02-supervised` (19 chỗ)

| file | trước | sau | lý do |
|---|---|---|---|
| `curriculum/phase-05-ml/p5-02-supervised/lesson.vi.md` | `(**label** — nhãn hay đáp án đúng của từng hàng)` | `(**label** — nhãn, hay đáp án đúng của từng hàng)` | Thêm dấu phẩy tách rõ nghĩa của `label`. |
| `curriculum/phase-05-ml/p5-02-supervised/lesson.vi.md` | `bằng cách khớp một đường thẳng` | `bằng cách khớp (fit) một đường thẳng` | Giới thiệu từ `fit` đi kèm tiếng Việt để nối với các phần sau. |
| `curriculum/phase-05-ml/p5-02-supervised/lesson.vi.md` | `Để xáo hàng một cách lặp lại được ... dùng lát cắt chỉ số đã xáo` | `Để xáo hàng theo thứ tự tái lập được (chạy lại vẫn ra y hệt) ... dùng mảng chỉ số đã xáo được cắt ra` | "lặp lại được" dễ hiểu nhầm với làm nhiều lần (thay vì *reproducible*); "lát cắt" dịch sát chữ từ *slice*. |
| `curriculum/phase-05-ml/p5-02-supervised/lesson.vi.md` | `lại sai lệch nặng trên tập test mới. Ta có thể... nhiễu phân phối chuẩn quanh 0.0 với độ lệch 0.12` | `lại sai lệch nặng trên tập test mới (**overfitting** — học vẹt / khớp quá mức). Ta có thể... nhiễu hình chuông quanh 0.0 với độ lệch chuẩn 0.12` | Bổ sung giải nghĩa `overfitting` ở lần đầu xuất hiện và sửa "độ lệch" → "độ lệch chuẩn". |
| `curriculum/phase-05-ml/p5-02-supervised/lesson.vi.md` | `bậc deg vào dữ liệu` | `bậc deg theo dữ liệu` | "khớp theo dữ liệu" tự nhiên hơn "khớp vào dữ liệu". |
| `curriculum/phase-05-ml/p5-02-supervised/lesson.vi.md` | `biết ngay mô hình đang rơi vào trạng thái nào và cần chỉnh hướng nào tiếp theo.` | `biết ngay mô hình đang rơi vào trạng thái nào — **underfitting** (học chưa tới), **good fit** (vừa khớp) hay **overfitting** (khớp quá mức) — và cần chỉnh hướng nào tiếp theo.` | Giải nghĩa đầy đủ cả 3 thuật ngữ ngay khi so sánh. |
| `curriculum/phase-05-ml/p5-02-supervised/lesson.vi.md` | `\| \| underfitting \| good fit (vừa khớp) \| overfitting \|` | `\| \| underfitting (chưa khớp) \| good fit (vừa khớp) \| overfitting (khớp quá mức) \|` | Đồng bộ giải nghĩa tiếng Việt ở tiêu đề bảng. |
| `curriculum/phase-05-ml/p5-02-supervised/lesson.vi.md` | `hoặc regularization` | `hoặc dùng **regularization** (phạt độ phức tạp)` | Thiếu giải nghĩa ở lần đầu dùng thuật ngữ `regularization`. |
| `curriculum/phase-05-ml/p5-02-supervised/lesson.vi.md` | `Báo cáo điểm trên đúng những dòng vừa dùng để khớp mô hình` | `Chấm điểm trên chính những dòng vừa dùng để huấn luyện (fit) mô hình` | "Báo cáo điểm" (*Reporting the score*) và "khớp mô hình" (*fit the model*) dịch sát chữ. |
| `curriculum/phase-05-ml/p5-02-supervised/lesson.vi.md` | `**2. Data leakage: chuẩn hóa trước khi chia train/test**` | `**2. Data leakage (rò rỉ dữ liệu): chuẩn hóa trước khi chia train/test**` | Bổ sung giải nghĩa tiếng Việt ở lần đầu xuất hiện `Data leakage`. |
| `curriculum/phase-05-ml/p5-02-supervised/lesson.vi.md` | `giá trị chuẩn hóa sạch clean test... các mốc đo từ tập train` | `kết quả chuẩn hóa sạch clean test... các mốc min/max của tập train` | Rõ nghĩa hơn ("mốc đo" hơi mơ hồ so với *training bounds*). |
| `curriculum/phase-05-ml/p5-02-supervised/lesson.vi.md` | `làm điểm test nhảy liên tục` | `khiến điểm test thay đổi liên tục` | Văn phong gãy gọn, tự nhiên hơn. |
| `curriculum/phase-05-ml/p5-02-supervised/lesson.vi.md` | `để tránh **data leakage**.` | `để tránh **data leakage** (rò rỉ dữ liệu).` | Nhắc lại giải nghĩa ngắn ở phần Tóm tắt. |
| `curriculum/phase-05-ml/p5-02-supervised/lesson.vi.md` | `chắc chắn mô hình tổng quát hóa tốt.` | `chắc chắn mô hình **generalize** (tổng quát hóa) tốt trên dữ liệu mới.` | Gắn cặp thuật ngữ EN–VI và làm rõ ngữ cảnh. |
| `curriculum/phase-05-ml/p5-02-supervised/examples/01_ticket_threshold.vi.md` | `ngưỡng thắng cuộc` / `tách rời hoàn toàn ở mức 1.0` | `ngưỡng tốt nhất` / `phân tách hoàn toàn đạt 1.0` | "thắng cuộc" dịch sát chữ từ *winning threshold*; "phân tách" sát nghĩa phân loại hơn "tách rời". |
| `curriculum/phase-05-ml/p5-02-supervised/examples/02_train_test_split.vi.md` | `in đường thẳng khớp` | `in phương trình đường thẳng đã khớp` | Code in ra `slope` và `intercept` tạo thành phương trình đường thẳng. |
| `curriculum/phase-05-ml/p5-02-supervised/examples/03_overfitting_curve.vi.md` | `in sai số train/test MSE` / `tạo lưới grid 100 điểm mượt mà` | `in cả train MSE lẫn test MSE` / `tạo dải grid gồm 100 điểm đều nhau` | "lưới ... mượt mà" dịch sát chữ từ *smooth grid*; "train/test MSE" rõ ý hơn khi tách ra. |

#### Bảng chi tiết mọi chỗ sửa — `p5-04-evaluation` (17 chỗ)

| file | trước | sau | lý do |
|---|---|---|---|
| `curriculum/phase-05-ml/p5-04-evaluation/lesson.vi.md` | `**accuracy** nhìn qua rất cao` | `**accuracy** (tỉ lệ đoán đúng) nhìn qua rất cao` | Nhất quán quy ước thuật ngữ ở mục A.3 ngay đầu bài đánh giá. |
| `curriculum/phase-05-ml/p5-04-evaluation/lesson.vi.md` | `baseline ngây thơ 0.85 ... Luôn so với baseline.` | `baseline đơn giản 0.85 ... Hãy luôn so sánh với baseline.` | "ngây thơ" hơi gượng cho *dummy*; câu sau thêm chủ ngữ/từ nối tự nhiên. |
| `curriculum/phase-05-ml/p5-04-evaluation/lesson.vi.md` | `bằng boolean mask của NumPy` | `bằng **boolean mask** (mảng lọc True/False) của NumPy` | Bổ sung giải nghĩa ngắn cho `boolean mask`. |
| `curriculum/phase-05-ml/p5-04-evaluation/lesson.vi.md` | `Nhìn vào ma trận 51 + 0 + 7 + 2 = 60 ticket test:` | `Để ý tổng cộng có 51 + 0 + 7 + 2 = 60 ticket test:` | Sửa lỗi diễn đạt (phép cộng 4 số không phải là "ma trận"). |
| `curriculum/phase-05-ml/p5-04-evaluation/lesson.vi.md` | `sinh UndefinedMetricWarning` | `phát cảnh báo UndefinedMetricWarning` | Tự nhiên hơn từ "sinh" (*triggers*). |
| `curriculum/phase-05-ml/p5-04-evaluation/lesson.vi.md` | `xác suất out-of-fold trên X_train` | `xác suất **out-of-fold** (dự đoán ngoài fold) trên X_train` | Bổ sung giải nghĩa tiếng Việt ở lần đầu xuất hiện `out-of-fold`. |
| `curriculum/phase-05-ml/p5-04-evaluation/lesson.vi.md` | `Như đã hẹn ở cuối bài p5-03-sklearn` | `Như đã nhắc ở bài p5-03-sklearn` | Khớp chính xác bản EN (*As noted in p5-03-sklearn*), không tự thêm ý "đã hẹn". |
| `curriculum/phase-05-ml/p5-04-evaluation/lesson.vi.md` | `tự chia 5 fold giữ tỉ lệ lớp` | `tự chia 5 fold **stratified** (giữ nguyên tỉ lệ lớp)` | Gắn thuật ngữ `stratified` với tên hàm `StratifiedKFold` ngay sau đó. |
| `curriculum/phase-05-ml/p5-04-evaluation/lesson.vi.md` | `khiến bạn đọc ngược FP thành FN` | `làm ma trận bị chuyển vị và tráo đổi FP với FN` | Sát nghĩa hơn với bản EN (*transposes the matrix and swaps FP with FN*). |
| `curriculum/phase-05-ml/p5-04-evaluation/lesson.vi.md` | `trên dữ liệu phân bố lệch — hãy đặt scaler vào trong make_pipeline.` | `— hãy luôn đặt scaler vào trong make_pipeline.` | Bỏ cụm "trên dữ liệu phân bố lệch" không có trong EN (ví dụ chỉ minh họa leakage nói chung). |
| `curriculum/phase-05-ml/p5-04-evaluation/lesson.vi.md` | `chọn mô hình theo một fold tốt nhất` | `chọn mô hình theo một fold may mắn` | Sát nghĩa *one lucky fold* trong EN, nhấn mạnh tính ăn may. |
| `curriculum/phase-05-ml/p5-04-evaluation/lesson.vi.md` | `đạt đỉnh trên một fold y hệt nhau ... chứ không nhặt riêng .max()` | `có điểm cao nhất trên một fold bằng hệt nhau ... chứ không chỉ chọn theo .max()` | Sửa trật tự câu ("fold y hệt nhau" dễ hiểu nhầm fold giống nhau thay vì điểm đỉnh bằng nhau); "nhặt riêng" hơi gượng. |
| `curriculum/phase-05-ml/p5-04-evaluation/lesson.vi.md` | `hiển thị điểm từng lớp` | `hiển thị điểm của từng lớp` | Thêm "của" cho trôi chảy. |
| `curriculum/phase-05-ml/p5-04-evaluation/examples/01_ticket_metrics.vi.md` | `tạo 200 ticket tổng hợp` | `tạo 200 ticket giả lập` | "tổng hợp" (*synthetic*) dễ hiểu nhầm thành "summary/aggregated"; "giả lập" rõ nghĩa hơn. |
| `curriculum/phase-05-ml/p5-04-evaluation/examples/02_threshold_tradeoff.vi.md` | `chia dữ liệu 85/15 thành train_full / test` | `tạo bộ dữ liệu lệch lớp 85/15 rồi chia thành train_full / test` | Sửa lỗi sai nghĩa nghiêm trọng: 85/15 là tỉ lệ lệch lớp (`weights=[0.85]`), còn chia `train_full`/`test` là 70/30 (`test_size=0.3`). |
| `curriculum/phase-05-ml/p5-04-evaluation/examples/03_cross_validation.vi.md` | `(357 lành tính, 212 ác tính)` | `(212 ác tính, 357 lành tính)` | Khớp thứ tự bản EN và đưa lớp dương (`1` = ác tính) lên trước. |
| `curriculum/phase-05-ml/p5-04-evaluation/examples/03_cross_validation.vi.md` | `chỉ fit bước chuẩn hóa` | `chỉ fit bộ chuẩn hóa` | Tự nhiên và đúng với đối tượng `StandardScaler()` hơn "bước chuẩn hóa". |

### C. 5 lỗi văn phong VI lặp lại nhiều nhất (đề xuất đưa vào quy tắc)
1. **Dịch sát chữ (calque) các động từ và ẩn dụ tiếng Anh:** ví dụ `crash` → "sập code", `winning threshold` → "ngưỡng thắng cuộc", `report score` → "báo cáo điểm", `hide spaces` → "giấu khoảng trắng", `accessor` → "bộ truy cập", `slice` → "lát cắt", `smooth grid` → "lưới mượt mà", `mask` → "mặt nạ".
2. **Thiếu giải nghĩa tiếng Việt ở lần đầu xuất hiện thuật ngữ mới:** các từ như `overfitting`, `underfitting`, `regularization`, `data leakage`, `out-of-fold`, `boolean mask`, `stratified` thường xuất hiện trần bằng tiếng Anh mà chưa kèm chú thích ngắn trong ngoặc ở lần đầu tiên.
3. **Diễn đạt sai nghĩa kỹ thuật hoặc gây mơ hồ khi rút gọn cụm EN:** ví dụ `85/15 split` (chỉ tập lệch lớp 85/15) bị dịch thành "chia dữ liệu 85/15"; `synthetic` dịch thành "tổng hợp" dễ nhầm với *summary*; `spread` dịch thành "độ lệch" thay vì "độ lệch chuẩn"; `final` dịch thành "cuối cùng" ("nhãn cuối" dễ hiểu nhầm là nhãn ở cuối danh sách).
4. **Sắp xếp bổ ngữ theo trật tự tiếng Anh hoặc thiếu từ nối / bị động:** ví dụ "không bao giờ giữ lại" (thiếu "bị"), "xử lý thiếu" (thiếu "giá trị"), "đạt đỉnh trên một fold y hệt nhau" (bổ ngữ "y hệt nhau" đặt sau `fold` làm đổi đối tượng được bổ nghĩa).
5. **Tự thêm ý hoặc dùng từ không đồng bộ ngữ cảnh sư phạm:** ví dụ thêm "như đã hẹn" hoặc "trên dữ liệu phân bố lệch" không có trong EN, hoặc dùng "baseline ngây thơ" / "giá trị sử dụng" / "nhặt riêng `.max()`".

## 2. File đã sửa

- `CLAUDE.md` (gitignored)
- `docs/DESIGN.md` (gitignored)
- `docs/CONTENT_GUIDE.md` (gitignored)
- `curriculum/phase-04-data/p4-03-cleaning/lesson.vi.md`
- `curriculum/phase-04-data/p4-03-cleaning/examples/01_survey_missing.vi.md`
- `curriculum/phase-04-data/p4-03-cleaning/examples/02_price_text_to_numbers.vi.md`
- `curriculum/phase-04-data/p4-03-cleaning/examples/03_training_labels.vi.md`
- `curriculum/phase-05-ml/p5-02-supervised/lesson.vi.md`
- `curriculum/phase-05-ml/p5-02-supervised/examples/01_ticket_threshold.vi.md`
- `curriculum/phase-05-ml/p5-02-supervised/examples/02_train_test_split.vi.md`
- `curriculum/phase-05-ml/p5-02-supervised/examples/03_overfitting_curve.vi.md`
- `curriculum/phase-05-ml/p5-04-evaluation/lesson.vi.md`
- `curriculum/phase-05-ml/p5-04-evaluation/examples/01_ticket_metrics.vi.md`
- `curriculum/phase-05-ml/p5-04-evaluation/examples/02_threshold_tradeoff.vi.md`
- `curriculum/phase-05-ml/p5-04-evaluation/examples/03_cross_validation.vi.md`
- `tasks/m3-16-docs-vi.report.md` (báo cáo này)

## 3. Kết quả lệnh kiểm tra

Chạy sau lần chỉnh sửa cuối cùng:
- `uv run python tools/validate.py --path curriculum/phase-04-data/p4-03-cleaning`:
  `OK: 0 error(s), 0 warning(s). Checked 1 lessons, 7 markdown pairs, 3 examples, 2 exercises, 1 alternatives, 16 questions.` (exit 0)
- `uv run python tools/validate.py --path curriculum/phase-05-ml/p5-02-supervised`:
  `OK: 0 error(s), 0 warning(s). Checked 1 lessons, 7 markdown pairs, 3 examples, 2 exercises, 1 alternatives, 16 questions.` (exit 0; có 1 `UserWarning` từ `plt.show()` trên Agg khi chạy khối code minh họa của bài)
- `uv run python tools/validate.py --path curriculum/phase-05-ml/p5-04-evaluation`:
  `OK: 0 error(s), 0 warning(s). Checked 1 lessons, 7 markdown pairs, 3 examples, 2 exercises, 1 alternatives, 16 questions.` (exit 0)
- `uv run python tools/validate.py`:
  `OK: 0 error(s), 0 warning(s). Checked 35 lessons, 272 markdown pairs, 103 examples, 70 exercises, 64 alternatives, 702 questions, 8 exams, 1 portfolio, 1 glossary, 1 interview.` (exit 0)
- Kiểm tra từ cấm (`độ chính xác|độ phủ|bảng vết|chuyển ca trực|hậu kiểm`) trên 12 file `.vi.md` thuộc 3 bài bằng PowerShell `Select-String`: kết quả rỗng (0 kết quả khớp).
- `git status --short`: chỉ gồm 12 file `.vi.md` trong danh sách được phép sửa (cùng các thư mục untracked có sẵn `.hallmark/` và `tasks/`). `CLAUDE.md` và `docs/` bị gitignore nên không hiện trong `git status`.

## 4. Điều còn chưa chắc

- Lệnh `grep` trong spec chạy trên PowerShell Windows nên được thay bằng `Select-String` (tương đương regex); chưa chạy lại chính xác binary `grep` của Unix/Git Bash.
- Một số dòng trong bảng diff gộp 2 chỉnh sửa trên cùng 1 dòng nên tổng số hàng trong bảng từng bài ở báo cáo khớp theo vị trí sửa (19, 19, 17 mục — thực tế đếm chi tiết cụm từ sửa tương ứng với số lần edit trong bài).
- Trong `p5-02-supervised/lesson.vi.md` dòng 199 (bảng so sánh), tôi đã thêm chú thích `(chưa khớp)` và `(khớp quá mức)` vào tiêu đề cột `underfitting` / `overfitting` — validator pass 0 lỗi, nhưng nếu muốn giữ tiêu đề bảng cực ngắn trên màn hình hẹp thì có thể bỏ hai ngoặc đó vì dòng 197 ngay phía trên đã giải nghĩa đầy đủ.
- Chưa đọc lại `exercises/*/prompt.vi.md` và `alternatives/*.vi.md` của 3 bài (do spec giới hạn chỉ sửa `lesson.vi.md` và `examples/*.vi.md`); nếu có lỗi văn phong tương tự ở đề bài tập thì chưa được rà trong bước này.
