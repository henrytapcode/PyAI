# M4 bước 11: bài p7-01 Calling an LLM API

## Mục tiêu
Viết bài `p7-01-llm-api` trong `curriculum/phase-07-llm/` (thư mục phase mới), đúng `docs/CONTENT_GUIDE.md` và song ngữ EN/VI.
- Bài **chạy trong Pyodide** (syllabus không có `runner: local`). Mọi lời gọi LLM đi qua fake client `pyai_llm`, đọc API của nó trong `packages/pyai_llm/README.md` và mục "Fake LLM client" ở CONTENT_GUIDE. Không gọi mạng, không cần API key.
- Người học đã xong phase 1–6: dict, list, hàm, class, dataclass, exception, typing, pytest. Phase 7 không dùng torch.
- Ý chính: mọi ứng dụng AI nói chuyện với LLM qua API. Bạn gửi danh sách message, nhận câu trả lời kèm số token (= tiền). Model không có trí nhớ: bạn tự gửi lại lịch sử. Lời gọi có thể lỗi tạm thời nên cần retry. Key thật nằm trong `.env`, không bao giờ in ra hay commit.
- Bài mẫu về giọng văn và hình dạng: `curriculum/phase-06-deep-learning/p6-02-training-loop/`.

## File được phép sửa/tạo
- Thư mục mới `curriculum/phase-07-llm/p7-01-llm-api/` và mọi file bên trong. **Không** tạo `phase-test.yaml`.
- `curriculum/glossary.yaml`: chỉ **thêm** thuật ngữ mới (LLM, prompt, system message, token, temperature, rate limit, API key, context window). Thuật ngữ đã có thì bỏ qua.
- `tasks/m4-p7-01-llm-api.report.md`

## Không được đụng
- `packages/`, `apps/`, `tools/`, `curriculum/syllabus.yaml`, `curriculum/topics.yaml` (tag `llm` đã có), các phase khác, `exams/`.
- Không xóa file, không `git commit`, **không chạy `pnpm --filter web build`**, không chạy server ở foreground.
- Không sửa `pyai_llm`. Nếu thấy hành vi của nó cản bài học, ghi vào report để boss quyết.

## Quy tắc code phase 7 (bắt buộc)
- Gọi LLM chỉ qua `from pyai_llm import ...`. Mọi output in ra phải là output **thật** của fake client (chạy rồi chép), không tự bịa.
- Không `input()`, không mạng, không `time.sleep` (retry chỉ **in** thời gian chờ theo backoff, không ngủ thật). Không ghi file.
- Code phải tương thích Pyodide (Python 3.13, chỉ thư viện chuẩn + `pyai_llm`). Sạch với `-W error`, stderr rỗng.
- Vì fake client tất định, mọi khối phải cho cùng output mỗi lần chạy. Khi dùng `temperature > 0` thì luôn truyền `seed`.
- Gọi API thật **chỉ** nằm trong fence `bash` (không chạy, không chấm): tạo `.env`, thêm `.env` vào `.gitignore`, và một script Python được ghi bằng heredoc `cat > call_llm.py <<'EOF' ... EOF`.
  - Script đọc key bằng `os.environ["LLM_API_KEY"]`, gửi POST bằng `httpx` tới URL placeholder `https://api.example-llm.com/v1/chat` với header `Authorization: Bearer ...`.
  - Không in key. Không gắn tên hay SDK của hãng cụ thể.
  - Một câu nói rằng mỗi nhà cung cấp có URL và tên trường riêng, đọc docs của họ, nhưng hình dạng (messages, temperature, max_tokens, usage) giống bài này.
- Khối mời **Visualize** phải dưới 600 step. Kiểm bằng `tools/pyrunner/tracer.py` (in `len(steps)`, `truncated`), và ghi vào report cả việc tracer có bước vào code của `pyai_llm` hay không.

