# M4 bước 19: p7-09 Mini-project RAG

## Mục tiêu
Viết bài `p7-09-mini-project-rag` (`kind: project`) trong `curriculum/phase-07-llm/`, đúng `docs/CONTENT_GUIDE.md` và song ngữ EN/VI.
- Bài **chạy trong Pyodide** (không có `runner: local`). Dùng `FakeLLM(embed_dim=256)` (`embed` + RAG mode của `chat`). Không mạng, không key, không ghi file.
- Đây là mini-project trọng yếu của phase 7 (vào portfolio ở bước docs sau). Người học ghép mọi thứ của p7-03…p7-08 thành **một RAG bot hoàn chỉnh có eval**: ingest → index → retrieve → answer có trích nguồn → eval trên dev set → chọn cấu hình → chấm test set **một lần** → báo cáo trung thực.
- Mẫu cấu trúc và giọng văn: `curriculum/phase-05-ml/p5-05-mini-project/` (mini-project phase 5: các "Part", báo cáo trung thực, test set dùng một lần, mục "Take it further"). Mẫu kỹ thuật: p7-05 (`answer_with_sources`), p7-08 (`hit_rate`, `score_answer`, so sánh cấu hình).

## Hành vi fake client cần biết (worker đọc lại `FakeLLM.chat`, `_try_rag`, `_normalize_words`, `embed`, bảng synonym trong `packages/pyai_llm/pyai_llm.py`)
- RAG mode của `chat`: cần dòng `Context:` rồi các dòng `[n] ...`. Model chọn chunk có nhiều **từ thô** chung nhất với câu hỏi (lowercase, dài ≥ 3, tính cả stopword, không bỏ "s", không synonym), cần ≥ 2 từ chung, rồi trả `"<câu đầu của chunk> [n]"`; không thì `"I don't know based on the provided context."`.
- `embed` bỏ "s" cuối và hiểu synonym (vd "money back" → "refund"). Nên retrieval và câu trả lời có thể lệch nhau, như p7-08 đã chỉ ra.
- Hệ quả thiết kế:
  - Model chỉ trả **câu đầu** của chunk: đặt sự thật chính ở câu đầu mỗi chunk sau khi chunk. Nếu chunk theo số từ cắt ngang câu thì câu trả lời sẽ xấu đi: đây là chất liệu thật cho việc so sánh cấu hình chunk.
  - Mọi con số trong bài phải là output **thật**. Thiết kế dữ liệu, chạy thử, rồi mới viết lời.
- **Không sửa `pyai_llm`.** Nếu không làm được bài mà không sửa, dừng và ghi rõ vào report.

## File được phép sửa/tạo
- Thư mục mới `curriculum/phase-07-llm/p7-09-mini-project-rag/` và mọi file bên trong.
- `curriculum/glossary.yaml`: chỉ **thêm** thuật ngữ chưa có (vd ingestion, dev set, held-out test set). Đã có thì bỏ qua.
- `tasks/m4-p7-09-mini-project-rag.report.md`

## Không được đụng
- `packages/`, `apps/`, `tools/`, `curriculum/syllabus.yaml`, `curriculum/topics.yaml`, `curriculum/portfolio.yaml`, các bài p7-01 … p7-08, các phase khác, `exams/`.
- Không xóa file, không `git commit`, **không chạy `pnpm --filter web build`**, không chạy server ở foreground.

## Quy tắc code (bắt buộc)
- Quy tắc phase 4+ và phase 7: không `input()`, mạng, `time.sleep`, ghi file; sạch với `-W error`; tất định. Không in NumPy scalar thô. Dùng `np.argsort(-scores, kind="stable")`.
- **Không** `eval(`/`exec(`/`subprocess`/`os.system` (tên biến như `eval_set`, `run_eval` thì được).
- Mỗi khối python trong bài phải tự chạy được (copy dữ liệu cần thiết vào khối). Để khối không quá dài, dữ liệu dùng chung giữ gọn: 8–10 tài liệu, mỗi tài liệu 2–4 câu ngắn.
- Mỗi khối dưới 10 giây trong Pyodide.
- Khối mời **Visualize** dưới 600 step và **không gọi `FakeLLM`**: đặt ở Part 1 (chunk một tài liệu ngắn, xem các chunk và id được tạo ra). Kiểm bằng `tools/pyrunner/tracer.py`, ghi số step vào report.
- In kết quả gọn: mỗi dòng dưới 70 ký tự.

