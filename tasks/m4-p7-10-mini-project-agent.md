# M4 bước 20: p7-10 Mini-project agent

## Mục tiêu
Viết bài `p7-10-mini-project-agent` (`kind: project`) trong `curriculum/phase-07-llm/`, đúng `docs/CONTENT_GUIDE.md` và song ngữ EN/VI.
- Bài **chạy trong Pyodide** (không có `runner: local`). Dùng `FakeLLM` với `tools=` và `script=`. Không mạng, không key, không ghi file. Tool là hàm Python thuần, tất định, chạy trên dict dữ liệu trong code.
- Đây là mini-project trọng yếu của phase 7 (vào portfolio ở bước docs sau). Người học ghép p7-06 (tool schema, dispatch) và p7-07 (vòng agent, trace, điều kiện dừng, duyệt hành động) thành **một agent hỗ trợ đơn hàng hoàn chỉnh** và **kiểm thử tất định** nó bằng một bộ kịch bản.
- Outcome syllabus: "Build a tool-using agent with safe step limits", "Test multi-step tool execution deterministically".
- Mẫu cấu trúc và giọng văn: `curriculum/phase-07-llm/p7-09-mini-project-rag/` và `curriculum/phase-05-ml/p5-05-mini-project/` (các Part, báo cáo trung thực, `## Recap` và `## Take it further` không đánh số). Mẫu kỹ thuật: p7-06 (`run_with_tools`, dispatch), p7-07 (`run_agent`, `stopped_reason`, `03_approval_gate`).

## Hành vi fake client cần biết (worker đọc lại `FakeLLM.chat` trong `packages/pyai_llm/pyai_llm.py`)
- Mặc định: model chọn tool có nhiều từ chung nhất với message user cuối (từ ≥ 3 ký tự, so với tên + description tool) và tự trích tham số; sau một message `role == "tool"` model **luôn** trả `"Based on the tool result: <content>"` và dừng, **không tự chain**.
- Vì vậy mọi kịch bản nhiều bước dùng `FakeLLM(script=[...])`, script đóng vai "bộ não" của model. Nói thật điều này trong một callout `[!NOTE]` (như p7-07): với model thật, quyết định đến từ model; còn vòng lặp, guard, duyệt và test do code của bạn viết thì giống hệt. Có đúng **một** ví dụ không dùng script (một bước, model tự chọn tool) để nối với p7-06.
- `script` hết phần tử thì raise `IndexError`; `ToolCall.id` tăng dần theo client: mỗi kịch bản tạo client mới.
- `resp.usage.total_tokens` có thật: dùng cho ngân sách token.
- Mọi output trong bài phải là output **thật**.
- **Không sửa `pyai_llm`.**

## File được phép sửa/tạo
- Thư mục mới `curriculum/phase-07-llm/p7-10-mini-project-agent/` và mọi file bên trong.
- `curriculum/glossary.yaml`: chỉ **thêm** thuật ngữ chưa có (vd scenario test, golden trajectory, side effect, allowlist). Đã có thì bỏ qua.
- `tasks/m4-p7-10-mini-project-agent.report.md`

## Không được đụng
- `packages/`, `apps/`, `tools/`, `curriculum/syllabus.yaml`, `curriculum/topics.yaml`, `curriculum/portfolio.yaml`, các bài p7-01 … p7-09, các phase khác, `exams/`.
- Không xóa file, không `git commit`, **không chạy `pnpm --filter web build`**, không chạy server ở foreground.

## Quy tắc code (bắt buộc)
- Quy tắc phase 7: không `input()`, mạng, `time.sleep`, ghi file; sạch với `-W error`; tất định.
- **Không** `eval(`/`exec(`/`subprocess`/`os.system`. Không `while True`; mọi vòng agent có `max_steps`.
- Định dạng message như p7-06/p7-07: assistant có tool call `{"role": "assistant", "content": None, "tool_calls": [{"id", "name", "arguments"}]}`; kết quả tool `{"role": "tool", "tool_call_id": ..., "content": str}`.
- Mỗi khối python tự chạy được. Dữ liệu dùng chung giữ gọn: 3–4 đơn hàng, 4 tool (3 chỉ đọc, 1 có side effect).
- Khối mời **Visualize** dưới 600 step và **không gọi `FakeLLM`**: đặt ở Part 4 (chạy bộ kịch bản đồ chơi, "model" là list quyết định viết tay, xem `passed` tăng). Kiểm bằng `tools/pyrunner/tracer.py`, ghi số step vào report.
- In trace và báo cáo gọn: mỗi dòng dưới 70 ký tự.