## Nội dung bài (boss chốt dàn ý, worker viết)
Opening (không heading): chatbot, trợ lý code, RAG… đều là một chương trình gửi message tới LLM qua API rồi đọc câu trả lời. Phase này dùng fake client tất định để bạn tập miễn phí, không cần key; cuối bài chỉ cách đổi sang API thật.

1. **Lời gọi đầu tiên: messages vào, câu trả lời ra.**
   - `FakeLLM()`, `client.chat([{"role": "user", "content": "What is RAG?"}])`. In `resp.content` và `resp.finish_reason`.
   - Giải thích dạng message (dict `role` + `content`) và các field của `ChatResponse`.
   - Callout `[!NOTE]`: đây là model giả với câu trả lời viết sẵn; nó dạy **hình dạng** API, không dạy độ thông minh.
2. **System message: dặn model trước.**
   - Role `system` đặt luật chung cho cả cuộc hội thoại. Ví dụ "pirate" của fake client so với không có system message.
   - **Bảng so sánh** `| role | who writes it | purpose |` cho system / user / assistant.
3. **Model không có trí nhớ: tự gửi lại lịch sử.**
   - Hội thoại 2–3 lượt: sau mỗi lượt append câu trả lời `assistant`, rồi append câu hỏi mới.
   - **Trace table** `| turn | messages sent | prompt_tokens |`: số message và số prompt token tăng dần (số thật).
   - **Mermaid** `flowchart LR` (≤ 7 node): history → append user → chat() → append assistant → history.
   - Section này mời bấm **Visualize** để xem list `history` lớn dần. Giữ khối ngắn.
4. **Temperature và tính lặp lại được.**
   - `temperature=0` luôn ra một câu. `temperature=0.8` với vài `seed` khác nhau ra lời mở đầu khác nhau. Cùng seed thì lặp lại được, nên test mới tin được.
   - **Bảng** `| temperature | use it for |` (trích thông tin, phân loại, test / viết sáng tạo, brainstorm).
   - Callout `[!TIP]`: model thật với `temperature > 0` thường không lặp lại được ngay cả khi có seed, nên test thật hay khóa temperature 0 hoặc dùng fake/mock như ở đây.
5. **Token: thứ bạn trả tiền.**
   - `resp.usage` (prompt / completion / total), `count_tokens`. **Picture in text** (fence `text`, giống hệt ở EN và VI): một câu và các token của nó theo cách đếm của fake client, căn cột. Nói rõ tokenizer thật (subword, nối với p6-03) đếm khác, nhưng ý tưởng giống.
   - Tính chi phí bằng **giá ví dụ** ghi rõ là giả định (vd `$0.50` / 1M input token, `$1.50` / 1M output token). Tính cho một cuộc hội thoại ở §3: lịch sử dài thì tiền tăng.
   - `max_tokens=5` → câu bị cắt, `finish_reason == "length"`. Luôn kiểm `finish_reason`.
6. **Lỗi tạm thời và retry.**
   - `FakeLLM(fail_times=2)`: vòng `for attempt in range(1, max_attempts + 1)` với `try/except RateLimitError`, in thời gian chờ backoff `0.5 * 2 ** (attempt - 1)` giây (không ngủ thật). Thành công ở lần 3.
   - Trường hợp hết lượt thì raise lại lỗi.
   - **Mermaid** cho luồng retry (≤ 7 node).
   - Callout `[!WARNING]`: chỉ retry lỗi tạm thời (rate limit, timeout), không retry lỗi do request sai.
7. **Gọi API thật (đọc, không chạy trong app).**
   - Khối `bash` như mục quy tắc: `.env`, `.gitignore`, heredoc script, `uv run python call_llm.py`.
   - 2–3 câu: key là mật khẩu, chỉ để trong `.env`, không in, không commit, không dán vào code. Callout `[!WARNING]`.
