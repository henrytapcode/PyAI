# M4 bước 13: bài p7-03 Embeddings

## Mục tiêu
Viết bài `p7-03-embeddings` trong `curriculum/phase-07-llm/`, đúng `docs/CONTENT_GUIDE.md` và song ngữ EN/VI.
- Bài **chạy trong Pyodide** (không có `runner: local`). Embedding lấy từ `FakeLLM().embed(...)`. Tính toán dùng **NumPy**. Không mạng, không key.
- Người học đã xong:
  - p7-01, p7-02: `FakeLLM`, messages, JSON;
  - p5-01 math bridge: dot product, độ dài vector, có nhắc trước cosine similarity;
  - NumPy ở phase 4.
- Ý chính:
  - Embedding biến văn bản thành vector số sao cho câu có nghĩa gần nhau thì vector gần nhau.
  - Cosine similarity đo "gần", và vì vector đã chuẩn hóa nên cosine chỉ còn là dot product.
  - Có embedding thì xếp hạng được tài liệu theo câu hỏi. Đó là chữ "R" trong RAG (p7-05). Bài sau, p7-04, sẽ lưu các vector này vào một vector DB.
- Bài mẫu: `curriculum/phase-07-llm/p7-02-structured-output/` (giọng văn và hình dạng).

## Hành vi fake embedding (boss đã đọc code, worker phải đọc lại `_embed_one` trong `packages/pyai_llm/pyai_llm.py`)
- Embedding là **bag-of-words có bảng đồng nghĩa**:
  - chữ thường, bỏ `s` cuối với từ dài hơn 3 ký tự;
  - đổi từ đồng nghĩa về dạng gốc bằng `_SYNONYMS` (car/automobile/vehicle, refund/reimbursement/"money back", laptop/notebook/computer, cat/kitten/feline, doctor/physician, cheap/inexpensive/affordable, fast/quick/rapid, error/bug/failure, happy/glad/joyful, big/large/huge);
  - băm crc32 vào `embed_dim` ô, rồi chuẩn hóa L2, làm tròn 6 chữ số.
- Hệ quả bài phải nói **thật thà**:
  - Fake embedding chỉ "hiểu" từ trùng và các cặp đồng nghĩa có trong bảng. Embedding thật (một mô hình neural, nối với p6-03) học nghĩa từ dữ liệu khổng lồ nên hiểu rộng hơn nhiều. Ý tưởng hình học và code thì giống hệt.
  - Một callout `[!NOTE]` nói điều này.
- **Va chạm băm (hash collision):** với `embed_dim=64`, hai từ khác nhau có thể rơi vào cùng ô và gây điểm giả. Boss thử 4 câu hỏi về mật khẩu với `embed_dim=64` thì câu "Shipping takes three days" đứng trên "I forgot my login credentials".
  - Chọn câu và `embed_dim` sao cho xếp hạng trong bài **hợp lý với người đọc**. Gợi ý `FakeLLM(embed_dim=256)` cho các ví dụ xếp hạng, và ghi trong bài vì sao dùng 256.
  - Không cần giải thích sâu về băm: một câu là đủ ("model thật dùng vài trăm tới vài nghìn chiều").
  - Mọi số in ra phải là output **thật**.
- Ví dụ "keyword search bỏ sót, embedding bắt được" phải dựa vào bảng đồng nghĩa. Vd query "affordable automobile" khớp "cheap car" dù không chung từ nào.

## File được phép sửa/tạo
- Thư mục mới `curriculum/phase-07-llm/p7-03-embeddings/` và mọi file bên trong.
- `curriculum/glossary.yaml`: chỉ **thêm** thuật ngữ chưa có (embedding, vector, cosine similarity, semantic search, top-k, normalize). Thuật ngữ đã có thì bỏ qua.
- `tasks/m4-p7-03-embeddings.report.md`

