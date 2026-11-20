# M4 bước 17: bài p7-07 Simple agents

## Mục tiêu
Viết bài `p7-07-agents` trong `curriculum/phase-07-llm/`, đúng `docs/CONTENT_GUIDE.md` và song ngữ EN/VI.
- Bài **chạy trong Pyodide** (không có `runner: local`). Dùng `FakeLLM` với `tools=` và `script=`. Không mạng, không key, không ghi file. Tool là hàm Python thuần, tất định, chạy trên dữ liệu dict.
- Người học đã xong p7-06: tool schema, registry, `dispatch` an toàn, vòng tool một bước, `max_rounds`, side effect và xác nhận.
- Ý chính:
  - Agent là **vòng lặp có giới hạn**: observe (đọc messages và kết quả tool), think (gọi model), act (chạy tool model chọn), lặp lại cho tới khi model trả lời cuối hoặc chạm giới hạn.
  - Phần khó không phải vòng lặp mà là **dừng đúng lúc** và **theo dõi được** (trace) mọi quyết định.
  - Nhiều việc không cần agent: workflow cố định (pipeline) rẻ hơn, dễ test hơn. Chỉ dùng agent khi số bước và thứ tự phụ thuộc vào kết quả giữa chừng.
- Bài sau là p7-08 evals và mini-project p7-10 (agent). Bài này giữ một agent nhỏ, rõ ràng.
- Bài mẫu: `curriculum/phase-07-llm/p7-06-tool-use/`.

## Hành vi fake client cần biết (worker đọc lại `FakeLLM.chat` trong `packages/pyai_llm/pyai_llm.py`)
- Ở chế độ mặc định, khi message cuối là `role == "tool"`, fake model **luôn** trả `"Based on the tool result: <content>"` và dừng. Nó **không tự chain** tool thứ hai.
- Vì vậy mọi quyết định **nhiều bước** trong bài phải mô phỏng bằng `FakeLLM(script=[...])`, trong đó script đóng vai "bộ não" của model: bước 1 gọi tool A, bước 2 gọi tool B với tham số lấy từ kết quả A, bước 3 trả lời cuối.
  - Phải nói **thật** trong một callout `[!NOTE]`: script thay cho phần "suy nghĩ" của LLM thật. Model thật tự quyết định bước tiếp theo dựa trên kết quả tool. Còn vòng lặp, giới hạn, trace và guard mà **code của bạn** viết thì giống hệt.
  - Một ví dụ không dùng script (một bước, model tự chọn tool) để nối với p7-06 là được.
- `script` hết phần tử thì raise `IndexError`. Agent phải dừng trước đó bằng `max_steps`, hoặc bài dùng chính hành vi này để minh họa vì sao cần giới hạn (bắt lỗi rõ ràng).
- `ToolCall.id` tăng dần theo client: mỗi khối tạo client mới.
- `resp.usage` có `total_tokens`: dùng để minh họa **ngân sách token** (dừng khi tổng vượt ngưỡng). Số phải thật.
- Mọi output in ra phải là output **thật**.

## File được phép sửa/tạo
- Thư mục mới `curriculum/phase-07-llm/p7-07-agents/` và mọi file bên trong.
- `curriculum/glossary.yaml`: chỉ **thêm** thuật ngữ chưa có (agent, agent loop, observe-think-act, ReAct, max steps, trace, stop condition, workflow). Thuật ngữ đã có thì bỏ qua.
- `tasks/m4-p7-07-agents.report.md`

## Không được đụng
- `packages/`, `apps/`, `tools/`, `curriculum/syllabus.yaml`, `curriculum/topics.yaml`, các bài p7-01 … p7-06, các phase khác, `exams/`.
- Không xóa file, không `git commit`, **không chạy `pnpm --filter web build`**, không chạy server ở foreground.
- Không sửa `pyai_llm`.

## Quy tắc code (bắt buộc)
- Quy tắc phase 7: không `input()`, mạng, `time.sleep`, ghi file; sạch với `-W error`; tất định.
- **Không** `eval`/`exec`/`subprocess`/`os.system` ở bất cứ đâu.
- Dùng đúng định dạng message của p7-06:
  - assistant có tool call: `{"role": "assistant", "content": None, "tool_calls": [{"id", "name", "arguments"}]}`;
  - kết quả tool: `{"role": "tool", "tool_call_id": ..., "content": str}`.
