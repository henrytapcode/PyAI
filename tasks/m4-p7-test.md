# M4 bước 21: Phase test 7 (LLM & GenAI)

## Mục tiêu
Viết `curriculum/phase-07-llm/phase-test.yaml`, bài kiểm tra cuối phase 7.
- Định dạng giống `curriculum/phase-06-deep-learning/phase-test.yaml`: schema `tools/schema/exam.schema.json`, `kind: phase_test`.
- Boss đã chốt blueprint bên dưới. Worker viết câu hỏi theo đúng blueprint.

## File được phép sửa/tạo
- Chỉ một file mới: `curriculum/phase-07-llm/phase-test.yaml`.
- Báo cáo `tasks/m4-p7-test.report.md`.

## Không được đụng
- Mọi file khác, gồm: quiz các bài, `tools/`, `apps/`, glossary, topics.
- Không xóa file, không `git commit`.
- **Không chạy `pnpm --filter web build`.**

## Blueprint (boss chốt)

### Thông tin chung
- `id: p7-phase-test`, `phase: p7`.
- Title EN: "Phase 7 test: LLMs & GenAI". Title VI: "Bài kiểm tra Phase 7: LLM & GenAI".
- Description nêu số câu và các chủ đề.
- `duration_min: 30`, `pass_score: 0.7`.
- **20 câu**, id từ `p7-test-q01` tới `p7-test-q20`.
- Nhóm câu theo chủ đề bằng comment, ví dụ `# ---- llm api`.

### Phân bổ theo chủ đề
| Chủ đề (bài) | Số câu | Ý chính phải kiểm |
|---|---|---|
| LLM API (p7-01) | 2 | `messages` (system/user/assistant, history gửi lại mỗi lượt); `temperature`; `Usage` và tính cost theo token; retry chỉ cho lỗi tạm thời (`RateLimitError`) với exponential backoff |
| Structured output (p7-02) | 2 | tách JSON khỏi text thừa; validate theo schema (thiếu field, sai kiểu, `enum`); retry kèm thông báo lỗi rồi mới fallback |
| Embeddings (p7-03) | 2 | cosine similarity; vector đã chuẩn hóa thì dot = cosine; top-k bằng `argsort` giảm dần; ngưỡng phải đo lại cho từng model |
| Vector DB (p7-04) | 2 | lọc metadata **trước** top-k (lọc sau có thể ra ít hơn k); upsert/delete giữ id ↔ hàng ma trận đồng bộ; lưu và nạp lại |
| RAG (p7-05) | 3 | chunk theo cửa sổ từ hoặc theo đoạn, overlap; prompt có `Context:` đánh số `[n]` kèm luật "chỉ dùng context, không biết thì nói không biết"; citation phải nằm trong `1..len(hits)`; `min_score` để bỏ qua LLM; văn bản truy xuất là input chưa tin cậy (prompt injection) |
| Tool use (p7-06) | 2 | tool schema (name/description/parameters/required); dispatch qua allowlist; message `tool` có `tool_call_id`; args của model là input chưa tin cậy; cờ xác nhận và hạn mức nằm trong code, model không tự đặt được |
| Agents (p7-07) | 2 | vòng lặp có giới hạn (`max_steps`); guard `repeat`; `budget` theo token; side effect thì `needs_approval` |
| Evals (p7-08) | 2 | hit rate@k; faithful (mọi câu trả lời có căn cứ, citation hợp lệ) khác với "đúng sự thật"; dev set dùng để chọn, held-out dùng để báo cáo |
| Mini-project RAG (p7-09) | 1 | câu tích hợp: chọn cấu hình (chunk, k, `min_score`) trên dev, báo cáo một lần trên test; đếm hit/facts/refusal |
| Mini-project agent (p7-10) | 2 | golden trajectory (danh sách tool đúng thứ tự); kịch bản script nên chạy tất định; `rejected` khác `needs_approval`; ToolBox trả bản sao (`copy.deepcopy`) |