## Bối cảnh dự án
Agent hỗ trợ khách của một shop. Dữ liệu: `ORDERS` (vd `"1042": {"status": "delayed", "carrier": "FastShip", "total": 59.0, "days_late": 4}`), chính sách hoàn tiền (vd trễ ≥ 3 ngày được hoàn tối đa 20% hoặc một số cụ thể).
Tool:
- `lookup_order(order_id)` (chỉ đọc), `track_shipment(carrier, order_id)` hoặc tương đương (chỉ đọc), `check_refund_policy(days_late)` (chỉ đọc);
- `issue_refund(order_id, amount)` (**side effect**, phải được duyệt).

## Nội dung bài (boss chốt dàn ý, worker viết)
Opening (không heading): sếp muốn một agent trả lời "đơn của tôi đâu, trễ thì hoàn tiền giúp tôi", nhưng không được tự ý hoàn tiền, không được chạy vô hạn, và phải có bộ test chứng minh nó hành xử đúng trước khi lên production.

1. **The plan / Kế hoạch.**
   - Mermaid `flowchart LR` (≤ 8 node): task → agent loop → toolbox (allowlist, validate) → read-only tools / side-effect tool → approval gate → answer + trace → scenario tests.
   - Bảng `| part | what you build | from lesson |` nối từng part với p7-06/p7-07/p7-08.
   - Luật chơi: mọi hành động có side effect cần duyệt; mọi vòng có giới hạn; hành vi được chứng minh bằng test kịch bản, không bằng "chạy thử thấy ổn".
2. **Dữ liệu và tool.** In bảng đơn hàng; schema 4 tool. **Bảng** `| tool | reads/writes | needs approval |`.
3. **Part 1: toolbox an toàn.**
   - Đăng ký tool kèm schema và cờ `side_effect`. Gọi tool qua một lớp kiểm: tên không có trong allowlist → `"error: unknown tool <name>"`; thiếu tham số bắt buộc → `"error: missing <arg>"`; tham số lạ bị bỏ; exception → `"error: <msg>"`; dict → `json.dumps`.
   - Demo từng trường hợp với output thật.
   - Có ví dụ một bước không dùng script (model tự chọn tool) ở đây.
4. **Part 2: vòng agent có giới hạn.**
   - Vòng như p7-07 với `stopped_reason` `final`, `max_steps`, `repeat`, `budget`. Chạy kịch bản 3 bước (tra đơn → tra chính sách → trả lời) bằng `script`. In trace.
   - Callout `[!NOTE]` về script.
   - **Trace table** `| step | tool | args | observation |`.
5. **Part 3: cổng duyệt cho side effect.**
   - Khi model gọi tool `side_effect=True`: gọi hàm `approve(name, args) -> bool` do code truyền vào. True → chạy tool và tiếp tục; False hoặc không có `approve` → dừng `needs_approval`, trả `pending = {"tool", "args"}`, **không** chạy tool. Nhật ký ghi rõ ai duyệt.
   - Demo cả hai nhánh (duyệt / không duyệt) và một quy tắc duyệt bằng code (vd tự từ chối khi `amount` vượt mức chính sách).
   - Callout `[!WARNING]`: quyền tối thiểu, không bao giờ để model tự duyệt chính nó, log mọi hành động không đảo ngược được.
6. **Part 4: kiểm thử tất định bằng kịch bản.**
   - Một kịch bản = `{"name", "task", "script", "approve", "expect": {"stopped_reason", "tools", "answer_contains"}}`. `tools` là **golden trajectory** (danh sách tên tool theo thứ tự).
   - Bộ 6–8 kịch bản: đường vui; đơn không tồn tại (tool trả lỗi, agent vẫn trả lời); bị kẹt lặp → `repeat`; quá bước → `max_steps`; hoàn tiền được duyệt; hoàn tiền bị từ chối → `needs_approval`; vượt ngân sách → `budget`. Chạy và in bảng `| scenario | expected | got | pass |`.
   - Ít nhất **một** kịch bản fail thật ở phiên bản đầu (vd agent bản đầu chưa có guard nào đó), sau khi sửa code thì pass. Cho thấy test bắt được lỗi.
   - Lời mời **Visualize** ở khối bộ kịch bản đồ chơi (không gọi FakeLLM).
   - Một câu nối với pytest: mỗi kịch bản có thể là một test `parametrize`.
