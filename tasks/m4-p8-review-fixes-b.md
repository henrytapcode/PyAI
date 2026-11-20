# M4 bước 25b (đợt b): sửa p8-04, p8-05 theo review

## Mục tiêu
Sửa các lỗi reviewer tìm ra ở p8-04-monitoring và p8-05-mini-project. Danh sách tóm tắt nằm ở `tasks/m4-p8-review.md`, mục "Nửa B". Chỉ sửa nội dung, không thêm bài mới.
- Mọi sửa đổi làm ở cả EN và VI và giữ parity: code block giống nhau trừ `#` comment, text fence giống hệt, mermaid cùng số dòng, callout cùng thứ tự.
- Mọi output ghi trong comment `# ...` phải là output chạy thật. Kiểm bằng `tasks/check_lesson_comments.py`.
- p8-01..p8-03 vừa được sửa ở đợt a (commit `bb5a1ae`); đọc p8-03 §4 để thấy quy ước đồng hồ và phần giải thích `__call__`.

## File được phép sửa/tạo
- Mọi file trong `curriculum/phase-08-production/p8-04-monitoring/**` và `p8-05-mini-project/**`.
  Được đổi tên thư mục exercise nếu đổi đề, nhưng id giữ dạng `p8-0N-ex0M`.
- `curriculum/glossary.yaml`: chỉ **thêm** term, không sửa hay xóa dòng có sẵn.
- `tasks/m4-p8-review-fixes-b.report.md`

## Không được đụng
- `tools/**`, `apps/**`, `packages/**`, `curriculum/syllabus.yaml`, `curriculum/topics.yaml`, `curriculum/conftest.py`, p8-01..p8-03, các phase khác, `docs/**`, `tasks/check_*.py`.
- Không sửa `pyai_llm`. Cần hành vi khác của FakeLLM thì ghi vào report, không tự sửa.

## Quy ước đồng hồ chung (giống p8-03)
Đồng hồ là **hàm không tham số trả về số giây**. Mọi chỗ trong p8-04 và p8-05 (lesson, examples, exercises, test, quiz, flashcard) dùng đúng class này:
```python
class FakeClock:
    def __init__(self, start: float = 0.0) -> None:
        self.t = start

    def __call__(self) -> float:
        return self.t

    def advance(self, seconds: float) -> None:
        self.t += seconds
```
Code đo thời gian gọi `clock()`. Latency tính bằng `(clock() - start) * 1000` ra ms. Không còn `now_ms` hay `.now`. Lần đầu dùng ở p8-04, nhắc 1 câu rằng đây là `FakeClock` của p8-03: gọi `clock()` được là nhờ `__call__`.

## Việc cần làm

### B1 + M2. p8-05: bài tập không được chép bài học, và dịch vụ phải có nhánh lỗi (blocker)
Bài học p8-05 giữ nguyên cấu trúc (Part 1–6). Hai bài tập **đổi yêu cầu** để người học phải tự ghép thêm phần bài học không có. Đo bằng `tasks/check_overlap.py`: mỗi solution có tỉ lệ dòng trùng lesson **≤ 35%** và chuỗi dòng trùng liên tiếp **≤ 4**. Hiện tại ex01 là 56% và chuỗi 9, ex02 là 46% và chuỗi 10. Được giảm trùng bằng cách đổi yêu cầu, đổi tên biến hoặc tách hàm phụ, nhưng không được làm lời giải tối nghĩa.

