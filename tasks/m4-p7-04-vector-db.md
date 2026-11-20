# M4 bước 14: bài p7-04 Vector databases

## Mục tiêu
Viết bài `p7-04-vector-db` trong `curriculum/phase-07-llm/`, đúng `docs/CONTENT_GUIDE.md` và song ngữ EN/VI.
- Bài **chạy trong Pyodide** (không có `runner: local`). Embedding lấy từ `FakeLLM(embed_dim=256).embed(...)`, tính toán bằng NumPy. Không mạng, không key, **không ghi file**.
- Người học đã xong p7-03: embed, cosine bằng dot product trên vector đã chuẩn hóa, `D @ q`, `np.argsort(-scores, kind="stable")`, ngưỡng `min_score`. Họ cũng đã học class, dataclass, NumPy (p4-01).
- Ý chính:
  - Vector database là "ma trận `D` của p7-03 cộng thêm phần sổ sách": id, văn bản gốc, metadata, thêm/xóa, lọc, và tìm nhanh khi dữ liệu lớn.
  - Người học tự xây một `VectorStore` nhỏ trong bộ nhớ để hiểu bên trong, rồi biết các sản phẩm thật làm thêm những gì.
  - Bài này chuẩn bị trực tiếp cho p7-05 RAG: store chứa các **chunk** kèm metadata nguồn (`source`, `page`…).
- Bài mẫu: `curriculum/phase-07-llm/p7-03-embeddings/`. Copy giọng văn và hình dạng.

## File được phép sửa/tạo
- Thư mục mới `curriculum/phase-07-llm/p7-04-vector-db/` và mọi file bên trong.
- `curriculum/glossary.yaml`: chỉ **thêm** thuật ngữ chưa có (vector database, metadata, chunk, metadata filter, approximate nearest neighbor (ANN), index). Thuật ngữ đã có thì bỏ qua.
- `tasks/m4-p7-04-vector-db.report.md`

## Không được đụng
- `packages/`, `apps/`, `tools/`, `curriculum/syllabus.yaml`, `curriculum/topics.yaml`, các bài p7-01 … p7-03, các phase khác, `exams/`.
- Không xóa file, không `git commit`, **không chạy `pnpm --filter web build`**, không chạy server ở foreground.
- Không sửa `pyai_llm`. Hành vi nào cản bài học thì ghi vào report.

## Quy tắc code (bắt buộc)
- Áp dụng mọi quy tắc phase 7 và Data & ML phase 4+ như spec p7-03:
  - in số bằng `round(float(x), 3)` hoặc `.tolist()`;
  - không in vector dài, không in NumPy scalar thô, không in dtype số nguyên;
  - sạch với `-W error`, output tất định.
- Thứ tự xếp hạng tất định: `np.argsort(-scores, kind="stable")`, hòa điểm thì thứ tự thêm vào trước đứng trước.
- Dùng `FakeLLM(embed_dim=256)` cho mọi ví dụ có embedding (lý do đã giải thích ở p7-03; nhắc lại trong một câu).
- **Lưu trữ không dùng file:** minh họa "lưu và nạp lại" bằng `json.dumps` thành **chuỗi** rồi `json.loads` lại. Ghi chú rằng ngoài đời chuỗi đó ghi ra đĩa, và DB thật lo việc này.
- Khối mời **Visualize** phải dưới 600 step và **không gọi `FakeLLM`**: dùng store đồ chơi với vector 2–3 chiều viết tay (đã chuẩn hóa hoặc gần đủ). Kiểm bằng `tools/pyrunner/tracer.py` và ghi số step vào report.
- Bảng so sánh sản phẩm thật chỉ là **mô tả trung lập**, không có code cài đặt hay chạy chúng (vd FAISS, Chroma, pgvector, Qdrant). Mỗi dòng nói nó là gì, không quảng cáo.

## Nội dung bài (boss chốt dàn ý, worker viết)
Opening (không heading): ở p7-03 bạn giữ mọi vector trong một ma trận và một list văn bản song song. Khi có hàng nghìn tài liệu, cần thêm, xóa, biết vector nào đến từ file nào, hay chỉ tìm trong tài liệu tiếng Việt, thì hai list rời rạc sẽ vỡ. Vector database gom hết vào một chỗ.

