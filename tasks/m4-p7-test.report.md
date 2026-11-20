# Báo cáo M4 bước 21: Phase test 7 (`p7-phase-test`)

## 1. Đã làm gì
Tạo mới bài kiểm tra cuối phase 7 tại `curriculum/phase-07-llm/phase-test.yaml` (`id: p7-phase-test`, `kind: phase_test`, `phase: p7`, `duration_min: 30`, `pass_score: 0.7`, gồm 20 câu hỏi song ngữ EN/VI từ `p7-test-q01` tới `p7-test-q20`) sau khi đã đọc toàn bộ 10 file `curriculum/phase-07-llm/p7-*/quiz.yaml`, `curriculum/phase-06-deep-learning/phase-test.yaml`, `tools/schema/exam.schema.json`, `curriculum/topics.yaml`, `docs/CONTENT_GUIDE.md` và `packages/pyai_llm/pyai_llm.py`.

### Bảng đếm thực tế theo blueprint
- **Tổng số câu:** 20
- **Phân bổ loại câu:** `mcq`: 9, `output`: 5, `fill`: 4, `parsons`: 2 (đúng 9/5/4/2).
- **Phân bổ độ khó:** mức 1: 4 (`q01`, `q04`, `q05`, `q17`), mức 2: 11 (`q03`, `q06`, `q08`, `q09`, `q10`, `q12`, `q14`, `q16`, `q18`, `q19`, `q20`), mức 3: 5 (`q02`, `q07`, `q11`, `q13`, `q15`) (đúng 4/11/5).
- **Phân bổ đáp án `mcq` (0–3):** `0`: 3 (`q02`, `q11`, `q17`), `1`: 2 (`q06`, `q15`), `2`: 2 (`q04`, `q13`), `3`: 2 (`q07`, `q20`) (đúng 3/2/2/2).
- **Tags sử dụng:** chỉ dùng trong `[llm, rag, agents, evaluation, json, testing]` (tất cả đều có trong `curriculum/topics.yaml`).

| Chủ đề | Số câu | Loại câu thực tế | Độ khó | Ý chính kiểm tra (mới so với 10 quiz) |
|---|---|---|---|---|
| LLM API (`p7-01`) | 2 (`q01`–`q02`) | `output`, `mcq` | 1, 3 | `q01`: tổng `Usage` (`prompt_tokens`/`completion_tokens`) và tính cost USD; `q02`: bẫy retry bắt `Exception` làm retry cả `ValueError` cố định kèm exponential backoff thay vì chỉ lỗi tạm thời (`RateLimitError`) |
| Structured output (`p7-02`) | 2 (`q03`–`q04`) | `fill`, `mcq` | 2, 1 | `q03`: tách JSON khỏi text thừa + validate `required`, chặn `bool` khi kiểm `int`, và kiểm `enum`; `q04`: quy trình retry kèm thông báo lỗi có giới hạn rồi mới fallback |
| Embeddings (`p7-03`) | 2 (`q05`–`q06`) | `output`, `mcq` | 1, 2 | `q05`: vector chuẩn hóa L2 có dot product = cosine và top-k bằng `np.argsort(-scores, kind="stable")`; `q06`: ngưỡng `min_score` phải đo lại trên dev khi đổi embedding model |
| Vector DB (`p7-04`) | 2 (`q07`–`q08`) | `mcq`, `fill` | 3, 2 | `q07`: bẫy lọc metadata sau top-k (`post-filter`) trả thiếu `k` mục (thực tế ra `[]`); `q08`: upsert giữ `ids` ↔ hàng ma trận đồng bộ và lưu/nạp lại bằng `json.dumps`/`tolist()` |
| RAG (`p7-05`) | 3 (`q09`–`q11`) | `parsons`, `output`, `mcq` | 2, 2, 3 | `q09`: pipeline RAG hoàn chỉnh (embed query → cosine top-1 → prompt `Context:` kèm luật chỉ dùng context → `FakeLLM.chat`); `q10`: chunk theo đoạn `\n\n` theo `max_words` + ngưỡng `min_score` bỏ qua LLM; `q11`: bẫy citation `[0]` thiếu `1 <= int(n)` thành `hits[-1]` |
| Tool use (`p7-06`) | 2 (`q12`–`q13`) | `parsons`, `mcq` | 2, 3 | `q12`: một lượt tool call đầy đủ (gọi `chat` với schema → lấy `tool_calls[0]` → nối `assistant` → dispatch qua allowlist → nối `tool` có `tool_call_id` → gọi `chat` lần 2); `q13`: args của model (gồm `confirmed=True` bị prompt injection) là input chưa tin cậy, xác nhận và hạn mức phải nằm trong code (`app_state`) |
| Agents (`p7-07`) | 2 (`q14`–`q15`) | `fill`, `mcq` | 2, 3 | `q14`: các chốt chặn `max_steps`, `budget` theo token, `repeat` và `needs_approval` cho side effect; `q15`: bẫy quên nối message `tool` khiến `FakeLLM` lặp lại cùng `lookup_order` và dừng ở `repeat` |
| Evals (`p7-08`) | 2 (`q16`–`q17`) | `output`, `mcq` | 2, 1 | `q16`: tính `hit@2` (bỏ `expected=None`) + kiểm tra `faithful` (citation trong `1..len(ctx)` và từ ngữ nằm trong context); `q17`: phân biệt `faithful` (có căn cứ theo `[1]`) với "đúng sự thật ngoài đời" |
| Mini-project RAG (`p7-09`) | 1 (`q18`) | `output` | 2 | `q18`: câu tích hợp chọn cấu hình `(chunk, k, min_score)` tốt nhất trên `dev`, đánh giá một lần trên `test` và đếm `hit`/`facts`/`refusal` |
| Mini-project agent (`p7-10`) | 2 (`q19`–`q20`) | `fill`, `mcq` | 2, 2 | `q19`: `copy.deepcopy` bảo vệ schema khỏi sửa ngoài ý muốn và phân biệt `needs_approval` (`approve_fn is None`) vs `rejected` (`False`); `q20`: ý nghĩa của test kịch bản `FakeLLM(script=...)` tất định với golden trajectory có thứ tự |

