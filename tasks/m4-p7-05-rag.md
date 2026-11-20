# M4 bước 15: bài p7-05 RAG

## Mục tiêu
Viết bài `p7-05-rag` trong `curriculum/phase-07-llm/`, đúng `docs/CONTENT_GUIDE.md` và song ngữ EN/VI.
- Bài **chạy trong Pyodide** (không có `runner: local`). Dùng `FakeLLM` cho cả `embed` (`embed_dim=256`) lẫn `chat`, cùng NumPy. Không mạng, không key, không ghi file.
- Người học đã xong:
  - p7-01: messages, system message;
  - p7-02: parse/validate;
  - p7-03: embedding, cosine, top-k, ngưỡng;
  - p7-04: vector store, metadata, pre-filter.
- Ý chính:
  - Model không biết tài liệu riêng của bạn.
  - RAG = **retrieve** các chunk liên quan, **augment** prompt bằng chúng (đánh số `[n]`), rồi **generate** câu trả lời chỉ dựa trên chúng và trích nguồn.
  - Không có chunk đủ liên quan thì nói "không biết" thay vì bịa.
- Đây là bài nền cho mini-project p7-09 (RAG) và p7-08 (evals). Giữ phạm vi gọn: một pipeline nhỏ, rõ ràng, không làm thành sản phẩm.
- Bài mẫu: `curriculum/phase-07-llm/p7-04-vector-db/`.

## Hành vi fake RAG (boss đã chạy thử; worker đọc lại `_try_rag`, `_parse_rag_context`, `_normalize_words` trong `packages/pyai_llm/pyai_llm.py`)
- Chế độ RAG bật khi một message `system` hoặc `user` có dòng đúng bằng `Context:`, theo sau là các dòng `[1] ...`, `[2] ...`.
- Fake model chọn chunk có **nhiều từ chung nhất** với câu hỏi:
  - từ ≥ 3 ký tự, chữ thường;
  - **không** stemming: "take" ≠ "takes";
  - **không** bỏ stopword: "the", "and", "how" đều được đếm.
- Cần ≥ 2 từ chung. Đạt thì trả `"<câu đầu của chunk> [n]"`, không thì trả `"I don't know based on the provided context."`.
- Boss đã thử:
  - "How many days do refunds take?" với chunk "Refunds are issued within 30 days of purchase. …" → `'Refunds are issued within 30 days of purchase. [1]'`.
  - "How long does shipping take?" với chunk "Shipping takes three to five business days." → **I don't know**, vì chỉ có 1 từ chung ("shipping"; "take" ≠ "takes").
- Vì vậy:
  - **Chọn câu hỏi và chunk sao cho kết quả hợp lý với người đọc.** Không để ví dụ nào ra kết quả "ngớ ngẩn" mà không giải thích.
  - Callout `[!NOTE]` (giống tinh thần p7-03) nói thật: fake model "trả lời" bằng cách chọn chunk trùng từ nhiều nhất và trả câu đầu. LLM thật đọc hiểu và tổng hợp nhiều chunk, nhưng **hình dạng pipeline và prompt thì giống hệt**.
  - Ghi trong report các quirk gặp phải (stopword, stemming), để boss cân nhắc cho p7-08 và p7-09.
- Mọi output in ra phải là output **thật**.

## File được phép sửa/tạo
- Thư mục mới `curriculum/phase-07-llm/p7-05-rag/` và mọi file bên trong.
- `curriculum/glossary.yaml`: chỉ **thêm** thuật ngữ chưa có (RAG, retrieval, chunking, chunk overlap, grounding, citation, hallucination, context window). Thuật ngữ đã có thì bỏ qua.
- `tasks/m4-p7-05-rag.report.md`

## Không được đụng
- `packages/`, `apps/`, `tools/`, `curriculum/syllabus.yaml`, `curriculum/topics.yaml`, các bài p7-01 … p7-04, các phase khác, `exams/`.
- Không xóa file, không `git commit`, **không chạy `pnpm --filter web build`**, không chạy server ở foreground.
- Không sửa `pyai_llm`.

## Quy tắc code (bắt buộc)
- Áp dụng mọi quy tắc phase 7 và Data & ML phase 4+ như spec p7-04:
  - in số làm tròn;
  - không in vector, NumPy scalar thô hay dtype số nguyên;
  - sạch với `-W error`; tất định; xếp hạng bằng `np.argsort(-scores, kind="stable")`.
