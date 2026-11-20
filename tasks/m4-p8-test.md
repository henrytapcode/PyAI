# M4 bước 26: Phase test 8 (Production)

## Mục tiêu
Viết `curriculum/phase-08-production/phase-test.yaml`, bài kiểm tra cuối phase 8.
- Định dạng giống `curriculum/phase-07-llm/phase-test.yaml`: schema `tools/schema/exam.schema.json`, `kind: phase_test`.
- Boss đã chốt blueprint bên dưới. Worker viết câu hỏi theo đúng blueprint.

## File được phép sửa/tạo
- Chỉ một file mới: `curriculum/phase-08-production/phase-test.yaml`.
- Báo cáo `tasks/m4-p8-test.report.md`.

## Không được đụng
- Mọi file khác, gồm: quiz các bài, `tools/`, `apps/`, glossary, topics.
- Không xóa file, không `git commit`.
- **Không chạy `pnpm --filter web build`.**

## Blueprint (boss chốt)

### Thông tin chung
- `id: p8-phase-test`, `phase: p8`.
- Title EN: "Phase 8 test: Production". Title VI: "Bài kiểm tra Phase 8: Production".
- Description nêu số câu và các chủ đề.
- `duration_min: 25`, `pass_score: 0.7`.
- **16 câu**, id từ `p8-test-q01` tới `p8-test-q16`.
- Nhóm câu theo chủ đề bằng comment, ví dụ `# ---- fastapi`.

### Phân bổ theo chủ đề
| Chủ đề (bài) | Số câu | Ý chính phải kiểm |
|---|---|---|
| FastAPI (p8-01) | 3 | path param có kiểu (`int`) và 422 khi sai kiểu; Pydantic `Field` ràng buộc body (`min_length`, `ge`/`le`) → 422 trước khi vào hàm; `HTTPException(404)`; `TestClient` để test không cần server |
| Docker (p8-02) | 3 | thứ tự layer: `COPY requirements.txt` + `pip install` trước `COPY . .`; `--host 0.0.0.0` trong container; `.dockerignore` khớp từ gốc context (`**/__pycache__`); secret truyền lúc chạy (`--env-file`), không `ENV API_KEY` hay `COPY .env`; pin tag base image |
| Caching (p8-03) | 4 | key gồm mọi input ảnh hưởng output (model, messages kể cả `role`, `temperature`, `max_tokens`), `json.dumps(sort_keys=True)` + `sha256`; chỉ cache khi `temperature == 0`; LRU bằng `OrderedDict` (`move_to_end`, `popitem(last=False)`); TTL với `clock() >= expires_at` là miss; đồng hồ là callable (`FakeClock` có `__call__`, production truyền `time.monotonic`) |
| Monitoring (p8-04) | 3 | percentile nearest-rank (`ceil(p/100 * n)`, chỉ số từ 1); trung bình che phần đuôi chậm; cost = token/1000 × giá in/out; khởi tạo `status = "error"` trước `try` và ghi record trong `finally`; cảnh báo dùng `>` (bằng ngưỡng không báo), `budget-warning` khác `budget-exceeded` |
| Mini-project RAG service (p8-05) | 3 | app factory `create_app(docs, client, clock)` để test không chia sẻ state; cache hit thì không gọi `embed`/`chat` và cost `0.0`; refusal không gọi LLM; `RateLimitError` → 503, ghi `status="error"`, không cache; mọi request được chấp nhận đều vào metric (kể cả hit và lỗi), còn 422 thì không |

### Loại câu và độ khó
- **Loại câu:** 7 `mcq`, 4 `output`, 3 `fill`, 2 `parsons`.
  - Chủ đề có từ 3 câu trở lên thì phải có ít nhất 2 loại khác nhau.
  - Docker không có code Python chạy được, nên câu Docker nghiêng về `mcq`. Được dùng 1 câu `output`/`fill` mô phỏng bằng Python (ví dụ: tìm layer đầu tiên phải build lại, khớp `.dockerignore`).