1. **Từ hai list rời rạc tới một store.**
   - Cho thấy vấn đề: xóa một văn bản khỏi list mà quên xóa dòng tương ứng trong ma trận khiến kết quả lệch index. In ra kết quả sai.
   - Một bản ghi gồm `id`, `text`, `vector`, `metadata`.
   - **Picture in text** (fence `text`, giống hệt EN/VI): bảng bản ghi với cột id | text | metadata | vector[…].
2. **Xây `VectorStore` tối giản.**
   - Class có `add(ids, texts, metadatas)`: embed **một lần cho cả lô** và nối vào ma trận bằng `np.vstack`. Có `search(query, k)` trả list hit (dataclass `Hit(id, score, text, metadata)`) và `__len__`.
   - Id trùng thì raise `ValueError`.
   - Code đầy đủ, có thể dài khoảng 40–50 dòng. Chạy demo với 6 chunk FAQ.
   - **Mermaid** `flowchart LR` (≤ 8 node): add (texts → embed → vstack → matrix + records) và search (query → embed → `matrix @ q` → top-k → hits).
3. **Metadata và lọc.**
   - `search(query, k, where={"lang": "vi"})`: chỉ xét bản ghi mà mọi cặp key/value trong `where` khớp.
   - **Lọc trước rồi mới top-k** (pre-filter), không lấy top-k rồi mới lọc (post-filter), vì post-filter có thể trả ít hơn `k` kết quả, thậm chí 0. Chứng minh bằng output thật cho cả hai cách.
   - **Trace table** `| id | lang | score | kept? |`.
   - Section này mời **Visualize** trên store đồ chơi viết tay: xem mask được dựng và điểm được tính.
4. **Cập nhật và xóa.**
   - `delete(id)`: xóa cả bản ghi lẫn dòng ma trận (`np.delete(..., axis=0)`).
   - `upsert` (thêm mới hoặc ghi đè theo id): một câu giải thích và code ngắn, hoặc để thành bài "Try it yourself" của ví dụ.
   - Cho thấy sau khi xóa, search không còn trả bản ghi đó và index vẫn khớp.
5. **Lưu và nạp lại.**
   - `to_json()` trả chuỗi JSON chứa ids, texts, metadatas, vectors (list float). `from_json(s)` dựng lại store mà **không cần embed lại**, kiểm bằng search ra cùng kết quả.
   - Callout `[!TIP]`: embedding tốn tiền và thời gian, nên lưu lại. Nếu đổi model embedding thì phải embed lại toàn bộ, vì số chiều và không gian khác nhau (nối với lỗi ở p7-03).
6. **Khi dữ liệu lớn: index và ANN.**
   - `matrix @ q` là brute force: so với **mọi** vector, O(n·dim). Với vài nghìn vector thì vẫn ổn. Với hàng triệu vector, DB thật dùng chỉ mục approximate nearest neighbor (ANN), nhanh hơn rất nhiều nhưng đôi khi bỏ sót một kết quả gần nhất.
   - Một **bảng** ước lượng phép nhân theo n, tính bằng code thật (vd n × dim). Không đo thời gian thật vì không tất định.
   - **Bảng so sánh** `| tool | what it is | good for |`: NumPy store (bài này), FAISS, Chroma, pgvector, Qdrant. Mô tả trung lập, mỗi ô ngắn.
   - Callout `[!NOTE]`: API mỗi sản phẩm khác nhau, nhưng đều có add, search, filter, delete như store của bạn.
7. **Lỗi thường gặp** (VI: `## 7. Lỗi thường gặp`), chạy thật để lấy đúng thông báo:
   - Thêm id trùng → `ValueError` của store (hoặc cho thấy kết quả bị trùng nếu không kiểm).
   - Lọc sau top-k nên nhận ít kết quả hơn mong đợi.
   - Query embed bằng client khác `embed_dim` so với store → lỗi shape (in gọn như p7-03: tên lỗi và shape).
   - Search trên store rỗng → `np.vstack` hoặc `@` lỗi. Sửa bằng cách trả `[]` sớm.
8. **Recap / Tóm tắt**: 4–6 gạch đầu dòng.

Thời lượng 12–15 phút.