## Bối cảnh dự án
Help-desk bot cho một shop online nhỏ. Kho kiến thức: 8–10 trang FAQ (`refunds.md`, `shipping.md`, `warranty.md`, `payment.md`, `accounts.md`, ...), mỗi trang 2–4 câu, có sự thật cụ thể (số ngày, giờ, giá, điều kiện).
Eval set: 10–12 câu, có ít nhất 2 câu không trả lời được, ít nhất 2 câu diễn đạt khác tài liệu (paraphrase). Chia **cố định** thành `dev_set` (khoảng 7–8 câu, dùng để chọn cấu hình) và `test_set` (khoảng 4 câu, chấm **một lần** ở cuối). Mỗi câu: `{"id", "question", "expected_source", "expected_facts"}` như p7-08.

## Nội dung bài (boss chốt dàn ý, worker viết)
Opening (không heading): sếp nhờ bạn làm bot trả lời câu hỏi khách hàng từ các trang FAQ. Yêu cầu: trả lời đúng, trích nguồn, nói "không biết" khi tài liệu không có, và có con số chứng minh nó đủ tốt. Đây là mọi thứ của phase 7 ghép lại.

1. **The plan / Kế hoạch.**
   - Mermaid `flowchart LR` (≤ 8 node): docs → ingest/chunk → embed index → retrieve top-k → prompt Context → answer + sources → eval.
   - Bảng `| part | what you build | from lesson |` nối từng part với bài cũ (p7-03…p7-08).
   - Luật chơi như p5-05: chọn cấu hình trên dev set, test set chỉ chạy một lần, báo cáo cả chỗ dở.
2. **Dữ liệu: kho FAQ và eval set.**
   - In số tài liệu, số câu dev/test. Picture in text (fence `text`, giống hệt EN/VI) cho cách chia dev/test.
3. **Part 1: ingest và chunk.**
   - Chunk mỗi tài liệu, mỗi chunk mang `{"id": "<source>#<n>", "source", "text"}`. Hai chiến lược để so sánh sau: theo **câu** (tách bằng `". "` hoặc regex đơn giản) và theo **cửa sổ từ** (`size`, `overlap` như p7-05).
   - Lời mời **Visualize** ở khối chunk một tài liệu ngắn (không gọi FakeLLM).
   - Trace table `| id | source | text |` cho vài chunk.
4. **Part 2: index và retrieve.**
   - Embed mọi chunk một lần thành ma trận, `retrieve(question, k, min_score)` trả list chunk theo điểm. In top-k cho 2 câu.
5. **Part 3: trả lời có trích nguồn.**
   - Prompt `Context:` + `[n]`, gọi `chat`, đọc citation `[n]` → danh sách `source` hợp lệ (như p7-05). Câu "không biết" trả `sources` rỗng.
   - Demo một câu trả lời được và một câu không có trong tài liệu.
6. **Part 4: eval trên dev set và chọn cấu hình.**
   - Chấm `hit@k`, facts, grounded (citation hợp lệ + từ có trong context, như p7-08), idk cho câu không trả lời được.
   - So **ít nhất 2 cấu hình** trên dev set (vd chunk theo câu vs cửa sổ từ, và/hoặc k khác nhau). Bảng tổng bằng số đếm + %. Chọn cấu hình theo **dev**, nói rõ tiêu chí chọn trước khi nhìn số (vd ưu tiên facts, hòa thì ưu tiên idk).
   - Callout `[!WARNING]`: tập nhỏ nhiễu; không quay lại chỉnh sau khi đã nhìn test.
7. **Part 5: chấm test set một lần và viết báo cáo.**
   - Chạy cấu hình đã chọn trên test set **một lần**. In báo cáo dạng dòng: cấu hình, dev scores, test scores, các câu sai kèm lý do (retrieval miss / answer miss / không từ chối được).
   - Phải có ít nhất **một** câu sai thật trên dev hoặc test, và báo cáo gọi tên nó. Báo cáo trung thực quan trọng hơn điểm đẹp.
   - Callout `[!TIP]` về cách đọc báo cáo khi test thấp hơn dev.
