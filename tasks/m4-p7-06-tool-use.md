# M4 bước 16: bài p7-06 Tool use

## Mục tiêu
Viết bài `p7-06-tool-use` trong `curriculum/phase-07-llm/`, đúng `docs/CONTENT_GUIDE.md` và song ngữ EN/VI.
- Bài **chạy trong Pyodide** (không có `runner: local`). Dùng `FakeLLM` với tham số `tools=`. Không mạng, không key, không ghi file. Các "tool" là **hàm Python thuần, tất định**, chạy cục bộ: thời tiết lấy từ dict giả, đổi tiền theo tỉ giá cố định, tra đơn hàng trong dict. Không gọi API thật.
- Người học đã xong:
  - p7-01: messages, roles;
  - p7-02: JSON schema, validate, không `eval`;
  - p7-05: RAG.
- Ý chính:
  - LLM chỉ sinh văn bản. Tool use cho phép model **đề nghị** gọi một hàm, kèm tên và tham số có cấu trúc.
  - **Code của bạn** quyết định có chạy hay không, chạy hàm đó, rồi gửi kết quả lại để model trả lời cuối.
  - Model không bao giờ tự chạy code. Mọi tham số từ model là input không tin cậy.
- Bài sau p7-07 (agents) sẽ lặp vòng này nhiều bước. Bài này giữ ở **một vòng tool**, cùng một giới hạn số vòng đơn giản.
- Bài mẫu: `curriculum/phase-07-llm/p7-05-rag/`.

## Hành vi fake tool calling (boss đã chạy thử; worker đọc lại bước 3 và 4 trong `FakeLLM.chat` và `_extract_schema_values`)
- Truyền `tools=[{"name", "description", "parameters": <JSON schema>}]`. Fake model chọn tool có **nhiều từ chung nhất** (từ ≥ 3 ký tự, chữ thường, không stemming, đếm cả stopword) giữa `name + description` và tin nhắn user cuối.
  - Chỉ cần **≥ 1 từ chung** là gọi tool. Vì vậy description chứa từ phổ biến ("the", "for", "and") có thể khiến tool bị gọi nhầm.
  - Viết description ngắn, không có stopword, để ví dụ hợp lý. Đồng thời biến chuyện này thành bài học: description tốt rất quan trọng (model thật cũng chọn tool dựa vào description).
- Kết quả đã thử:
  - `'What is the weather in Hanoi?'` → `ToolCall(id='call_1', name='get_weather', arguments={'city': 'Hanoi', 'unit': ''})`, `finish_reason='tool_calls'`, `content=None`.
    - Tham số tùy chọn không tìm thấy được điền **giá trị rỗng giả** (`''`, `0`, `False`), giống p7-02. Code dispatch phải xử lý chuyện này (bỏ qua giá trị rỗng, hoặc dùng mặc định), và bài nên nói ra.
  - `'Convert 100 dollars to currency EUR'` → `convert_currency(amount=100.0, to='EUR')`.
  - `'Tell me a joke'` (không từ chung) → trả lời thường, `tool_calls=[]`, `finish_reason='stop'`.
  - Gửi lại: `[user, {"role": "assistant", "content": None, "tool_calls": [...]}, {"role": "tool", "tool_call_id": "call_1", "content": "31C and sunny"}]` → `'Based on the tool result: 31C and sunny'`, `finish_reason='stop'`.
- `ToolCall.id` tăng dần theo client (`call_1`, `call_2`, …), nên mỗi khối phải tạo client mới để output tất định.
- `FakeLLM(script=[{"tool_calls": [{"name": ..., "arguments": {...}}]}, "final text"])` dùng để giả lập: model gọi tool không tồn tại, tham số sai kiểu, hoặc gọi tool nhiều lần (để test giới hạn vòng).
- Kiểm xem `_validate_messages` chấp nhận dạng message nào (assistant có `tool_calls`, role `tool` có `tool_call_id`). Dùng đúng dạng đó trong toàn bài và ghi vào report.
- Mọi output in ra phải là output **thật**.

