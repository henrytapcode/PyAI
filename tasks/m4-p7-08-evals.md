# M4 bước 18: bài p7-08 Evals

## Mục tiêu
Viết bài `p7-08-evals` trong `curriculum/phase-07-llm/`, đúng `docs/CONTENT_GUIDE.md` và song ngữ EN/VI.
- Bài **chạy trong Pyodide** (không có `runner: local`). Dùng `FakeLLM` (`embed` + RAG mode của `chat`, và `script=` để giả lập câu trả lời bịa). Không mạng, không key, không ghi file.
- Người học đã xong:
  - p7-05 RAG: chunk, `embed`, top-k, prompt `Context:` + `[n]`, trích nguồn, "I don't know";
  - p5-04 evaluation: train/test, tỉ lệ đoán đúng (accuracy), không tune trên test set.
- Ý chính:
  - Eval là **test cho hệ thống LLM**: một tập câu hỏi nhỏ có kết quả kỳ vọng, chạy lại sau mỗi thay đổi để biết tốt lên hay tệ đi, thay vì "đọc vài câu thấy ổn".
  - Chấm **từng tầng riêng**: retrieval (lấy đúng tài liệu chưa?) rồi answer (trả lời đúng và bám nguồn chưa?). Sai ở tầng nào thì sửa tầng đó.
  - So sánh hai cấu hình trên **cùng** tập eval, đọc số đếm chứ không chỉ phần trăm, vì tập nhỏ thì nhiễu.
- Bài sau là mini-project p7-09 (RAG có eval). Bài này cung cấp các hàm chấm nhỏ, rõ ràng, sẽ dùng lại ở đó.
- Bài mẫu: `curriculum/phase-07-llm/p7-05-rag/` (định dạng chunk `{"source", "text"}`, prompt `Context:`).

## Hành vi fake client cần biết (worker đọc lại `FakeLLM.chat`, `_try_rag`, `_normalize_words`, `embed` trong `packages/pyai_llm/pyai_llm.py`)
- RAG mode của `chat`: cần dòng `Context:` rồi các dòng `[n] ...`. Model chọn chunk có **nhiều từ chung nhất** với câu hỏi (từ thô, lowercase, dài ≥ 3, **tính cả stopword**, **không** bỏ "s" số nhiều, **không** dùng từ đồng nghĩa). Cần ≥ 2 từ chung, nếu không trả `"I don't know based on the provided context."`. Có thì trả `"<câu đầu của chunk> [n]"`.
- `embed` thì khác: bỏ "s" cuối và hiểu từ đồng nghĩa. Vì vậy một câu hỏi có thể **retrieve đúng** nhưng **trả lời "I don't know"**, hoặc ngược lại. Đây là chất liệu tốt cho bài: eval tách tầng sẽ **bắt được** chuyện này. Nhưng mọi con số trong bài phải là output **thật**: thiết kế câu hỏi rồi chạy thử, đừng đoán.
- Dùng `FakeLLM(embed_dim=256)` để tránh va chạm hash.
- Fake model **không** làm được LLM-as-judge. Chấm faithfulness bằng **heuristic tất định** (xem §4). LLM-as-judge chỉ giới thiệu bằng lời trong một callout `[!NOTE]`, kèm nói thật rằng judge cũng cần được eval và có thể thiên lệch.
- Câu trả lời "bịa" (không bám context) mô phỏng bằng `FakeLLM(script=[...])`. Phải nói thật trong callout đó là script đóng vai model trả lời sai.
- `script` hết phần tử thì raise `IndexError`: mỗi khối tạo client mới, đủ phần tử.
- **Không sửa `pyai_llm`.** Nếu thấy không thể làm bài mà không sửa, dừng và ghi rõ vào report.