## Không được đụng
- `packages/`, `apps/`, `tools/`, `curriculum/syllabus.yaml`, `curriculum/topics.yaml`, các bài p7-01 và p7-02, các phase khác, `exams/`.
- Không xóa file, không `git commit`, **không chạy `pnpm --filter web build`**, không chạy server ở foreground.
- Không sửa `pyai_llm`. Hành vi nào cản bài học thì ghi vào report.

## Quy tắc code (bắt buộc)
- Áp dụng mọi quy tắc phase 7 (không `input()`, mạng, `time.sleep`, ghi file; sạch với `-W error`; tất định) và **mọi quy tắc Data & ML phase 4+** trong CONTENT_GUIDE:
  - in số bằng `round(float(x), 3)` hoặc `.tolist()`, không in NumPy scalar thô;
  - không in dtype số nguyên, dùng `"int64"` rõ ràng nếu cần;
  - vector dài 64/256 chiều **không in nguyên**, chỉ in `len`, vài phần tử đầu (đã làm tròn) hoặc `shape`.
- Thứ tự xếp hạng phải tất định khi điểm bằng nhau: dùng `sorted(..., key=lambda p: (-score, index))` hoặc `np.argsort(-scores, kind="stable")`, và nói rõ trong bài.
- Khối mời **Visualize** phải dưới 600 step. Embedding 256 chiều làm tracer chậm, nên khối Visualize nên tính cosine **bằng tay trên vector nhỏ 3 chiều** (list Python). Kiểm bằng `tools/pyrunner/tracer.py` và ghi số step vào report.

## Nội dung bài (boss chốt dàn ý, worker viết)
Opening (không heading): khách hỏi "I can't sign in" nhưng tài liệu viết "reset your password". Tìm theo từ khóa sẽ trượt. Embedding giúp tìm theo **nghĩa**, và đó là nền của semantic search, gợi ý và RAG.

1. **Văn bản thành vector.**
   - `client.embed(["a cheap car", ...])` trả list các vector. In số vector, số chiều, 5 phần tử đầu (làm tròn).
   - **Picture in text** (fence `text`, giống hệt EN/VI): 3 câu thành 3 mũi tên trong không gian. Vẽ đơn giản bằng ký tự, với 2 câu cùng nghĩa gần nhau và 1 câu khác nghĩa ở xa.
   - `embed` nhận **list** chuỗi. Truyền một chuỗi đơn sẽ lỗi `TypeError`, để dành cho phần lỗi thường gặp.
2. **Cosine similarity: đo độ gần.**
   - Công thức `a·b / (|a||b|)` với NumPy. Nhắc lại p5-01.
   - Khối nhỏ tính bằng tay trên vector 3 chiều để mời **Visualize**.
   - Vector đã chuẩn hóa thì `|a| = |b| = 1` nên cosine chính là dot product. Chứng minh bằng số: `np.linalg.norm(v)` ra `1.0`, `cosine` của `pyai_llm` bằng `a @ b`.
   - **Bảng** `| cosine | meaning |` cho khoảng 1, 0, âm. Lưu ý fake embedding không có số âm nên cosine nằm trong [0, 1]; embedding thật có thể âm.
3. **Keyword search và semantic search.**
   - Hàm keyword: đếm số từ chung. So với embedding trên cùng 4–5 tài liệu và một query đồng nghĩa: keyword trả 0 điểm, embedding tìm đúng.
   - **Bảng so sánh** `| approach | finds | misses |`.
4. **Xếp hạng tài liệu: top-k.**
   - Ma trận tài liệu `D` (shape `(n, dim)`) và query `q`, rồi `scores = D @ q` (một dòng thay cho vòng lặp), `np.argsort(-scores, kind="stable")[:k]`.
   - **Trace table** `| rank | doc | score |`.
   - **Mermaid** `flowchart LR` (≤ 7 node): docs → embed → matrix; query → embed → `D @ q` → top-k.
   - Nhấn mạnh: embed tài liệu **một lần** rồi tái sử dụng, chỉ embed query mỗi lần hỏi. Nối sang p7-04 (lưu vector).
