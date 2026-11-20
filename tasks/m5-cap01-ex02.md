# M5 bước 2c: capstone 1, exercise 2 "eval hội thoại + cổng hồi quy"

## Mục tiêu
Viết exercise `cap-01-ex02` trong `curriculum/capstones/cap-01-rag-chatbot/exercises/ex02-dialog-eval/`. Đây là mốc 2 trong bảng §7 của lesson (đọc lesson §5 và §7 trước). Học viên viết bộ chấm golden dialog theo từng lượt và so lần chạy với baseline để chặn hồi quy.

Bot được truyền vào qua `make_bot` (hàm không tham số trả về object có `ask(question) -> {"answer", "sources", "rewritten"}`, cùng hợp đồng với `ChatBot` ở ex01). Bài này **không** cần ex01: test dùng bot giả viết trong file test.

## File được phép sửa/tạo
- `curriculum/capstones/cap-01-rag-chatbot/exercises/ex02-dialog-eval/`: `exercise.yaml`, `prompt.en.md`, `prompt.vi.md`, `starter.py`, `solution.py`, `test_exercise.py`, `alternatives/01_*.py|.en.md|.vi.md`
- `tasks/m5-cap01-ex02.report.md`

## Không được đụng
- Mọi file khác (lesson, examples, ex01, meta, tools, apps, packages, phase khác). Không tạo `quiz.yaml`.

## Hợp đồng (viết đúng vào prompt Rules)
```python
REFUSAL = "I don't know based on the provided context."

def score_turn(result: dict, turn: dict) -> str | None: ...
def run_dialog_eval(make_bot, dialogs: list[dict]) -> list[dict]: ...
def compare_to_baseline(current: list[dict], baseline: list[dict], min_pass_rate: float = 0.8) -> dict: ...
```
- Một dialog: `{"id": "d1", "turns": [{"question": str, "expected_source": str | None, "expected_facts": list[str]}, ...]}`.
- `score_turn` trả `None` nếu lượt đạt, ngược lại trả **lý do đầu tiên** theo thứ tự:
  - `expected_source is None`: đạt khi `answer == REFUSAL` và `sources == []`; không thì `"no_refusal"`.
  - Ngược lại: `answer == REFUSAL` → `"refused"`; `expected_source not in sources` → `"wrong_source"`; có fact không nằm trong `answer` (so không phân biệt hoa thường) → `"missing_fact"`.
- `run_dialog_eval`: với **mỗi dialog gọi `make_bot()` một lần** (bot mới, không lẫn lịch sử giữa dialog), hỏi các lượt theo thứ tự, trả list theo đúng thứ tự dialog rồi lượt: `{"dialog": id, "turn": n, "ok": bool, "reason": str | None}` với `n` đếm từ 1.
- `compare_to_baseline`:
  - `current` rỗng → `ValueError`.
  - Ghép theo khóa `(dialog, turn)`.
  - `pass_rate = round(số ok / len(current), 3)`.
  - `fixed`: khóa trước fail (trong baseline) nay ok; `broken`: trước ok nay fail; `new`: khóa không có trong baseline (không tính vào fixed/broken). Ba list chứa tuple `(dialog, turn)`, theo thứ tự trong `current`.
  - `failures`: list `(dialog, turn, reason)` của mọi lượt fail trong `current`, theo thứ tự.
  - `gate_ok = not broken and pass_rate >= min_pass_rate`.
  - Trả `{"pass_rate", "fixed", "broken", "new", "failures", "gate_ok"}`.

Phần lesson **chưa** làm (ghi rõ trong prompt): bot mới cho từng dialog, lý do fail theo thứ tự ưu tiên, khóa `(dialog, turn)`, ca `new`, danh sách `failures`, cổng `gate_ok`.

