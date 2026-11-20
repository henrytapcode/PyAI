# M4 bước 24: bài p8-03 Caching

## Mục tiêu
Viết bài `p8-03-caching` trong `curriculum/phase-08-production/`, đúng `docs/CONTENT_GUIDE.md` (gồm mục "phase 6+"), song ngữ EN/VI.
- Bài **không** có `runner: local`: mọi khối `python`, example, exercise và quiz chạy trong **Pyodide**. Chỉ dùng thư viện chuẩn có trong Pyodide (`collections.OrderedDict`, `hashlib`, `json`, `functools`) cùng `pyai_llm`.
- Người học đã có:
  - p2-07: decorator, có nhắc `functools.cache` trong một bảng;
  - p7-01, p7-03: `FakeLLM.chat` và `embed`, `Usage`, tính cost theo token;
  - p8-01: endpoint FastAPI;
  - p8-02: Docker.
- Ý chính: gọi LLM và tạo embedding vừa chậm vừa tốn tiền, mà nhiều câu hỏi lặp lại. Cache trả lời ngay những câu đã gặp. Khó nhất là chọn **key** đúng và biết khi nào dữ liệu trong cache đã cũ.
- Bài mẫu về giọng văn và hình dạng: `curriculum/phase-08-production/p8-01-fastapi/` và `p8-02-docker/` (commit `da2612a`).

## File được phép sửa/tạo
- Thư mục mới `curriculum/phase-08-production/p8-03-caching/` và mọi file bên trong.
- `curriculum/glossary.yaml`: chỉ **thêm** thuật ngữ mới: cache, cache hit, cache miss, hit rate, TTL, LRU, eviction, cache key, invalidation. Thuật ngữ nào đã có thì bỏ qua. `git diff --numstat curriculum/glossary.yaml` phải có 0 dòng xóa.
- `tasks/m4-p8-03-caching.report.md`

## Không được đụng
- Mọi file khác, gồm `apps/`, `tools/`, `packages/`, `curriculum/syllabus.yaml`, `curriculum/topics.yaml`, phase 0–7, `p8-01-fastapi`, `p8-02-docker`, `exams/`, `pyproject.toml`, `uv.lock`.
- Tag chỉ dùng tag có sẵn trong `topics.yaml`: `production` (chính), có thể thêm `performance` và `llm`.
- Không xóa file, không `git commit`, **không chạy `pnpm --filter web build`**, không chạy server hay dev server.
- `meta.yaml` **không** có trường `runner`.

## Quy tắc code (bắt buộc)
- **Không dùng thời gian thật**: không `time.time()`, `time.sleep`, `datetime.now()`. TTL dùng **đồng hồ tiêm vào**, tức tham số `now: float` hoặc một class `FakeClock` nhỏ có `advance(seconds)`, để output tất định và test chạy tức thì.
  - Một câu trong bài: ở production bạn truyền `time.monotonic` vào.
  - Một câu: dùng `monotonic` chứ không dùng giờ hệ thống, vì giờ hệ thống có thể bị chỉnh lùi.
- "Độ chậm" của LLM chỉ được **đếm**: số lần gọi thật, token và chi phí ước tính theo giá giả định ghi rõ trong code. Không đo thời gian thật.
- Đếm số lần gọi LLM bằng wrapper hoặc biến đếm của chính bạn. Không đọc thuộc tính private `_chat_calls` của `FakeLLM`.
- LLM chỉ qua `from pyai_llm import FakeLLM, ...`. Mọi output in ra là output thật (chạy rồi chép).
- Key dùng `json.dumps(..., sort_keys=True)` rồi `hashlib.sha256(...).hexdigest()`. Khi in hash, chỉ in 12 ký tự đầu.
- Không đọc hay ghi file, không mạng, không `subprocess`. Sạch với `uv run python -W error`, stderr rỗng.
- Khối mời **Visualize** phải dưới 600 step. Kiểm bằng `tools/pyrunner/tracer.py`, ghi `len(steps)` và `truncated` vào report.

## Nội dung bài (boss chốt dàn ý, worker viết)
Opening (không heading): bot hỗ trợ khách hàng nhận câu "How do I reset my password?" hàng trăm lần mỗi ngày. Lần nào cũng gọi LLM thì vừa tốn tiền, vừa bắt người dùng chờ. **Cache** nhớ câu trả lời của lần trước.

1. **Cache là gì: hit, miss, hit rate.**
   - Ví von: mảnh giấy ghi chú dán cạnh bàn, có sẵn thì khỏi đi tra sổ.
   - Khối `python`: một dict làm cache đặt trước hàm "chậm" (đếm số lần gọi thật). Gọi 6 lần với 3 câu hỏi lặp, in hits/misses, hit rate, và số lần gọi thật.
   - **Trace table** `| call | question | hit? | real calls | cache size |`.
   - Đây là section mời bấm **Visualize** (xem `cache` lớn dần và `hits` tăng).