- Retrieval trong bài dùng ma trận NumPy gọn (như p7-03/p7-04) hoặc một class store rút gọn. **Không import code từ bài khác**: mỗi khối tự chứa.
- Khối mời **Visualize** phải dưới 600 step và **không gọi `FakeLLM`**. Đặt nó ở phần chunking: xem các cửa sổ chunk được tạo với `size` và `overlap` trên một list từ ngắn. Kiểm bằng `tools/pyrunner/tracer.py` và ghi số step vào report.
- Định dạng context **cố định** trong toàn bài:
  ```
  Context:
  [1] <chunk text>
  [2] <chunk text>
  ```
  Đặt trong message `system`, sau phần hướng dẫn. Câu hỏi nằm trong message `user` riêng.
- Văn bản tài liệu viết bằng tiếng Anh (chuỗi trong code không dịch).

## Nội dung bài (boss chốt dàn ý, worker viết)
Opening (không heading): hỏi chatbot về chính sách đổi trả của shop bạn thì nó không biết, hoặc tệ hơn là bịa (hallucination). RAG cho model đọc đúng đoạn tài liệu liên quan ngay trước khi trả lời, giống thi "được mở tài liệu".

1. **Vì sao cần RAG.**
   - Gọi `chat` không có context với câu hỏi về shop: fake model trả lời chung chung (output thật).
   - Ba cách để model biết dữ liệu của bạn: nhét **cả** tài liệu vào prompt (tốn token, vượt context window), fine-tune (đắt, chậm cập nhật, nối p6-04), và RAG (chỉ đưa phần liên quan).
   - **Bảng so sánh** `| approach | cost | freshness | good for |`.
2. **Chunking: cắt tài liệu thành miếng.**
   - Hàm `chunk_words(text, size, overlap)` cắt theo từ, bước nhảy `size - overlap`.
   - Vì sao cần overlap: câu nằm vắt qua ranh giới không bị cắt mất ngữ cảnh.
   - **Picture in text** (fence `text`, giống hệt EN/VI): 10 từ đánh số, các cửa sổ `size=4, overlap=1` gối nhau.
   - Khối **Visualize** (không FakeLLM).
   - **Bảng** `| chunk size | pro | con |` (nhỏ / vừa / lớn).
3. **Pipeline RAG từ đầu đến cuối.**
   - **Mermaid** `flowchart LR` (≤ 9 node): docs → chunk → embed → store; question → embed → top-k → build prompt → chat → answer + sources.
   - Một khối code đầy đủ nhưng gọn: 3 tài liệu ngắn có `source` (vd `refunds.md`, `shipping.md`, `warranty.md`) → chunk → embed → câu hỏi → top-2 → prompt → `chat` → in câu trả lời.
4. **Prompt có căn cứ (grounded prompt).**
   - Hàm `build_messages(question, hits)` trả `[system, user]`. System có 3 luật: chỉ dùng context; không có thì nói không biết; trích `[n]`.
   - In ra prompt thật để người học thấy hình dạng (chỉ in system content, gọn).
   - Callout `[!WARNING]`: văn bản trong tài liệu cũng là "input lạ". Một chunk chứa câu "ignore previous instructions" có thể lái model (prompt injection). Một câu cảnh báo, không đi sâu.
5. **Trích nguồn và kiểm trích dẫn.**
   - Parse `[n]` trong câu trả lời bằng `re.findall(r"\[(\d+)\]", answer)` rồi map sang `source` của chunk.
   - Kiểm số trích dẫn có tồn tại trong context không: trích `[7]` khi chỉ có 2 chunk là dấu hiệu bịa.
   - **Trace table** `| question | top chunk | score | answer | sources |` cho 3 câu hỏi.
6. **Khi không tìm thấy: đừng bịa.**
   - Hai lớp bảo vệ:
     - (a) điểm retrieval < `min_score` thì **không gọi** LLM, trả "I don't know" luôn (tiết kiệm tiền);
     - (b) model tự nói không biết khi context không đủ.
   - Demo cả hai bằng output thật.
   - Một câu nối sang p7-08: đo chất lượng RAG bằng eval, không bằng cảm tính.
7. **Lỗi thường gặp** (VI: `## 7. Lỗi thường gặp`), output thật:
   - Không overlap nên câu trả lời bị cắt đôi giữa hai chunk, retrieval trượt.
   - `overlap >= size` khiến vòng lặp không tiến (bước nhảy ≤ 0). Bắt bằng `ValueError`.
   - Quên đánh số `[n]` hoặc sai định dạng `Context:` nên không trích được nguồn. Cho thấy fake model rơi về trả lời thường.
   - Tin trích dẫn mà không kiểm, dẫn tới nguồn không tồn tại.