8. **Lỗi thường gặp** (VI: `## 8. Lỗi thường gặp`). Chạy thật để lấy đúng thông báo:
   - Truyền chuỗi thay cho list message → `ValueError` (thông báo thật của fake client).
   - Sai tên role (vd `"bot"`) → `ValueError`.
   - Quên gửi lại lịch sử, nên model "quên" ý trước. Cho thấy bằng output.
   - Bỏ qua `finish_reason == "length"` và dùng câu trả lời bị cắt.
9. **Recap / Tóm tắt**: 4–6 gạch đầu dòng.

Thời lượng 12–15 phút.
`meta.yaml`:
- `phase: p7`, `order: 1`, `tags: [llm]`
- `prerequisites: [p2-05-typing, p3-01-pytest]`
- `outcomes` khớp syllabus (có thể thêm 1 dòng)
- `review_by: "2027-05-01"` (≤ 6 tháng), không có `runner`
- `further_reading`: 1–2 link ổn định, trung lập, ví dụ trang giải thích tokenization và giá của một nhà cung cấp lớn, hoặc tài liệu chung về HTTP API / `.env`. Mở thử để chắc URL còn sống và ghi vào report.

## Examples (3)
- `01_support_reply`: system message cho trợ lý hỗ trợ, 3 câu hỏi của khách, in câu trả lời và token mỗi lượt, cuối cùng in tổng token và chi phí theo giá ví dụ.
- `02_chat_session`: class nhỏ `ChatSession` (dataclass hoặc class thường) giữ `history`, có method `ask(text) -> str` và `total_tokens`. Chạy 3 lượt, in độ dài lịch sử.
- `03_retry_with_backoff`: hàm `call_with_retry` dùng `FakeLLM(fail_times=2)`, in từng lần thử và thời gian chờ, rồi in câu trả lời. Thêm một lần gọi với `fail_times=5` cho thấy lỗi được raise lại và bắt ở ngoài.

## Exercises (2)
- `ex01-build-messages` (`kind: fill`): `build_messages(system: str, history: list[tuple[str, str]], user: str) -> list[dict]`.
  - Trả `[system] + mỗi cặp (user, assistant) trong history thành 2 message + [user mới]`. Các ô `___` nằm trong thân hàm.
  - 4–5 test: thứ tự role đúng; history rỗng; nội dung giữ nguyên; độ dài `1 + 2*len(history) + 1`; kết quả `FakeLLM().chat(...)` chạy được không lỗi.
- `ex02-reliable-call` (`kind: code`), hai hàm:
  - `ask_with_retry(client, messages, max_attempts=3) -> tuple[str, int]`: trả `(content, số lần đã thử)`. Bắt `RateLimitError`; hết lượt thì raise lại đúng lỗi đó; lỗi khác (vd `ValueError`) **không** retry.
  - `estimate_cost(usage, price_in_per_m: float, price_out_per_m: float) -> float`: chi phí USD, làm tròn 6 chữ số.
  - 6–8 test:
    - thành công ngay (`attempts == 1`);
    - thành công ở lần 3 với `fail_times=2`;
    - `fail_times=3, max_attempts=3` → `pytest.raises(RateLimitError)`;
    - `ValueError` không bị retry: client đếm số lần gọi qua một fake nhỏ định nghĩa trong test, hoặc kiểm bằng `fail_times` còn lại;
    - `estimate_cost` với số biết trước;
    - kiểu trả về;
    - khi hàm trả `None`, thông báo dễ hiểu.
  - Starter import được, fail **mọi** test.
  - `alternatives/01_while_loop.py`: retry bằng `while`. File `.md` so sánh với `for`.
- Hint 3 tầng **đúng luật mới** (đã sửa ở phase 6):
  - hint 2 chỉ là các bước bằng lời, không có biểu thức Python hoàn chỉnh;
  - hint 3 là skeleton, mỗi hàm chừa đúng một `...` ở dòng cốt lõi;
  - ghép hint 2 và hint 3 không ra nguyên solution.

