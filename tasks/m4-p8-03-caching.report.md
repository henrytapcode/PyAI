# Báo cáo M4 bước 24: bài `p8-03-caching` (Caching)

## 1. Đã làm gì

- **Meta (`meta.yaml`):**
  - Tạo `id: p8-03-caching`, `phase: p8`, `order: 3`, `kind: lesson`, `level: beginner`, `tags: [production, performance, llm]`, `prerequisites: [p8-01-fastapi]`, `duration_min: 16`, `review_by: "2027-05-01"`. Không có trường `runner` (chạy hoàn toàn trong Pyodide).
  - `outcomes` khớp `curriculum/syllabus.yaml` và thêm 1 mục về ước lượng token và chi phí API tiết kiệm được.
  - `further_reading` gồm 3 link chính thức đã mở kiểm tra HTTP `200 OK` bằng `urllib.request`:
    - `https://docs.python.org/3/library/functools.html#functools.lru_cache` (`200`)
    - `https://docs.python.org/3/library/collections.html#collections.OrderedDict` (`200`)
    - `https://developers.openai.com/api/docs/guides/prompt-caching` (`200`, ghi rõ là prompt caching phía nhà cung cấp, khác với cache trong app)

- **Bài học (`lesson.en.md` và `lesson.vi.md`):**
  - Mở đầu không heading về bot hỗ trợ khách hàng nhận `"How do I reset my password?"` hàng trăm lần mỗi ngày.
  - 8 mục nội dung + `Recap` / `Tóm tắt`:
    1. **Cache là gì: hit, miss và hit rate:** ví von mảnh giấy ghi chú cạnh bàn; khối Python mô phỏng 6 lần gọi với 3 câu hỏi lặp, in `hits`, `misses`, `hit_rate`, `real_calls`, `cache_size`; trace table `| call | question | hit? | real calls | cache size |`; lời mời bấm **Visualize** theo dõi `cache` và `hits`.
       - Kết quả `tools/pyrunner/tracer.py` trên khối Visualize: `len(steps) = 48`, `truncated = False`, `error = None`.
    2. **`functools.lru_cache`: cache có sẵn cho hàm thuần:** nối với `p2-07-decorators`, dùng `@lru_cache(maxsize=3)`, in `cache_info()`, nêu 3 giới hạn (đối số phải hashable, không có TTL, không dùng cho hàm có side effect hoặc đổi theo thời gian) và callout `[!NOTE]`.
    3. **Cache key cho prompt:** giải thích `model`, `system` + `messages`, `temperature` (chỉ cache khi `0`), `max_tokens`; hàm `make_prompt_key` dùng `normalize_text` (strip + gộp khoảng trắng, kèm cảnh báo không tự ý viết thường hay bỏ dấu câu), `json.dumps(..., sort_keys=True)` và `hashlib.sha256` (in 12 ký tự đầu); bảng so sánh `| include in key | why |` (`| đưa vào key | vì sao |`); picture in text trong fence `text` giống hệt nhau giữa EN và VI.
    4. **Cache embedding:** cache theo `(model, text)`, chỉ gọi `FakeLLM.embed` một batch cho các text chưa có trong cache rồi ghép lại đúng thứ tự ban đầu; in số text gửi đi khi re-index kho 5 tài liệu có 1 tài liệu sửa (`5` rồi `1`); nhắc lại từ `p7-03-embeddings` rằng đổi model embedding phải bỏ toàn bộ cache cũ.
    5. **LRU: giới hạn bộ nhớ:** lớp `LRUCache` dùng `collections.OrderedDict` (`move_to_end`, `popitem(last=False)`), biểu đồ Mermaid `flowchart TD` (7 node, 8 dòng bằng nhau giữa EN và VI), in thứ tự key sau 6 thao tác với `maxsize=3`.
    6. **TTL: dữ liệu cũ thì bỏ:** lớp `FakeClock` và `TTLCache` kiểm tra `now >= expires_at` và xóa entry hết hạn; in timeline tại `t=0`, `t=30` (hit), `t=61` (miss); nêu rõ ở production truyền `time.monotonic` và dùng monotonic chứ không dùng giờ hệ thống vì giờ hệ thống có thể bị chỉnh lùi; bàn về invalidation (đánh đổi TTL ngắn/dài, gắn `index_version`/`prompt_version` vào key); callout `[!WARNING]` không cache dữ liệu riêng của người dùng dưới key dùng chung.
    7. **Đo hiệu quả cache:** chạy 20 request giả lập qua `FakeLLM` có cache với `PRICE_PER_1K = 0.002` và bộ đếm lời gọi riêng; in `hit_rate: 0.75`, `real_calls: 5`, `tokens_saved: 415`, `cost_without: 0.0011`, `cost_with: 0.00027`; nối sang `p8-04-monitoring`.
    8. **Lỗi thường gặp:** 4 lỗi kèm code sai, output sai thật và cách sửa (thiếu `system`/model trong key khiến formal nhận câu trả lời pirate `"Arr! ..."`, cache khi `temperature > 0`, dùng `str(dict)` thay cho `sort_keys=True`, và dict không giới hạn kích thước/TTL).
    9. **Tóm tắt / Recap:** 5 gạch đầu dòng.