`meta.yaml`:
- `phase: p7`, `order: 4`, `tags`: tag có sẵn trong `curriculum/topics.yaml` (vd `llm`, `numpy`, và `oop` nếu có). Không thêm tag mới.
- `prerequisites: [p7-03-embeddings, p4-01-numpy]`
- `outcomes` khớp syllabus
- `review_by: "2027-05-01"`, không có `runner`
- `further_reading`: 1–2 link ổn định và trung lập (vd trang wiki FAISS hoặc docs pgvector trên GitHub). Mở thử và ghi vào report.

## Examples (3)
- `01_faq_store`: `VectorStore` gọn với 8 chunk FAQ có metadata `topic` và `lang`. Trả lời 3 câu hỏi, một câu có filter. In hit dạng `id score text`, mỗi dòng dưới 70 ký tự.
- `02_filter_before_topk`: so sánh pre-filter và post-filter trên cùng dữ liệu. Post-filter trả thiếu kết quả, pre-filter trả đủ `k`.
- `03_save_and_reload`: dựng store, `to_json`, nạp lại từ chuỗi, xóa một id, search lại. In `len` và kết quả trước/sau. Có thể in số lần gọi `embed` để chứng minh nạp lại không embed lại: đếm bằng một wrapper nhỏ, hoặc dùng `usage` nếu `embed` có ghi.

## Exercises (2)
- `ex01-metadata-filter` (`kind: fill`): `matches(metadata: dict, where: dict | None) -> bool` và `filter_indexes(metadatas: list[dict], where: dict | None) -> list[int]`.
  - `where` là `None` hoặc `{}` thì khớp tất cả. Key thiếu trong metadata thì không khớp.
  - Các `___` trong thân hàm.
  - 5–6 test (parametrize): `where` rỗng hoặc `None`; khớp một key; khớp nhiều key; key thiếu; giá trị khác; `filter_indexes` giữ đúng thứ tự.
- `ex02-mini-store` (`kind: code`): class `MiniStore(client)` với:
  - `add(ids: list[str], texts: list[str], metadatas: list[dict] | None = None) -> None`: gọi `client.embed(texts)` **đúng một lần** mỗi lần add. Id trùng (với store hoặc trong lô) thì raise `ValueError` và **không thêm gì**. `metadatas=None` thì mỗi bản ghi có `{}`.
  - `search(query: str, k: int = 3, where: dict | None = None) -> list[tuple[str, float]]`: trả `(id, score)`, điểm làm tròn 3 chữ số, kiểu `float` Python. Pre-filter. Giảm dần, hòa điểm thì bản ghi thêm trước đứng trước. Store rỗng hoặc không bản ghi nào khớp filter thì trả `[]` và không lỗi.
  - `delete(id: str) -> None`: id không có thì raise `KeyError`.
  - `__len__`.
  - Lưu trữ nội bộ tự chọn (ma trận NumPy hoặc list), test chỉ kiểm hành vi.
  - 8–9 test:
    - query đồng nghĩa đứng đầu;
    - `k` đúng;
    - filter;
    - filter không khớp → `[]`;
    - store rỗng → `[]`;
    - id trùng → `ValueError` và `len` không đổi;
    - `delete` rồi search không còn id;
    - `delete` id lạ → `KeyError`;
    - spy client đếm `embed` gọi đúng 1 lần mỗi `add` (search được phép gọi thêm cho query).
  - Starter: class có đủ method, mỗi method chỉ `pass`/`return None` kèm TODO. Import được và fail **mọi** test.
    - Lưu ý `__len__` trả `None` sẽ gây `TypeError` khi gọi `len()`. Đó cũng là fail, chấp nhận được, miễn là test không crash cả file.
  - `alternatives/01_list_of_records.py`: lưu list dataclass bản ghi và tính điểm bằng vòng lặp thay cho ma trận, kèm `.md` so sánh (dễ xóa và sửa hơn, chậm hơn khi lớn).
- Hint 3 tầng đúng luật:
  - hint 2 chỉ là các bước bằng lời, không có biểu thức Python hoàn chỉnh;
  - hint 3 là skeleton, **mỗi method** chừa đúng một `...` ở dòng cốt lõi, và **không** có câu nào sau skeleton nói ra phần còn thiếu (lỗi đã gặp ở p7-03);
  - ghép hint 2 và hint 3 không ra nguyên solution.