7. **Part 5: báo cáo.**
   - In báo cáo: số kịch bản pass/tổng, theo từng `stopped_reason`, tổng token, kịch bản fail kèm lý do (trajectory khác / stopped_reason khác / answer thiếu).
   - Callout `[!TIP]`: test kịch bản chỉ kiểm code điều khiển với quyết định đã viết sẵn; với model thật cần thêm eval trên nhiều task (nối p7-08), vì model thật có thể chọn khác script.
8. **Lỗi thường gặp** (VI: `## 8. Lỗi thường gặp`), output thật, 3–4 lỗi:
   - Chạy tool side effect trước khi hỏi duyệt (hoàn tiền đã xảy ra rồi mới hỏi).
   - So trajectory bằng set thay vì list → bỏ sót sai thứ tự.
   - Dùng chung một client cho nhiều kịch bản → script cạn hoặc `ToolCall.id` lệch, test phụ thuộc thứ tự.
   - Test chỉ kiểm câu trả lời cuối, không kiểm tool đã gọi → agent "đúng nhờ may".
9. `## Recap` (VI `## Tóm tắt`), 4–6 gạch đầu dòng, không đánh số.
10. `## Take it further` (VI `## Làm thêm`), không đánh số, 3–4 gợi ý (thêm tool, chạy bộ kịch bản với model thật đọc key từ `.env` trong khối `bash` dùng tên trung lập `LLM_API_KEY`, ghi trace vào monitoring ở phase 8, đo tỉ lệ thành công trên nhiều task).

Thời lượng 40–50 phút.

`meta.yaml`:
- `phase: p7`, `order: 10`, `kind: project`, `tags`: tag có sẵn trong `curriculum/topics.yaml` (vd `llm`, `agents`, `testing` nếu có). Không thêm tag mới.
- `prerequisites: [p7-07-agents]`
- `outcomes`: 2 outcome của syllabus giữ nguyên, có thể thêm 1–2 outcome cụ thể.
- `review_by: "2027-05-01"`, không có `runner`.
- `further_reading`: 1–2 link ổn định, trung lập (mở thử, ghi vào report).

## Examples (3)
- `01_toolbox`: đăng ký tool, gọi từng trường hợp lỗi/thành công, in observation.
- `02_agent_with_approval`: chạy agent trên 3 task (chỉ đọc; hoàn tiền được duyệt; hoàn tiền bị từ chối), in trace, `stopped_reason`, `pending`.
- `03_scenario_suite`: chạy bộ kịch bản đầy đủ, in bảng pass/fail và báo cáo.

## Exercises (2, đều `kind: project`)
Bài học hướng dẫn từng bước, nhưng hàm trong exercise phải **ghép lại và có yêu cầu riêng**; **không** hàm nào trong solution trùng nguyên văn (thân hàm) một khối trong lesson/examples. Kiểm bằng AST như p7-09 và ghi vào report.
- `ex01-toolbox`: class `ToolBox`.
  - `register(fn, schema: dict, side_effect: bool = False) -> None`; tên tool lấy từ `schema["name"]`; đăng ký trùng tên → `ValueError`.
  - `schemas() -> list[dict]`: list schema theo thứ tự đăng ký (bản sao, sửa kết quả không ảnh hưởng toolbox).
  - `is_side_effect(name) -> bool` (tên lạ → False).
  - `call(name, args: dict) -> str`: tên lạ → `"error: unknown tool <name>"`; thiếu tham số `required` → `"error: missing <arg>"` (arg đầu tiên thiếu theo thứ tự `required`); bỏ tham số không có trong `properties`; exception → `"error: <msg>"`; dict/list → `json.dumps`; khác → `str`. Không sửa `args` đầu vào.
  - 9–11 test. Starter import được và fail **mọi** test. `alternatives/01_*.py` cách khác thật sự (vd lưu bằng một dict `name -> (fn, schema, side_effect)` thay vì nhiều dict, hoặc dùng dataclass), kèm `.md`.