8. **Lỗi thường gặp** (VI: `## 8. Lỗi thường gặp`), output thật, 3–4 lỗi:
   - Chỉnh cấu hình dựa trên test set (data leakage kiểu p5-04).
   - Citation trỏ tới số không tồn tại / không map về source → sources sai.
   - Chunk cắt ngang câu nên câu đầu của chunk thiếu sự thật → câu trả lời dở dù retrieval đúng.
   - Embed lại toàn bộ tài liệu cho mỗi câu hỏi (chậm, tốn tiền ngoài đời) thay vì index một lần. Đo bằng số lần gọi `embed` (đếm, không đo thời gian).
9. **Recap / Tóm tắt** 4–6 gạch đầu dòng.
10. **Take it further / Làm thêm**: 3–4 gợi ý (thêm câu eval từ log thật, reranking, LLM-as-judge với API thật đọc key từ `.env` trong khối `bash`, đưa bot lên FastAPI ở phase 8).

Thời lượng 40–50 phút.

`meta.yaml`:
- `phase: p7`, `order: 9`, `kind: project`, `tags`: tag có sẵn trong `curriculum/topics.yaml` (vd `llm`, `rag`, `evaluation`). Không thêm tag mới.
- `prerequisites: [p7-08-evals]`
- `outcomes`: 2 outcome của syllabus giữ nguyên, có thể thêm 1–2 outcome cụ thể như p5-05.
- `review_by: "2027-05-01"`, không có `runner`.
- `further_reading`: 1–2 link ổn định, trung lập (mở thử, ghi vào report).

## Examples (3)
- `01_ingest_and_index`: chunk kho FAQ theo hai chiến lược, in số chunk mỗi cách và vài id; index một lần và in top-k cho một câu.
- `02_answer_with_sources`: chạy bot trên 3 câu (một trả lời được, một paraphrase, một không có trong tài liệu), in answer và sources.
- `03_eval_report`: chạy toàn bộ: so cấu hình trên dev, chọn, chấm test một lần, in báo cáo.

## Exercises (2, đều `kind: project`)
Bài học hướng dẫn từng bước, nhưng hàm trong exercise phải **ghép lại và có yêu cầu riêng** để người học không chép nguyên một khối trong bài.
- `ex01-ingest-retrieve`: `build_index(docs: list[dict], client, mode: str = "sentence", size: int = 8, overlap: int = 2) -> dict` và `retrieve(index: dict, question: str, client, k: int = 2, min_score: float = 0.2) -> list[dict]`.
  - `build_index`: chunk mỗi doc theo `mode` (`"sentence"` hoặc `"words"`; mode khác → `ValueError`), bỏ chunk rỗng, id `"<source>#<n>"` đánh số từ 0 theo từng source, gọi `client.embed` **đúng một lần** cho mọi chunk. Trả `{"chunks": [...], "vectors": <list hoặc ndarray>}`.
  - `retrieve`: embed câu hỏi, xếp theo điểm (stable), lấy top-k, bỏ chunk dưới `min_score`. Trả list chunk (dict có `id`, `source`, `text`, `score` làm tròn 3 chữ số).
  - Quy tắc tách câu ghi rõ trong prompt, có ví dụ.
  - 8–10 test: số chunk và id mỗi mode; mode lạ raise; doc rỗng bị bỏ; embed gọi đúng 1 lần trong `build_index` (spy client bọc FakeLLM); top-k đúng source cho câu dễ; `min_score` lọc hết → list rỗng; k lớn hơn số chunk; không sửa `docs`.
  - Starter import được và fail **mọi** test. `alternatives/01_*.py` dùng cách thật sự khác (vd vòng lặp thuần không NumPy cho phần xếp hạng), kèm `.md`.
- `ex02-eval-report`: `evaluate_bot(answer_fn, eval_set: list[dict]) -> dict` và `report_lines(summary: dict) -> list[str]`.
  - `answer_fn(question) -> {"answer": str, "sources": list[str], "retrieved": list[str]}` (người học không cần FakeLLM trong hàm này; test truyền hàm giả tất định).
  - `evaluate_bot` trả `{"n", "hits", "n_answerable", "facts_ok", "idk_ok", "n_unanswerable", "failures"}`:
    - `hits`: câu có `expected_source` nằm trong `retrieved`;
    - `facts_ok`: câu trả lời được có đủ mọi fact (lowercase `in`);
    - `idk_ok`: câu không trả lời được có "i don't know" và `sources` rỗng;
    - `failures`: list `(id, reason)` theo thứ tự eval set, reason là một trong `"retrieval_miss"`, `"answer_miss"`, `"no_refusal"`. Câu trả lời được mà retrieval miss thì chỉ ghi `retrieval_miss`.
  - `report_lines` trả các dòng định dạng cố định ghi trong prompt (vd `"hit@k: 4/5 (80%)"`, `"facts: 3/5 (60%)"`, `"refusals: 1/2 (50%)"`, rồi mỗi failure một dòng `"FAIL q3: answer_miss"`, cuối cùng `"failures: 2"`). Mẫu số bằng 0 thì in `"n/a"`.
  - 8–10 test: bot hoàn hảo; retrieval miss; answer miss; không từ chối; câu không trả lời được nhưng có sources → `no_refusal`; thứ tự failures; định dạng report đúng từng dòng; mẫu số 0 → `n/a`; không sửa `eval_set`.
  - Starter import được và fail **mọi** test. `alternatives/01_*.py` cách khác thật sự (vd dùng `collections.Counter` hoặc tách hàm `classify(row, out)`), kèm `.md`.
