# M4 bước 25: bài p8-04 Monitoring, cost & latency

## Mục tiêu
Viết bài `p8-04-monitoring` trong `curriculum/phase-08-production/`, đúng `docs/CONTENT_GUIDE.md` (gồm mục "phase 6+"), song ngữ EN/VI.
- Bài **không** có `runner: local`: mọi khối `python`, example, exercise và quiz chạy trong **Pyodide**. Chỉ dùng thư viện chuẩn (`json`, `logging`, `statistics`, `math`, `dataclasses`, `collections`) cùng `pyai_llm`.
- Người học đã có:
  - p3-03: `logging` (logger, level, handler, format);
  - p7-01: `FakeLLM.chat`, `Usage` (prompt/completion tokens), tính cost theo token;
  - p8-01: endpoint FastAPI;
  - p8-03: cache, hit rate, đồng hồ tiêm vào (`FakeClock`).
- Ý chính: hệ thống LLM ở production hỏng theo những cách "im lặng": chậm dần, đắt dần, cache hit rate tụt. Không đo thì không biết. Bài dạy ghi **một dòng log có cấu trúc cho mỗi request**, tính **p50/p95** và chi phí từ các dòng đó, rồi đặt **ngưỡng cảnh báo** đơn giản.
- Bài mẫu về giọng văn và hình dạng: `curriculum/phase-08-production/p8-03-caching/` (commit `bb6b9c4`), `p8-01-fastapi/`.

## File được phép sửa/tạo
- Thư mục mới `curriculum/phase-08-production/p8-04-monitoring/` và mọi file bên trong.
- `curriculum/glossary.yaml`: chỉ **thêm** thuật ngữ mới: metric, latency, percentile, p50, p95, structured logging, alert, threshold, budget, observability. Thuật ngữ nào đã có thì bỏ qua. `git diff --numstat curriculum/glossary.yaml` phải có 0 dòng xóa.
- `tasks/m4-p8-04-monitoring.report.md`

## Không được đụng
- Mọi file khác, gồm `apps/`, `tools/`, `packages/`, `curriculum/syllabus.yaml`, `curriculum/topics.yaml`, phase 0–7, `p8-01`…`p8-03`, `exams/`, `pyproject.toml`, `uv.lock`.
- Tag chỉ dùng tag có sẵn trong `topics.yaml`: `production` (chính), có thể thêm `performance`, `logging`, `llm`.
- Không xóa file, không `git commit`, **không chạy `pnpm --filter web build`**, không chạy server hay dev server.
- `meta.yaml` **không** có trường `runner`.

## Quy tắc code (bắt buộc)
- **Không dùng thời gian thật**: không `time.time()`, `time.perf_counter()`, `time.sleep`, `datetime.now()`. Latency là **số giả lập tất định**:
  - hoặc một `FakeClock` có `advance(ms)` được hàm "LLM giả" gọi theo một công thức cố định (vd latency = 200 + 3 × số token completion, hoặc lấy từ một list cố định);
  - hoặc list latency (ms) viết sẵn trong code.
  - Một câu trong bài: ở production bạn đo bằng `time.perf_counter()` trước và sau lời gọi (chỉ nhắc trong câu văn hoặc comment, không gọi).
- **Percentile dùng phương pháp nearest-rank, tự viết**: sắp xếp, `rank = math.ceil(p / 100 * n)`, lấy phần tử `rank - 1`. Ghi rõ trong bài vì sao chọn cách này (đơn giản, luôn trả một giá trị có thật). Có thể nhắc một câu rằng `statistics.quantiles` dùng nội suy nên có thể ra số khác một chút; nếu dùng nó trong code thì in kết quả thật.
- Token lấy từ `response.usage` của `FakeLLM`; giá giả định ghi rõ trong code, vd `PRICE_IN_PER_1K = 0.0005`, `PRICE_OUT_PER_1K = 0.0015`. Tiền in bằng `round(x, 4)` hoặc f-string `:.4f`.
- Log có cấu trúc: mỗi request một dòng `json.dumps(record, sort_keys=True)`. Khi dùng `logging`, handler ghi ra `sys.stdout` với `format="%(message)s"` để output tất định (không có giờ). Không in timestamp thật; nếu record có trường thời gian thì lấy từ `FakeClock`.
- Không đọc thuộc tính private của `FakeLLM`. LLM chỉ qua `from pyai_llm import FakeLLM, ...`. Mọi output in ra là output thật (chạy rồi chép).
- Không đọc hay ghi file, không mạng, không `subprocess`. Sạch với `uv run python -W error`, stderr rỗng (chú ý `logging` mặc định ghi stderr: phải cấu hình sang stdout hoặc dùng `print`).
- Khối mời **Visualize** phải dưới 600 step. Kiểm bằng `tools/pyrunner/tracer.py`, ghi `len(steps)` và `truncated` vào report.