## File được phép sửa/tạo
- Thư mục mới `curriculum/phase-07-llm/p7-06-tool-use/` và mọi file bên trong.
- `curriculum/glossary.yaml`: chỉ **thêm** thuật ngữ chưa có (tool use, function calling, tool schema, tool call, dispatch, side effect, allowlist). Thuật ngữ đã có thì bỏ qua.
- `tasks/m4-p7-06-tool-use.report.md`

## Không được đụng
- `packages/`, `apps/`, `tools/`, `curriculum/syllabus.yaml`, `curriculum/topics.yaml`, các bài p7-01 … p7-05, các phase khác, `exams/`.
- Không xóa file, không `git commit`, **không chạy `pnpm --filter web build`**, không chạy server ở foreground.
- Không sửa `pyai_llm`. Quirk nào gặp thì ghi vào report.

## Quy tắc code (bắt buộc)
- Quy tắc phase 7: không `input()`, mạng, `time.sleep`, ghi file; sạch với `-W error`; tất định.
- **Không** `eval`/`exec`/`subprocess`/`os.system` ở bất cứ đâu, kể cả "ví dụ sai". Chỉ **nói** trong văn bản là không được làm vậy.
- Kết quả tool gửi về model phải là **chuỗi**. Kết quả dạng dict thì `json.dumps`.
- Khối mời **Visualize** phải dưới 600 step và **không gọi `FakeLLM`**. Đặt nó ở phần dispatch: một `ToolCall` dựng tay (hoặc dict), tra registry, kiểm tham số, gọi hàm, dựng message `tool`. Kiểm bằng `tools/pyrunner/tracer.py` và ghi số step vào report.
- Định dạng message thống nhất trong toàn bài:
  - assistant có tool call: `{"role": "assistant", "content": None, "tool_calls": [{"id", "name", "arguments"}]}`;
  - kết quả tool: `{"role": "tool", "tool_call_id": ..., "content": str}`.

## Nội dung bài (boss chốt dàn ý, worker viết)
Opening (không heading): hỏi chatbot "thời tiết Hà Nội lúc này?" hay "đơn hàng #1042 đang ở đâu?" thì model không biết, vì dữ liệu nằm trong hệ thống của bạn. Tool use để model **xin** gọi hàm của bạn. Code của bạn chạy hàm và đưa kết quả lại.

1. **Model đề nghị, code của bạn thực thi.**
   - Một lời gọi `chat(..., tools=[weather_tool])`: in `finish_reason`, `content` và `tool_calls[0].name/arguments`.
   - Nhấn mạnh `content` là `None`: model chưa trả lời mà đang **hỏi xin** chạy tool.
   - **Picture in text** (fence `text`, giống hệt EN/VI): ai làm gì, theo dạng cột `you | model | your code`.
2. **Mô tả tool bằng schema.**
   - Tool là dict `name` / `description` / `parameters` (JSON schema của p7-02).
   - Hàm nhỏ `tool_schema(func_name, description, params, required)` dựng dict.
   - **Bảng** `| field | purpose | tip |`.
   - Thí nghiệm description: hai tool cùng câu hỏi, description mơ hồ có stopword thì bị chọn nhầm, description rõ thì chọn đúng. Output thật.
3. **Vòng tool hoàn chỉnh.**
   - Các bước:
     1. `chat` với tools;
     2. nếu `finish_reason == "tool_calls"` thì dispatch;
     3. append assistant message (có `tool_calls`) **và** tool message;
     4. `chat` lần 2;
     5. in câu trả lời cuối.
   - **Mermaid** `flowchart LR` (≤ 8 node), có nhánh "no tool call → answer".
   - **Trace table** `| step | role | content / tool call |` liệt kê messages qua từng bước.
4. **Registry và dispatch an toàn.**
   - `REGISTRY = {"get_weather": get_weather, ...}`.
   - Hàm `dispatch(call, registry) -> str`:
     - tên lạ thì trả `"error: unknown tool <name>"`;
     - kiểm tham số bắt buộc;
     - bỏ giá trị rỗng giả của tham số tùy chọn;
     - gọi `func(**args)`;
     - bắt exception thành `"error: ..."`;
     - dict thì `json.dumps`.
   - Section này mời **Visualize** (không FakeLLM).
   - Nói rõ: lỗi trả về **như một tool result** để model biết và trả lời tử tế, thay vì làm sập chương trình.
