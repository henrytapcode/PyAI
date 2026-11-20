# M4 bước 25b (đợt a): sửa p8-01..p8-03 theo review

## Mục tiêu
Sửa các lỗi reviewer tìm ra trong 3 bài đầu phase 8: p8-01-fastapi, p8-02-docker, p8-03-caching. Danh sách tóm tắt nằm ở `tasks/m4-p8-review.md`, mục "Nửa A". Chỉ sửa nội dung, không thêm bài mới.
- Mọi sửa đổi làm ở cả EN và VI và giữ parity: code block giống nhau trừ `#` comment, text fence giống hệt, mermaid cùng số dòng, callout cùng thứ tự.
- Mọi output ghi trong comment `# ...` phải là output chạy thật. Kiểm bằng `tasks/check_lesson_comments.py` (xem Lệnh kiểm tra).

## File được phép sửa/tạo
- Mọi file trong `curriculum/phase-08-production/p8-01-fastapi/**`, `p8-02-docker/**`, `p8-03-caching/**`.
- `curriculum/glossary.yaml`: chỉ **thêm** term, không sửa hay xóa dòng có sẵn.
- `tasks/m4-p8-review-fixes-a.report.md`

## Không được đụng
- `tools/**`, `apps/**`, `packages/**`, `curriculum/syllabus.yaml`, `curriculum/topics.yaml`, `curriculum/conftest.py`, p8-04, p8-05, các phase khác, `docs/**`, `tasks/check_lesson_comments.py`.

## Quy ước đồng hồ chung (áp dụng từ p8-03, đợt b sẽ áp tiếp cho p8-04/p8-05)
Đồng hồ là một **hàm không tham số trả về số giây** (`float`), giống `time.monotonic`. Trong bài và test dùng:
```python
class FakeClock:
    def __init__(self, start: float = 0.0) -> None:
        self.t = start

    def __call__(self) -> float:
        return self.t

    def advance(self, seconds: float) -> None:
        self.t += seconds
```
Code dùng đồng hồ thì gọi `self.clock()`. Ở production truyền `time.monotonic` (không có ngoặc). Ngay chỗ `FakeClock` xuất hiện lần đầu ở p8-03, giải thích `__call__` trong 2–3 câu: định nghĩa `__call__` thì object gọi được như hàm, `clock()` chạy `clock.__call__()`, nhờ vậy test truyền `FakeClock()` còn production truyền `time.monotonic`, code cache không cần biết là cái nào. Thêm term `__call__` vào glossary nếu chưa có.

## Việc cần làm

### B1. p8-03 "Lỗi thường gặp" 2 (lesson.en/vi quanh l.445-480): output sai
Comment `# good temp=0.8 #2: Here is what I know: ...` không khớp output thật. Hai dòng `good` in ra giống hệt nhau, nên khối code không chứng minh được gì. Viết lại khối để chứng minh bằng **số lần gọi model thật**:
- Đếm số lần `client.chat` thật sự chạy, ví dụ bọc trong hàm `call_model` có tăng biến đếm.
- Bản sai gọi `ask_bad("hello", 0.8)` hai lần: chỉ 1 lần gọi thật, lần sau trả lại bản cache.
- Bản đúng gọi `ask_good("hello", 0.8)` hai lần: 2 lần gọi thật.
- In số đếm và mọi giá trị khác ra comment đúng output thật. Không in nội dung câu trả lời có prefix ngẫu nhiên, trừ khi chạy lại và ghi đúng.
- Đoạn văn trước và sau khối phải nói đúng điều khối chứng minh: bản sai đóng băng mẫu ngẫu nhiên đầu tiên, bản đúng lần nào cũng gọi model.

### M1. p8-02 `.dockerignore` (lesson §5 l.177-216, `examples/03_dockerignore_check.*`, quiz f05 và mọi câu quiz nhắc pattern)
Docker so pattern **từ gốc build context**. Pattern `*.pyc` hoặc `__pycache__/` chỉ khớp ở thư mục gốc, không khớp `rag/__pycache__/x.pyc`. Muốn khớp mọi cấp phải viết `**/__pycache__` và `**/*.pyc`. Khác với `.gitignore`, nơi pattern không có `/` khớp ở mọi cấp.
- Thay hàm mô phỏng ở lesson §5 và examples/03 bằng bản khớp từ gốc. Dùng đúng logic sau (được đổi tên biến):
  ```python
  from fnmatch import fnmatchcase


  def _match_from(pat_parts: list[str], path_parts: list[str]) -> bool:
      # pattern khớp path hoặc một thư mục cha của path
      if len(pat_parts) > len(path_parts):
          return False
      return all(fnmatchcase(s, p) for p, s in zip(pat_parts, path_parts))


  def is_ignored(rel_path: str, patterns: list[str]) -> bool:
      parts = rel_path.split("/")
      for raw in patterns:
          pat = raw.strip().strip("/")
          if not pat or pat.startswith("#"):
              continue
          pat_parts = pat.split("/")
          if pat_parts[0] == "**":
              rest = pat_parts[1:]
              if any(_match_from(rest, parts[i:]) for i in range(len(parts))):
                  return True
          elif _match_from(pat_parts, parts):
              return True
      return False
  ```
  Ghi chú trong bài: mô phỏng này bỏ qua luật `!` (ngoại lệ). Mỗi pattern khớp từng đoạn của đường dẫn, và `*` không vượt qua `/`.