### Loại câu và độ khó
- **Loại câu:** 9 `mcq`, 5 `output`, 4 `fill`, 2 `parsons`.
  - Rải đều giữa các chủ đề.
  - Chủ đề có từ 2 câu trở lên thì phải có ít nhất 2 loại khác nhau.
- **Độ khó:** 4 câu mức 1, 11 câu mức 2, 5 câu mức 3.
  - Câu mức 3 nên là câu tích hợp hoặc bẫy phổ biến, ví dụ:
    - lọc sau top-k;
    - citation `[n]` ngoài phạm vi;
    - chọn k trên test;
    - model tự đặt `confirmed=True`;
    - retry cả lỗi không tạm thời;
    - quên gửi lại tool message nên agent lặp.

### Quy tắc riêng cho mcq
- Rải `answer` qua vị trí 0–3 theo phân bổ 3/2/2/2.
- Distractor là hiểu lầm thật, không dùng "All of the above".
- **Cân độ dài:** `len(đúng) <= 1.2 × trung bình len(distractor)` ở cả en và vi.
- Đáp án đúng không kèm lý do ("because…", "so that…", "vì…", "để…"). Lý do để trong `explanation`.
- Đáp án đúng chỉ được là phương án dài nhất duy nhất ở tối đa 3/9 câu.

### Yêu cầu chung cho mọi câu
- **Câu phải mới hoàn toàn.** Đọc hết 10 file `curriculum/phase-07-llm/p7-*/quiz.yaml` trước khi viết. Không chép, và không chỉ sửa sơ một câu có sẵn, dù trùng ý hay trùng code.
- Mỗi câu có:
  - `tags` lấy trong `[llm, rag, agents, evaluation, json, testing]`. Kiểm từng tag có trong `curriculum/topics.yaml`; tag nào không có thì bỏ.
  - `explanation` song ngữ, nói **vì sao**.
- **parsons:**
  - `lines` theo thứ tự đúng, chạy được, mỗi dòng duy nhất.
  - Chỉ có một thứ tự đúng, nhờ ràng buộc phụ thuộc hoặc kết quả in ra.
  - Gợi ý: một lượt tool call (gọi chat → lấy `tool_calls[0]` → chạy tool → append assistant → append tool → gọi chat lần hai, in câu trả lời); hoặc pipeline RAG (embed → top-k → dựng prompt → chat → in).
- Chỉ dùng kiến thức đã dạy ở phase 1–7. Được dùng regex `re.findall(r"\[(\d+)\]", ...)` vì p7-05 đã dạy.

## Quy tắc code (bắt buộc)
- Trong app, câu hỏi bài thi chỉ hiển thị code. Validator chạy code trên máy và so với đáp án.
- **Không gọi mạng, không cần API key.** Gọi LLM chỉ qua `pyai_llm` (`from pyai_llm import FakeLLM, ...`), như quiz phase 7.
  - Hành vi của FakeLLM xem `docs/CONTENT_GUIDE.md`, mục "Fake LLM client".
  - Muốn có nhiều bước thì dùng `script=`.
  - Ưu tiên câu không cần LLM: logic thuần trên dict/list hoặc NumPy nhỏ, cho dễ tính tay.
- NumPy:
  - In số bằng `round(float(x), 3)` hoặc `.tolist()`, không in scalar NumPy thô.
  - Không in dtype số nguyên.
  - Dùng `"int64"` tường minh nếu cần.
- Code không phát warning nào. Kiểm bằng `uv run python -W error snippet.py`.
- Code ngắn (câu output/fill dưới khoảng 15 dòng) và chạy nhanh.
- Thuật ngữ VI giữ tiếng Anh (embedding, chunk, retrieval, tool call, agent), gloss tiếng Việt khi cần. accuracy là "tỉ lệ đoán đúng"; không dùng "độ chính xác".