5. **Nhiều tool và giới hạn vòng.**
   - Ba tool (thời tiết, đổi tiền, tra đơn). Ba câu hỏi, mỗi câu fake model chọn đúng tool.
   - Dùng `script` mô phỏng model cứ gọi tool mãi, chặn bằng `max_rounds` rồi trả thông báo dừng. Một câu nối sang p7-07 agents.
6. **An toàn: tool có tác dụng phụ.**
   - Phân biệt tool chỉ đọc (tra cứu) với tool có **side effect** (gửi email, hoàn tiền, xóa). Side effect cần allowlist, cần người xác nhận, cần giới hạn số tiền.
   - Demo bằng tool `issue_refund(order_id, amount)`: code chặn khi `amount` vượt ngưỡng, hoặc khi chưa có `confirmed=True` từ phía người dùng. Output thật.
   - Callout `[!WARNING]`: tham số từ model là input không tin cậy (nối với prompt injection ở p7-05). Không bao giờ đưa thẳng vào shell, SQL ghép chuỗi, hay `eval`.
7. **Lỗi thường gặp** (VI: `## 7. Lỗi thường gặp`), output thật:
   - Quên append assistant message có `tool_calls` trước tool message. Cho thấy fake client báo gì, hoặc nếu nó không báo thì nói model thật sẽ từ chối (ghi trung thực).
   - Gọi `func(args)` thay vì `func(**args)` → `TypeError` (thông báo thật).
   - Tool trả dict thay vì chuỗi. Sửa bằng `json.dumps`.
   - Tin giá trị rỗng giả `''` của tham số tùy chọn, ví dụ đơn vị nhiệt độ rỗng.
8. **Recap / Tóm tắt**: 4–6 gạch đầu dòng.

Thời lượng 14–16 phút.

`meta.yaml`:
- `phase: p7`, `order: 6`, `tags`: tag có sẵn trong `curriculum/topics.yaml` (vd `llm`, `functions`, `dicts`). Không thêm tag mới.
- `prerequisites: [p7-02-structured-output]`
- `outcomes` khớp syllabus
- `review_by: "2027-05-01"`, không có `runner`
- `further_reading`: 1–2 link ổn định, trung lập (vd tài liệu chung về function calling của một nhà cung cấp lớn, hoặc JSON Schema reference). Mở thử và ghi vào report.

## Examples (3)
- `01_order_assistant`: 2 tool (tra đơn, ước tính ngày giao) trên dữ liệu dict. Hai câu hỏi đi trọn vòng tool. In từng bước gọn: tool nào, args, kết quả, câu trả lời cuối.
- `02_safe_dispatch`: `dispatch` chịu lỗi, chạy trên 5 `ToolCall` dựng tay (hoặc từ `script`): hợp lệ, tool lạ, thiếu tham số, tham số sai kiểu, hàm raise. In kết quả từng cái.
- `03_refund_guard`: tool có side effect `issue_refund`, kèm guard (ngưỡng tiền, cần xác nhận). Dùng `script` mô phỏng model đề nghị hoàn tiền nhỏ (được duyệt) và lớn (bị chặn). In nhật ký hành động.

## Exercises (2)
- `ex01-tool-schema` (`kind: fill`): `tool_schema(name: str, description: str, params: dict[str, str], required: list[str]) -> dict`.
  - `params` map tên tham số tới kiểu JSON (`"string"`, `"number"`, …).
  - Trả dict `{"name", "description", "parameters": {"type": "object", "properties": {p: {"type": t}}, "required": required}}`.
  - Raise `ValueError` khi `required` chứa tên không có trong `params`, hoặc khi kiểu không thuộc 4 kiểu cơ bản.
  - Các `___` trong thân hàm.
  - 5–6 test: hình dạng đúng; properties đúng; required giữ thứ tự; required lạ → `ValueError`; kiểu lạ → `ValueError`; schema dùng được với `FakeLLM(...).chat(..., tools=[...])` và chọn được tool.
