# M5 bước 2b: capstone 1, exercise 1 `ChatBot`

## Mục tiêu
Viết exercise `cap-01-ex01` trong `curriculum/capstones/cap-01-rag-chatbot/exercises/ex01-chatbot/`: học viên đóng gói ý §3 (lịch sử có ngân sách token) và §4 (viết lại câu nối tiếp) của lesson thành một class `ChatBot` nhiều lượt, có citation và từ chối. Đây là mốc 1 trong bảng §7 của lesson; đọc lesson trước.

Phần chia chunk + truy xuất **đã học ở p7-09**, nên **cho sẵn trong starter** (hàm `build_index`, `retrieve` đã viết xong, có docstring). Học viên chỉ viết class `ChatBot`.

Thêm: sửa quy tắc tiền tố còn sót ở 2 example (xem mục 5).

## File được phép sửa/tạo
- `curriculum/capstones/cap-01-rag-chatbot/exercises/ex01-chatbot/`: `exercise.yaml`, `prompt.en.md`, `prompt.vi.md`, `starter.py`, `solution.py`, `test_exercise.py`, `alternatives/01_*.py|.en.md|.vi.md`
- `curriculum/capstones/cap-01-rag-chatbot/examples/01_follow_up_chat.py`, `examples/02_dialog_eval.py` (chỉ dòng `startswith`, xem mục 5)
- `tasks/m5-cap01-ex01.report.md`

## Không được đụng
- `lesson.*.md`, `meta.yaml`, các example khác, `tools/**`, `apps/**`, `packages/**`, mọi phase.
- Không tạo `quiz.yaml` (bước 2e).

## Hợp đồng `ChatBot` (viết đúng như sau vào prompt Rules)
```python
REFUSAL = "I don't know based on the provided context."
DEFAULT_SYSTEM = "Answer only from the shop FAQ context and cite sources as [n]."

class ChatBot:
    def __init__(self, docs, client, system_prompt=DEFAULT_SYSTEM, k=2, min_score=0.2, max_history_tokens=60): ...
    history: list[dict]   # chỉ các lượt {"role": "user"|"assistant", "content"}, không chứa system
    def ask(self, question: str) -> dict:  # {"answer": str, "sources": list[str], "rewritten": str}
```
Quy tắc:
1. `__init__` gọi `build_index(docs, client)` **một lần** (embed chunk đúng một lần cho cả đời bot). Mỗi bot có `history` riêng (không dùng biến cấp class hay default mutable).
2. `ask`: câu hỏi rỗng hoặc chỉ khoảng trắng → `ValueError`. Câu hỏi được `strip()`.
3. **Viết lại:** lấy câu `user` gần nhất trong `history` (câu gốc người dùng gõ, không phải câu đã viết lại). Nếu có, và câu mới có ≤ 4 từ hoặc từ đầu (chữ thường) là `"and"`, hoặc bắt đầu bằng `"what about "` / `"how about "` → `rewritten = f"{prev_user} {question}"`. Ngược lại `rewritten = question`.
4. Truy xuất bằng `retrieve(index, rewritten, client, k, min_score)`. Không có hit nào → `answer = REFUSAL`, `sources = []`, **không gọi `client.chat`**.
5. Có hit → gọi `client.chat` **một lần** với `messages = [{"role": "system", "content": system_prompt + "\n\nContext:\n[1] <text>\n[2] <text>..."}, *history, {"role": "user", "content": rewritten}]`, `temperature=0.0`.
6. **Citation:** tìm mọi `[n]` trong câu trả lời; chỉ giữ `1 <= n <= len(hits)`; `sources` = nguồn (`hit["source"]`) của các citation hợp lệ, không trùng, theo thứ tự xuất hiện. Câu trả lời trả về nguyên văn.
7. **Lịch sử:** sau mỗi `ask` (kể cả từ chối) thêm `{"role": "user", "content": question}` rồi `{"role": "assistant", "content": answer}`. Sau đó cắt: khi `count_tokens(system_prompt) + tổng count_tokens các lượt > max_history_tokens` và `len(history) > 2`, bỏ lượt cũ nhất (`pop(0)`). System prompt không bao giờ bị bỏ; cặp lượt mới nhất luôn được giữ.

Đây là những phần lesson **chưa** làm (ghi rõ trong prompt): ghim system prompt khi cắt, gom vào class có trạng thái, từ chối không gọi chat, lọc citation hợp lệ, viết lại theo câu gốc.