- **Độ khó:** 3 câu mức 1, 9 câu mức 2, 4 câu mức 3.
  - Câu mức 3 nên là câu tích hợp hoặc bẫy phổ biến, ví dụ:
    - cache cả khi `temperature > 0`;
    - key thiếu `role` hoặc `max_tokens`;
    - `status = "ok"` khởi tạo trước `try`;
    - p95 bị nhầm với max;
    - `COPY . .` đặt trước `pip install`;
    - lỗi bị cache nên retry vẫn nhận lỗi cũ.

### Quy tắc riêng cho mcq
- Rải `answer` qua vị trí 0–3 theo phân bổ 2/2/2/1.
- Distractor là hiểu lầm thật, không dùng "All of the above".
- **Cân độ dài:** `len(đúng) <= 1.2 × trung bình len(distractor)` ở cả en và vi.
- Đáp án đúng không kèm lý do ("because…", "so that…", "vì…", "để…"). Lý do để trong `explanation`.
- Đáp án đúng chỉ được là phương án dài nhất duy nhất ở tối đa 2/7 câu.

### Yêu cầu chung cho mọi câu
- **Câu phải mới hoàn toàn.** Đọc hết 5 file `curriculum/phase-08-production/p8-*/quiz.yaml` trước khi viết. Không chép, và không chỉ sửa sơ một câu có sẵn, dù trùng ý hay trùng code.
- Mỗi câu có:
  - `tags` lấy trong `[production, apis, performance, testing, logging, packaging, rag, llm]`. Kiểm từng tag có trong `curriculum/topics.yaml`.
  - `explanation` song ngữ, nói **vì sao**.
- **parsons:**
  - `lines` theo thứ tự đúng, chạy được, mỗi dòng duy nhất.
  - Chỉ có một thứ tự đúng, nhờ ràng buộc phụ thuộc hoặc kết quả in ra.
  - Gợi ý: dựng cache key (dict → `json.dumps(sort_keys=True)` → `sha256` → in 8 ký tự đầu); hoặc đo một request với `FakeClock` (`start = clock()` → `clock.advance(...)` → tính ms → in).
- Chỉ dùng kiến thức đã dạy ở phase 1–8. Đọc lesson phase 8 (bản đã sửa ở commit `bb5a1ae`, `02e9e3d`) để biết API và quy ước nào đã dạy. Đặc biệt `FakeClock` dùng đúng dạng:
  ```python
  class FakeClock:
      def __init__(self, start: float = 0.0) -> None:
          self.t = start

      def __call__(self) -> float:
          return self.t

      def advance(self, seconds: float) -> None:
          self.t += seconds
  ```

## Quy tắc code (bắt buộc)
- Trong app, câu hỏi bài thi chỉ hiển thị code. Validator chạy code trên máy và so với đáp án.
- **Không gọi mạng, không cần API key, không chạy Docker, không chạy server.**
  - Gọi LLM chỉ qua `pyai_llm` (hành vi của FakeLLM xem `docs/CONTENT_GUIDE.md`, mục "Fake LLM client").
  - FastAPI chỉ dùng qua `fastapi.testclient.TestClient`. Tối đa 2 câu dùng FastAPI; ưu tiên logic thuần trên dict/list cho dễ tính tay.
  - Dockerfile chỉ xuất hiện dưới dạng chuỗi Python hoặc trong text của câu mcq.
- Không dùng thời gian thật (`time.time`, `time.sleep`, `perf_counter`) trong code chạy; dùng `FakeClock`.
- In số thực bằng `round(x, 3)` hoặc f-string có định dạng, tránh dạng `3.6e-05`.
- Code không phát warning nào. Kiểm bằng `uv run python -W error snippet.py`.
- Code ngắn (câu output/fill dưới khoảng 15 dòng) và chạy nhanh.
- Thuật ngữ VI giữ tiếng Anh (cache, key, latency, endpoint, container, image, layer), gloss tiếng Việt khi cần. Dùng "bạn", không dùng "ta".