## Nội dung bài (boss chốt dàn ý, worker viết)
Opening (không heading): bot RAG chạy ổn tuần đầu. Tuần thứ ba, hóa đơn API gấp ba và người dùng than chậm, nhưng không ai biết từ lúc nào và vì đâu. **Monitoring** là ghi lại đủ số liệu để trả lời câu đó trong 5 phút.

1. **Ghi gì cho mỗi request: metric có cấu trúc.**
   - Ví von: hộp đen máy bay, ghi đều đặn những con số nhỏ để khi có chuyện thì tra lại được.
   - Các trường: `request_id`, `route`, `model`, `latency_ms`, `prompt_tokens`, `completion_tokens`, `cost_usd`, `cache_hit`, `status` (`"ok"`/`"error"`).
   - Khối `python`: wrapper `tracked_chat(...)` gọi `FakeLLM`, đo latency bằng `FakeClock`, tạo dict record, in bằng `json.dumps(sort_keys=True)`.
   - **Bảng so sánh** `| log kiểu chữ tự do | log có cấu trúc (JSON) |`: grep được hay không, tính tổng được hay không, v.v.
   - Callout `[!WARNING]`: không ghi nguyên prompt, câu trả lời, API key hay dữ liệu cá nhân vào log metric. Ghi độ dài hoặc hash nếu cần.
2. **Ghi log bằng `logging`, không phải `print`.**
   - Nối với p3-03: logger `"app.metrics"`, handler ra stdout, `format="%(message)s"`, `logger.info(json.dumps(record))`.
   - Một câu: ở production các dòng này được gom về một nơi (vd hệ thống log của cloud) để tìm và vẽ biểu đồ; bài này giữ trong list để tính toán.
3. **Latency: vì sao trung bình đánh lừa bạn.**
   - Với 10 latency (vd 9 request khoảng 200 ms, 1 request 3000 ms): in mean, p50, p95. Mean bị kéo lên bởi một request, p50 cho thấy "người dùng thường gặp", p95 cho thấy "người dùng xui nhất trong 20 người".
   - **Picture in text** (fence `text`): 10 latency đã sắp xếp nằm trên một hàng, đánh dấu vị trí p50 và p95 bằng `^`. Giống hệt giữa EN và VI.
   - Tự viết `percentile(values, p)` nearest-rank. Đây là section mời bấm **Visualize** (xem list được sắp xếp và `rank` được tính).
   - **Trace table** `| p | n | p/100 × n | rank (ceil) | index | value |` cho p=50 và p=95 với n=10.
4. **Chi phí: từ token ra tiền.**
   - `cost = prompt_tokens / 1000 × PRICE_IN + completion_tokens / 1000 × PRICE_OUT`. Nhấn mạnh token ra thường đắt hơn token vào.
   - Tổng hợp từ list record: tổng chi phí, chi phí trung bình mỗi request, chi phí theo `route` (dùng dict cộng dồn hoặc `defaultdict`), in theo thứ tự sắp xếp.
   - Ước lượng tháng: chi phí trung bình × số request/ngày × 30 (số liệu giả định ghi rõ).