2. **`functools.lru_cache`: cache có sẵn cho hàm thuần.**
   - Nối với p2-07.
   - Dùng `@lru_cache(maxsize=...)` trên một hàm tính toán thuần, in `cache_info()`.
   - Giới hạn: chỉ nhận đối số hashable, không có TTL, và không nên dùng cho hàm có side effect hay kết quả thay đổi theo thời gian.
   - Callout `[!NOTE]`.
3. **Cache key cho prompt: cái gì làm câu trả lời khác đi?**
   - Câu trả lời phụ thuộc vào `model`, `messages` (gồm system prompt), `temperature` và các tham số như `max_tokens`. Key phải chứa **tất cả**, nếu không bạn sẽ trả nhầm câu trả lời.
   - Hàm `make_key(model, messages, **params)` dùng `json.dumps(sort_keys=True)` và `sha256`.
   - Chuẩn hóa nhẹ (strip, gộp khoảng trắng) để `"Reset password?"` và `" Reset  password? "` trúng cùng key. Một câu cảnh báo: không tự ý viết thường hay bỏ dấu câu, vì có thể đổi nghĩa.
   - Chỉ cache khi `temperature == 0`: khi temperature > 0, người dùng mong mỗi lần một câu trả lời khác.
   - **Bảng so sánh** `| include in key | why |`.
   - **Picture in text** (fence `text`): các phần `model | system | messages | temperature | max_tokens` → JSON → sha256 → key `"3f2a9c..."`. Chuỗi minh họa có thể rút gọn; fence giống hệt nhau giữa EN và VI.
4. **Cache embedding.**
   - `embed(texts)` với key `(model, text)`. Chỉ gọi `embed` cho những text chưa có trong cache (gom thành một batch), rồi ghép kết quả **đúng thứ tự** ban đầu.
   - In số text thật sự gửi đi khi re-index một kho có 5 tài liệu, trong đó 1 tài liệu vừa sửa.
   - Một câu: đổi model embedding thì phải bỏ toàn bộ cache, vì vector của hai model khác nhau không so được (nối với p7-03).
5. **LRU: giới hạn bộ nhớ.**
   - Cache không giới hạn sẽ ăn hết RAM.
   - Tự viết `LRUCache` bằng `OrderedDict`: `get` gọi `move_to_end`, `set` gọi `popitem(last=False)` khi vượt `maxsize`.
   - **Mermaid** `flowchart TD` (≤ 8 node): get key → có trong cache? → (có) đưa lên đầu, trả về → (không) gọi hàm thật → lưu → vượt maxsize? → bỏ phần tử dùng lâu nhất.
   - In thứ tự key sau mỗi thao tác cho một chuỗi 6 thao tác với `maxsize=3`.
6. **TTL: dữ liệu cũ thì bỏ.**
   - Mỗi entry lưu `expires_at = now + ttl`. Khi `get`, nếu hết hạn thì xóa và tính là miss.
   - Dùng `FakeClock`. In một timeline: set lúc t=0 với ttl=60, get lúc t=30 (hit), get lúc t=61 (miss vì hết hạn).
   - Bàn về **invalidation**:
     - TTL ngắn hay dài là đánh đổi giữa độ tươi của dữ liệu và hit rate;
     - khi tài liệu nguồn của RAG đổi, hãy đưa **phiên bản** (vd `index_version` hoặc `prompt_version`) vào key thay vì đi xóa từng entry.
   - Callout `[!WARNING]`: không cache câu trả lời chứa dữ liệu riêng của người dùng dưới key dùng chung. Thêm `user_id` vào key, hoặc không cache.
7. **Đo hiệu quả.**
   - Chạy 20 request giả lập (list cố định, có lặp) qua `FakeLLM` có cache.
   - In hit rate, số lần gọi thật, token tiết kiệm được, và chi phí ước tính với và không có cache. Giá giả định ghi trong code, vd `PRICE_PER_1K = 0.002`.
   - Nối sang p8-04: hit rate là một metric cần theo dõi.
8. **Lỗi thường gặp** (VI: `## 8. Lỗi thường gặp`). Mỗi lỗi có code sai, output sai thật, và cách sửa:
   - key thiếu system prompt hoặc model, nên trả câu trả lời của cấu hình khác (cho thấy hai cấu hình khác nhau cùng trúng một key);
   - cache cả khi `temperature > 0`;
   - dùng `str(dict)` làm key: thứ tự field khác nhau thì key khác nhau, nên miss oan. Sửa bằng `sort_keys=True`;
   - cache không giới hạn cũng không có TTL, nên dữ liệu cũ và bộ nhớ cứ tăng (in `len(cache)` sau nhiều request khác nhau).