**ex01 `create_app(docs, client, min_score=0.2)`**: giữ mọi luật cũ, thêm:
1. `GET /documents/{doc_id}`: trả `{"id": ..., "text": ...}`; không có thì 404 `{"detail": "document not found"}`.
2. Response `/ask` có thêm `"scores"`: list điểm cosine của các hit, làm tròn 3 chữ số, cùng thứ tự với `sources`. Khi từ chối thì `[]`.
3. Nếu model trả về đúng câu từ chối `"I don't know based on the provided context."` thì `sources` và `scores` là `[]`. Đây là m8, p7-09 cũng làm vậy. Test bằng `FakeLLM(script=[...])` hoặc spy trả câu từ chối.
4. M5: các test sau phải có:
   - `min_score=0.0` với `top_k=3` thì đúng 3 sources;
   - assert **toàn bộ** list `sources` theo đúng thứ tự, không chỉ phần tử đầu;
   - spy bắt messages và assert context có cả `"[1] "` và `"[2] "` với đúng text tương ứng.
   Ghi mutant vào report: `scored[:2]` cố định, sắp sources theo alphabet, đánh số `[1]` mọi dòng. Cả ba phải fail.

**ex02 `create_app(docs, client, clock, cache_ttl=300.0, price_in_per_1k=0.0005, price_out_per_1k=0.0015)`**: giữ luật cache và metric cũ, thêm:
1. Nếu `client.chat` hoặc `client.embed` (lúc hỏi) ném `RateLimitError` (`from pyai_llm import RateLimitError`):
   - trả **503** `{"detail": "model busy, retry later"}` bằng `HTTPException`;
   - **không** cache;
   - vẫn ghi record với `status="error"`, `cost=0.0`, latency đo như thường.
   Các request khác ghi `status="ok"`.
2. `/metrics` có thêm `"error_rate"`: số record lỗi chia tổng, `0.0` khi rỗng.
3. `GET /metrics?last=N`: tham số tùy chọn, số nguyên ≥ 1. Có thì mọi chỉ số chỉ tính trên N record cuối. `last=0` thì 422. Không có thì tính trên tất cả.
4. Thứ tự key trong `/metrics` chốt trong prompt: `requests`, `cache_hit_rate`, `error_rate`, `p95_ms`, `total_cost`.
5. Test mới:
   - `FakeLLM(fail_times=1)`: request đầu 503, request lặp lại sau đó 200 với `cached: false`, chứng tỏ lỗi không bị cache; `error_rate == 0.5`.
   - `last=N` đúng và `last=0` cho 422.
   - M3: p95 dùng ≥ 20 request với latency khác nhau, sao cho p95 ≠ max. Mutant `max(...)` phải fail.
   - M4: câu hỏi bị từ chối (crypto) vẫn được đếm, `requests == 1`. Có thêm app dùng giá `0.001`/`0.002`, `total_cost` khớp. Mutant hardcode giá phải fail.
   Ghi mọi mutant vào report.

**Sửa bài học p8-05 cho khớp:**
- §5 (l.461): bỏ `"status": "ok"` gán cứng trong record. Thêm 1–2 câu: dịch vụ ở bài học chưa xử lý lỗi model, bài tập 2 sẽ cho bạn thêm nhánh `RateLimitError` → 503.
- Mistake 4 giữ nguyên ý: ghi cả request lỗi. Nối 1 câu về bài tập 2.
- Bảng "endpoints" ở §1 và Recap: nói rõ `p50_ms`/`alerts` là của bản bài học. Không để mâu thuẫn với dạng `/metrics` của ex02. Có thể ghi: bài tập dùng một bộ chỉ số khác.
- Cập nhật prompt, hint (3 tầng đúng luật ở M7), alternatives (phải pass test mới) và quiz/flashcard nào nhắc tới đề cũ.

### M1. p8-04 `try/finally` ghi lỗi lạ thành `"ok"` (lesson l.382-413, q16, f05)
Khởi tạo `status = "error"` trước `try`. Chỉ gán `"ok"` **sau khi** `chat` thành công. Output in ra phải là output chạy thật, và có một trường hợp lỗi lạ (ví dụ `ValueError`) cho thấy được ghi là `"error"`. Sửa q16, f05 theo.