- Lesson §5 phải cho thấy **lỗi thật**: chạy với pattern kiểu cũ (`__pycache__/`, `*.pyc`) thì `rag/__pycache__/retriever.cpython-313.pyc` lọt vào context; với `**/__pycache__`, `**/*.pyc` thì bị loại. Thêm 1 câu so sánh với `.gitignore`.
- Danh sách khuyên dùng ở §5, f05 và examples/03 đổi thành: `.venv/`, `.git/`, `**/__pycache__`, `**/*.pyc`, `.env`, `data/raw/`.
- Bây giờ mới giới thiệu `fnmatchcase` và `split("/")`: thêm 1 câu giải thích `fnmatchcase` (so một chuỗi với pattern có `*`, `?`, phân biệt hoa thường). Bỏ `PurePosixPath` nếu không còn dùng (m3).
- Cập nhật `.out` của example bằng output chạy thật, và `.en.md`/`.vi.md` của nó.

### M2. p8-03 TTL dùng đồng hồ callable
- Lesson §4 (quanh l.277-320) và `examples/03_ttl_lru_timeline.py`: đổi sang quy ước đồng hồ chung ở trên (`self.clock()` thay cho `self.clock.now`, `FakeClock.t`). Câu ở l.277 lúc này mới đúng: "ở production truyền `time.monotonic`".
- Nếu `TTLCache.__init__` có type hint `clock: FakeClock`, đổi thành `clock: Callable[[], float]` (import từ `collections.abc`) hoặc bỏ hint. Chọn cách bỏ nếu `Callable` chưa được dạy.
- VI l.41: bỏ "hay đổi múi giờ". Đồng hồ hệ thống nhảy lùi là do đồng bộ giờ, không phải do múi giờ. Sửa EN tương ứng nếu EN cũng nói vậy.
- Cập nhật mọi quiz/flashcard nhắc `clock.now`.

### M3. p8-01 ex02 `ask-service`: test yếu
Thêm test (parametrize được) để các mutant sau phải fail:
- bỏ `.lower()`: query `"FASTAPI Tests"` cho cùng kết quả với `"fastapi tests"`;
- bỏ `ge=1`: `top_k=0` → 422;
- bỏ `max_length`: `"a" * 201` → 422, còn `"a" * 200` không bị 422 (được 404 hoặc 200 tùy dữ liệu);
- so chuỗi con thay cho so từ: chọn query có một từ là chuỗi con của từ trong doc nhưng không trùng nguyên từ (ví dụ `"test"` với doc chứa `"tests"`). Kết quả phải là không khớp. Chọn từ cụ thể theo `DOCS` thật.
Tự chạy từng mutant trên solution và ghi kết quả vào report.

### M4. p8-02 ex02 linter: test yếu
Thêm case vào parametrize để các mutant sau phải fail:
- `ENV` chỉ kiểm `KEY`: thêm `ENV HF_TOKEN=abc`, `ENV DB_SECRET=x`;
- chỉ kiểm `COPY`: thêm `ADD .env /app/.env`;
- so `:latest` phân biệt hoa thường: thêm `FROM python:LATEST`;
- `copy-before-install` tính mọi `RUN` thay vì `RUN` có `pip install`: thêm Dockerfile có `RUN apt-get update` trước `COPY . .` rồi mới `RUN pip install`, kỳ vọng vẫn có `copy-before-install`;
- `ENV` chỉ xét token đầu: thêm `ENV MODE=prod API_KEY=abc` (cú pháp nhiều cặp), kỳ vọng `secret-in-image`. Nếu solution hiện tại chưa xử lý dạng này, sửa solution và alternatives, ghi rõ luật trong prompt.
Ghi kết quả từng mutant vào report.

### M5. p8-03 ex02 `llm-cache`: test yếu
- Entry hết hạn phải tính là miss: sau một lần `get` của entry hết hạn, assert `misses` tăng đúng 1 và `hit_rate()` đúng (ví dụ `0.5` cho 1 hit 1 miss).
- Key phải đổi khi `max_tokens` đổi, và khi `role` của một message đổi (cùng `content`): test cả hai.
Ghi kết quả mutant vào report.