9. **Recap / Tóm tắt**: 4–6 gạch đầu dòng.

**meta.yaml**
- `phase: p8`, `order: 3`, `kind: lesson`.
- `tags: [production]`, có thể thêm `performance` và `llm`.
- `prerequisites: [p8-01-fastapi]`.
- `duration_min` 14–18.
- `outcomes` khớp syllabus (có thể thêm 1 dòng).
- `review_by: "2027-05-01"`.
- `further_reading`: Python docs `functools.lru_cache`, Python docs `collections.OrderedDict`, và một trang chính thức về prompt caching của một nhà cung cấp LLM (ghi rõ đây là cache phía nhà cung cấp, khác với cache trong app). Mở thử từng link rồi ghi vào report.

## Examples (3)
- `01_faq_cache`: bot FAQ với 12 câu hỏi có lặp và khác nhau về khoảng trắng. Cache theo key đã chuẩn hóa. In từng dòng `HIT/MISS question`, rồi in tổng hit rate.
- `02_embedding_cache`: index 6 tài liệu, sửa 2 tài liệu, index lại. In số text gửi đi mỗi lần và kiểm thứ tự vector khớp với thứ tự tài liệu (`match: True`).
- `03_ttl_lru_timeline`: cache vừa TTL vừa LRU (`maxsize=3`, `ttl=30`) với `FakeClock`. In bảng `t | op | key | result | keys in cache` cho khoảng 8 thao tác, có cả eviction do LRU và hết hạn do TTL.

## Exercises (2)
Test import code người học như module `exercise`. Pyodide chạy được.
- `ex01-lru-cache` (`kind: fill`):
  - Class `LRUCache(maxsize)` dựa trên `OrderedDict`, có `get(key)` (trả `None` khi miss), `set(key, value)`, `hits`, `misses`.
  - 3–4 ô `___` nằm trong thân method: `move_to_end`, `popitem(last=False)`, điều kiện vượt `maxsize`, tăng `hits`.
  - 5 test:
    - get/set cơ bản;
    - bỏ đúng key dùng lâu nhất;
    - `get` làm key "mới" lại nên không bị bỏ;
    - đếm hits và misses;
    - set lại key đã có thì cập nhật giá trị, không tăng kích thước.
  - Starter phải import được (ô `___` nằm trong method, nên chỉ crash khi gọi) và fail mọi test.
- `ex02-llm-cache` (`kind: code`), hai phần:
  - `make_key(model: str, messages: list[dict], **params) -> str`:
    - chuẩn hóa `content` (strip, gộp khoảng trắng);
    - `json.dumps(..., sort_keys=True)` rồi sha256 `hexdigest`;
    - thứ tự `params` khác nhau vẫn ra cùng key; khác `model`, `system` hay `temperature` thì ra key khác.
  - `class TTLCache` với `__init__(self, ttl: float)` và `get(key, now)`, `set(key, value, now)`:
    - `get` trả `None` khi miss hoặc đã hết hạn (`now >= expires_at`), xóa entry hết hạn;
    - có thuộc tính `hits`, `misses` và method `hit_rate()` (trả `0.0` khi chưa có lượt nào).
  - 7–8 test, có `parametrize`:
    - key ổn định khi đảo thứ tự params;
    - key khác nhau khi đổi model, system hay temperature;
    - khoảng trắng thừa ra cùng key;
    - key là hex 64 ký tự;
    - TTL hit trước hạn, miss đúng ở mốc hết hạn;
    - entry hết hạn bị xóa;
    - `hit_rate` đúng;
    - `hit_rate` của cache rỗng là `0.0`.
  - Starter import được, có docstring kèm ví dụ, `# TODO`, `return None`, và fail **mọi** test.
  - `alternatives/01_*`: một cách khác thật sự, ví dụ TTL lưu `(value, expires_at)` trong tuple so với dataclass `Entry`, hoặc key dùng `repr` của tuple đã sort thay cho JSON. File `.md` nói ưu và nhược điểm, gồm việc vì sao JSON với `sort_keys` an toàn hơn.
- Hint 3 tầng đúng CONTENT_GUIDE. Hint 3 chỉ cho **khung**, để trống ít nhất 2–3 dòng logic chính, không chép gần trọn lời giải.
- Lời giải của exercise **không được** là bản sao của code trong lesson. Lesson có thể dạy cùng ý, nhưng code exercise phải khác về API hoặc yêu cầu, vd ex02 có `now` ở tham số và `hit_rate`, còn lesson dùng `FakeClock`. Ghi vào report điểm khác.