### M6. p8-04 ex02 `MetricsTracker`: test ranh giới
Parametrize các trường hợp **đúng bằng ngưỡng**, không được kích hoạt cảnh báo:
- `p95_ms == max_p95_ms`;
- `total_cost == budget` (chỉ `budget-warning`, không `budget-exceeded`);
- `error_rate == 0.05`.
Thêm một trường hợp vượt ngưỡng một chút, phải kích hoạt. Mutant `>=` thay `>` ở từng điều kiện phải fail. Thêm test `total_cost` có giá trị chưa làm tròn dài hơn 6 chữ số (m10); mutant bỏ `round` phải fail.

### M7. Hint đúng luật
Áp dụng cho mọi exercise của 2 bài, cả en và vi:
- Hint 1: ý tưởng, mục trong bài (đúng số heading thật), kết quả cho một input cụ thể.
- Hint 2: các bước bằng lời, danh sách đánh số. Không có biểu thức Python hoàn chỉnh.
- Hint 3: skeleton có control flow, bỏ trống `...` phần lõi (1–2 chỗ). Với bài `fill`, chỉ gợi ý blank khó nhất. Chỉ dùng tên có trong starter.
- Ghép hint 2 + hint 3 không được ra nguyên solution.
Chỗ cụ thể:
- p8-04 ex01 (fill): prompt l.11 (en/vi) đang lộ 3/4 blank. Viết lại Rules bằng lời ("dùng nearest-rank: rank là trần của p/100 × n, chỉ số bắt đầu từ 1"). Hint 2 đang lộ blank còn lại. Hint 3 yếu hơn starter. Đổi tên test `test_empty_list_raises_value_error` cho đúng điều nó kiểm, hoặc tách thành 2 test (m10).
- p8-04 ex02: hint 1 không chỉ mục, hint 2 lộ logic, hint 3 gap quá lớn.
- p8-05 ex02: hint 3 dùng `_run_rag` không có trong starter; hint 1 ghi "Parts 3 and 4" lệch số heading.

### M8. p8-05: đừng dùng thứ chưa dạy
- `__call__`: không giải thích lại, chỉ nhắc 1 câu "như `FakeClock` ở p8-03".
- App factory: bảng §1 l.24 ghi "builds on p8-01" là sai, vì p8-01 dùng `app` ở module level. Sửa cột "from lesson" cho Part 1 thành ý "mới trong bài này". §2 đã giải thích app factory; giữ nguyên.
- `zip(strict=True)`: thêm 1 câu ở lần đầu dùng (`strict=True` báo lỗi nếu hai list dài khác nhau), hoặc bỏ `strict=True`.
- `FakeClock`: đổi sang quy ước chung (`self.t`).

### Minor
1. m1: sửa mọi số dòng trong `examples/*.en.md`/`.vi.md` của 2 bài cho đúng file `.py` **sau khi sửa**. Đếm bằng script.
2. m2: p8-04 `examples/03` `.en.md` nhắc `warn_ratio` mà code không có: thêm vào code hoặc bỏ khỏi `.md`. Dữ liệu có request cache hit hoặc lỗi thì cost phải là `0.0`, khớp với §1.
3. m3: VI/EN lệch:
   - p8-04 `02` VI "hầu như đứng yên": dịch đúng ý EN.
   - p8-05 `02` VI thiếu ý "bỏ qua embed".
   - "Bài này minh họa" → "Ví dụ này minh họa".
   - Tiêu đề example VI theo mẫu p1-01 (`**Ví dụ này cho thấy:**`, `**Từng bước**`, `**Để ý:**`, `**Tự thử:**`) ở cả 6 file.
4. m4: p8-04 l.171: lý do token output đắt hơn là "model sinh tuần tự từng token" (không phải "forward pass"). Đổi "3×-4×" thành "thường đắt hơn vài lần".
5. m5: p8-04:
   - l.7 nói "inject" mà §1 dùng biến `clock` toàn cục: sửa lời hoặc truyền `clock` vào hàm.
   - §1 và §2 cùng dùng `req-01` nhưng khác cost: đổi id ở một chỗ.
   - Tránh in `3.6e-05`: dùng `f"{x:.6f}"` hoặc `round`.