## Quiz
- 15–18 câu, mỗi loại `mcq`, `output`, `fill`, `parsons` ít nhất 2. Khoảng 5 dễ, 7 vừa, 3 khó. 6 flashcard. Tag `llm`.
- **mcq cân độ dài:** `len(đúng) <= 1.2 × trung bình len(distractor)` ở cả en và vi. Đáp án đúng không kèm lý do. Đáp án đúng là phương án dài nhất duy nhất ở tối đa 1/3 số câu mcq.
- Câu `output` chạy fake client thật (validator chạy và so).
- Phải có câu về:
  - model không nhớ, phải gửi lại lịch sử;
  - system message;
  - temperature và seed;
  - prompt token tăng theo lịch sử;
  - `finish_reason == "length"`;
  - retry chỉ cho lỗi tạm thời;
  - không in hay commit key.

## Tiêu chí hoàn thành (checklist)
1. [ ] Đủ file theo layout CONTENT_GUIDE. `meta.yaml` đúng như trên, không có `runner`.
2. [ ] Lesson đúng dàn ý, đủ: mermaid, trace table, picture in text, bảng so sánh, một lời mời Visualize, callout. Khối `bash` gọi API thật đúng quy tắc.
3. [ ] Code giữa EN và VI giống hệt, chỉ khác comment. Số dòng mermaid bằng nhau. Fence `text` giống hệt.
4. [ ] Mọi khối python, example và quiz chạy với `-W error`, stderr rỗng, output khớp.
5. [ ] Exercise: starter fail **mọi** test (ghi số test pass với starter, phải là 0). Solution và alternative pass (pytest **và** browser runner trong validate).
6. [ ] Script độ dài mcq in `violations: 0`.
7. [ ] Bản VI tự nhiên, xưng "bạn", thuật ngữ giữ tiếng Anh kèm giải nghĩa lần đầu.
8. [ ] Report ghi: số step khối Visualize, link further_reading đã mở, mọi hành vi của `pyai_llm` thấy lạ.

## Lệnh kiểm tra
Từ gốc repo:
```
uv run python tools/validate.py --path curriculum/phase-07-llm/p7-01-llm-api
uv run python -m pytest curriculum/phase-07-llm
uv run ruff check curriculum/phase-07-llm
grep -rnE "input\(|time\.sleep|requests\.|urllib|open\(" curriculum/phase-07-llm/p7-01-llm-api --include=*.py
uv run python tools/build_content.py
git status --short
```
Script độ dài mcq (phải in `violations: 0`):
```
uv run python -c "
import yaml
bad=0
for q in yaml.safe_load(open('curriculum/phase-07-llm/p7-01-llm-api/quiz.yaml',encoding='utf-8'))['questions']:
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
- grep rỗng. Script trong fence `bash` không tính, vì grep chỉ quét `.py`.
- Chỉ có thay đổi trong các file được phép.

## Ghi chú cho worker
- Đọc `docs/CONTENT_GUIDE.md`, `packages/pyai_llm/README.md` và `packages/pyai_llm/pyai_llm.py` (để biết chính xác hành vi và thông báo lỗi), `curriculum/syllabus.yaml` (mục p7), rồi bài p6-02 làm mẫu.
- Test chỉ dùng: assert, pytest.raises, pytest.approx, pytest.mark.parametrize, `@pytest.fixture` định nghĩa trong file test.
- Dùng `uv run python -m pytest`, không dùng `uv run pytest`. Kiểm warning bằng `uv run python -W error <file>`.
- Mọi lệnh phải tự kết thúc. Không chạy server.

## Trạng thái
- Bước hiện tại: xong, commit `045b301` (đạt vòng 1; boss kiểm: validate toàn bộ 0 lỗi, typecheck + build 63 trang; trong app qua Pyodide: khối §3 ra đúng token, Visualize 21 bước, starter ex02 0/7, solution qua hết; chờ user duyệt commit)
- Vòng: 1/3
- Số lần swap: 0
- Fallback: không
- Model: Gemini 4 Hydrogen (High)