### Bảng độ dài 4 phương án (EN) của từng câu `mcq`
| Câu | `answer` | Độ dài 4 phương án EN `[0, 1, 2, 3]` | Trung bình distractor | Đáp án dài nhất duy nhất? |
|---|---|---|---|---|
| `p7-test-q02` | 0 | `[60, 60, 63, 58]` | 60.3 | Không |
| `p7-test-q04` | 2 | `[63, 72, 69, 71]` | 68.7 | Không |
| `p7-test-q06` | 1 | `[74, 70, 66, 68]` | 69.3 | Không |
| `p7-test-q07` | 3 | `[60, 60, 63, 64]` | 61.0 | Có |
| `p7-test-q11` | 0 | `[68, 68, 67, 67]` | 67.3 | Không (hòa) |
| `p7-test-q13` | 2 | `[74, 71, 70, 69]` | 71.3 | Không |
| `p7-test-q15` | 1 | `[61, 58, 57, 57]` | 58.3 | Không |
| `p7-test-q17` | 0 | `[60, 61, 65, 63]` | 63.0 | Không |
| `p7-test-q20` | 3 | `[66, 69, 65, 62]` | 66.7 | Không |

Kết quả script kiểm độ dài MCQ: `violations: 0 longest-unique: 1` (đạt yêu cầu `violations: 0` và `longest-unique <= 3`).

## 2. File đã sửa / tạo
- Tạo mới: `curriculum/phase-07-llm/phase-test.yaml`
- Tạo mới: `tasks/m4-p7-test.report.md`
- Lưu ý: `uv run python tools/build_content.py` có tạo/cập nhật output build trong `apps/web/src/generated` (đã gitignore, không hiện trong `git status --short`). Không sửa bất kỳ file nào khác trong repo.

## 3. Kết quả lệnh kiểm tra
Chạy sau lần chỉnh sửa cuối cùng của `curriculum/phase-07-llm/phase-test.yaml`:

- `uv run python tools/validate.py --path curriculum/phase-07-llm`
  - Exit code `0`: `OK: 0 error(s), 0 warning(s). Checked 10 lessons, 72 markdown pairs, 30 examples, 20 exercises, 12 alternatives, 179 questions, 1 exams.` (số exams tăng từ 0 lên 1 trong phạm vi phase 7, toàn bộ phase 1–7 từ 9 lên 10 như `build_content.py` ghi nhận).
- `uv run python tools/build_content.py`
  - Exit code `0`: `Built 49 lessons, 10 exams, 294 flashcards, 786 questions -> apps\web\src\generated` (10 exams).
- `Select-String -Path "curriculum/phase-07-llm/phase-test.yaml" -Pattern "api_key|OPENAI|httpx|requests\.|độ chính xác"`
  - Không có dòng nào khớp (0 kết quả).