6. m6: thêm 1 câu nối ở p8-04 §1 hoặc p8-05 §4: `time.perf_counter` và `time.monotonic` đều không chạy lùi; `perf_counter` mịn hơn nên hợp đo latency, `monotonic` đủ dùng cho TTL. Cả hai đều truyền vào được như `clock`.
7. m7: p8-05 §4 l.240: thêm 1 câu giải thích vì sao key chỉ cần question + `top_k`: model, prompt và `min_score` cố định trong một app; đổi chúng thì phải thêm vào key hoặc dùng `index_version`.
8. m8:
   - `/health` ở §2 trả thêm `"t"`, lệch với spec `{"status","docs"}`: bỏ `"t"`.
   - Bảng l.664-673 có 6 dòng cho 5 test: cho khớp.
   - l.680 "single-line main.py": sửa thành "`main.py` chỉ cần vài dòng nối".
   - `duration_min` của p8-05 đổi thành 75.
   - `sources=[]` khi model từ chối: đã nằm trong ex01.
9. m9: đã nằm trong M7.
10. m11 quiz:
    - Viết lại distractor vô lý thành hiểu nhầm có thật: p8-04 q03, q06, q12, q14; p8-05 q01. Giữ `answer`, id, số phương án, luật độ dài.
    - Fill p8-04 q09: thêm đáp án chấp nhận `rank-1` (nếu chạy đúng).
    - Fill p8-05 q06: thêm `95.0`.
    - p8-05 q14: bỏ dòng `vec[0]` gượng.
11. m12 VI p8-05:
    - l.38 trộn "ta"/"bạn": dùng "bạn".
    - l.680 "một dòng nối dây": sửa lời tự nhiên.

## Tiêu chí hoàn thành (checklist)
- [ ] B1: `check_overlap.py` cho p8-05: mỗi solution ≤ 35%, longest copied run ≤ 4
- [ ] ex01: `/documents/{doc_id}`, `scores`, refusal của model → `sources=[]`; test M5 có, 3 mutant fail
- [ ] ex02: 503 + record lỗi + không cache, `error_rate`, `?last=N`; test M3/M4 có, mutant fail
- [ ] Lesson p8-05 không còn `"status": "ok"` gán cứng; bảng §1, Recap khớp
- [ ] M1: lỗi lạ ghi `"error"`, có output chứng minh; q16/f05 khớp
- [ ] M6: test ranh giới; mutant `>=` và bỏ `round` fail
- [ ] M7: hint 3 tầng đúng luật ở 4 exercise; prompt p8-04 ex01 không lộ blank
- [ ] M8 + quy ước `FakeClock` thống nhất (grep `now_ms\|\.now\b` trong 2 bài ra 0 dòng)
- [ ] m1–m12 xong
- [ ] `check_lesson_comments.py` in `comment mismatches: 0` cho 2 bài (comment giải thích ngay sau `print` thì đưa lên trước `print` hoặc chèn dòng trống)
- [ ] Script MCQ: `violations: 0`, longest-unique ≤ 1/3 mỗi file
- [ ] Validate 2 bài 0 lỗi; pytest phase 8 xanh; starter fail mọi test; ruff sạch
- [ ] `git diff --numstat curriculum/glossary.yaml` có 0 dòng xóa
- [ ] Không file nào ngoài phạm vi bị sửa

## Lệnh kiểm tra
Chạy từ gốc repo `D:\Proj\python-ai-platform`:
```bash
P=curriculum/phase-08-production
for d in p8-04-monitoring p8-05-mini-project; do uv run python tools/validate.py --path $P/$d; done
uv run python -m pytest $P -q -p no:warnings
EXERCISE_TARGET=starter uv run python -m pytest $P/p8-04-monitoring $P/p8-05-mini-project -q -p no:warnings --tb=no
uv run ruff check $P
PYTHONIOENCODING=utf-8 PYTHONPATH=packages/pyai_llm uv run python tasks/check_lesson_comments.py $P/p8-04-monitoring $P/p8-05-mini-project
PYTHONIOENCODING=utf-8 uv run python tasks/check_overlap.py $P/p8-05-mini-project
grep -rn "now_ms\|\.now\b" $P/p8-04-monitoring $P/p8-05-mini-project
git diff --numstat curriculum/glossary.yaml
```
Mutant: sửa tạm solution (rồi `git checkout` lại file đó ngay), chạy pytest thư mục exercise, ghi số test fail vào bảng trong report.