## Tiêu chí hoàn thành (checklist)
1. [ ] Đúng blueprint: 20 câu, đúng phân bổ chủ đề, loại câu, độ khó và vị trí đáp án mcq. Ghi bảng đếm thực tế vào report.
2. [ ] Không trùng câu với quiz của 10 bài. Report liệt kê mỗi câu kiểm ý nào.
3. [ ] EN/VI đầy đủ, bản VI tự nhiên, code giống hệt nhau giữa hai ngôn ngữ.
4. [ ] Script độ dài mcq bên dưới in `violations: 0` và `longest-unique` ≤ 3. Report ghi bảng độ dài 4 phương án (EN) của từng câu mcq.
5. [ ] Tuân thủ "Quy tắc code": mọi câu output/fill/parsons chạy với `-W error` mà không có stderr.
6. [ ] Lệnh kiểm tra xanh, chạy đúng như ghi.

## Lệnh kiểm tra
Chạy từ gốc repo `D:\Proj\python-ai-platform`:
```
uv run python tools/validate.py --path curriculum/phase-07-llm
uv run python tools/build_content.py
grep -nE "api_key|OPENAI|httpx|requests\.|độ chính xác" curriculum/phase-07-llm/phase-test.yaml
git status --short
```
Kiểm độ dài mcq (phải in `violations: 0` và `longest-unique` ≤ 3):
```
uv run python -c "
import yaml
bad=lu=0
for q in yaml.safe_load(open('curriculum/phase-07-llm/phase-test.yaml',encoding='utf-8'))['questions']:
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
- validate 0 lỗi, số exams tăng 1 (9 → 10);
- build_content in số exams tăng 1;
- grep không ra dòng nào;
- chỉ có một file mới là `phase-test.yaml`, ngoài `tasks/` và `.hallmark/` vốn đã untracked từ trước.

## Ghi chú cho worker
- Đọc mẫu `curriculum/phase-06-deep-learning/phase-test.yaml`, 10 file quiz phase 7 và các lesson phase 7 để biết API nào đã dạy.
- Dùng `uv run python -m pytest`, không dùng `uv run pytest`.
- Không chạy server hay dev server.

## Trạng thái
- Bước hiện tại: xong, đã commit `f15a3a3`
- Vòng: 2/3
- Số lần swap: 0
- Fallback: không
- Model: Gemini 4 Hydrogen (High)

## Feedback vòng 2
Boss đã kiểm: blueprint đúng (20 câu; 9/5/4/2; 4/11/5; mcq 3/2/2/2), độ dài mcq đạt, VI tự nhiên. Còn 2 điểm:
1. `p7-test-q15` (en + vi): sau khi áp dụng đáp án đúng (nối message `tool`), lượt 2 FakeLLM trả lời văn bản với `tool_calls == []`, nên `client.chat(...).tool_calls[0]` ném `IndexError` (boss đã chạy). Sửa code để vòng lặp xử lý được câu trả lời văn bản:
   - lấy `reply = client.chat(msgs, tools=tools)`;
   - `if not reply.tool_calls: print("final:", reply.content); break`;
   - rồi mới lấy `tc = reply.tool_calls[0]`.
   Giữ nguyên lỗi cần tìm (thiếu nối message `tool`), để code như đề vẫn in `stopped: repeat`. Tự kiểm: bản đã sửa theo đáp án in dòng `final: ...`, và ghi cả hai output vào report. Cập nhật prompt/explanation nếu cần; giữ `answer` và độ dài các phương án đạt script.
2. `p7-test-q20` (en + vi): phương án 1 ("tool schemas inside `ToolBox` remain mutable…") không phải hiểu lầm thật. Thay bằng một hiểu lầm thật, ví dụ "That the agent's final answer is factually correct for the user". Giữ `answer: 3` và luật độ dài.
Chạy lại: `validate.py --path curriculum/phase-07-llm`, script độ dài mcq. Ghi kết quả vào cuối report, dưới mục "Vòng 2".