## Việc cần làm
1. `exercise.yaml`: `id: cap-01-ex01`, `kind: project`, `difficulty: 3`, `tags: [llm, rag]` (tag có trong `topics.yaml`), title en/vi, 3 hint mỗi ngôn ngữ theo CONTENT_GUIDE (hint 1 trỏ §3/§4 và nêu ví dụ cụ thể; hint 2 kế hoạch đánh số; hint 3 khung code có 1–2 chỗ `...`, không phải lời giải). **Không** có `runner` (chạy Pyodide).
2. `starter.py`: import (`re`, `numpy as np`, `from pyai_llm import count_tokens`), hằng `REFUSAL`, `DEFAULT_SYSTEM`, hàm `build_index` và `retrieve` **viết sẵn đầy đủ** (gọn, chia câu như p7-09; tự viết lại, không chép nguyên văn khối dài từ p7-09 solution), rồi `class ChatBot` có `__init__` và `ask` với docstring + ví dụ + `# TODO` theo từng bước + `return None`/`pass`. Starter phải import được để test hiện đỏ/xanh từng cái.
3. `solution.py`: đúng hợp đồng. `alternatives/01_*.py`: cách khác thật sự (ví dụ tách `_rewrite`, `_trim`, `_cite` thành hàm thuần ở cấp module, hoặc dùng `collections.deque` cho lịch sử), kèm `.en.md`/`.vi.md` 2–4 câu.
4. `test_exercise.py` (6–10 test, chỉ dùng tập con pytest được phép; client giả `SpyClient` bọc `FakeLLM(embed_dim=256)` đếm `chat`/`embed` và lưu `messages` cuối, giống style p7-09 ex01). Bắt buộc có test cho:
   - câu trong FAQ trả nguồn đúng và citation;
   - câu ngoài FAQ: `REFUSAL`, `sources == []`, số lần gọi `chat` không tăng;
   - câu nối tiếp ("What about express?" sau "How much does delivery cost?") có `rewritten` ghép đúng và trả về `shipping.md`;
   - viết lại dùng câu gốc: hai câu nối tiếp liên tiếp không ghép chồng ba câu;
   - "android" / câu dài không có tiền tố thì không bị viết lại;
   - cắt lịch sử: sau nhiều lượt, tổng token ≤ ngân sách (trừ khi chỉ còn 2 lượt), và `messages[0]["role"] == "system"` trong lần gọi `chat` cuối;
   - citation không hợp lệ bị bỏ (dùng `FakeLLM(script=["... [7]"])` hoặc spy trả câu có `[1]` và `[9]`);
   - hai bot không dùng chung lịch sử; `embed` cho chunk chỉ gọi một lần khi tạo bot;
   - câu rỗng → `ValueError`.
   Tên test đọc như câu; assert có message khi lỗi dễ gây khó hiểu.
5. Examples: trong `01_follow_up_chat.py` và `02_dialog_eval.py`, đổi `startswith(("what about", "and", "how about"))` thành dạng khớp theo từ như lesson §4 (`("what about ", "and ", "how about ")`). Output `.out` phải không đổi; nếu đổi thì dừng và ghi vào report.
6. `prompt.en.md` / `prompt.vi.md`: task 2–4 câu, **Example** (một hội thoại 3 lượt: câu thường → câu nối tiếp → câu ngoài FAQ, kèm dict trả về), **Rules** (đủ 7 quy tắc trên). VI: tự nhiên, "bạn", không "ta"/"chúng ta", thuật ngữ giữ tiếng Anh.

## Tiêu chí hoàn thành (checklist)
- [ ] Starter: mọi test fail (với `EXERCISE_TARGET=starter`); solution và alternative: mọi test pass, cả pytest lẫn runner trình duyệt (validate kiểm)
- [ ] Validate capstone chỉ còn 1 lỗi mong đợi: `missing quiz.yaml`; **không** có cảnh báo "copied from lesson code" cho ex01
- [ ] Mutant: bỏ ghim system prompt, gọi chat khi không có hit, giữ citation sai, viết lại bằng câu đã viết lại → mỗi cái làm ít nhất một test fail (ghi kết quả vào report; tạo mutant ở thư mục tạm, không sửa solution trong repo)
- [ ] 2 example đã đổi vẫn khớp `.out`

## Lệnh kiểm tra
Chạy từ gốc repo `D:\Proj\python-ai-platform`:
```bash
D=curriculum/capstones/cap-01-rag-chatbot
uv run python tools/validate.py --path $D
uv run python -m pytest $D -q
EXERCISE_TARGET=starter uv run python -m pytest $D/exercises/ex01-chatbot -q
uv run ruff check $D
for f in $D/examples/*.py; do PYTHONPATH=packages/pyai_llm uv run python -W error "$f" | tr -d '\r' | diff - "${f%.py}.out" > /dev/null && echo "ok $f"; done
git status --short
```
Mong đợi: validate chỉ báo `missing quiz.yaml`; pytest xanh; lệnh starter: mọi test fail (pytest exit khác 0, 0 passed); 3 dòng `ok`.

## Ghi chú cho worker
- Không chạy server hay dev server.
- Đọc trước: lesson cap-01 (§3, §4, §7, §9), `docs/CONTENT_GUIDE.md` (Exercises, Hints, Alternative solutions, Fake LLM client), `curriculum/phase-07-llm/p7-09-mini-project-rag/exercises/ex01-ingest-retrieve/` (khuôn file), `packages/pyai_llm/pyai_llm.py` (`_try_rag` dùng câu `user` cuối và cần ≥ 2 từ chung).
- Test import code học viên bằng `from exercise import ...` như các bài khác.

## Trạng thái
- Bước hiện tại: 5 (đạt vòng 2; boss kiểm: validate chỉ `missing quiz.yaml`, 13 test pass, starter 0 pass, 9 mutant đều bị bắt; chờ duyệt commit)
- Vòng: 2/3
- Số lần swap: 0
- Fallback: không
- Model: Gemini 4 Hydrogen (High)

## Feedback vòng 2
Boss kiểm: validate chỉ còn `missing quiz.yaml`, pytest 11 pass, starter 0 pass, ruff sạch, example khớp. Boss chạy thêm mutant trên bản chép của solution; 2 mutant **sống sót** (mọi test vẫn pass). Chỉ thêm test, không đổi solution/starter/prompt trừ khi test mới lộ lỗi:
1. `while ... and len(self.history) > 2` đổi thành `> 0` vẫn pass 11/11. Thêm test: `max_history_tokens` rất nhỏ (ví dụ 5) → sau 2 lượt `ask`, `history` vẫn còn đúng 2 lượt mới nhất (user + assistant của lượt cuối).
2. Bỏ qua `k` (truyền cứng `3` vào `retrieve`) vẫn pass. Thêm test: `ChatBot(..., k=1)` → trong lần gọi `chat`, nội dung system chỉ có `[1]`, không có `[2]`.
Chạy lại toàn bộ lệnh kiểm tra trong spec và ghi kết quả 2 test mới (pass với solution và alternative, fail với starter) vào report.