- **Examples (3):**
  - `01_faq_cache`: 12 câu hỏi FAQ có lặp và khác khoảng trắng, chuẩn hóa trước khi tạo key SHA-256, in từng dòng `HIT`/`MISS` và `total=12 hits=6 misses=6 hit_rate=0.50`.
  - `02_embedding_cache`: lập chỉ mục 6 tài liệu (`sent 6/6`), sửa 2 tài liệu rồi chạy lại (`sent 2/6`), kiểm tra khớp thứ tự với `client.embed(docs_v2)` (`match: True`).
  - `03_ttl_lru_timeline`: `TTLLRUCache(maxsize=3, ttl=30.0)` với `FakeClock`, in bảng `t | op | key | result | keys in cache` qua 9 thao tác có cả eviction do LRU (`k2`) và hết hạn do TTL (`k1`).

- **Exercises (2) — khác API/cài đặt với code trong lesson:**
  - `ex01-lru-cache` (`kind: fill`): `LRUCache(maxsize)` dùng `OrderedDict`, có `get`, `set`, `hits`, `misses`, `__len__`; 4 ô `___` nằm trong thân method (`move_to_end`, `1`, `self.maxsize`, `popitem`); 5 test. Starter import được và fail **5/5** test (`0 passed`), solution pass **5/5**.
    - Khác biệt với lesson: `ex01` dùng method `set`, đếm `hits`/`misses` và hỗ trợ `len(cache)`, trong khi lesson §5 dùng `put` và không có bộ đếm.
  - `ex02-llm-cache` (`kind: code`): `make_key(model, messages, **params)` và `TTLCache(ttl)` với `set(key, value, now)`, `get(key, now)`, `hits`, `misses`, `hit_rate()`, `__len__()`. 8 hàm test (10 test item qua `parametrize`). Starter import được, có docstring + ví dụ + `# TODO` + `return None`, fail **10/10** test (`0 passed`); `solution.py` (dùng dataclass `_Entry`) và `alternatives/01_tuple_entries_and_repr_key.py` (dùng tuple `(value, expires_at)` và sorted `repr` thay cho JSON) đều pass **10/10** trên cả pytest lẫn browser runner.
    - Khác biệt với lesson: lesson §3 dùng `make_prompt_key` với tham số tường minh `(model, messages, temperature=0.0, max_tokens=128)`, còn `ex02` nhận `**params` và bảo toàn các field phụ của message; lesson §6 tiêm đối tượng `FakeClock` ở `__init__`, còn `ex02` truyền `now: float` vào từng lần gọi `get`/`set` và thêm `hits`, `misses`, `hit_rate()`.

- **Quiz (`quiz.yaml`):**
  - 16 câu hỏi (`7 mcq`, `3 output`, `3 fill`, `3 parsons`; độ khó: 5 mức 1, 8 mức 2, 3 mức 3) + 6 flashcards (`p8-03-f01` .. `p8-03-f06`).
  - Kiểm tra đủ các chủ đề: hit rate, thiếu system prompt trong key, `sort_keys=True`, `temperature > 0`, LRU eviction, ranh giới TTL (`now >= expires_at`), đổi model embedding, dữ liệu riêng người dùng, giới hạn `functools.lru_cache`.

- **Glossary (`curriculum/glossary.yaml`):**
  - Bỏ qua `cache` và `hit rate` vì đã có sẵn trong file.
  - Chỉ thêm 7 thuật ngữ mới vào cuối file: `cache hit`, `cache miss`, `TTL`, `LRU`, `eviction`, `cache key`, `invalidation`.

## 2. File đã sửa / tạo

- Tạo mới thư mục `curriculum/phase-08-production/p8-03-caching/`:
  - `meta.yaml`
  - `lesson.en.md`, `lesson.vi.md`
  - `quiz.yaml`
  - `examples/01_faq_cache.{py,out,en.md,vi.md}`
  - `examples/02_embedding_cache.{py,out,en.md,vi.md}`
  - `examples/03_ttl_lru_timeline.{py,out,en.md,vi.md}`
  - `exercises/ex01-lru-cache/{exercise.yaml,prompt.en.md,prompt.vi.md,starter.py,solution.py,test_exercise.py}`
  - `exercises/ex02-llm-cache/{exercise.yaml,prompt.en.md,prompt.vi.md,starter.py,solution.py,test_exercise.py}`
  - `exercises/ex02-llm-cache/alternatives/01_tuple_entries_and_repr_key.{py,en.md,vi.md}`
- Sửa (chỉ thêm dòng): `curriculum/glossary.yaml`
- Tạo mới báo cáo: `tasks/m4-p8-03-caching.report.md`