8. **Recap / Tóm tắt**: 4–6 gạch đầu dòng.

Thời lượng 14–16 phút.

`meta.yaml`:
- `phase: p7`, `order: 5`, `tags`: tag có sẵn trong `curriculum/topics.yaml` (vd `llm`, `numpy`, `strings`). Không thêm tag mới.
- `prerequisites: [p7-04-vector-db]`
- `outcomes` khớp syllabus
- `review_by: "2027-05-01"`, không có `runner`
- `further_reading`: 1–2 link ổn định, trung lập (vd paper RAG gốc trên arXiv 2005.11401, một trang giải thích chunking trong docs của một thư viện lớn). Mở thử và ghi vào report.

## Examples (3)
- `01_policy_bot`: bộ tài liệu chính sách nhỏ (4–5 đoạn, mỗi đoạn có `source`). Trả lời 3 câu hỏi, in câu trả lời và `sources`. Một câu ngoài phạm vi thì in "I don't know" và ghi rõ là không gọi LLM.
- `02_chunk_size_compare`: cùng tài liệu và cùng 3 câu hỏi, so `size`/`overlap` khác nhau. In bảng gọn: số chunk và có retrieve đúng chunk chứa đáp án không. Mỗi dòng dưới 60 ký tự.
- `03_citation_check`: dùng `FakeLLM(script=[...])` để giả lập model trích `[3]` khi chỉ có 2 chunk, và một câu trả lời không có trích dẫn. Hàm `check_citations(answer, n_chunks)` gắn cờ cả hai.

## Exercises (2)
- `ex01-chunk-words` (`kind: fill`): `chunk_words(text: str, size: int, overlap: int) -> list[str]`.
  - Tách theo khoảng trắng và ghép mỗi cửa sổ bằng một dấu cách.
  - Cửa sổ cuối có thể ngắn hơn `size`, nhưng **không** tạo cửa sổ chỉ chứa phần đã nằm trọn trong cửa sổ trước. Mô tả chính xác quy tắc dừng trong prompt kèm ví dụ.
  - `size <= 0` hoặc `overlap < 0` hoặc `overlap >= size` thì raise `ValueError`.
  - Text rỗng thì trả `[]`.
  - Các `___` trong thân hàm.
  - 6 test (có parametrize): ví dụ cơ bản; không overlap; có overlap; text ngắn hơn `size` ra 1 chunk; text rỗng; tham số sai → `ValueError`.
- `ex02-answer-with-sources` (`kind: code`): `answer_with_sources(question: str, chunks: list[dict], client, k: int = 2, min_score: float = 0.2) -> dict`.
  - Mỗi chunk là `{"text": str, "source": str}`.
  - Trả `{"answer": str, "sources": list[str]}`.
  - Các bước:
    1. Embed mọi chunk text trong **một** lần gọi, và embed câu hỏi.
    2. Lấy top-k theo dot product, sort ổn định.
    3. Điểm cao nhất `< min_score` (hoặc `chunks` rỗng) thì trả `{"answer": "I don't know.", "sources": []}` và **không gọi** `chat`.
    4. Dựng messages đúng định dạng context cố định, đánh số theo thứ tự top-k.
    5. Gọi `chat`.
    6. Parse `[n]` hợp lệ (1 ≤ n ≤ số chunk trong context), map sang `source`, bỏ trùng, giữ thứ tự xuất hiện.
  - 8 test:
    - câu hỏi đúng có `answer` chứa nội dung chunk đúng và `sources == ["refunds.md"]` (hoặc tương đương);
    - ngoài phạm vi → `I don't know.`, `sources == []`, spy client xác nhận `chat` **không** được gọi;
    - `chunks` rỗng;
    - spy kiểm message system có dòng `Context:` và đúng số dòng `[n]` bằng `k`;
    - `script` trả trích dẫn `[5]` không hợp lệ → bị bỏ;
    - `script` trả `[2] … [1] … [2]` → sources theo thứ tự xuất hiện, không trùng;
    - `embed` gọi đúng 2 lần (chunks + question) hoặc 1 lần nếu gộp, nói rõ cái nào được chấp nhận trong prompt;
    - kiểu trả về đúng.
  - Starter import được, fail **mọi** test.
  - `alternatives/01_two_helpers.py`: tách `retrieve` và `build_messages` thành hàm riêng (hoặc một cách khác thật sự khác), kèm `.md` so sánh.