## File được phép sửa/tạo
- Thư mục mới `curriculum/phase-07-llm/p7-08-evals/` và mọi file bên trong.
- `curriculum/glossary.yaml`: chỉ **thêm** thuật ngữ chưa có (eval, eval set, golden answer, hit rate, faithfulness, groundedness, LLM-as-judge, regression). Thuật ngữ đã có thì bỏ qua.
- `tasks/m4-p7-08-evals.report.md`

## Không được đụng
- `packages/`, `apps/`, `tools/`, `curriculum/syllabus.yaml`, `curriculum/topics.yaml`, các bài p7-01 … p7-07, các phase khác, `exams/`.
- Không xóa file, không `git commit`, **không chạy `pnpm --filter web build`**, không chạy server ở foreground.

## Quy tắc code (bắt buộc)
- Quy tắc phase 4+ và phase 7: không `input()`, mạng, `time.sleep`, ghi file; sạch với `-W error`; tất định. Không in NumPy scalar thô (dùng `round(float(x), 3)`).
- **Không** `eval(`/`exec(`/`subprocess`/`os.system`. Lưu ý: chữ "eval" trong tên biến/hàm (`eval_set`, `run_eval`) là được, chỉ cấm gọi built-in `eval(`.
- Kho tài liệu chung cho bài: 6–8 chunk ngắn của một shop (refunds, shipping, warranty, store hours, ...), dạng `{"source": "refunds.md", "text": "..."}`. Mỗi chunk 1–2 câu, câu đầu chứa sự thật chính.
- Eval set dạng list dict:
  `{"id": "q1", "question": "...", "expected_source": "refunds.md", "expected_facts": ["30 days"]}`.
  Câu không có trong tài liệu: `"expected_source": None, "expected_facts": []` và kỳ vọng hệ thống trả "I don't know".
- So khớp fact: lowercase, `fact.lower() in answer.lower()`. Nói rõ trong bài đây là cách chấm thô, có ưu nhược.
- Khối mời **Visualize** dưới 600 step và **không gọi `FakeLLM`**: đặt ở §3, tính hit rate trên list kết quả retrieval viết tay (vd 4 câu, mỗi câu có list source top-k). Kiểm bằng `tools/pyrunner/tracer.py`, ghi số step vào report.
- In bảng kết quả gọn: mỗi dòng dưới 70 ký tự.

## Nội dung bài (boss chốt dàn ý, worker viết)
Opening (không heading): bạn đổi chunk size trong RAG bot và thấy câu trả lời "có vẻ tốt hơn". Nhưng "có vẻ" là bao nhiêu câu? Câu nào tệ đi? Eval trả lời bằng con số, giống test set ở p5-04 nhưng cho hệ thống LLM.

1. **Eval là gì và vì sao cần.**
   - Định nghĩa: tập câu hỏi cố định + kết quả kỳ vọng + hàm chấm. Chạy lại sau mỗi thay đổi (prompt, chunk size, k, model).
   - Nối với p5-04: eval set giống test set; nếu chỉnh cấu hình cho tới khi eval set đẹp thì nó thành tập tune. Một câu về việc giữ riêng một phần, hoặc thêm câu mới định kỳ.
   - **Bảng so sánh** `| check | question it answers | example |`: unit test (p3) / eval / đọc thử bằng mắt.
2. **Xây eval set nhỏ.**
   - Kho tài liệu + 5–6 câu eval, có ít nhất 1 câu không trả lời được.
   - Nguyên tắc: câu hỏi viết như người dùng thật hỏi (không chép nguyên văn tài liệu); fact kỳ vọng ngắn, kiểm được; có câu khó và câu "không có trong tài liệu".
   - **Picture in text** (fence `text`, giống hệt EN/VI): pipeline `question → retrieve → top-k sources → generate → answer`, đánh dấu hai điểm chấm: `hit@k` ở retrieval, `facts / faithful` ở answer.