- `ex02-run-scenarios`: `run_scenario(scenario: dict, toolbox, make_client) -> dict` và `summarize(results: list[dict]) -> list[str]`.
  - `run_scenario` tự tạo client bằng `make_client(scenario["script"])`, chạy agent (vòng có `max_steps` lấy từ `scenario.get("max_steps", 6)`, `token_budget` từ `scenario.get("token_budget")`, kiểm budget → final → repeat → side effect/approve như bài, dispatch qua `toolbox.call`), rồi so với `expect`.
  - Trả `{"name", "passed": bool, "stopped_reason", "tools": list[str], "reasons": list[str]}`; `reasons` là các lý do fail theo thứ tự cố định `"stopped_reason"`, `"tools"`, `"answer"` (rỗng khi pass). `tools` gồm cả tool side effect đã được duyệt và chạy; tool bị chặn chờ duyệt **không** tính.
  - `summarize` trả các dòng định dạng cố định ghi trong prompt: `"passed: 5/7"`, rồi mỗi kịch bản fail một dòng `"FAIL <name>: stopped_reason, tools"`, cuối `"all passed"` nếu không có fail.
  - Test dùng `FakeLLM(script=...)` và toolbox nhỏ định nghĩa trong file test (không import solution ex01; test tự có một toolbox tối giản). 9–11 test: đường vui pass; trajectory sai thứ tự → `tools` trong reasons; `needs_approval` khi `approve` trả False và tool **không** chạy (kiểm bằng biến đếm); duyệt True thì tool chạy; `repeat`; `max_steps`; `budget`; answer thiếu chuỗi → `answer`; mỗi kịch bản client mới (gọi `make_client` đúng số lần); định dạng `summarize`; không sửa `scenario`.
  - Starter import được và fail **mọi** test. `alternatives/01_*.py` cách khác thật sự (vd tách `step()` thành class hoặc generator sinh từng bước), kèm `.md`.
- Hint 3 tầng đúng luật cho cả hai: hint 1 trỏ tới Part và cho một input cụ thể với kết quả; hint 2 chỉ là bước bằng lời; hint 3 skeleton, mỗi hàm/method chừa đúng một `...` ở khối cốt lõi, không câu nào sau skeleton nói ra phần thiếu; ghép hint 2 + hint 3 không ra nguyên solution.

## Quiz
- 15–18 câu, mỗi loại `mcq`, `output`, `fill`, `parsons` ít nhất 2. Khoảng 5 dễ, 7 vừa, 3 khó. 6 flashcard.
- **mcq cân độ dài:** `len(đúng) <= 1.2 × trung bình len(distractor)` ở cả en và vi. Đáp án đúng không kèm lý do. Đáp án đúng là phương án dài nhất duy nhất ở tối đa 1/3 số câu mcq.
- Phải có câu về: allowlist và tool lạ; thiếu tham số bắt buộc; khi nào cần duyệt; không để model tự duyệt; golden trajectory so bằng list; client mới mỗi kịch bản; test kịch bản khác eval với model thật; thứ tự kiểm điều kiện dừng.

## Tiêu chí hoàn thành (checklist)
1. [ ] Đủ file theo layout CONTENT_GUIDE. `meta.yaml` đúng như trên.
2. [ ] Lesson đúng dàn ý, đủ: mermaid, trace table, bảng so sánh, một lời mời Visualize (không gọi FakeLLM), callout `[!NOTE]`, `[!WARNING]`, `[!TIP]`, `## Recap`/`## Take it further` không đánh số.
3. [ ] Code giữa EN và VI giống hệt, chỉ khác comment. Số dòng mermaid bằng nhau. Fence `text` giống hệt.
4. [ ] Mọi khối python, example và quiz chạy với `-W error`, stderr rỗng, output khớp. Mọi số liệu trong văn bản và bảng khớp output thật.
5. [ ] Part 4 có ít nhất một kịch bản fail thật rồi pass sau khi sửa, giải thích đúng.
6. [ ] Exercise: starter fail **mọi** test (số pass với starter là 0, ghi vào report). Solution và alternative pass (pytest **và** browser runner trong validate). Không thân hàm solution nào trùng nguyên văn khối trong bài (kiểm AST, ghi report).
7. [ ] Script độ dài mcq in `violations: 0`.
8. [ ] Bản VI tự nhiên, xưng "bạn", thuật ngữ giữ tiếng Anh kèm giải nghĩa lần đầu.
9. [ ] Report ghi: số step khối Visualize, link further_reading đã mở, danh sách kịch bản và kết quả. `glossary.yaml` chỉ có dòng thêm.