- `ex02-run-tools` (`kind: code`): `run_with_tools(client, question: str, tools: list[dict], registry: dict, max_rounds: int = 3) -> tuple[str, list[str]]`.
  - Trả `(final_answer, called)`, trong đó `called` là danh sách tên tool đã chạy theo thứ tự.
  - Mỗi vòng:
    - `chat(messages, tools=tools)`;
    - không có tool call thì trả `content`;
    - có thì với **mỗi** tool call: dispatch (tên lạ → `"error: unknown tool <name>"`; exception → `"error: <msg>"`; dict → `json.dumps`), append assistant message rồi các tool message, sang vòng sau.
  - Hết `max_rounds` vẫn còn tool call thì trả `("stopped: too many tool calls", called)`.
  - Không sửa list `tools` hay `registry`.
  - 8 test:
    - câu hỏi thời tiết → câu trả lời chứa kết quả tool và `called == ["get_weather"]`;
    - câu không cần tool → `called == []`;
    - tool lạ qua `script` → không crash, tool message chứa `error: unknown tool`;
    - hàm raise → `error:`;
    - kết quả dict được `json.dumps`;
    - `script` gọi tool 5 lần với `max_rounds=2` → `stopped`;
    - spy kiểm thứ tự message: assistant có `tool_calls` đứng ngay trước tool message, đúng `tool_call_id`;
    - kiểu trả về.
  - Starter import được và fail **mọi** test.
  - `alternatives/01_dispatch_helper.py`: tách `dispatch` thành hàm riêng (hoặc một cách khác thật sự khác), kèm `.md` so sánh.
- Hint 3 tầng đúng luật:
  - hint 2 chỉ là các bước bằng lời, không có biểu thức Python hoàn chỉnh;
  - hint 3 là skeleton, mỗi hàm chừa đúng một `...` ở dòng cốt lõi, và không có câu nào sau skeleton nói ra phần còn thiếu;
  - ghép hint 2 và hint 3 không ra nguyên solution. Với ex02, để trống **cả phần dispatch một tool call** thành một `...`.

## Quiz
- 15–18 câu, mỗi loại `mcq`, `output`, `fill`, `parsons` ít nhất 2. Khoảng 5 dễ, 7 vừa, 3 khó. 6 flashcard.
- **mcq cân độ dài:** `len(đúng) <= 1.2 × trung bình len(distractor)` ở cả en và vi. Đáp án đúng không kèm lý do. Đáp án đúng là phương án dài nhất duy nhất ở tối đa 1/3 số câu mcq.
- Phải có câu về:
  - model không tự chạy hàm;
  - `content is None` khi có tool call;
  - vai trò của description;
  - thứ tự message (assistant tool_calls rồi mới tool);
  - `tool_call_id`;
  - `func(**args)`;
  - trả lỗi như một tool result;
  - side effect và xác nhận;
  - `max_rounds`.

## Tiêu chí hoàn thành (checklist)
1. [ ] Đủ file theo layout CONTENT_GUIDE. `meta.yaml` đúng như trên, tag có trong topics.yaml.
2. [ ] Lesson đúng dàn ý, đủ: picture in text, mermaid, trace table, bảng, một lời mời Visualize (không gọi FakeLLM), callout `[!WARNING]`.
3. [ ] Code giữa EN và VI giống hệt, chỉ khác comment. Số dòng mermaid bằng nhau. Fence `text` giống hệt.
4. [ ] Mọi khối python, example và quiz chạy với `-W error`, stderr rỗng, output khớp. Không `eval`/`exec`/`subprocess`.
5. [ ] Mọi lựa chọn tool trong bài hợp lý với người đọc. Report ghi các quirk đã gặp và dạng message mà `_validate_messages` chấp nhận.
6. [ ] Exercise: starter fail **mọi** test (số pass với starter phải là 0, ghi vào report). Solution và alternative pass (pytest **và** browser runner trong validate).
7. [ ] Script độ dài mcq in `violations: 0`.
8. [ ] Bản VI tự nhiên, xưng "bạn", thuật ngữ giữ tiếng Anh kèm giải nghĩa lần đầu.
9. [ ] Report ghi: số step khối Visualize, link further_reading đã mở. `glossary.yaml` chỉ có dòng thêm.