- Mọi vòng lặp agent đều có `max_steps`. Không có `while True` không giới hạn, kể cả trong ví dụ "sai". Nếu cần minh họa vòng lặp vô tận thì dùng `for` có giới hạn lớn, kèm comment.
- Khối mời **Visualize** phải dưới 600 step và **không gọi `FakeLLM`**. Đặt nó ở phần trace/stop condition: một agent đồ chơi trong đó "model" là một **list quyết định viết tay**, xem `step`, `trace`, `stopped_reason` thay đổi. Kiểm bằng `tools/pyrunner/tracer.py` và ghi số step vào report.
- In trace gọn: mỗi dòng dưới 70 ký tự, kiểu `step 1: lookup_order({'order_id': '1042'}) -> shipped`.

## Nội dung bài (boss chốt dàn ý, worker viết)
Opening (không heading): "Đơn #1042 của tôi bao giờ tới, và nếu trễ thì hoàn tiền cho tôi?" cần nhiều bước: tra đơn, xem ngày giao, kiểm chính sách, có thể hoàn tiền. Số bước phụ thuộc kết quả từng bước. Đó là chỗ dùng agent. Nhưng agent không có phanh thì đốt tiền và có thể làm việc nguy hiểm, nên bài này dạy cả vòng lặp lẫn phanh.

1. **Từ một lần gọi tool tới vòng lặp.**
   - Nhắc vòng một bước của p7-06.
   - **Picture in text** (fence `text`, giống hệt EN/VI): chu trình observe → think → act → observe…, có nhánh "final answer → stop".
   - Định nghĩa agent = model + tools + vòng lặp + điều kiện dừng.
   - **Bảng so sánh** `| approach | steps decided by | good for |`: workflow cố định / router một bước (p7-06) / agent.
2. **Vòng lặp agent tối giản.**
   - Hàm `run_agent(client, task, tools, registry, max_steps)`. Mỗi bước: `chat` → không có tool call thì trả lời cuối → có thì dispatch, append messages, ghi trace.
   - Chạy với `script` mô phỏng 3 bước (tra đơn → ước tính giao → trả lời). In trace.
   - **Mermaid** `flowchart LR` (≤ 8 node), có nhánh dừng do final answer và do max steps.
   - Callout `[!NOTE]` về script (xem mục Hành vi fake client).
3. **Trace: thấy được agent đã nghĩ gì.**
   - Mỗi bước ghi dict `{"step", "tool", "args", "observation"}`. In bảng trace.
   - **Trace table** `| step | tool | args | observation |` cho ví dụ §2.
   - Một câu: khi agent sai, trace là thứ đầu tiên bạn đọc. Ngoài đời người ta log trace vào hệ thống monitoring (nối sang phase 8).
4. **Điều kiện dừng: phanh của agent.**
   - Bốn lý do dừng, trả về trong `stopped_reason`:
     - `final`: có câu trả lời;
     - `max_steps`;
     - `repeat`: gọi lại **đúng** tool và tham số như bước trước, tức là bị kẹt;
     - `budget`: tổng `usage.total_tokens` vượt ngưỡng.
   - Demo mỗi lý do bằng output thật, dùng `script`.
   - Section này mời **Visualize** trên agent đồ chơi không gọi FakeLLM.
   - **Bảng** `| stopped_reason | what happened | what to do |`.
5. **Lỗi giữa chừng và tự sửa.**
   - Tool trả `"error: ..."` (từ dispatch của p7-06). Model đọc lỗi và thử tham số khác ở bước sau (script mô phỏng). Agent không crash.
   - Nói rõ giới hạn: nếu lỗi lặp lại thì guard `repeat` hoặc `max_steps` sẽ dừng.
6. **An toàn khi agent có quyền hành động.**
   - Agent nhiều bước làm rủi ro của p7-06 tăng lên: một chuỗi bước sai có thể dẫn tới hành động có side effect.
   - Demo: tool `issue_refund` chỉ được **đề xuất**. Agent dừng với `stopped_reason == "needs_approval"` và trả về hành động chờ duyệt, không tự chạy (human-in-the-loop).
   - Callout `[!WARNING]`: quyền tối thiểu (chỉ đưa tool cần thiết), giới hạn bước và ngân sách, người duyệt mọi hành động không đảo ngược được.
   - Một câu: khi nào **không** nên dùng agent.
7. **Lỗi thường gặp** (VI: `## 7. Lỗi thường gặp`), output thật:
   - Không có `max_steps` → script hết phần tử → `IndexError` (thông báo thật), ngoài đời thì tốn tiền vô hạn.
   - Không append tool result nên model "không thấy" quan sát và lặp lại cùng một tool. Guard `repeat` bắt được.
   - Trả về sau bước đầu tiên (quên lặp), nên câu trả lời thiếu.
   - Không ghi trace, nên không biết agent sai ở bước nào. Cho thấy output không trace so với có trace.