## Lệnh kiểm tra
Từ gốc repo:
```
uv run python tools/validate.py --path curriculum/phase-07-llm/p7-10-mini-project-agent
uv run python -m pytest curriculum/phase-07-llm
uv run ruff check curriculum/phase-07-llm
grep -rnE "input\(|time\.sleep|requests\.|urllib|open\(|[^_a-z]eval\(|exec\(|subprocess|os\.system|while True" curriculum/phase-07-llm/p7-10-mini-project-agent --include=*.py
git diff --numstat curriculum/glossary.yaml
uv run python tools/build_content.py
git status --short
```
Script độ dài mcq (phải in `violations: 0`):
```
uv run python -c "
import yaml
bad=0
for q in yaml.safe_load(open('curriculum/phase-07-llm/p7-10-mini-project-agent/quiz.yaml',encoding='utf-8'))['questions']:
    if q['type']!='mcq': continue
    for lang in ('en','vi'):
        o=q[lang]['options']; L=[len(x) for x in o]; a=q['answer']
        d=[l for i,l in enumerate(L) if i!=a]
        if L[a] > 1.2*sum(d)/len(d): bad+=1; print(q['id'],lang,L)
print('violations:',bad)
"
```
Mong đợi: validate 0 lỗi, pytest exit 0, ruff sạch, grep rỗng, glossary chỉ có dòng thêm. Ngoài ra `grep -n "while True" curriculum/phase-07-llm/p7-10-mini-project-agent/*.md` rỗng.

## Ghi chú cho worker
- Đọc `docs/CONTENT_GUIDE.md` (mục Fake LLM client), `packages/pyai_llm/README.md` và `pyai_llm.py`, mục p7 trong `curriculum/syllabus.yaml`, `curriculum/topics.yaml`, bài p7-06, p7-07 (đặc biệt `examples/03_approval_gate.py`) và p7-09 (cấu trúc project).
- Test chỉ dùng: assert, pytest.raises, pytest.approx, pytest.mark.parametrize, `@pytest.fixture` định nghĩa trong file test.
- Dùng `uv run python -m pytest`, không dùng `uv run pytest`. Kiểm warning bằng `uv run python -W error <file>`.
- Mọi lệnh phải tự kết thúc. Không chạy server.
- Ghi report ngay khi xong từng phần lớn (lesson, examples, exercises, quiz), để nếu bị ngắt vẫn còn dấu vết.

## Trạng thái
- Bước hiện tại: xong — đã commit `7d48537`
- Vòng: 2/3
- Số lần swap: 0
- Fallback: không
- Model: Gemini 4 Hydrogen (High)

## Feedback vòng 2
Cổng kiểm tra đều xanh, bài tốt. Chỉ sửa đúng 3 điểm rõ nghĩa sau (EN và VI, code giống hệt nhau, output thật):

1. **Tên lý do fail không thống nhất.** Part 5 (§7) và có thể example 03 in lý do `trajectory` (`FAIL repeat_guard: stopped_reason, trajectory`), còn `ex02-run-scenarios` dùng `"tools"`. Đổi lesson/examples sang `"tools"` cho khớp exercise (cập nhật `.out`, comment output, văn bản, recap, quiz/flashcard nếu có nhắc `trajectory` như **tên lý do**; thuật ngữ "golden trajectory" giữ nguyên).
2. **Part 5 không nói báo cáo đến từ phiên bản nào.** Báo cáo `passed: 6/7` là của `v1`. Thêm một câu trước khối nói rõ đang báo cáo `v1` để thấy một dòng FAIL, và (tùy chọn) một dòng output thêm cho `v2` → `passed: 7/7`. Số liệu phải thật.
3. **Ký hiệu `final(2)` trong bảng Part 4 chưa được giải thích.** Thêm nửa câu: số trong ngoặc là số tool đã chạy.

Chạy lại toàn bộ Lệnh kiểm tra.