## Lệnh kiểm tra
Từ gốc repo:
```
uv run python tools/validate.py --path curriculum/phase-07-llm/p7-06-tool-use
uv run python -m pytest curriculum/phase-07-llm
uv run ruff check curriculum/phase-07-llm
grep -rnE "input\(|time\.sleep|requests\.|urllib|open\(|eval\(|exec\(|subprocess|os\.system" curriculum/phase-07-llm/p7-06-tool-use
git diff --numstat curriculum/glossary.yaml
uv run python tools/build_content.py
git status --short
```
Script độ dài mcq (phải in `violations: 0`):
```
uv run python -c "
import yaml
bad=0
for q in yaml.safe_load(open('curriculum/phase-07-llm/p7-06-tool-use/quiz.yaml',encoding='utf-8'))['questions']:
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
- grep (quét **mọi** file, kể cả `.md` và `.yaml`) chỉ được trúng các dòng **văn bản** nói "đừng dùng eval/exec/subprocess", không trúng dòng code. Ghi kết quả grep vào report.
- glossary chỉ có dòng thêm (cột xóa = 0).

## Ghi chú cho worker
- Đọc `docs/CONTENT_GUIDE.md` (cả mục Fake LLM client), `packages/pyai_llm/README.md` và `pyai_llm.py`, mục p7 trong `curriculum/syllabus.yaml`, `curriculum/topics.yaml`. Dùng bài p7-05 làm mẫu.
- Test chỉ dùng: assert, pytest.raises, pytest.approx, pytest.mark.parametrize, `@pytest.fixture` định nghĩa trong file test.
- Dùng `uv run python -m pytest`, không dùng `uv run pytest`. Kiểm warning bằng `uv run python -W error <file>`.
- Mọi lệnh phải tự kết thúc. Không chạy server.

## Trạng thái
- Bước hiện tại: xong, commit `0add225` (đạt vòng 2; boss kiểm: validate toàn bộ 0 lỗi trên 45 bài, typecheck + build; trong app qua Pyodide: khối §5 ba tool + loop guard ra đúng, starter ex02 0/8, solution qua hết; chờ user duyệt commit)
- Vòng: 2/3
- Số lần swap: 0
- Fallback: không
- Model: Gemini 4 Hydrogen (High)

## Feedback vòng 2
Boss đã chạy lại: validate bài 0 lỗi, pytest 94 passed, ruff sạch, grep rỗng, glossary chỉ có dòng thêm. Nội dung tốt. Chỉ sửa **một** điểm sư phạm, không đụng gì khác:

1. **Description kiểu "liệt kê từ khóa" dễ dạy sai** (`lesson.en.md` và `lesson.vi.md`, §2; bảng `field | purpose | tip`).
   - Các description "clear" như `"weather city temperature forecast"` chỉ là danh sách từ khóa. Kiểu này hợp với FakeLLM (đếm từ chung), nhưng **không** phải cách viết tốt cho model thật. Model thật đọc câu đầy đủ, nên description tốt là một câu rõ ràng nói khi nào dùng tool, vd "Get the current weather for a city."
   - Sửa như sau:
     - (a) Ngay sau khối so sánh vague/clear ở §2, thêm callout `[!NOTE]` (EN và VI, cùng vị trí). Nội dung: description trong bài viết kiểu từ khóa vì `FakeLLM` chọn tool bằng cách đếm từ chung. Với model thật, hãy viết **một câu rõ ràng** nói tool làm gì và khi nào dùng, kèm ví dụ một câu như trên. Nguyên tắc chung giống nhau: cụ thể, phân biệt được với các tool khác, không lan man.
     - (b) Sửa cột `tip` của dòng `description` trong bảng cho khớp: "One clear sentence: what it does and when to use it; make tools easy to tell apart" (VI tương ứng).
     - (c) Câu văn ngay sau khối code ("Short, specific descriptions fix the routing immediately.") giữ ý nhưng không được ngụ ý rằng liệt kê từ khóa là cách tốt nhất.
   - **Không** đổi code hay output.

Sau khi sửa, chạy lại:
```
uv run python tools/validate.py --path curriculum/phase-07-llm/p7-06-tool-use
```
Cập nhật report: thêm mục "Vòng 2".