### M6. Hint leo thang đúng luật, starter không lộ đáp án
Áp dụng cho **mọi** exercise trong 3 bài, cả en và vi:
- Hint 1: ý tưởng, mục trong bài, kết quả cho một input cụ thể. **Không** liệt kê blank hay liệt kê lỗi.
- Hint 2: các bước bằng lời, danh sách đánh số. Không có biểu thức Python hoàn chỉnh.
- Hint 3: skeleton trong python fence, bỏ trống (`...`) phần lõi (1–2 chỗ). Với bài `fill`, hint 3 chỉ gợi ý blank khó nhất. Hint 3 không được chép lại starter.
- Ghép hint 2 + hint 3 không được ra nguyên solution.
Các chỗ cụ thể reviewer nêu:
- p8-01 ex01: hint 1 đang nêu mọi blank; hint 3 chép starter.
- p8-01 ex02: hint 2 + 3 ghép ra lời giải.
- p8-02 ex01 (debug): starter `# TODO`, prompt và hint 1 đang liệt kê đủ 4 lỗi. Starter và prompt chỉ được nói **số lỗi** và **triệu chứng** (test nào fail, ảnh hưởng gì), không nói cách sửa. Hint 1 chỉ về mục trong bài. Hint 2 gợi ý nhóm lỗi. Hint 3 chỉ ra 1 lỗi khó nhất.
- p8-03 ex01 (fill LRU): hint 2 đang nêu blank. Ngoài ra solution gần chép `LRUCache` ở §5, nên **đổi yêu cầu**: thêm bộ đếm `self.evictions` (tăng mỗi lần loại một key) và method `peek(key)` trả giá trị hoặc `None` mà **không** đổi thứ tự và **không** đổi `hits`/`misses`. Đặt blank ở các phần mới (`peek`, `evictions`) và ở phần thứ tự, không khoét blank vào đúng mấy dòng lesson đã in. Thêm 2–3 test cho `peek` và `evictions`. Starter vẫn fail.

### M7. Tiêu đề tiếng Việt trong examples
6 file `examples/*.vi.md` của p8-02 và p8-03 đang để tiêu đề tiếng Anh. Đổi theo mẫu p1-01: `**Ví dụ này cho thấy:**`, `**Từng bước**`, `**Để ý:**`, `**Tự thử:**`. Kiểm luôn 3 file của p8-01 cho đồng bộ.

### Minor
1. m1: sửa mọi số dòng trong `examples/*.en.md`/`.vi.md` của 3 bài cho đúng file `.py` **sau khi sửa**. Đếm bằng script, không đoán.
2. m2 p8-01:
   - `02_validation_report.vi.md`: "bốn payload sai kiểu" → "bốn payload không hợp lệ" (hoặc đúng số thật).
   - Route `/docs/{doc_id}` dễ nhầm với trang tài liệu tự sinh `/docs` của FastAPI. Đổi thành `/documents/{doc_id}` ở lesson l.76, q01, f02 và mọi chỗ khác.
   - ex01: thêm test `GET /notes/1` thành công sau khi tạo note, kiểm đúng kiểu `id` là `int`.
3. m3 p8-02:
   - ex01: `FROM python:slim` hiện vẫn qua test, và `--host=0.0.0.0` lại bị fail. Sửa test/solution để tag phải có số phiên bản (ví dụ `python:3.13-slim`) và chấp nhận cả `--host 0.0.0.0` lẫn `--host=0.0.0.0`.
   - l.116: "every instruction builds a layer" là nói quá. Sửa: chỉ `RUN`, `COPY`, `ADD` tạo layer filesystem; các lệnh khác chỉ ghi metadata.
   - l.229: pin tag không chặn hết thay đổi (tag có thể được đẩy lại). Thêm 1 câu: muốn tuyệt đối thì pin digest `@sha256:...`.
   - l.177: build context được gửi khi bắt đầu build, không phải "trước khi `COPY . .` chạy".
   - `split(None, 1)` chưa được giới thiệu: thêm 1 câu ở chỗ xuất hiện đầu.
4. m4 p8-03:
   - l.95: giải thích sha256 trong 1–2 câu (biến chuỗi bất kỳ thành mã hex dài cố định, cùng input thì cùng mã).
   - l.145: text picture JSON phải đúng output `json.dumps` thật, kể cả dấu cách.
   - l.63: p2-07 dạy `cache_results` tự viết, không dạy `functools.cache`. Sửa câu cho đúng.
   - l.206: key đã có tên model rồi, nên lý do xóa cache khi đổi model là để giải phóng RAM, không phải tránh trả nhầm. Sửa câu.
   - VI: "hàm thuần (pure function)" thì giữ, nhưng gloss đúng lần đầu; "tiêm" → "truyền vào (inject)".
   - `examples/01` phần Try-it: đổi temperature không có tác dụng trong example này, nên đổi sang việc có tác dụng thật.
   - ex02 hint 3 dùng `{**m, ...}` chưa được dạy: bỏ hoặc giải thích.