3. **Chấm retrieval: hit rate.**
   - `hit@k`: `expected_source` có nằm trong top-k không. Hit rate = số hit / số câu **có** expected_source (bỏ câu không trả lời được, nói rõ vì sao).
   - Chạy thật trên eval set với retrieval của p7-05.
   - **Trace table** `| id | top-2 sources | expected | hit |` cho các câu.
   - Lời mời **Visualize** trên khối tính hit rate viết tay (không gọi FakeLLM), xem `hits` tăng dần.
4. **Chấm câu trả lời: đúng fact và bám nguồn.**
   - `fact_score`: tỉ lệ `expected_facts` có trong answer. Câu không trả lời được: đúng khi answer chứa "I don't know".
   - `faithful` (heuristic): mọi từ nội dung của answer (lowercase, dài ≥ 4, bỏ citation `[n]`) đều xuất hiện trong context đã đưa vào prompt. Câu "I don't know" coi là faithful.
   - Demo: một câu trả lời thật từ RAG mode (faithful) và một câu bịa từ `script` (không faithful dù **nghe hợp lý**). In kết quả chấm thật.
   - Callout `[!NOTE]`: heuristic từ chung chỉ là xấp xỉ; ngoài đời người ta dùng LLM-as-judge (một model khác chấm theo rubric) hoặc người chấm, và judge cũng cần kiểm lại. Script ở đây đóng vai model bịa.
   - **Mermaid** `flowchart TD` (≤ 8 node): chấm một câu: retrieval hit? → answer chứa fact? → faithful? → ghi kết quả; có nhánh "không trả lời được → kiểm I don't know".
5. **So sánh hai cấu hình RAG.**
   - Hai cấu hình khác nhau thật sự (vd `k=1` vs `k=3`, hoặc chunk theo câu vs gộp đoạn, hoặc `min_score` khác). Worker chọn cặp cho ra khác biệt **có ý nghĩa** trên tập eval, và chạy thật.
   - In bảng tổng `| config | hit@k | facts | faithful | idk |` bằng **số đếm** (vd `4/5`) kèm phần trăm.
   - Đọc kết quả từng câu: chỉ ra ít nhất một câu cấu hình B tốt hơn và (nếu có thật) một câu tệ đi. Đây là lý do nhìn từng câu, không chỉ nhìn tổng.
   - Callout `[!WARNING]`: tập 5–6 câu thì 1 câu = 17–20%; khác biệt 1 câu chưa nói được gì. Tập thật cần vài chục tới vài trăm câu.
6. **Eval như regression test.**
   - Biến eval thành test: `assert hit_rate >= 0.8`, chạy mỗi khi đổi prompt hoặc cấu hình. Nối với pytest ở phase 3.
   - Một ví dụ ngắn hàm `check_eval(results, min_hit=0.8, min_facts=0.8)` trả list lỗi; in thật.
   - Một câu: lưu kết quả eval mỗi lần chạy để so theo thời gian (nối sang monitoring ở phase 8).
7. **Lỗi thường gặp** (VI: `## 7. Lỗi thường gặp`), output thật:
   - Chỉ chấm câu trả lời cuối, không chấm retrieval → không biết sai ở tầng nào (cho ví dụ retrieve đúng nhưng answer "I don't know", hoặc ngược lại, lấy từ quirk thật của fake client nếu có).
   - Tính hit rate có cả câu không trả lời được ở mẫu số → số bị kéo xuống sai.
   - So fact phân biệt hoa thường hoặc đúng nguyên câu → chấm trượt câu trả lời đúng.
   - Chỉnh cấu hình tới khi eval set đạt 100% → overfit eval set (nối p5-04).
8. **Recap / Tóm tắt**: 4–6 gạch đầu dòng.

Thời lượng 14–16 phút.

`meta.yaml`:
- `phase: p7`, `order: 8`, `tags`: tag có sẵn trong `curriculum/topics.yaml` (vd `llm`, `rag`, `evaluation`). Không thêm tag mới.
- `prerequisites: [p7-05-rag, p5-04-evaluation]`
- `outcomes` khớp syllabus
- `review_by: "2027-05-01"`, không có `runner`
- `further_reading`: 1–2 link ổn định, trung lập (vd tài liệu chung về eval của một nhà cung cấp LLM lớn, hoặc paper RAGAS arXiv 2309.15217). Mở thử và ghi vào report.