5. **Ngưỡng và "không tìm thấy".**
   - Điểm cao nhất thấp (vd < 0.3) nghĩa là không có tài liệu liên quan. Trả "không biết" tốt hơn trả bừa. Đây là chuẩn bị cho RAG.
   - Chọn ngưỡng bằng vài query mẫu có nhãn, không chọn theo cảm tính. Một câu thôi, eval sâu ở p7-08.
6. **Chi phí và batch.** `embed` tính token như `chat`, và có thể dùng `count_tokens` để ước lượng. Gọi một lần cho cả list thay vì từng câu một. Callout `[!TIP]`: lưu embedding lại, không tính lại mỗi lần chạy.
7. **Lỗi thường gặp** (VI: `## 7. Lỗi thường gặp`), chạy thật để lấy đúng thông báo:
   - `embed("one string")` → `TypeError` (thông báo thật).
   - So sánh vector có số chiều khác nhau (embed bằng hai client khác `embed_dim`) → lỗi shape của NumPy (thông báo thật, rút gọn nếu quá dài).
   - Dùng khoảng cách Euclid hoặc dot product trên vector **chưa** chuẩn hóa, khiến văn bản dài được điểm cao hơn. Cho thấy bằng một vector tự tạo.
   - `argsort` tăng dần nên lấy nhầm tài liệu kém nhất. Sửa bằng `-scores`.
8. **Recap / Tóm tắt**: 4–6 gạch đầu dòng.

Thời lượng 12–15 phút.

`meta.yaml`:
- `phase: p7`, `order: 3`, `tags`: dùng tag có sẵn trong `curriculum/topics.yaml` (vd `llm`, và `numpy` nếu có). Không thêm tag mới.
- `prerequisites: [p7-01-llm-api, p5-01-math-bridge]`
- `outcomes` khớp syllabus
- `review_by: "2027-05-01"`, không có `runner`
- `further_reading`: 1–2 link ổn định, trung lập (vd bài giải thích embeddings trên một trang tài liệu lớn, docs `numpy.argsort`). Mở thử và ghi vào report.

## Examples (3)
- `01_faq_search`: 6 câu FAQ của shop. Embed một lần thành ma trận, trả lời 3 câu hỏi khách bằng top-1 kèm điểm. Một câu không liên quan thì in "no good match" theo ngưỡng.
- `02_keyword_vs_semantic`: bảng so sánh điểm keyword và cosine cho 3 query × 4 tài liệu. In gọn, mỗi dòng dưới 60 ký tự.
- `03_dedupe_tickets`: tìm cặp ticket gần trùng (cosine ≥ ngưỡng) trong 5 ticket, dùng `D @ D.T` và chỉ lấy tam giác trên. In các cặp.

## Exercises (2)
- `ex01-cosine` (`kind: fill`): `cosine_sim(a: list[float], b: list[float]) -> float`, dùng NumPy và làm tròn 3 chữ số.
  - Vector toàn 0 thì trả `0.0`. Độ dài khác nhau thì raise `ValueError`.
  - Các `___` trong thân hàm.
  - 5–6 test: cùng hướng → 1.0; vuông góc → 0.0; ngược hướng → -1.0; scale không đổi kết quả; vector 0; độ dài khác → `pytest.raises(ValueError)`.
