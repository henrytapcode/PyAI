# M4 bước 12: bài p7-02 Structured output

## Mục tiêu
Viết bài `p7-02-structured-output` trong `curriculum/phase-07-llm/`, đúng `docs/CONTENT_GUIDE.md` và song ngữ EN/VI.
- Bài **chạy trong Pyodide** (không có `runner: local`). Mọi lời gọi LLM đi qua `pyai_llm`. Không gọi mạng, không cần key.
- Người học đã xong p7-01: `FakeLLM`, messages, `finish_reason`, `usage`, retry `RateLimitError`. Họ cũng đã học dict, `json`, dataclass, exception, typing.
- Ý chính: code của bạn không đọc được văn xuôi, nó cần **dữ liệu**. Bạn mô tả hình dạng mong muốn bằng một schema, yêu cầu model trả JSON, rồi **không tin** kết quả: parse, kiểm tra, chuyển thành object có kiểu. Nếu sai thì retry, còn không được nữa thì fallback.
- Bài mẫu: `curriculum/phase-07-llm/p7-01-llm-api/`. Copy giọng văn và hình dạng của nó.

## Hành vi fake client cần dùng (boss đã chạy thử)
- `client.chat(messages, response_format={"type": "json", "schema": schema})` trả `content` là chuỗi JSON theo `schema["properties"]`, lấy giá trị từ tin nhắn user cuối. Mẫu có sẵn: `<key>: <val>` hoặc `<key> is <val>`.
  - Ví dụ: `"name: Lan, age is 31, vip true"` cho ra `{"name": "Lan", "age": 31, "vip": true}`.
  - Khi không tìm thấy giá trị: `"hello there"` cho ra `{"name": "", "age": 0, "vip": false}`. Đây là **giá trị rỗng giả**, chất liệu tốt để dạy việc kiểm tra.