## Examples (3)
- `01_build_eval_set`: kho tài liệu + eval set; chạy retrieval, in bảng hit@2 từng câu và hit rate.
- `02_score_answers`: chạy RAG đầy đủ (FakeLLM) trên eval set, in `fact_score`, `faithful`, "idk" từng câu; thêm một câu trả lời bịa từ `script` để thấy `faithful = False`.
- `03_compare_configs`: so hai cấu hình trên cùng eval set, in bảng tổng và danh sách câu khác nhau giữa hai cấu hình.

## Exercises (2)
- `ex01-hit-rate` (`kind: fill`): `hit_rate(results: list[dict], k: int) -> float`.
  - Mỗi phần tử: `{"expected_source": str | None, "retrieved": list[str]}` (đã xếp theo điểm).
  - Bỏ qua phần tử có `expected_source` là `None`. Hit khi `expected_source in retrieved[:k]`.
  - Không còn phần tử nào để tính thì trả `0.0`.
  - Các `___` trong thân hàm.
  - 5–6 test (parametrize được): tất cả hit → 1.0; một nửa → 0.5; `k` cắt bớt làm mất hit; bỏ câu `None` khỏi mẫu số; list rỗng / toàn `None` → 0.0; dùng `pytest.approx`.
- `ex02-score-answer` (`kind: code`): `score_answer(answer: str, expected_facts: list[str], context: str) -> dict`.
  - Trả dict:
    - `facts` (float): tỉ lệ fact có trong answer (lowercase, `in`). `expected_facts` rỗng → 1.0 nếu answer chứa "i don't know" (lowercase), ngược lại 0.0.
    - `faithful` (bool): answer chứa "i don't know" → True; ngược lại mọi từ của answer sau khi lowercase, bỏ citation dạng `[n]`, tách bằng regex `[a-z0-9]+` và giữ từ dài ≥ 4, đều có trong tập từ (cùng cách tách) của `context`.
    - `unsupported` (list[str]): các từ không có trong context, giữ thứ tự xuất hiện, không trùng. Rỗng khi faithful.
  - Quy tắc tách từ ghi rõ trong prompt, có ví dụ.
  - 7–9 test: đủ fact; thiếu một fact → 0.5; hoa thường; câu không trả lời được đúng/sai; faithful thật; câu bịa → `faithful False` và `unsupported` đúng thứ tự; citation `[1]` không tính; từ ngắn < 4 ký tự bỏ qua; không sửa `expected_facts`.
  - Starter import được và fail **mọi** test.
  - `alternatives/01_set_ops.py`: cách khác thật sự (vd dùng set difference và `sum` generator thay cho vòng lặp, hoặc ngược lại), kèm `.md` so sánh. Phải giữ thứ tự `unsupported`.
- Hint 3 tầng đúng luật:
  - hint 1 trỏ tới section và cho một input cụ thể với kết quả;
  - hint 2 chỉ là các bước bằng lời, không có biểu thức Python hoàn chỉnh;
  - hint 3 là skeleton, mỗi hàm chừa đúng một `...` ở dòng cốt lõi, không có câu nào sau skeleton nói ra phần còn thiếu;
  - ghép hint 2 và hint 3 không ra nguyên solution. Với ex02, để trống phần tính `unsupported` thành một `...`.