## Quiz
- 15–18 câu; mỗi loại `mcq`, `output`, `fill`, `parsons` có ít nhất 2. Khoảng 5 dễ, 7 vừa, 3 khó. 6 flashcard.
- Code là Python thuần chạy được trong Pyodide, không dùng thời gian thật.
- `parsons` phải chỉ có **một** thứ tự đúng, nhờ phụ thuộc giữa các dòng hoặc nhờ output in ra.
- Phải có câu về:
  - hit rate;
  - key thiếu system prompt;
  - `sort_keys`;
  - `temperature > 0`;
  - LRU bỏ phần tử nào;
  - TTL hết hạn ở mốc nào;
  - đổi model embedding;
  - dữ liệu riêng của người dùng;
  - giới hạn của `lru_cache`.
- Luật MCQ:
  - đáp án đúng có `len <= 1.2 ×` trung bình độ dài distractor (cả en và vi);
  - đáp án đúng là phương án dài nhất duy nhất ở tối đa 1/3 số MCQ;
  - không giấu lý do trong đáp án đúng.
  - Chạy script độ dài trong `tasks/m4-p7-test.md`, đổi path sang `quiz.yaml` của bài này, rồi ghi kết quả.

## Tiêu chí hoàn thành (checklist)
1. [ ] Đủ file theo layout CONTENT_GUIDE. `meta.yaml` đúng mục meta, không có `runner`.
2. [ ] Lesson đúng dàn ý và có đủ:
   - picture in text;
   - trace table;
   - mermaid;
   - bảng so sánh;
   - một lời mời Visualize;
   - callout.
3. [ ] Parity EN/VI: code Python chỉ khác comment; fence `text` giống hệt; số dòng mermaid bằng nhau.
4. [ ] Tuân thủ Quy tắc code:
   - không dùng thời gian thật;
   - `-W error` sạch, stderr rỗng;
   - output là output thật;
   - lệnh grep bên dưới rỗng.
5. [ ] Exercise:
   - starter fail **mọi** test (ghi số test pass với starter, phải là 0);
   - solution và alternative pass cả pytest lẫn browser runner trong validate;
   - lời giải khác code trong lesson.
6. [ ] Bản VI tự nhiên, xưng "bạn". Thuật ngữ giữ tiếng Anh, lần đầu kèm giải nghĩa, vd "cache hit (trúng cache)", "eviction (loại bỏ khỏi cache)".
7. [ ] Report ghi:
   - số step của khối Visualize;
   - thời gian `validate.py --path`;
   - kết quả script MCQ;
   - các link đã mở.
8. [ ] Lệnh kiểm tra xanh, chạy đúng như ghi.

## Lệnh kiểm tra
Từ gốc repo `D:\Proj\python-ai-platform`:
```
uv run python tools/validate.py --path curriculum/phase-08-production/p8-03-caching
uv run python tools/validate.py --fast
uv run python -m pytest curriculum/phase-08-production -p no:warnings --color=no
uv run ruff check curriculum/phase-08-production
grep -rnE "time\.time|time\.sleep|monotonic\(\)|datetime\.now|_chat_calls|open\(|subprocess|requests\.|httpx" curriculum/phase-08-production/p8-03-caching --include=*.py --include=*.yaml
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
- build_content in số lesson tăng 1 (51 → 52);
- thay đổi chỉ nằm trong các file được phép, ngoài `tasks/` và `.hallmark/` vốn đã untracked.

Lưu ý: grep `monotonic\(\)` chặn việc gọi đồng hồ thật. Trong bài chỉ được **nhắc** `time.monotonic` trong câu văn hoặc trong comment.

## Ghi chú cho worker
- Đọc trước:
  - `docs/CONTENT_GUIDE.md`;
  - bài `p8-01-fastapi` và `p8-02-docker` (mẫu hình dạng);
  - `curriculum/phase-02-intermediate/p2-07-decorators` (ở đó đã nhắc `functools.cache`);
  - `packages/pyai_llm/pyai_llm.py` và `README.md`: API `chat`, `embed`, `Usage`, `count_tokens`.
- Dùng `uv run python -m pytest`, không dùng `uv run pytest`. Trên Windows có thể không có `grep` trong PATH; dùng Git Bash.
- Mọi lệnh phải tự kết thúc. Không chạy server.
- Kiểm cảnh báo bằng `uv run python -W error <file>`.

## Trạng thái
- Bước hiện tại: xong, đã commit bb6b9c4 (đạt vòng 1; boss kiểm: validate toàn bộ 0 lỗi (52 bài), pytest phase 8 44 passed, ruff sạch, grep rỗng, glossary +77/-0, typecheck + build 76 trang; trong app (Pyodide) ex02 starter 0/10, solution qua hết; chờ user duyệt commit)
- Vòng: 1/3
- Số lần swap: 0
- Fallback: không
- Model: Gemini 4 Hydrogen (High)