## Việc cần làm
1. `exercise.yaml`: `id: cap-01-ex02`, `kind: project`, `difficulty: 3`, `tags: [evaluation, rag]`, title en/vi, 3 hint mỗi ngôn ngữ theo CONTENT_GUIDE (hint 1 trỏ lesson §5 + ví dụ cụ thể; hint 2 kế hoạch đánh số; hint 3 khung code với 1–2 chỗ `...`). Không có `runner`.
2. `starter.py`: hằng `REFUSAL`, 3 hàm có chữ ký, docstring + ví dụ, `# TODO` từng bước, `return None`. Import được.
3. `solution.py` theo hợp đồng; **không chép** khối `compare_to_baseline` 5 dòng của lesson §5 (validator cảnh báo khi trùng ≥ 5 dòng liền). `alternatives/01_*.py`: cách khác thật (ví dụ dựng dict `{(dialog, turn): result}` bằng comprehension và dùng set cho fixed/broken rồi sắp lại theo thứ tự current), kèm `.en.md`/`.vi.md`.
4. `test_exercise.py` (8–12 test, chỉ tập con pytest được phép). Bot giả trong file test: ví dụ `ScriptedBot(replies: dict[str, dict])` trả kết quả theo câu hỏi, và một bot có lịch sử để kiểm cô lập dialog (ví dụ bot trả `REFUSAL` nếu đã được hỏi trước đó trong cùng đời bot). Bắt buộc có test cho:
   - mỗi lý do `no_refusal`, `refused`, `wrong_source`, `missing_fact`, và thứ tự ưu tiên (lượt vừa sai nguồn vừa thiếu fact → `"wrong_source"`);
   - fact so không phân biệt hoa thường;
   - `make_bot` được gọi đúng một lần mỗi dialog và lịch sử không lẫn giữa dialog;
   - thứ tự và dạng phần tử kết quả của `run_dialog_eval` (turn đếm từ 1);
   - `fixed`, `broken`, `new` đúng trên một baseline có ca thiếu; `failures` đúng thứ tự;
   - `gate_ok` sai khi có `broken` dù `pass_rate` cao, sai khi `pass_rate` dưới ngưỡng, đúng khi cả hai ổn; giá trị biên `pass_rate == min_pass_rate` là đạt;
   - `current` rỗng → `ValueError`.
5. `prompt.en.md` / `prompt.vi.md`: task 2–4 câu, **Example** (2 dialog ngắn, kết quả `run_dialog_eval` và `compare_to_baseline`), **Rules** đủ hợp đồng. VI tự nhiên, "bạn", không "ta"/"chúng ta".

## Tiêu chí hoàn thành (checklist)
- [ ] Starter: mọi test fail; solution + alternative: mọi test pass (pytest và runner trình duyệt, validate kiểm)
- [ ] Validate capstone chỉ còn `missing quiz.yaml`, 0 cảnh báo
- [ ] Mutant (làm ở thư mục tạm, không sửa repo): gọi `make_bot` một lần cho mọi dialog; đảo thứ tự lý do; tính `new` vào `broken`; `>` thay `>=` ở ngưỡng; bỏ hạ chữ thường khi so fact → mỗi cái làm ít nhất một test fail. Ghi kết quả vào report.

## Lệnh kiểm tra
Chạy từ gốc repo `D:\Proj\python-ai-platform`:
```bash
D=curriculum/capstones/cap-01-rag-chatbot
uv run python tools/validate.py --path $D
uv run python -m pytest $D -q
EXERCISE_TARGET=starter uv run python -m pytest $D/exercises/ex02-dialog-eval -q
uv run ruff check $D
git status --short
```
Mong đợi: validate chỉ báo `missing quiz.yaml`; pytest xanh; lệnh starter 0 passed.

## Ghi chú cho worker
- Không chạy server hay dev server.
- Khuôn file: xem `curriculum/capstones/cap-01-rag-chatbot/exercises/ex01-chatbot/` (vừa xong) và `docs/CONTENT_GUIDE.md`.

## Trạng thái
- Bước hiện tại: 5 (đạt vòng 1; boss kiểm: validate chỉ `missing quiz.yaml`, 26 test capstone pass, starter 0 pass, thêm 6 mutant của boss đều bị bắt; chờ duyệt commit)
- Vòng: 1/3
- Số lần swap: 0
- Fallback: không
- Model: Gemini 4 Hydrogen (High)