## Quiz
- 15–18 câu, mỗi loại `mcq`, `output`, `fill`, `parsons` ít nhất 2. Khoảng 5 dễ, 7 vừa, 3 khó. 6 flashcard.
- **mcq cân độ dài:** `len(đúng) <= 1.2 × trung bình len(distractor)` ở cả en và vi. Đáp án đúng không kèm lý do. Đáp án đúng là phương án dài nhất duy nhất ở tối đa 1/3 số câu mcq.
- Phải có câu về:
  - eval khác unit test ở đâu;
  - vì sao chấm retrieval và answer riêng;
  - hit@k (tính tay);
  - bỏ câu không trả lời được khỏi mẫu số hit rate;
  - faithful nhưng sai fact, và đúng fact nhưng không faithful;
  - tập eval nhỏ thì nhiễu;
  - overfit eval set;
  - LLM-as-judge và giới hạn của nó.

## Tiêu chí hoàn thành (checklist)
1. [ ] Đủ file theo layout CONTENT_GUIDE. `meta.yaml` đúng như trên, tag có trong topics.yaml.
2. [ ] Lesson đúng dàn ý, đủ: picture in text, mermaid, trace table, bảng so sánh, một lời mời Visualize (không gọi FakeLLM), callout `[!NOTE]` về heuristic/LLM-as-judge/script, callout `[!WARNING]` về tập nhỏ.
3. [ ] Code giữa EN và VI giống hệt, chỉ khác comment. Số dòng mermaid bằng nhau. Fence `text` giống hệt.
4. [ ] Mọi khối python, example và quiz chạy với `-W error`, stderr rỗng, output khớp. Mọi số liệu trong văn bản và bảng khớp output thật.
5. [ ] So sánh §5 cho ra khác biệt thật, giải thích đúng nguyên nhân (đọc lại `_try_rag`/`embed` nếu cần).
6. [ ] Exercise: starter fail **mọi** test (số pass với starter là 0, ghi vào report). Solution và alternative pass (pytest **và** browser runner trong validate).
7. [ ] Script độ dài mcq in `violations: 0`.
8. [ ] Bản VI tự nhiên, xưng "bạn", thuật ngữ giữ tiếng Anh kèm giải nghĩa lần đầu. Dùng thuật ngữ VI của CONTENT_GUIDE cho accuracy/precision/recall nếu nhắc tới.
9. [ ] Report ghi: số step khối Visualize, link further_reading đã mở, cặp cấu hình đã chọn và kết quả. `glossary.yaml` chỉ có dòng thêm.

## Lệnh kiểm tra
Từ gốc repo:
```
uv run python tools/validate.py --path curriculum/phase-07-llm/p7-08-evals
uv run python -m pytest curriculum/phase-07-llm
uv run ruff check curriculum/phase-07-llm
grep -rnE "input\(|time\.sleep|requests\.|urllib|open\(|[^_a-z]eval\(|exec\(|subprocess|os\.system|while True" curriculum/phase-07-llm/p7-08-evals --include=*.py
git diff --numstat curriculum/glossary.yaml
uv run python tools/build_content.py
git status --short
```
Script độ dài mcq (phải in `violations: 0`):
```
uv run python -c "
import yaml
bad=0
for q in yaml.safe_load(open('curriculum/phase-07-llm/p7-08-evals/quiz.yaml',encoding='utf-8'))['questions']:
    if q['type']!='mcq': continue
    for lang in ('en','vi'):
        o=q[lang]['options']; L=[len(x) for x in o]; a=q['answer']
        d=[l for i,l in enumerate(L) if i!=a]
        if L[a] > 1.2*sum(d)/len(d): bad+=1; print(q['id'],lang,L)
print('violations:',bad)
"
```
Mong đợi:
- validate 0 lỗi, pytest exit 0, ruff sạch.
- grep rỗng.
- glossary chỉ có dòng thêm.

## Ghi chú cho worker
- Đọc `docs/CONTENT_GUIDE.md` (mục Data & ML, mục Fake LLM client), `packages/pyai_llm/README.md` và `pyai_llm.py`, mục p7 trong `curriculum/syllabus.yaml`, `curriculum/topics.yaml`. Dùng bài p7-05 làm mẫu cho retrieval và prompt, p5-04 cho giọng văn về evaluation.
- Test chỉ dùng: assert, pytest.raises, pytest.approx, pytest.mark.parametrize, `@pytest.fixture` định nghĩa trong file test.
- Dùng `uv run python -m pytest`, không dùng `uv run pytest`. Kiểm warning bằng `uv run python -W error <file>`.
- Mọi lệnh phải tự kết thúc. Không chạy server.
- Ghi report ngay khi xong từng phần lớn (lesson, examples, exercises, quiz), để nếu bị ngắt vẫn còn dấu vết.