8. **Recap / Tóm tắt**: 4–6 gạch đầu dòng.

Thời lượng 14–16 phút.

`meta.yaml`:
- `phase: p7`, `order: 7`, `tags`: tag có sẵn trong `curriculum/topics.yaml` (vd `llm`, `loops`, `functions`). Không thêm tag mới.
- `prerequisites: [p7-06-tool-use]`
- `outcomes` khớp syllabus
- `review_by: "2027-05-01"`, không có `runner`
- `further_reading`: 1–2 link ổn định, trung lập (vd paper ReAct trên arXiv 2210.03629, một bài hướng dẫn chung về xây agent của một nhà cung cấp lớn). Mở thử và ghi vào report.

## Examples (3)
- `01_order_agent`: agent hỗ trợ đơn hàng với 3 tool chỉ đọc (tra đơn, ước tính giao, tra chính sách). Một nhiệm vụ 3 bước bằng `script`. In trace và câu trả lời cuối.
- `02_stop_conditions`: chạy cùng agent với 4 script khác nhau, cho ra lần lượt `final`, `max_steps`, `repeat`, `budget`. In `stopped_reason` và số bước của từng lần.
- `03_approval_gate`: agent đề xuất `issue_refund`, bị dừng ở `needs_approval`. Code "người duyệt" (biến bool trong code, không phải `input()`) duyệt thì mới chạy tool. In nhật ký.

## Exercises (2)
- `ex01-detect-repeat` (`kind: fill`): `is_repeat(history: list[tuple[str, dict]], name: str, args: dict) -> bool`.
  - True khi bước **ngay trước** có cùng tên tool **và** cùng args (so dict bằng `==`).
  - `history` rỗng thì False.
  - Các `___` trong thân hàm.
  - 5–6 test (parametrize): rỗng; khác tên; cùng tên khác args; cùng hệt → True; trùng với bước cũ hơn nhưng không phải bước ngay trước → False; args dict khác thứ tự key nhưng bằng nhau → True.
- `ex02-run-agent` (`kind: code`): `run_agent(client, task: str, tools: list[dict], registry: dict, max_steps: int = 5, token_budget: int | None = None) -> dict`.
  - Trả dict với các key:
    - `answer` (str, rỗng nếu không có);
    - `stopped_reason` (`"final"`, `"max_steps"`, `"repeat"`, `"budget"`);
    - `steps` (int, số lần gọi `chat`);
    - `trace` (list dict `{"step", "tool", "args", "observation"}`).
  - Mỗi lần gọi `chat`:
    - cộng `usage.total_tokens`, nếu có `token_budget` và tổng vượt thì dừng `budget`;
    - không có tool call thì dừng `final`;
    - có thì với tool call **đầu tiên**: nếu lặp đúng bước trước thì dừng `repeat` (không chạy tool);
    - không thì dispatch như p7-06 (tên lạ → `"error: unknown tool <name>"`; exception → `"error: <msg>"`; dict → `json.dumps`), append assistant và tool message, ghi trace.
  - Hết `max_steps` thì dừng `max_steps`.
  - Thứ tự kiểm (budget → final → repeat) ghi rõ trong prompt.
  - 8–9 test:
    - nhiệm vụ 3 bước bằng `script` → `final`, `steps == 3`, trace 2 phần tử đúng tool/args/observation;
    - không cần tool → `final`, `steps == 1`, trace rỗng;
    - script gọi mãi → `max_steps`;
    - script lặp cùng tool và args → `repeat`;
    - `token_budget` nhỏ → `budget`;
    - tool lạ → observation bắt đầu bằng `error: unknown tool`, agent tiếp tục;
    - tool raise → `error:`;
    - spy kiểm thứ tự message (assistant `tool_calls` rồi tool message đúng `tool_call_id`);
    - không sửa `tools` hay `registry`.
  - Starter import được và fail **mọi** test.
  - `alternatives/01_class_agent.py`: cài bằng class `Agent` có method `step()` (hoặc một cách khác thật sự khác), kèm `.md` so sánh.
- Hint 3 tầng đúng luật:
  - hint 2 chỉ là các bước bằng lời, không có biểu thức Python hoàn chỉnh;
  - hint 3 là skeleton, mỗi hàm chừa đúng một `...` ở dòng cốt lõi, và không có câu nào sau skeleton nói ra phần còn thiếu;
  - ghép hint 2 và hint 3 không ra nguyên solution. Với ex02, để trống **cả phần xử lý một tool call** (kiểm repeat, dispatch, append, trace) thành một `...`.