- Hint 3 tầng đúng luật cho cả hai:
  - hint 1 trỏ tới Part và cho một input cụ thể với kết quả;
  - hint 2 chỉ là các bước bằng lời, không có biểu thức Python hoàn chỉnh;
  - hint 3 là skeleton, mỗi hàm chừa đúng một `...` ở dòng/khối cốt lõi, không câu nào sau skeleton nói ra phần thiếu; ghép hint 2 + hint 3 không ra nguyên solution.

## Quiz
- 15–18 câu, mỗi loại `mcq`, `output`, `fill`, `parsons` ít nhất 2. Khoảng 5 dễ, 7 vừa, 3 khó. 6 flashcard.
- **mcq cân độ dài:** `len(đúng) <= 1.2 × trung bình len(distractor)` ở cả en và vi. Đáp án đúng không kèm lý do. Đáp án đúng là phương án dài nhất duy nhất ở tối đa 1/3 số câu mcq.
- Phải có câu về: thứ tự các bước pipeline; vì sao index một lần; chunk theo câu vs cửa sổ từ; dev vs test set; khi test thấp hơn dev; phân loại failure (retrieval miss vs answer miss); citation không hợp lệ; câu không trả lời được.

## Tiêu chí hoàn thành (checklist)
1. [ ] Đủ file theo layout CONTENT_GUIDE. `meta.yaml` đúng như trên.
2. [ ] Lesson đúng dàn ý, đủ: mermaid, picture in text, trace table, bảng so sánh, một lời mời Visualize (không gọi FakeLLM), callout `[!WARNING]`, `[!TIP]`, mục Take it further.
3. [ ] Code giữa EN và VI giống hệt, chỉ khác comment. Số dòng mermaid bằng nhau. Fence `text` giống hệt.
4. [ ] Mọi khối python, example và quiz chạy với `-W error`, stderr rỗng, output khớp. Mọi số liệu trong văn bản và bảng khớp output thật.
5. [ ] Chọn cấu hình theo dev, test chạy một lần, báo cáo có ít nhất một câu sai thật và giải thích đúng nguyên nhân.
6. [ ] Exercise: starter fail **mọi** test (số pass với starter là 0, ghi vào report). Solution và alternative pass (pytest **và** browser runner trong validate). Hàm exercise không trùng nguyên văn khối nào trong bài.
7. [ ] Script độ dài mcq in `violations: 0`.
8. [ ] Bản VI tự nhiên, xưng "bạn", thuật ngữ giữ tiếng Anh kèm giải nghĩa lần đầu.
9. [ ] Report ghi: số step khối Visualize, link further_reading đã mở, cấu hình đã so và đã chọn, điểm dev/test. `glossary.yaml` chỉ có dòng thêm.

## Lệnh kiểm tra
Từ gốc repo:
```
uv run python tools/validate.py --path curriculum/phase-07-llm/p7-09-mini-project-rag
uv run python -m pytest curriculum/phase-07-llm
uv run ruff check curriculum/phase-07-llm
grep -rnE "input\(|time\.sleep|requests\.|urllib|open\(|[^_a-z]eval\(|exec\(|subprocess|os\.system|while True" curriculum/phase-07-llm/p7-09-mini-project-rag --include=*.py
git diff --numstat curriculum/glossary.yaml
uv run python tools/build_content.py
git status --short
```
Script độ dài mcq (phải in `violations: 0`):
```
uv run python -c "
import yaml
bad=0
for q in yaml.safe_load(open('curriculum/phase-07-llm/p7-09-mini-project-rag/quiz.yaml',encoding='utf-8'))['questions']:
    if q['type']!='mcq': continue
    for lang in ('en','vi'):
        o=q[lang]['options']; L=[len(x) for x in o]; a=q['answer']
        d=[l for i,l in enumerate(L) if i!=a]
        if L[a] > 1.2*sum(d)/len(d): bad+=1; print(q['id'],lang,L)
print('violations:',bad)
"
```
Mong đợi: validate 0 lỗi, pytest exit 0, ruff sạch, grep rỗng, glossary chỉ có dòng thêm.