## Trạng thái
- Bước hiện tại: 5 (đạt vòng 2; boss kiểm: validate bài 0 lỗi, pytest 126 pass, ruff sạch, typecheck + build 70 trang; trong app qua Pyodide: bảng so sánh §5 khớp, ex02 starter 0/10, solution 10/10; validate toàn bộ 0 lỗi trên 47 bài) — xong, commit `c133e77`
- Vòng: 2/3
- Số lần swap: 0
- Fallback: không
- Model: Gemini 4 Hydrogen (High)

## Feedback vòng 2
Cổng kiểm tra đều xanh, nội dung bài tốt. Còn **một** điểm cần sửa:

- **ex02 bị lộ đáp án trong bài.** `score_answer` ở §4 `lesson.*.md` (và §5) giống hệt `solution.py` của `ex02-score-answer`, hint 3 cũng gần như nguyên văn. Người học chỉ cần chép lại. Giữ nguyên lesson (§4, §5 vẫn dùng bản đơn giản). Sửa **chỉ** ex02 thành bản mở rộng có kiểm citation, phần bài chưa dạy:
  - Đổi tên hàm thành `score_grounded(answer: str, expected_facts: list[str], context: str) -> dict`.
  - Ngoài `facts`, `faithful`, `unsupported` như cũ, trả thêm:
    - `citations` (list[int]): các số `n` trong `[n]` của answer, theo thứ tự xuất hiện, không trùng;
    - `bad_citations` (list[int]): các số trong `citations` không có dòng `[n] ...` tương ứng trong `context` (context là các dòng `"[n] text"` nối bằng `\n`, như p7-05).
  - `faithful` mới = (answer là "i don't know") **hoặc** (không có từ unsupported **và** `citations` khác rỗng **và** `bad_citations` rỗng). Câu trả lời bám nguồn phải trích nguồn có thật.
  - Câu "i don't know": `citations` vẫn tính bình thường từ answer, `faithful True`, `unsupported []`.
  - Prompt nói rõ đây là bản mở rộng của `score_answer` ở §4, kèm bảng ví dụ (không citation → `faithful False`; `[3]` khi context chỉ có `[1]`,`[2]` → `bad_citations [3]`).
  - Test 8–10: giữ các test cũ còn hợp lệ (đổi tên hàm); thêm: không citation → faithful False; citation sai số → bad_citations; citation trùng `[1] ... [1]` → `citations [1]`; nhiều citation đúng thứ tự `[2] ... [1]` → `[2, 1]`.
  - Starter import được và fail **mọi** test. Solution và alternative pass (cập nhật `alternatives/01_set_ops.py` + `.md`).
  - Hint viết lại đúng luật: hint 1 một ví dụ cụ thể có citation sai; hint 2 bước bằng lời; hint 3 skeleton có thể dùng `_content_words` và phần `facts` như §4, chừa **một** `...` cho phần tính `citations`/`bad_citations` (phần mới), không câu nào sau skeleton nói ra phần thiếu.
  - Cập nhật `exercise.yaml` (title EN/VI), `prompt.*.md`. Giữ thư mục `ex02-score-answer` (không đổi tên thư mục, id `p7-08-ex02` giữ nguyên).
- Nếu quiz/flashcard nhắc tên `score_answer` của bài tập thì vẫn đúng (vì bài vẫn có `score_answer`), không cần sửa.

Chạy lại toàn bộ Lệnh kiểm tra và ghi số pass của starter (phải 0) vào report.