5. **Bảng tổng kết (summary) từ log.**
   - Hàm `summarize(records)` trả dict: `count`, `error_rate`, `p50_ms`, `p95_ms`, `total_cost`, `cache_hit_rate`. Nối sang p8-03: hit rate tụt là dấu hiệu cache key hỏng hoặc TTL quá ngắn.
   - **Mermaid** `flowchart LR` (≤ 8 node): request → LLM call → record → log → summarize → so với ngưỡng → alert.
6. **Cảnh báo: ngưỡng ngân sách và độ trễ.**
   - `check_alerts(summary, max_p95_ms, max_cost, max_error_rate)` trả list chuỗi cảnh báo theo thứ tự cố định, list rỗng nghĩa là ổn.
   - Chạy với hai "ngày" dữ liệu: ngày bình thường (không cảnh báo) và ngày tệ (p95 vượt và chi phí vượt). In kết quả.
   - Bàn về chọn ngưỡng: đặt theo p95 chứ không theo mean; quá chặt thì báo động giả liên tục và mọi người sẽ phớt lờ; cảnh báo ngân sách nên báo **trước** khi chạm trần (vd ở 80%).
   - Callout `[!TIP]`: bắt đầu với 3 cảnh báo (p95 latency, chi phí ngày, error rate), thêm dần khi thật sự cần.
7. **Lỗi thường gặp** (VI: `## 7. Lỗi thường gặp`). Mỗi lỗi có code sai, output sai thật, và cách sửa:
   - chỉ theo dõi latency trung bình, bỏ sót request chậm (cho thấy mean "trông ổn" trong khi p95 rất tệ);
   - percentile trên list chưa sắp xếp, ra số vô nghĩa;
   - tính chi phí bằng một giá cho cả token vào và ra (hoặc quên chia 1000), sai lệch lớn;
   - không ghi record khi request lỗi (chỉ log trong nhánh thành công), nên error rate luôn là 0. Sửa bằng `try/finally` hoặc ghi record ở cả nhánh `except`.
8. **Recap / Tóm tắt**: 4–6 gạch đầu dòng.

**meta.yaml**
- `phase: p8`, `order: 4`, `kind: lesson`.
- `tags: [production]`, có thể thêm `performance`, `logging`, `llm`.
- `prerequisites: [p8-03-caching]`.
- `duration_min` 14–18.
- `outcomes` khớp syllabus (có thể thêm 1 dòng).
- `review_by: "2027-05-01"`.
- `further_reading`: Python docs `logging` (Logging HOWTO), Python docs `statistics.quantiles`, và trang tổng quan chính thức của OpenTelemetry (ghi một câu: đây là chuẩn mở để thu metric/trace ở quy mô lớn, ngoài phạm vi bài). Mở thử từng link rồi ghi vào report.

## Examples (3)
- `01_request_log`: 8 request qua `FakeLLM` (có 2 cache hit với latency rất nhỏ và 0 token, 1 request lỗi do `fail_times` hoặc script), mỗi request in một dòng JSON qua `logging` ra stdout, cuối cùng in số dòng đã ghi.
- `02_latency_report`: 20 latency cố định, in bảng `metric | value` gồm min, mean, p50, p90, p95, max; rồi in 3 request chậm nhất (theo `request_id`).
- `03_daily_budget`: 3 ngày dữ liệu (list record cố định), mỗi ngày in summary ngắn và cảnh báo (nếu có); ngày 3 có cảnh báo "đã dùng 85% ngân sách" kiểu cảnh báo sớm.

## Exercises (2)
Test import code người học như module `exercise`. Pyodide chạy được.
- `ex01-percentile` (`kind: fill`):
  - Hàm `percentile(values: list[float], p: float) -> float` nearest-rank, và `latency_report(values) -> dict` trả `{"p50": ..., "p95": ..., "max": ...}`.
  - 3–4 ô `___` trong thân hàm: `sorted(...)`, `math.ceil(...)`, chỉ số `rank - 1`, gọi `percentile(values, 95)`.
  - `percentile` phải `raise ValueError` khi list rỗng hoặc `p` ngoài `(0, 100]` (phần này viết sẵn, không phải ô trống).
  - 5 test: p50 của list lẻ/chẵn; p95 với n=20; không phụ thuộc thứ tự đầu vào (list đảo ngược ra cùng kết quả); p=100 trả max; `pytest.raises(ValueError)` cho list rỗng.
  - Starter phải import được (ô `___` nằm trong hàm) và fail mọi test (test `raises` cũng phải fail, vd vì kiểm tra nằm sau một dòng có `___` hoặc vì cách viết starter; ghi rõ trong report cách đảm bảo).