## 3. Kết quả lệnh kiểm tra

- `uv run python tools/validate.py --path curriculum/phase-08-production/p8-03-caching`:
  - `OK: 0 error(s), 0 warning(s). Checked 1 lessons, 7 markdown pairs, 3 examples, 2 exercises, 1 alternatives, 16 questions.` (thời gian đo bằng `Measure-Command`: `3.53s`, exit `0`).
- `uv run python tools/validate.py --fast`:
  - `OK: 0 error(s), 0 warning(s). Checked 52 lessons, 394 markdown pairs, 154 examples, 104 exercises, 84 alternatives, 1009 questions, 10 exams, 1 portfolio, 1 glossary, 1 interview.` (exit `0`).
- `uv run python -m pytest curriculum/phase-08-production -p no:warnings --color=no`:
  - `44 passed in 0.39s` (exit `0`).
- Kiểm tra starter (`EXERCISE_TARGET=starter` trên `p8-03-caching/exercises`):
  - `15 failed` (`0 passed`: `ex01` fail `5/5`, `ex02` fail `10/10`).
- Kiểm tra `ex02` alternative (`01_tuple_entries_and_repr_key.py`):
  - `10 passed` trên pytest (và đã pass qua `runner.py` trong `validate.py`).
- `uv run ruff check curriculum/phase-08-production`:
  - `All checks passed!` (exit `0`).
- Kiểm tra regex `time\.time|time\.sleep|monotonic\(\)|datetime\.now|_chat_calls|open\(|subprocess|requests\.|httpx` trên `curriculum/phase-08-production/p8-03-caching` (`.py`, `.yaml`):
  - `GREP HITS: 0`.
- `git diff --numstat curriculum/glossary.yaml`:
  - `77  0  curriculum/glossary.yaml` (77 dòng thêm, 0 dòng xóa).
- `uv run python tools/build_content.py`:
  - `Built 52 lessons, 10 exams, 312 flashcards, 834 questions -> apps\web\src\generated` (tăng từ 51 lên 52 lessons).
- Kiểm tra `-W error` (CPython, stderr rỗng):
  - `lesson.en.md` (`11/11` khối Python), `lesson.vi.md` (`11/11` khối Python), `examples/` (`3/3` file khớp `.out`), `quiz.yaml` (`9/9` câu code `output`/`fill`/`parsons`), và import `5/5` file `.py` trong `exercises/` đều exit `0`, stderr rỗng.
- Script kiểm tra độ dài MCQ trên `curriculum/phase-08-production/p8-03-caching/quiz.yaml`:
  - `total_mcq: 7`, `violations: 0`, `longest-unique: 2` (`<= 7/3`).
  - Chi tiết từng câu MCQ:
    - `p8-03-q01` (ans=1): EN `[54, 50, 53, 53]` (`ratio=0.94`), VI `[52, 49, 51, 48]` (`ratio=0.97`)
    - `p8-03-q03` (ans=0): EN `[58, 63, 65, 66]` (`ratio=0.90`), VI `[57, 55, 60, 60]` (`ratio=0.98`)
    - `p8-03-q06` (ans=2): EN `[53, 57, 55, 55]` (`ratio=1.00`), VI `[52, 55, 56, 50]` (`ratio=1.07`)
    - `p8-03-q08` (ans=3): EN `[58, 63, 57, 64]` (`ratio=1.08`), VI `[57, 54, 57, 59]` (`ratio=1.05`)
    - `p8-03-q10` (ans=0): EN `[50, 56, 57, 51]` (`ratio=0.91`), VI `[44, 58, 51, 56]` (`ratio=0.80`)
    - `p8-03-q13` (ans=1): EN `[56, 49, 54, 53]` (`ratio=0.90`), VI `[59, 55, 60, 53]` (`ratio=0.96`)
    - `p8-03-q16` (ans=2): EN `[56, 56, 58, 57]` (`ratio=1.03`), VI `[57, 54, 61, 53]` (`ratio=1.12`)
- `git status --short`:
  - Chỉ có `M curriculum/glossary.yaml` và `?? curriculum/phase-08-production/p8-03-caching/` (ngoài `?? tasks/` và `?? .hallmark/`).

## 4. Điều còn chưa chắc / chưa kiểm trên máy

- **Chạy thực tế trên Pyodide trong trình duyệt:** toàn bộ code Python chỉ dùng thư viện chuẩn (`collections.OrderedDict`, `hashlib`, `json`, `functools`, `dataclasses`) cùng `pyai_llm` và đã qua `tools/pyrunner/runner.py` + `tools/pyrunner/tracer.py` trên CPython; chưa bật app web để chạy trực tiếp trong Pyodide wasm32 trên trình duyệt.
- **Web build / dev server:** chưa chạy `pnpm --filter web build` và không chạy server theo quy tắc của spec.