5. m5 quiz:
   - Viết lại distractor vô lý thành hiểu nhầm có thật: p8-01 q03, p8-02 q01, p8-03 q13, q16.
   - p8-02 q10: bỏ dòng lọc `.env` vô nghĩa.
   - p8-02 q04 (fill): thêm `".env*"` vào danh sách đáp án chấp nhận nếu hợp lệ.
   - Giữ `answer`, id, số phương án, luật độ dài MCQ.

## Tiêu chí hoàn thành (checklist)
- [ ] B1: khối p8-03 chứng minh bằng số lần gọi thật; comment khớp output
- [ ] M1: mô phỏng khớp từ gốc; lesson cho thấy pattern cũ lọt `rag/__pycache__`; examples/03 + `.out` + f05 cập nhật
- [ ] M2: p8-03 dùng đồng hồ callable; có giải thích `__call__`; glossary có `__call__`
- [ ] M3, M4, M5: mọi mutant nêu trên fail trên test mới (ghi bảng mutant → số test fail vào report)
- [ ] M6: hint 3 tầng đúng luật ở 6 exercise; p8-02 ex01 starter/prompt không lộ cách sửa; p8-03 ex01 có `peek` + `evictions`
- [ ] M7: 9 file `examples/*.vi.md` dùng tiêu đề tiếng Việt
- [ ] m1–m5 xong
- [ ] `tasks/check_lesson_comments.py` in `comment mismatches: 0` cho 3 bài
- [ ] Script MCQ: `violations: 0`, longest-unique ≤ 1/3 mỗi file
- [ ] Validate 3 bài 0 lỗi; pytest phase 8 xanh; starter fail mọi test; ruff sạch
- [ ] `git diff --numstat curriculum/glossary.yaml` có 0 dòng xóa
- [ ] Không file nào ngoài phạm vi bị sửa

## Lệnh kiểm tra
Chạy từ gốc repo `D:\Proj\python-ai-platform`:
```bash
P=curriculum/phase-08-production
for d in p8-01-fastapi p8-02-docker p8-03-caching; do uv run python tools/validate.py --path $P/$d; done
uv run python -m pytest $P -q -p no:warnings
EXERCISE_TARGET=starter uv run python -m pytest $P/p8-01-fastapi $P/p8-02-docker $P/p8-03-caching -q -p no:warnings --tb=no
uv run ruff check $P
PYTHONIOENCODING=utf-8 PYTHONPATH=packages/pyai_llm uv run python tasks/check_lesson_comments.py $P/p8-01-fastapi $P/p8-02-docker $P/p8-03-caching
git diff --numstat curriculum/glossary.yaml
```
Lệnh starter: mọi test phải FAILED (hoặc ERROR với bài `fill`/`debug` crash khi import). Mutant: sửa tạm solution trong thư mục tạm ngoài repo (hoặc sửa rồi `git checkout` lại ngay), chạy test, ghi số fail.

Kiểm độ dài MCQ (phải in `violations: 0`; `longest-unique` mỗi file ≤ 1/3 số MCQ):
```bash
uv run python -c "
import yaml,glob
bad=0
for f in sorted(glob.glob('curriculum/phase-08-production/p8-0[1-3]*/quiz.yaml')):
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
- Không chạy server hay dev server. p8-01 dùng `fastapi.testclient.TestClient`, chạy trong pytest bình thường.
- `curriculum/conftest.py` nạp `solution.py` mặc định; biến môi trường `EXERCISE_TARGET=starter` để chạy starter. Không copy starter thành `exercise.py`.
- Test chỉ dùng tập con được phép (assert, pytest.raises/approx/mark.parametrize/fail, fixture trong file, capsys, tmp_path, caplog, monkeypatch).
- Quiz `output`/`fill`/`parsons` bị sửa phải chạy đúng (validate sẽ chạy).
- `check_lesson_comments.py` coi mọi dòng `# ...` ngay sau dòng `print(` là output kỳ vọng. Nếu cần comment giải thích ngay sau `print`, chèn một dòng trống hoặc đặt comment lên trước `print`.

## Trạng thái
- Bước hiện tại: 5 (đạt vòng 1; boss kiểm: validate 3 bài + toàn bộ 54 bài 0 lỗi, pytest phase 8 98 pass, starter 53 fail + 1 lỗi import (fill), ruff sạch, comment mismatches 0, glossary +12/-0, typecheck + build 78 trang; mutant `.lower()` và expired-miss bị bắt; trong app: khối B1 in bad calls 1 / good calls 2, ex01 LRU starter 0/7, solution qua hết; chờ duyệt commit)
- Vòng: 1/3
- Số lần swap: 0
- Fallback: không
- Model: Gemini 4 Hydrogen (High)