- `ex02-metrics-tracker` (`kind: code`):
  - `class MetricsTracker` với `__init__(self, price_in_per_1k: float, price_out_per_1k: float)`:
    - `record(latency_ms: float, prompt_tokens: int, completion_tokens: int, ok: bool = True) -> float`: lưu một record, trả chi phí của request đó;
    - `summary() -> dict` trả `count`, `error_rate`, `p95_ms` (nearest-rank), `total_cost` (làm tròn 6 chữ số); khi chưa có record: `count` 0, các giá trị còn lại `0.0`;
    - `alerts(max_p95_ms: float, budget: float, warn_ratio: float = 0.8) -> list[str]` trả theo thứ tự cố định các mã: `"p95-latency"` khi `p95_ms > max_p95_ms`; `"budget-exceeded"` khi `total_cost > budget`, ngược lại `"budget-warning"` khi `total_cost >= warn_ratio * budget`; `"error-rate"` khi `error_rate > 0.05`.
  - Request lỗi (`ok=False`) vẫn được tính vào `count`, latency và chi phí.
  - 8–10 test, có `parametrize` và `pytest.approx`: chi phí một request; tổng chi phí; error rate; p95; summary rỗng; từng mã cảnh báo; budget-warning và budget-exceeded không xuất hiện cùng lúc; thứ tự mã cố định; list rỗng khi mọi thứ ổn.
  - Starter import được, có docstring kèm ví dụ, `# TODO`, `return None`/`pass`, và fail **mọi** test.
  - `alternatives/01_*`: một cách khác thật sự, vd lưu các cột song song (list latency, list cost) thay cho list record dataclass, hoặc dùng `statistics` cho phần tổng hợp. File `.md` nói ưu và nhược điểm.
- Hint 3 tầng đúng CONTENT_GUIDE. Hint 3 chỉ cho **khung**, để trống ít nhất 2–3 dòng logic chính, không chép gần trọn lời giải.
- Lời giải exercise **không được** là bản sao code trong lesson: lesson dùng `summarize(records)` và `check_alerts(summary, ...)` với chuỗi cảnh báo tự do; ex02 là class với API, mã cảnh báo và luật budget-warning khác. ex01 phải khác `percentile` trong §3 ở chỗ có `latency_report` và kiểm tra lỗi; ghi điểm khác vào report.

## Quiz
- 15–18 câu; mỗi loại `mcq`, `output`, `fill`, `parsons` có ít nhất 2. Khoảng 5 dễ, 7 vừa, 3 khó. 6 flashcard.
- Code là Python thuần chạy được trong Pyodide, không dùng thời gian thật.
- `parsons` phải chỉ có **một** thứ tự đúng, nhờ phụ thuộc giữa các dòng hoặc nhờ output in ra.
- Phải có câu về:
  - vì sao p95 tốt hơn mean để theo dõi latency;
  - tính nearest-rank (output);
  - chi phí token vào/ra;
  - log có cấu trúc vs chữ tự do;
  - không ghi dữ liệu nhạy cảm vào log;
  - ghi record cả khi lỗi;
  - cảnh báo ngân sách sớm;
  - báo động giả khi ngưỡng quá chặt;
  - cache hit rate như một metric.
- Luật MCQ:
  - đáp án đúng có `len <= 1.2 ×` trung bình độ dài distractor (cả en và vi);
  - đáp án đúng là phương án dài nhất duy nhất ở tối đa 1/3 số MCQ;
  - không giấu lý do trong đáp án đúng.
  - Chạy script độ dài trong `tasks/m4-p7-test.md`, đổi path sang `quiz.yaml` của bài này, rồi ghi kết quả.