- `FakeLLM(script=[...])` trả lần lượt các chuỗi viết sẵn, bỏ qua mọi luật khác. Dùng nó để mô phỏng model trả **JSON hỏng**:
  - JSON bọc trong ```` ```json ```` fence;
  - có câu dẫn "Sure! Here is the JSON: ...";
  - thiếu key;
  - sai kiểu (`"age": "thirty"`);
  - JSON cắt dở.
  Lần gọi sau trả JSON đúng, để minh họa retry.
- Đọc `packages/pyai_llm/pyai_llm.py` (`_extract_schema_values`) để biết chính xác các kiểu được hỗ trợ. Mọi output in ra phải là output **thật**.

## File được phép sửa/tạo
- Thư mục mới `curriculum/phase-07-llm/p7-02-structured-output/` và mọi file bên trong.
- `curriculum/glossary.yaml`: chỉ **thêm** thuật ngữ chưa có (structured output, JSON schema, parse, validation, fallback). Thuật ngữ đã có thì bỏ qua.
- `tasks/m4-p7-02-structured-output.report.md`

## Không được đụng
- `packages/`, `apps/`, `tools/`, `curriculum/syllabus.yaml`, `curriculum/topics.yaml`, bài p7-01, các phase khác, `exams/`.
- Không xóa file, không `git commit`, **không chạy `pnpm --filter web build`**, không chạy server ở foreground.
- Không sửa `pyai_llm`. Hành vi nào cản bài học thì ghi vào report.

## Quy tắc code (bắt buộc)
- Áp dụng nguyên mọi quy tắc phase 7 của spec p7-01: không `input()`, không mạng, không `time.sleep`, không ghi file, sạch với `-W error`, output tất định.
- **Exercise, example và quiz chỉ dùng thư viện chuẩn** (`json`, `dataclasses`, `typing`) cộng `pyai_llm`. Không dùng pydantic ở đó.
- **Pydantic** chỉ xuất hiện trong **một section** của lesson (§5). Pyodide 0.29.5 có `pydantic 2.12.5`, local cũng ghim `2.12.5`, và worker Pyodide tự nạp gói theo import.
  - **Không in** `str(ValidationError)`, vì nó chứa URL `errors.pydantic.dev` và phụ thuộc phiên bản.
  - Chỉ in các trường ổn định: `e.errors()[0]["loc"]`, `["type"]`, `len(e.errors())`.
  - In model bằng `.model_dump()`.
- Khối mời **Visualize** phải dưới 600 step. Kiểm bằng `tools/pyrunner/tracer.py` và ghi số step vào report.

## Nội dung bài (boss chốt dàn ý, worker viết)
Opening (không heading): một ứng dụng thật, vd đọc email khách hàng rồi tạo ticket với `name`, `order_id`, `urgent`. Văn xuôi đẹp cho người đọc nhưng code không dùng được. Bài này biến câu trả lời thành dữ liệu có thể tin.

1. **Văn xuôi không phải dữ liệu.**
   - Hỏi bình thường, nhận câu trả lời dạng câu. Thử lấy tên bằng `split`, thấy mong manh.
   - Rồi gọi lại với `response_format` JSON, nhận chuỗi JSON.
   - `json.loads` chuyển nó thành dict.
2. **Schema: mô tả hình dạng bạn muốn.**
   - Một JSON schema nhỏ (`type`, `properties`, `required`) dưới dạng dict Python.
   - **Bảng so sánh** `| JSON type | Python type |`: string/str, integer/int, number/float, boolean/bool, array/list, object/dict.
   - Callout `[!NOTE]`: model thật thường hỗ trợ "JSON mode" hoặc "structured outputs" theo schema, nhưng bạn vẫn phải kiểm tra phía mình.
3. **Parse và kiểm tra: không bao giờ tin model.**
   - Hàm `validate(data, schema) -> list[str]` trả danh sách lỗi: thiếu key bắt buộc, sai kiểu. Lưu ý `bool` là lớp con của `int` (`isinstance(True, int)` là True), nên phải kiểm `bool` trước.
   - **Mermaid** `flowchart LR` (≤ 8 node): reply → json.loads → validate → ok? → object / error.
   - Một ví dụ chạy với các chuỗi hỏng từ `script` (JSON trong fence, sai kiểu, thiếu key): in lỗi của từng chuỗi.
   - Section này có lời mời **Visualize** (giữ khối ngắn): xem list `errors` được thêm dần.
4. **Từ dict sang dataclass.**
   - `@dataclass class Ticket` và `Ticket(**data)`.
   - Vì sao object có kiểu tốt hơn dict: IDE gợi ý, lỗi chính tả tên trường lộ ngay.
   - Bẫy "giá trị rỗng giả": JSON hợp lệ, đúng kiểu, nhưng `name == ""` hoặc `age == 0` thì vẫn là thông tin thiếu. Thêm kiểm tra nghiệp vụ (`__post_init__` raise `ValueError`).
5. **Pydantic: thư viện người ta dùng thật.**
   - `class Ticket(BaseModel)`, `Ticket.model_validate_json(reply)`, `.model_dump()`.
   - Một reply sai kiểu → `ValidationError`, in `loc` và `type`.
   - Ghi chú: pydantic làm mọi thứ của §3–§4 trong vài dòng. Bài tập dùng thư viện chuẩn để bạn hiểu bên trong.
   - **Bảng** `| approach | good for |`: dict + kiểm tay / dataclass / pydantic.
6. **Khi model trả sai: retry rồi fallback.**
   - Vòng `for attempt in range(1, max_attempts + 1)`: gọi, parse, validate.
   - Lỗi thì **thêm thông báo lỗi vào messages** (assistant reply cũ + user "Your JSON was invalid: ... Return only JSON.") rồi thử lại. Dùng `script` để lần 1 hỏng, lần 2 đúng.
   - Hết lượt thì trả fallback (vd `None` hoặc giá trị mặc định có cờ `needs_review=True`), không làm sập chương trình.
   - **Trace table** `| attempt | reply | errors | action |`.
   - Callout `[!WARNING]`: không dùng `eval()` để "parse" output của model. Đó là chạy code lạ.
7. **Lỗi thường gặp** (VI: `## 7. Lỗi thường gặp`), chạy thật để lấy đúng thông báo:
   - `json.loads` trên reply có fence ```` ``` ```` hoặc câu dẫn → `json.JSONDecodeError` (in thông báo thật). Cách sửa: cắt phần nằm giữa `{` đầu tiên và `}` cuối cùng, hoặc yêu cầu "only JSON".
   - Kiểm `isinstance(x, int)` với `True` → lọt qua.
   - Truy cập `data["order_id"]` khi key thiếu → `KeyError`. Dùng validate hoặc `.get`.
   - Tin giá trị rỗng giả.
8. **Recap / Tóm tắt**: 4–6 gạch đầu dòng.

Thời lượng 12–15 phút. Trong lesson, ở chỗ đầu tiên nói tới việc gửi lại reply sai cho model, nhắc tới `p7-01` (lịch sử message).

`meta.yaml`:
- `phase: p7`, `order: 2`, `tags: [llm]`
- `prerequisites: [p7-01-llm-api]`
- `outcomes` khớp syllabus
- `review_by: "2027-05-01"`, không có `runner`
- `further_reading`: 1–2 link ổn định, ví dụ trang JSON Schema "Getting started" và docs pydantic "Models". Mở thử và ghi vào report.

## Examples (3)
- `01_ticket_extractor`: 3 email khách (chuỗi), mỗi email gọi chat với schema rồi parse, validate và dựng `Ticket` dataclass. In từng ticket. Email thiếu thông tin thì in lý do bị loại.
- `02_robust_parser`: hàm `extract_json(text) -> dict` xử lý fence, câu dẫn, và trả lỗi rõ khi không có JSON. Chạy trên 5 reply mẫu (dùng `script`), in kết quả hoặc lỗi.
- `03_retry_then_fallback`: hàm `get_structured(client, messages, schema, max_attempts=3)` có retry kèm phản hồi lỗi. Chạy hai lần: lần 1 có `script` hỏng 1 lần rồi đúng; lần 2 hỏng 3 lần thì in fallback.

## Exercises (2)
- `ex01-check-reply` (`kind: fill`): `check_reply(data: dict, schema: dict) -> list[str]`.
  - Trả list lỗi theo định dạng cố định, nêu chính xác trong prompt: `"missing: <key>"`, `"wrong type: <key>"`.
  - Hỗ trợ `string`, `integer`, `number`, `boolean`. Bool không được tính là integer. Integer được chấp nhận cho `number`.
  - Các `___` nằm trong thân hàm. Map kiểu cho sẵn trong starter.
  - 5–6 test, dùng parametrize: hợp lệ cho ra `[]`; thiếu key; sai kiểu; `True` cho integer là sai; `3` cho number là đúng; key không có trong `required` mà thiếu thì không lỗi.
- `ex02-structured-call` (`kind: code`), hai hàm:
  - `parse_reply(text: str) -> dict`: cắt từ `{` đầu tiên tới `}` cuối cùng rồi `json.loads`. Không có `{` thì raise `ValueError`. Kết quả không phải dict thì raise `ValueError`.
  - `get_ticket(client, messages, schema, max_attempts=3) -> tuple[dict | None, int]`: trả `(data, số lần đã thử)`. Mỗi lần: chat với `response_format`, `parse_reply`, rồi kiểm bằng `check_reply`.
    - Một hàm kiểm tra nhỏ được định nghĩa lại trong solution/starter, **không import từ ex01**. Có thể cho sẵn trong starter.
    - Lỗi (`ValueError` hoặc list lỗi không rỗng) thì append reply cũ (role assistant) và một tin nhắn user nêu lỗi, rồi thử lại. Hết lượt thì trả `(None, max_attempts)`.
    - **Không** sửa list `messages` gốc của người gọi.
  - 7–8 test:
    - parse JSON trần;
    - parse JSON trong fence/câu dẫn;
    - parse không có JSON → `pytest.raises(ValueError)`;
    - `get_ticket` đúng ngay lần 1;
    - hỏng 1 lần rồi đúng → attempts 2;
    - hỏng hết → `(None, 3)`;
    - list messages gốc không bị đổi độ dài;
    - lần retry có gửi kèm lỗi: dùng một spy client nhỏ trong test ghi lại messages nhận được.
  - Starter import được và fail **mọi** test.
  - `alternatives/01_regex_or_raw_decode.py`: dùng `json.JSONDecoder().raw_decode` (hoặc một cách khác thật sự khác), kèm `.md` so sánh.
- Hint 3 tầng đúng luật:
  - hint 2 chỉ là các bước bằng lời, không có biểu thức Python hoàn chỉnh;
  - hint 3 là skeleton, mỗi hàm chừa đúng một `...` ở dòng cốt lõi;
  - ghép hint 2 và hint 3 không ra nguyên solution.

## Quiz
- 15–18 câu, mỗi loại `mcq`, `output`, `fill`, `parsons` ít nhất 2. Khoảng 5 dễ, 7 vừa, 3 khó. 6 flashcard. Tag `llm`.
- **mcq cân độ dài:** `len(đúng) <= 1.2 × trung bình len(distractor)` ở cả en và vi. Đáp án đúng không kèm lý do. Đáp án đúng là phương án dài nhất duy nhất ở tối đa 1/3 số câu mcq.
- Câu `output` và `fill` chỉ dùng thư viện chuẩn + `pyai_llm`, không pydantic.
- Phải có câu về:
  - vì sao cần JSON thay cho văn xuôi;
  - `json.loads` trên reply có fence;
  - bool và int;
  - thiếu key bắt buộc;
  - giá trị rỗng giả;
  - retry kèm thông báo lỗi;
  - fallback thay vì crash;
  - không dùng `eval`.

## Tiêu chí hoàn thành (checklist)
1. [ ] Đủ file theo layout CONTENT_GUIDE. `meta.yaml` đúng như trên.
2. [ ] Lesson đúng dàn ý, đủ: mermaid, trace table, bảng so sánh, một lời mời Visualize, callout.
3. [ ] Code giữa EN và VI giống hệt, chỉ khác comment. Số dòng mermaid bằng nhau. Fence `text` (nếu có) giống hệt.
4. [ ] Mọi khối python, example và quiz chạy với `-W error`, stderr rỗng, output khớp. Khối pydantic không in URL lỗi.
5. [ ] Exercise: starter fail **mọi** test (số pass với starter phải là 0, ghi vào report). Solution và alternative pass (pytest **và** browser runner trong validate).
6. [ ] Script độ dài mcq in `violations: 0`.
7. [ ] Bản VI tự nhiên, xưng "bạn", thuật ngữ giữ tiếng Anh kèm giải nghĩa lần đầu.
8. [ ] Report ghi: số step khối Visualize, link further_reading đã mở, phiên bản pydantic local, mọi hành vi lạ của `pyai_llm`.

## Lệnh kiểm tra
Từ gốc repo:
```
uv run python tools/validate.py --path curriculum/phase-07-llm/p7-02-structured-output
uv run python -m pytest curriculum/phase-07-llm
uv run ruff check curriculum/phase-07-llm
grep -rnE "input\(|time\.sleep|requests\.|urllib|open\(|eval\(|pydantic" curriculum/phase-07-llm/p7-02-structured-output --include=*.py
uv run python -c "import pydantic; print(pydantic.VERSION)"
uv run python tools/build_content.py
git status --short
```
Script độ dài mcq (phải in `violations: 0`):
```
uv run python -c "
import yaml
bad=0
for q in yaml.safe_load(open('curriculum/phase-07-llm/p7-02-structured-output/quiz.yaml',encoding='utf-8'))['questions']:
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
- grep rỗng, vì pydantic chỉ nằm trong lesson `.md`.
- pydantic `2.12.5`.
- Chỉ có thay đổi trong các file được phép.

## Ghi chú cho worker
- Đọc `docs/CONTENT_GUIDE.md`, `packages/pyai_llm/README.md` và `pyai_llm.py`, mục p7 trong `curriculum/syllabus.yaml`, rồi bài p7-01 làm mẫu.
- Test chỉ dùng: assert, pytest.raises, pytest.approx, pytest.mark.parametrize, `@pytest.fixture` định nghĩa trong file test.
- Dùng `uv run python -m pytest`, không dùng `uv run pytest`. Kiểm warning bằng `uv run python -W error <file>`.
- Mọi lệnh phải tự kết thúc. Không chạy server.

## Trạng thái
- Bước hiện tại: xong, commit `139e9e6` (đạt vòng 1; boss kiểm: validate toàn bộ 0 lỗi trên 41 bài, typecheck + build 64 trang; trong app qua Pyodide: khối pydantic §5 chạy đúng, starter ex02 0/8, solution qua hết; chờ user duyệt commit)
- Vòng: 1/3
- Số lần swap: 0
- Fallback: không
- Model: Gemini 4 Hydrogen (High)