## Quiz
- 15–18 câu, mỗi loại `mcq`, `output`, `fill`, `parsons` ít nhất 2. Khoảng 5 dễ, 7 vừa, 3 khó. 6 flashcard.
- **mcq cân độ dài:** `len(đúng) <= 1.2 × trung bình len(distractor)` ở cả en và vi. Đáp án đúng không kèm lý do. Đáp án đúng là phương án dài nhất duy nhất ở tối đa 1/3 số câu mcq.
- Phải có câu về:
  - agent khác workflow ở đâu;
  - vì sao cần `max_steps`;
  - phát hiện lặp;
  - ngân sách token;
  - trace dùng để làm gì;
  - lỗi tool trả về như observation;
  - human-in-the-loop cho side effect;
  - khi nào không nên dùng agent.

## Tiêu chí hoàn thành (checklist)
1. [ ] Đủ file theo layout CONTENT_GUIDE. `meta.yaml` đúng như trên, tag có trong topics.yaml.
2. [ ] Lesson đúng dàn ý, đủ: picture in text, mermaid, trace table, bảng so sánh, một lời mời Visualize (không gọi FakeLLM), callout `[!NOTE]` về script, callout `[!WARNING]`.
3. [ ] Code giữa EN và VI giống hệt, chỉ khác comment. Số dòng mermaid bằng nhau. Fence `text` giống hệt.
4. [ ] Mọi khối python, example và quiz chạy với `-W error`, stderr rỗng, output khớp. Không `eval`/`exec`/`subprocess`, không vòng lặp không giới hạn.
5. [ ] Mọi trace trong bài hợp lý với người đọc.
6. [ ] Exercise: starter fail **mọi** test (số pass với starter phải là 0, ghi vào report). Solution và alternative pass (pytest **và** browser runner trong validate).
7. [ ] Script độ dài mcq in `violations: 0`.
8. [ ] Bản VI tự nhiên, xưng "bạn", thuật ngữ giữ tiếng Anh kèm giải nghĩa lần đầu.
9. [ ] Report ghi: số step khối Visualize, link further_reading đã mở. `glossary.yaml` chỉ có dòng thêm.

## Lệnh kiểm tra
Từ gốc repo:
```
uv run python tools/validate.py --path curriculum/phase-07-llm/p7-07-agents
uv run python -m pytest curriculum/phase-07-llm
uv run ruff check curriculum/phase-07-llm
grep -rnE "input\(|time\.sleep|requests\.|urllib|open\(|eval\(|exec\(|subprocess|os\.system|while True" curriculum/phase-07-llm/p7-07-agents --include=*.py
git diff --numstat curriculum/glossary.yaml
uv run python tools/build_content.py
git status --short
```
Script độ dài mcq (phải in `violations: 0`):
```
uv run python -c "
import yaml
bad=0
for q in yaml.safe_load(open('curriculum/phase-07-llm/p7-07-agents/quiz.yaml',encoding='utf-8'))['questions']:
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
- grep rỗng. Khối code trong `.md` không được có `while True`; kiểm thêm bằng `grep -n "while True" curriculum/phase-07-llm/p7-07-agents/*.md`.
- glossary chỉ có dòng thêm.

## Ghi chú cho worker
- Đọc `docs/CONTENT_GUIDE.md` (cả mục Fake LLM client), `packages/pyai_llm/README.md` và `pyai_llm.py`, mục p7 trong `curriculum/syllabus.yaml`, `curriculum/topics.yaml`. Dùng bài p7-06 làm mẫu, đặc biệt `dispatch` và định dạng message.
- Test chỉ dùng: assert, pytest.raises, pytest.approx, pytest.mark.parametrize, `@pytest.fixture` định nghĩa trong file test.
- Dùng `uv run python -m pytest`, không dùng `uv run pytest`. Kiểm warning bằng `uv run python -W error <file>`.
- Mọi lệnh phải tự kết thúc. Không chạy server.

## Trạng thái
- Bước hiện tại: xong, commit `1de7ae3` (đạt vòng 1; boss kiểm: validate toàn bộ 0 lỗi trên 46 bài, typecheck + build; trong app qua Pyodide: 4 điều kiện dừng §4 ra đúng, starter ex02 0/9, solution qua hết; chờ user duyệt commit)
- Vòng: 1/3
- Số lần swap: 0
- Fallback: không
- Model: Gemini 4 Hydrogen (High)
- Lần gọi 1: MCP ngắt sau 1800s im lặng (timeout, không phải quota); worker đã xong và ghi report, tiến trình agy treo đã được boss dừng.