- `ex02-top-k` (`kind: code`): `top_k(query: str, docs: list[str], client, k: int = 2, min_score: float = 0.0) -> list[tuple[int, float]]`.
  - Trả list `(index, score)` theo điểm giảm dần, điểm bằng nhau thì index nhỏ trước. Bỏ tài liệu có điểm `< min_score`. Điểm làm tròn 3 chữ số, kiểu `float` Python (không phải NumPy).
  - Embed tài liệu **trong một lần gọi**.
  - `k` lớn hơn số tài liệu thì trả tất cả. `docs` rỗng thì trả `[]` và **không gọi** `embed`.
  - 7–8 test:
    - query đồng nghĩa đứng đầu;
    - đúng `k` phần tử;
    - thứ tự giảm dần;
    - tie-break theo index;
    - `min_score` lọc;
    - `docs` rỗng;
    - điểm là `float` Python;
    - spy client kiểm `embed` được gọi đúng 1 lần cho docs (cộng 1 lần cho query, hoặc gộp chung; nói rõ trong prompt cách nào được chấp nhận).
  - Starter import được, fail **mọi** test.
  - `alternatives/01_sorted_loop.py`: vòng lặp + `sorted` thay cho ma trận NumPy, kèm `.md` so sánh.
- Hint 3 tầng đúng luật:
  - hint 2 chỉ là các bước bằng lời, không có biểu thức Python hoàn chỉnh;
  - hint 3 là skeleton, mỗi hàm chừa đúng một `...` ở dòng cốt lõi;
  - ghép hint 2 và hint 3 không ra nguyên solution.

## Quiz
- 15–18 câu, mỗi loại `mcq`, `output`, `fill`, `parsons` ít nhất 2. Khoảng 5 dễ, 7 vừa, 3 khó. 6 flashcard.
- **mcq cân độ dài:** `len(đúng) <= 1.2 × trung bình len(distractor)` ở cả en và vi. Đáp án đúng không kèm lý do. Đáp án đúng là phương án dài nhất duy nhất ở tối đa 1/3 số câu mcq.
- Câu `output` in số đã làm tròn, không in vector dài.
- Phải có câu về:
  - embedding là gì;
  - cosine với vector đã chuẩn hóa bằng dot product;
  - argsort tăng dần;
  - keyword và semantic;
  - ngưỡng "không tìm thấy";
  - embed tài liệu một lần;
  - số chiều phải khớp;
  - fake embedding khác embedding thật ở điểm nào.

## Tiêu chí hoàn thành (checklist)
1. [ ] Đủ file theo layout CONTENT_GUIDE. `meta.yaml` đúng như trên, tag có trong topics.yaml.
2. [ ] Lesson đúng dàn ý, đủ: picture in text, mermaid, trace table, bảng so sánh, một lời mời Visualize, callout `[!NOTE]` về fake vs thật.
3. [ ] Code giữa EN và VI giống hệt, chỉ khác comment. Số dòng mermaid bằng nhau. Fence `text` giống hệt.
4. [ ] Mọi khối python, example và quiz chạy với `-W error`, stderr rỗng, output khớp. Không in NumPy scalar thô hay vector dài.
5. [ ] Mọi xếp hạng trong bài hợp lý với người đọc. Report liệt kê `embed_dim` đã dùng ở từng chỗ.
6. [ ] Exercise: starter fail **mọi** test (số pass với starter phải là 0, ghi vào report). Solution và alternative pass (pytest **và** browser runner trong validate).
7. [ ] Script độ dài mcq in `violations: 0`.
8. [ ] Bản VI tự nhiên, xưng "bạn", thuật ngữ giữ tiếng Anh kèm giải nghĩa lần đầu.
9. [ ] Report ghi: số step khối Visualize, link further_reading đã mở, mọi hành vi lạ của `pyai_llm`.