- Hint 3 tầng đúng luật:
  - hint 2 chỉ là các bước bằng lời, không có biểu thức Python hoàn chỉnh;
  - hint 3 là skeleton, mỗi hàm chừa đúng một `...` ở dòng cốt lõi, **không** có câu nào sau skeleton nói ra phần còn thiếu;
  - ghép hint 2 và hint 3 không ra nguyên solution. Với ex02, skeleton nên để trống **cả khối** dựng context thành một `...` (một dòng hoặc một biểu thức), thay vì cho sẵn gần hết.

## Quiz
- 15–18 câu, mỗi loại `mcq`, `output`, `fill`, `parsons` ít nhất 2. Khoảng 5 dễ, 7 vừa, 3 khó. 6 flashcard.
- **mcq cân độ dài:** `len(đúng) <= 1.2 × trung bình len(distractor)` ở cả en và vi. Đáp án đúng không kèm lý do. Đáp án đúng là phương án dài nhất duy nhất ở tối đa 1/3 số câu mcq.
- Phải có câu về:
  - RAG so với fine-tune;
  - vì sao cần overlap;
  - bước nhảy `size - overlap`;
  - định dạng context có đánh số;
  - không gọi LLM khi điểm thấp;
  - kiểm trích dẫn hợp lệ;
  - hallucination;
  - prompt injection qua tài liệu.

## Tiêu chí hoàn thành (checklist)
1. [ ] Đủ file theo layout CONTENT_GUIDE. `meta.yaml` đúng như trên, tag có trong topics.yaml.
2. [ ] Lesson đúng dàn ý, đủ: picture in text, mermaid, trace table, bảng so sánh, một lời mời Visualize (không gọi FakeLLM), callout `[!NOTE]` fake vs thật, callout `[!WARNING]` injection.
3. [ ] Code giữa EN và VI giống hệt, chỉ khác comment. Số dòng mermaid bằng nhau. Fence `text` giống hệt.
4. [ ] Mọi khối python, example và quiz chạy với `-W error`, stderr rỗng, output khớp.
5. [ ] Mọi câu trả lời trong bài hợp lý với người đọc. Report liệt kê quirk của fake RAG đã gặp.
6. [ ] Exercise: starter fail **mọi** test (số pass với starter phải là 0, ghi vào report). Solution và alternative pass (pytest **và** browser runner trong validate).
7. [ ] Script độ dài mcq in `violations: 0`.
8. [ ] Bản VI tự nhiên, xưng "bạn", thuật ngữ giữ tiếng Anh kèm giải nghĩa lần đầu.
9. [ ] Report ghi: số step khối Visualize, link further_reading đã mở.

## Lệnh kiểm tra
Từ gốc repo:
```
uv run python tools/validate.py --path curriculum/phase-07-llm/p7-05-rag
uv run python -m pytest curriculum/phase-07-llm
uv run ruff check curriculum/phase-07-llm
grep -rnE "input\(|time\.sleep|requests\.|urllib|open\(|eval\(|astype\(int\)|dtype=int\b" curriculum/phase-07-llm/p7-05-rag --include=*.py
uv run python tools/build_content.py
git status --short
```
Script độ dài mcq (phải in `violations: 0`):
```
uv run python -c "
import yaml
bad=0
for q in yaml.safe_load(open('curriculum/phase-07-llm/p7-05-rag/quiz.yaml',encoding='utf-8'))['questions']:
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
- Chỉ có thay đổi trong các file được phép. `glossary.yaml` chỉ có dòng thêm, không có dòng bị xóa (kiểm bằng `git diff curriculum/glossary.yaml`).

## Ghi chú cho worker
- Đọc `docs/CONTENT_GUIDE.md` (cả mục Data & ML và Fake LLM client), `packages/pyai_llm/README.md` và `pyai_llm.py`, mục p7 trong `curriculum/syllabus.yaml`, `curriculum/topics.yaml`. Dùng bài p7-04 làm mẫu.
- Test chỉ dùng: assert, pytest.raises, pytest.approx, pytest.mark.parametrize, `@pytest.fixture` định nghĩa trong file test.
- Dùng `uv run python -m pytest`, không dùng `uv run pytest`. Kiểm warning bằng `uv run python -W error <file>`.
- Mọi lệnh phải tự kết thúc. Không chạy server.

## Trạng thái
- Bước hiện tại: xong, commit `919ad49` (đạt vòng 1; boss kiểm: validate toàn bộ 0 lỗi trên 44 bài, typecheck + build; trong app qua Pyodide: pipeline §3 ra đúng, starter ex02 0/8, solution qua hết; chờ user duyệt commit)
- Vòng: 1/3
- Số lần swap: 0
- Fallback: không
- Model: Gemini 4 Hydrogen (High)