- `git status --short`
  - `?? .hallmark/`
  - `?? curriculum/phase-07-llm/phase-test.yaml`
  - `?? tasks/`
- Kiểm độ dài MCQ (script Python trong spec):
  - `violations: 0 longest-unique: 1`
- Chạy mọi đoạn code `output`, `fill` (đã điền đáp án đầu tiên), `parsons`, và `mcq` có `code` bằng `python -W error -c ...`:
  - Tất cả trả về exit code `0`, `stderr` rỗng (`ALL_CODE_CLEAN`).
- Kiểm tra riêng `_other_parsons_orders` cho `p7-test-q09` và `p7-test-q12`:
  - `p7-test-q09 other_order= None`, `p7-test-q12 other_order= None` (`PARSONS_UNIQUE_OK`).

## 4. Điều còn chưa chắc
- Chỉ chạy `validate.py --path curriculum/phase-07-llm` theo đúng spec, chưa chạy `validate.py` toàn repo hay `pnpm --filter web build` (do spec cấm chạy `pnpm --filter web build`), nên chưa kiểm tra build giao diện TypeScript/Next.js trên UI thực tế.
- Với các câu `fill` có 3–4 chỗ trống (`p7-test-q03`, `p7-test-q08`, `p7-test-q14`, `p7-test-q19`), validator chỉ thay lần lượt đáp án chuẩn để chạy kiểm tra cú pháp/không lỗi; nếu học viên điền cách viết tương đương khác (ví dụ trong `q08` có thể dùng từ đồng nghĩa cú pháp khác dù ngữ cảnh rất hẹp) thì chỉ chuỗi khớp danh sách `answer` mới được chấm đúng.

## Vòng 2

### 1. Sửa theo Feedback vòng 2
- `p7-test-q15` ([phase-test.yaml](file:///D:/Proj/python-ai-platform/curriculum/phase-07-llm/phase-test.yaml#L366-L404)): Sửa vòng lặp trong `code` để gán `reply = client.chat(msgs, tools=tools)`, kiểm tra `if not reply.tool_calls: print("final:", reply.content); break` trước khi lấy `tc = reply.tool_calls[0]`. Giữ nguyên lỗi thiếu bước nối message `tool`, `answer: 1`, `prompt` và các phương án.
- `p7-test-q20` ([phase-test.yaml](file:///D:/Proj/python-ai-platform/curriculum/phase-07-llm/phase-test.yaml#L511-L531)): Thay phương án 1 (vốn nói về tính mutable của `ToolBox`) bằng hiểu lầm thực tế (nhầm lẫn golden trajectory tất định với tính đúng sự thật của câu trả lời cuối):
  - EN: `"That the agent's final answer is factually correct for the user"` (63 ký tự)
  - VI: `"Câu trả lời cuối của agent là đúng sự thật đối với người dùng"` (61 ký tự)
  - Độ dài 4 phương án EN mới của `p7-test-q20`: `[66, 63, 65, 62]` (trung bình distractor `64.67`, giữ `answer: 3`).

### 2. Tự kiểm `p7-test-q15` với `-W error`
- Output của code trong đề (thiếu message `tool`):
  - `stopped: repeat`
- Output sau khi áp dụng đáp án đúng (nối `{"role": "tool", "tool_call_id": tc.id, "content": "order 1042 shipped"}` vào `msgs`):
  - `final: Based on the tool result: order 1042 shipped`

### 3. Kết quả lệnh kiểm tra (sau sửa vòng 2)
- `uv run python tools/validate.py --path curriculum/phase-07-llm`
  - Exit code `0`: `OK: 0 error(s), 0 warning(s). Checked 10 lessons, 72 markdown pairs, 30 examples, 20 exercises, 12 alternatives, 179 questions, 1 exams.`
- Script kiểm độ dài MCQ:
  - `p7-test-q20 en [66, 63, 65, 62] avg_d= 64.67`
  - `p7-test-q20 vi [63, 61, 62, 61] avg_d= 62.0`
  - `violations: 0 longest-unique: 1`
- `uv run python tools/build_content.py`
  - Exit code `0`: `Built 49 lessons, 10 exams, 294 flashcards, 786 questions -> apps\web\src\generated`
- `Select-String -Path "curriculum/phase-07-llm/phase-test.yaml" -Pattern "api_key|OPENAI|httpx|requests\.|độ chính xác"`
  - Không có dòng nào khớp.
- `git status --short`
  - `?? .hallmark/`
  - `?? curriculum/phase-07-llm/phase-test.yaml`
  - `?? tasks/`