## Lệnh kiểm tra
Từ gốc repo:
```
uv run python tools/validate.py --path curriculum/phase-07-llm/p7-03-embeddings
uv run python -m pytest curriculum/phase-07-llm
uv run ruff check curriculum/phase-07-llm
grep -rnE "input\(|time\.sleep|requests\.|urllib|open\(|eval\(|astype\(int\)|dtype=int\b" curriculum/phase-07-llm/p7-03-embeddings --include=*.py
uv run python tools/build_content.py
git status --short
```
Script độ dài mcq (phải in `violations: 0`):
```
uv run python -c "
import yaml
bad=0
for q in yaml.safe_load(open('curriculum/phase-07-llm/p7-03-embeddings/quiz.yaml',encoding='utf-8'))['questions']:
    if q['type']!='mcq': continue
    for lang in ('en','vi'):
        o=q[lang]['options']; L=[len(x) for x in o]; a=q['answer']
        d=[l for i,l in enumerate(L) if i!=a]
        if L[a] > 1.2*sum(d)/len(d): bad+=1; print(q['id'],lang,L)
print('violations:',bad)
"
```
Mong đợi:
- validate 0 lỗi, pytest exit 0, ruff sạch, grep rỗng.
- Chỉ có thay đổi trong các file được phép.

## Ghi chú cho worker
- Đọc `docs/CONTENT_GUIDE.md` (cả mục Data & ML phase 4+), `packages/pyai_llm/README.md` và `pyai_llm.py`, mục p7 trong `curriculum/syllabus.yaml`, `curriculum/topics.yaml`, và §2 bài `p5-01-math-bridge` (cosine). Dùng bài p7-02 làm mẫu.
- Test chỉ dùng: assert, pytest.raises, pytest.approx, pytest.mark.parametrize, `@pytest.fixture` định nghĩa trong file test.
- Dùng `uv run python -m pytest`, không dùng `uv run pytest`. Kiểm warning bằng `uv run python -W error <file>`.
- Mọi lệnh phải tự kết thúc. Không chạy server.

## Trạng thái
- Bước hiện tại: xong, commit `ca0ed76` (đạt vòng 2; boss kiểm: validate toàn bộ 0 lỗi trên 42 bài, typecheck + build; trong app qua Pyodide: khối numpy §3 ra đúng điểm, starter ex02 0/8, solution qua hết; chờ user duyệt commit)
- Vòng: 2/3
- Số lần swap: 0
- Fallback: không
- Model: Gemini 4 Hydrogen (High)
- Lần gọi 1 bị lỗi mạng (DNS) sau 18 phút; worker đã tạo đủ file lesson, examples, exercises, quiz, chưa có report. Gọi lại 1 lần để làm tiếp.

## Feedback vòng 2
Boss đã chạy lại: validate bài 0 lỗi, pytest 43 passed, ruff sạch, grep rỗng. Nội dung tốt. Chỉ sửa 2 điểm nhỏ, không đụng gì khác:

1. **Hint 3 lộ dòng cốt lõi** (`exercises/ex01-cosine/exercise.yaml`, `exercises/ex02-top-k/exercise.yaml`, cả `en` và `vi`).
   - Sau fence python của hint 3 có một câu nói thẳng phần còn thiếu:
     - ex01: "Divide the dot product by the product of `norm_a` and `norm_b`."
     - ex02: "Remember that normalized vectors let you score every row ... with a single matrix-vector multiplication."
   - Ghép với `...` thì ra nguyên solution. **Xóa câu đó ở cả EN và VI.** Có thể thay bằng một câu chỉ trỏ về section, vd "Look back at §2." / "Xem lại §4.", không nói phép tính.
   - Giữ nguyên skeleton và đúng một `...`.
2. **Thông báo lỗi NumPy quá dài** (`lesson.en.md` và `lesson.vi.md`, §7 lỗi 2).
   - `print("error:", err)` in ra một dòng hơn 150 ký tự, chứa chữ ký gufunc và phụ thuộc phiên bản NumPy.
   - Đổi thành in gọn và ổn định, vd `print("error:", type(err).__name__, "- shapes", v64.shape, v256.shape)`, rồi cập nhật comment output bằng output **thật**. Code EN/VI vẫn phải giống hệt.

Sau khi sửa, chạy lại:
```
uv run python tools/validate.py --path curriculum/phase-07-llm/p7-03-embeddings
uv run python -m pytest curriculum/phase-07-llm
```
Cập nhật report: thêm mục "Vòng 2".