## Tiêu chí hoàn thành (checklist)
1. [ ] Đúng blueprint: 16 câu, đúng phân bổ chủ đề, loại câu, độ khó và vị trí đáp án mcq. Ghi bảng đếm thực tế vào report.
2. [ ] Không trùng câu với quiz của 5 bài. Report liệt kê mỗi câu kiểm ý nào.
3. [ ] EN/VI đầy đủ, bản VI tự nhiên, code giống hệt nhau giữa hai ngôn ngữ.
4. [ ] Script độ dài mcq bên dưới in `violations: 0` và `longest-unique` ≤ 2. Report ghi bảng độ dài 4 phương án (EN) của từng câu mcq.
5. [ ] Tuân thủ "Quy tắc code": mọi câu output/fill/parsons chạy với `-W error` mà không có stderr.
6. [ ] Lệnh kiểm tra xanh, chạy đúng như ghi.

## Lệnh kiểm tra
Chạy từ gốc repo `D:\Proj\python-ai-platform`:
```
uv run python tools/validate.py --path curriculum/phase-08-production
uv run python tools/build_content.py
grep -nE "api_key=|OPENAI|httpx|requests\.|time\.sleep|time\.time|perf_counter\(\)|độ chính xác" curriculum/phase-08-production/phase-test.yaml
git status --short
```
Kiểm độ dài mcq (phải in `violations: 0` và `longest-unique` ≤ 2):
```
uv run python -c "
import yaml
bad=lu=0
for q in yaml.safe_load(open('curriculum/phase-08-production/phase-test.yaml',encoding='utf-8'))['questions']:
    if q['type']!='mcq': continue
    for lang in ('en','vi'):
        o=q[lang]['options']; L=[len(x) for x in o]; a=q['answer']
        d=[l for i,l in enumerate(L) if i!=a]
        if L[a] > 1.2*sum(d)/len(d): bad+=1; print(q['id'],lang,L)
        if lang=='en' and L[a]==max(L) and L.count(L[a])==1: lu+=1
print('violations:',bad,'longest-unique:',lu)
"
```
Kết quả mong đợi:
- validate 0 lỗi, số exams tăng 1 (10 → 11);
- build_content in số exams tăng 1;
- grep không ra dòng nào;
- chỉ có một file mới là `phase-test.yaml`, ngoài `tasks/` và `.hallmark/` vốn đã untracked từ trước.

## Ghi chú cho worker
- Đọc mẫu `curriculum/phase-07-llm/phase-test.yaml`, 5 file quiz phase 8 và các lesson phase 8.
- Dùng `uv run python -m pytest`, không dùng `uv run pytest`.
- Không chạy server hay dev server.

## Trạng thái
- Bước hiện tại: 5 (đạt vòng 2; boss đọc cả 16 câu; validate phase 8 + toàn bộ 0 lỗi (11 exams, 1057 câu), mcq violations 0 / longest-unique 1, typecheck + build 79 trang (build lần đầu bị Next.js chặn vì cảnh báo bảo mật, chạy lại qua); trong app bài thi hiện 16 câu, 25 phút, mcq có code và parsons hiển thị đúng; chờ duyệt commit)
- Vòng: 2/3
- Số lần swap: 0
- Fallback: không
- Model: Gemini 4 Hydrogen (High)

## Feedback vòng 1
Boss đã đọc cả 16 câu: blueprint đúng (7/4/3/2; 3/9/4; mcq 2/2/2/1), độ dài mcq đạt (violations 0, longest-unique 1), nội dung đúng kỹ thuật. Chỉ còn 1 điểm:
- `p8-test-q02` (code + explanation en/vi): route `/docs/{doc_id}` dễ nhầm với trang tài liệu tự sinh `/docs` của FastAPI; đợt sửa review p8-01 đã đổi mọi chỗ sang `/documents/{doc_id}`. Đổi route và 3 URL trong code thành `/documents/{doc_id}`, `/documents/x`, `/documents/5`, `/documents/20`, rồi cập nhật explanation cho khớp. Output giữ nguyên. Không sửa câu nào khác.
Chạy lại `validate.py --path curriculum/phase-08-production` và ghi kết quả vào cuối report, dưới mục "Vòng 2".