## Quiz
- 15–18 câu, mỗi loại `mcq`, `output`, `fill`, `parsons` ít nhất 2. Khoảng 5 dễ, 7 vừa, 3 khó. 6 flashcard.
- **mcq cân độ dài:** `len(đúng) <= 1.2 × trung bình len(distractor)` ở cả en và vi. Đáp án đúng không kèm lý do. Đáp án đúng là phương án dài nhất duy nhất ở tối đa 1/3 số câu mcq.
- Câu `output` in số đã làm tròn hoặc id, không in vector dài.
- Phải có câu về:
  - vector DB thêm gì so với ma trận trần;
  - metadata;
  - pre-filter và post-filter;
  - xóa phải xóa cả dòng ma trận;
  - lưu embedding để khỏi embed lại;
  - đổi model embedding thì phải embed lại;
  - brute force và ANN (đánh đổi tốc độ lấy độ chính xác);
  - embed theo lô.

## Tiêu chí hoàn thành (checklist)
1. [ ] Đủ file theo layout CONTENT_GUIDE. `meta.yaml` đúng như trên, tag có trong topics.yaml.
2. [ ] Lesson đúng dàn ý, đủ: picture in text, mermaid, trace table, bảng so sánh, một lời mời Visualize (không gọi FakeLLM), callout.
3. [ ] Code giữa EN và VI giống hệt, chỉ khác comment. Số dòng mermaid bằng nhau. Fence `text` giống hệt.
4. [ ] Mọi khối python, example và quiz chạy với `-W error`, stderr rỗng, output khớp. Không ghi file.
5. [ ] Kết quả search trong bài hợp lý với người đọc.
6. [ ] Exercise: starter fail **mọi** test (số pass với starter phải là 0, ghi vào report). Solution và alternative pass (pytest **và** browser runner trong validate).
7. [ ] Script độ dài mcq in `violations: 0`.
8. [ ] Bản VI tự nhiên, xưng "bạn", thuật ngữ giữ tiếng Anh kèm giải nghĩa lần đầu.
9. [ ] Report ghi: số step khối Visualize, link further_reading đã mở, mọi hành vi lạ của `pyai_llm`.

## Lệnh kiểm tra
Từ gốc repo:
```
uv run python tools/validate.py --path curriculum/phase-07-llm/p7-04-vector-db
uv run python -m pytest curriculum/phase-07-llm
uv run ruff check curriculum/phase-07-llm
grep -rnE "input\(|time\.sleep|requests\.|urllib|open\(|eval\(|astype\(int\)|dtype=int\b|faiss|chromadb|qdrant" curriculum/phase-07-llm/p7-04-vector-db --include=*.py
uv run python tools/build_content.py
git status --short
```
Script độ dài mcq (phải in `violations: 0`):
```
uv run python -c "
import yaml
bad=0
for q in yaml.safe_load(open('curriculum/phase-07-llm/p7-04-vector-db/quiz.yaml',encoding='utf-8'))['questions']:
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
- Đọc `docs/CONTENT_GUIDE.md` (cả mục Data & ML phase 4+), `packages/pyai_llm/README.md` và `pyai_llm.py`, mục p7 trong `curriculum/syllabus.yaml`, `curriculum/topics.yaml`. Dùng bài p7-03 làm mẫu.
- Test chỉ dùng: assert, pytest.raises, pytest.approx, pytest.mark.parametrize, `@pytest.fixture` định nghĩa trong file test.
- Dùng `uv run python -m pytest`, không dùng `uv run pytest`. Kiểm warning bằng `uv run python -W error <file>`.
- Mọi lệnh phải tự kết thúc. Không chạy server.

## Trạng thái
- Bước hiện tại: xong, commit `0dfaf4f` (đạt vòng 1; boss kiểm: validate toàn bộ 0 lỗi trên 43 bài, typecheck + build; trong app qua Pyodide: khối VectorStore §2 ra đúng, Visualize §3 54 bước, starter ex02 0/9, solution qua hết; chờ user duyệt commit)
- Vòng: 1/3
- Số lần swap: 0
- Fallback: không
- Model: Gemini 4 Hydrogen (High)