## Ghi chú cho worker
- Đọc `docs/CONTENT_GUIDE.md` (mục Data & ML, mục Fake LLM client), `packages/pyai_llm/README.md` và `pyai_llm.py`, mục p7 trong `curriculum/syllabus.yaml`, `curriculum/topics.yaml`, bài `p5-05-mini-project` (cấu trúc project), p7-05 và p7-08.
- Test chỉ dùng: assert, pytest.raises, pytest.approx, pytest.mark.parametrize, `@pytest.fixture` định nghĩa trong file test. Spy client là class nhỏ định nghĩa trong file test, bọc `FakeLLM` và đếm số lần gọi.
- Dùng `uv run python -m pytest`, không dùng `uv run pytest`. Kiểm warning bằng `uv run python -W error <file>`.
- Mọi lệnh phải tự kết thúc. Không chạy server.
- Ghi report ngay khi xong từng phần lớn (lesson, examples, exercises, quiz), để nếu bị ngắt vẫn còn dấu vết.

## Trạng thái
- Bước hiện tại: 5 (đạt vòng 2; boss kiểm: validate bài 0 lỗi, pytest 148 pass, ruff sạch, typecheck + build 71 trang; trong app qua Pyodide: báo cáo §7 khớp, ex02 starter 0/10, solution 10/10; validate toàn bộ 0 lỗi trên 48 bài) — xong, commit `7977522`
- Vòng: 2/3
- Số lần swap: 0
- Fallback: không
- Model: Gemini 4 Hydrogen (High)

## Feedback vòng 2
Cổng kiểm tra đều xanh, bài tốt, số liệu khớp. Sửa đúng các điểm sau:

1. **ex01 lộ đáp án (vi phạm tiêu chí 6).** `retrieve` trong `lesson.*.md` §4 (Part 2, quanh dòng 217) gần như trùng nguyên văn `retrieve` của `ex01-ingest-retrieve/solution.py` (cùng nhánh rỗng, `argsort` stable, lọc `min_score`, dict có `score` làm tròn). Sửa **ở lesson**, giữ nguyên exercise:
   - Ở §4, hàm trong bài đổi thành dạng đơn giản hơn và khác hình dạng: `top_k(index, question, client, k)` trả list `(score, chunk)` (tuple, chưa lọc `min_score`, chưa làm tròn trong dict). Việc lọc `min_score` trình bày là một bước riêng ngắn ở §6 khi so cấu hình (vd một dòng comprehension trong `eval_config`), không gói thành hàm `retrieve` giống exercise.
   - Các khối sau trong bài (§5, §6, §7, examples) cập nhật tương ứng nếu đang dùng `retrieve` y hệt solution. Kết quả in ra **phải giữ nguyên** (bảng §6, báo cáo §7). Nếu số đổi thì cập nhật mọi chỗ trích số trong văn bản, bảng, recap, quiz.
   - Sau khi sửa, kiểm: không khối nào trong lesson/examples chứa nguyên văn thân hàm `retrieve` hoặc `build_index` của solution ex01.
2. **Heading cuối theo CONTENT_GUIDE và p5-05:** `## 9. Recap` → `## Recap` (VI `## Tóm tắt`), `## 10. Take it further` → `## Take it further` (VI giữ tiêu đề tương ứng, không đánh số).
3. **Lỗi thường gặp 1:** khối này dùng một test set rút gọn 2 câu, nên "2 of 2" dễ bị đọc nhầm là test set 4 câu ở §7. Thêm nửa câu trước khối nói rõ đây là bản rút gọn 2 câu của test set (t1, t3).
4. **§10 Take it further:** đổi `OPENAI_API_KEY` thành tên trung lập `LLM_API_KEY` (ở cả EN và VI).

Chạy lại toàn bộ Lệnh kiểm tra; ghi vào report kết quả kiểm "không trùng nguyên văn" ở điểm 1.