Kiểm độ dài MCQ (phải in `violations: 0`; `longest-unique` mỗi file ≤ 1/3 số MCQ):
```bash
uv run python -c "
import yaml,glob
bad=0
for f in sorted(glob.glob('curriculum/phase-08-production/p8-0[45]*/quiz.yaml')):
    n=lu=0
    for q in yaml.safe_load(open(f,encoding='utf-8'))['questions']:
        if q['type']!='mcq': continue
        n+=1
        for lang in ('en','vi'):
            o=q[lang]['options']; L=[len(x) for x in o]; a=q['answer']
            d=[l for i,l in enumerate(L) if i!=a]
            if L[a] > 1.2*sum(d)/len(d): bad+=1; print(q['id'],lang,L)
            if lang=='en' and L[a]==max(L) and L.count(L[a])==1: lu+=1
    print(f, 'mcq', n, 'longest-unique', lu)
print('violations:',bad)
"
```

## Ghi chú cho worker
- Không chạy server hay dev server. p8-05 test dùng `fastapi.testclient.TestClient`, chạy trong pytest bình thường.
- `curriculum/conftest.py` nạp `solution.py` mặc định; `EXERCISE_TARGET=starter` để chạy starter.
- Test chỉ dùng tập con được phép (assert, pytest.raises/approx/mark.parametrize/fail, fixture trong file, capsys, tmp_path, caplog, monkeypatch).
- `FakeLLM(fail_times=N)` ném `RateLimitError` ở N lần gọi đầu, tính chung `chat` và `embed`. Nhớ là `create_app` gọi `embed` một lần lúc tạo app, nên lần ném đầu có thể rơi vào đó. Dựng test sao cho lỗi rơi đúng vào `/ask`, ví dụ dùng spy/wrapper tự ném ở lần gọi `chat` đầu.
- Quiz `output`/`fill`/`parsons` bị sửa phải chạy đúng (validate sẽ chạy).

## Trạng thái
- Bước hiện tại: 5 (đạt vòng 2; boss kiểm: validate 2 bài + toàn bộ 54 bài 0 lỗi, pytest phase 8 115 pass, starter 56 fail, ruff sạch, comment mismatches 0, overlap ex01 28% / ex02 20% không chuỗi ≥5, glossary không đổi, typecheck + build; mutant p95→max và >= bị bắt; trong app qua local runner ex02 starter 0/14, solution qua hết; chờ duyệt commit)
- Vòng: 2/3
- Số lần swap: 0
- Fallback: không
- Model: Gemini 4 Hydrogen (High)

## Feedback vòng 1
Boss đã kiểm: gate xanh; overlap ex01 28%, ex02 20%; mutant p95→`max` và `>=` bị bắt; trong app qua local runner, starter ex02 qua 0/14 test, solution qua hết. Chỉ còn 1 điểm:
- p8-05 ex02: `Query(default=None, ge=1)` chưa được dạy ở bài nào (grep `Query(` trong mọi lesson ra 0), nhưng solution, alternative, starter và hint đều dùng. Người học đọc prompt sẽ không biết làm sao để `last=0` trả 422. Sửa `prompt.en.md` và `prompt.vi.md`: trong Rules, thêm 1–2 câu giới thiệu `Query` của `fastapi`. Nó dùng cho tham số truy vấn giống `Field` dùng cho body, ví dụ `last: int | None = Query(default=None, ge=1)`, và FastAPI tự trả 422 khi vi phạm. Không sửa file nào khác.