## Tiêu chí hoàn thành (checklist)
1. [ ] Đủ file theo layout CONTENT_GUIDE. `meta.yaml` đúng mục meta, không có `runner`.
2. [ ] Lesson đúng dàn ý và có đủ: picture in text; trace table; mermaid; bảng so sánh; một lời mời Visualize; callout.
3. [ ] Parity EN/VI: code Python chỉ khác comment; fence `text` giống hệt; số dòng mermaid bằng nhau.
4. [ ] Tuân thủ Quy tắc code: không dùng thời gian thật; `-W error` sạch, stderr rỗng; output là output thật; lệnh grep bên dưới rỗng.
5. [ ] Exercise: starter fail **mọi** test (ghi số test pass với starter, phải là 0); solution và alternative pass cả pytest lẫn browser runner trong validate; lời giải khác code trong lesson.
6. [ ] Bản VI tự nhiên, xưng "bạn". Thuật ngữ giữ tiếng Anh, lần đầu kèm giải nghĩa, vd "latency (độ trễ)", "percentile (phân vị)", "alert (cảnh báo)".
7. [ ] Report ghi: số step của khối Visualize; thời gian `validate.py --path`; kết quả script MCQ; các link đã mở.
8. [ ] Lệnh kiểm tra xanh, chạy đúng như ghi.

## Lệnh kiểm tra
Từ gốc repo `D:\Proj\python-ai-platform`:
```
uv run python tools/validate.py --path curriculum/phase-08-production/p8-04-monitoring
uv run python tools/validate.py --fast
uv run python -m pytest curriculum/phase-08-production -p no:warnings --color=no
uv run ruff check curriculum/phase-08-production
grep -rnE "time\.time|time\.sleep|perf_counter\(\)|monotonic\(\)|datetime\.now|_chat_calls|open\(|subprocess|requests\.|httpx" curriculum/phase-08-production/p8-04-monitoring --include=*.py --include=*.yaml
git diff --numstat curriculum/glossary.yaml
uv run python tools/build_content.py
git status --short
```
Mong đợi:
- validate 0 lỗi;
- pytest exit 0;
- ruff sạch;
- grep rỗng;
- glossary chỉ có dòng thêm;
- build_content in số lesson tăng 1 (52 → 53);
- thay đổi chỉ nằm trong các file được phép, ngoài `tasks/` và `.hallmark/` vốn đã untracked.

Lưu ý: grep `perf_counter\(\)` / `monotonic\(\)` chặn việc gọi đồng hồ thật. Chỉ được **nhắc** chúng trong câu văn hoặc comment.

## Ghi chú cho worker
- Đọc trước:
  - `docs/CONTENT_GUIDE.md`;
  - bài `p8-03-caching` và `p8-01-fastapi` (mẫu hình dạng);
  - `curriculum/phase-03-code-quality/p3-03-logging` (logging đã dạy);
  - `packages/pyai_llm/pyai_llm.py` và `README.md`: API `chat`, `Usage`, `fail_times`, `script`, `RateLimitError`.
- Dùng `uv run python -m pytest`, không dùng `uv run pytest`. Trên Windows có thể không có `grep` trong PATH; dùng Git Bash.
- Mọi lệnh phải tự kết thúc. Không chạy server.
- Kiểm cảnh báo bằng `uv run python -W error <file>`; kiểm stderr rỗng (logging mặc định ghi stderr).

## Trạng thái
- Bước hiện tại: xong, đã commit a223b3a (đạt vòng 1; boss kiểm: validate toàn bộ 0 lỗi (53 bài), pytest phase 8 64 passed, ruff sạch, grep rỗng, glossary +100/-0, starter 5/5 và 15/15 fail, typecheck + build 77 trang; trong app (Pyodide) ex02 starter 0/15, solution qua hết; chờ user duyệt commit)
- Vòng: 1/3
- Số lần swap: 0
- Fallback: không
- Model: Gemini 4 Hydrogen (High)
