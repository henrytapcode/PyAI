# M5 bước 2f: sửa capstone 1 theo review Opus

## Mục tiêu
Reviewer Opus đã soát 100% `curriculum/capstones/cap-01-rag-chatbot/` (điểm: lesson 4, ex01 4, ex02 3.5, ex03 3, quiz 3.5, VI 4). Sửa mọi điểm dưới đây, giữ nguyên mọi thứ khác. Boss đã kiểm lại điểm 6: `ChatBot` thật từ chối "How much does delivery cost?" ở lượt 1.

## File được phép sửa
- Mọi file trong `curriculum/capstones/cap-01-rag-chatbot/` (lesson EN/VI, examples, 3 exercise kể cả `exercise.yaml`, prompt, starter, solution, alternatives, test, `quiz.yaml`, `meta.yaml`)
- `curriculum/syllabus.yaml`: chỉ outcomes của `cap-01-rag-chatbot`
- `curriculum/portfolio.yaml`: chỉ mục `cap-rag-chatbot`
- `tasks/m5-cap01-review-fixes.report.md`

## Không được đụng
- `tools/**`, `apps/**`, `packages/**`, `docs/**`, các phase, mục khác của syllabus/portfolio.

## Việc cần làm
### Nặng
1. **ex03 bộ đếm ID không cần `nonlocal`** (học viên chưa học `nonlocal`): trong `solution.py`, alternative, hint 3 (en/vi) và Rules của prompt, giữ bộ đếm bằng dạng đã học, ví dụ `state = {"next_id": 1}` trong closure (sửa phần tử dict, không gán lại tên). Prompt có 1 câu nói vì sao dùng dict (gán lại biến ngoài trong hàm lồng sẽ lỗi `UnboundLocalError`). Không dùng `nonlocal` ở đâu trong capstone.

### Vừa
2. **ex02 prompt Example (en/vi):** ví dụ phải tự đúng: định nghĩa rõ `make_bot` là bot giả (stub) trong khối ví dụ, và kết quả in ra khớp đúng stub đó. Không ngụ ý là `ChatBot` thật.
3. **ex02 hint 3 (en/vi):** không cho trọn `score_turn`; để `...` ở 2 nhánh, thêm khung vòng lặp cho `run_dialog_eval` (cũng có `...`).
4. **ex03 hint 3 (en/vi):** để `...` ở key của `min(...)` khi loại phiên; thay vào đó cho sẵn khung `require_session`. Tiêu đề hint khớp phần để trống.
5. **ex01 test:** thêm test câu dài > 4 từ bắt đầu bằng "What about " (ví dụ `"What about the photo ID needed at the counter?"`) được viết lại; thêm test không phân biệt hoa thường cho tiền tố (ví dụ `"AND photo ID please"` hoặc "WHAT ABOUT ..."). Thêm test khi có hit thì `chat` được gọi đúng 1 lần với `temperature=0.0` (SpyClient ghi lại kwargs). Đổi tên `test_long_question_and_android_prefix_are_not_rewritten` cho đúng nghĩa từng case (tách test nếu cần).
6. **Câu mẫu bị từ chối:** ở lesson §1 Story 1 (EN/VI), hint 1 ex01, "Try it" của example 01, prompt ex03: thay câu lượt 1 bằng câu mà `ChatBot` thật trả lời được, và câu nối tiếp sau đó vẫn ra đúng nguồn. Kiểm bằng `solution.py` của ex01 trên `docs` trong lesson (ghi đoạn chạy + output vào report). Nếu chỗ nào cố ý dùng câu bị từ chối thì nói rõ trong câu chữ ("lượt 1 bị từ chối nhưng vẫn vào history...").
7. **Lesson tự giải ex01:** §9 lỗi #2 (EN/VI) giữ code sai + output sai, nhưng phần sửa chỉ nói bằng lời (không có code sửa ghim system). Cột "chưa làm trong bài" của §7 giữ nguyên.
8. **Số dòng trong `examples/*.en.md` và `.vi.md`:** đánh lại cho khớp file `.py` hiện tại (reviewer: 01 ghi 28–35/38–61, thật 27–34/37–60; 02 "line 77" thật 81, khối 44–77; 03 thật 47–60/62–68). Tự kiểm lại từng số.
9. **quiz q02 explanation (en/vi):** sửa số token cho đúng (reviewer: `sys_msg`=5, lượt user bị bỏ=6, "What about express?"=4; 5+6+5+4=20 > 16, bỏ 6 còn 14). Tự tính lại bằng `count_tokens`.
10. **quiz distractor q01, q05, q08, q09, q13:** thay distractor phi lý bằng hiểu lầm thật (ví dụ: cắt từ cuối list; chỉ cắt khi vượt context window của model; dùng chung bot vẫn được vì index không đổi; so độ dài câu theo ký tự thay vì từ). Giữ độ dài lựa chọn xấp xỉ nhau, đáp án đúng không dài nhất duy nhất. Cập nhật explanation nếu cần.
11. **Claim "tested end to end":** viết lại outcome 4 trong `meta.yaml` + `syllabus.yaml` và `pitch`/`cv_bullet` portfolio cho đúng: dịch vụ nhận bất kỳ bot nào có `ask` (test bằng bot giả), nối với `ChatBot` của ex01 khi chạy thật.

### Nhẹ
12. **ex03 starter:** bỏ class `MessageRequest` viết sẵn; để `# TODO` cho học viên tự viết model body (rule 422). Starter vẫn import được (mọi test fail).
13. **ex02 test:** case `wrong_source` thứ 4 trùng ý case 2 → thay bằng `REFUSAL` kèm `sources` khác rỗng ở lượt cần từ chối (→ `"no_refusal"`).
14. **quiz q11:** chấp nhận thêm đáp án tương đương (`"0.8"` nếu ngữ cảnh đúng, `len(broken) == 0` / `not broken` cho ô đầu) theo dạng list accepted strings.
15. **`examples/03_session_store.py`:** `create()` với sid đã có không được ghi đè history (thêm nhánh `if sid in self.sessions`). Cập nhật `.out` và `.md` nếu output đổi.
16. **Lesson §4 (EN/VI):** thêm 1 câu nêu giới hạn quy tắc "≤ 4 từ" (ví dụ "Thanks" cũng bị ghép) và rằng ex01 chấp nhận giới hạn này.
17. **Alternative ex01 `.en.md`/`.vi.md`:** bỏ khẳng định "O(1)" hoặc nói đúng (code chuyển list↔deque mỗi lượt).
18. **Rubric §8 (EN/VI):** ghi rõ "100% grounded", "zero wasted chat() calls" đo bằng test ex01 (không phải bằng ex02).
19. **VI:** `ex03/prompt.vi.md` "vẫn còn đủ `max_sessions`" → "nếu sau khi dọn mà số phiên vẫn đạt `max_sessions`"; `ex01/prompt.vi.md` + hint 2 "từ đầu (chữ thường)" → "từ đầu tiên (viết thường)"; `lesson.vi.md` "vừa khít `budget`" → "nằm trong `budget`"; gloss "tất định (deterministic)" ở lần đầu.

## Tiêu chí hoàn thành (checklist)
- [ ] 19 điểm đã sửa (report có bảng: điểm → file → đã sửa gì)
- [ ] grep `nonlocal` trong capstone ra 0 dòng
- [ ] Validate capstone 0 lỗi 0 cảnh báo; pytest capstone xanh; starter của cả 3 exercise 0 passed
- [ ] MCQ: bảng độ dài như bước 2e, không câu nào đáp án đúng dài hơn lựa chọn dài thứ hai quá 20%
- [ ] Số dòng trong mọi `examples/*.md` khớp `.py`

## Lệnh kiểm tra
Chạy từ gốc repo `D:\Proj\python-ai-platform`:
```bash
D=curriculum/capstones/cap-01-rag-chatbot
uv run python tools/validate.py --path $D
uv run python -m pytest $D -q
for e in ex01-chatbot ex02-dialog-eval ex03-session-service; do EXERCISE_TARGET=starter uv run python -m pytest $D/exercises/$e -q | tail -1; done
uv run ruff check $D
grep -rn "nonlocal" $D || echo "no nonlocal"
grep -rnE "(^|[ .:(\"'])(Ta|ta|Chúng ta|chúng ta) " $D --include=*.vi.md | grep -v "người ta"
uv run python tools/validate.py --fast
git status --short
```

## Ghi chú cho worker
- Không chạy server hay dev server.
- Sau khi đổi solution/test, tự chạy lại mutant cũ của bước 2b–2d ở thư mục tạm nếu có liên quan (ít nhất: ex03 dùng chung bot, `>` thay `>=` TTL) và ghi kết quả.

## Trạng thái
- Bước hiện tại: 5 (đạt vòng 1; boss kiểm: validate capstone 0/0, 45 test pass, starter fail (validate kiểm), không nonlocal, câu Story 1 mới trả lời đúng với ChatBot thật, số dòng example khớp, validate --fast 0 lỗi; chờ duyệt commit)
- Vòng: 1/3
- Số lần swap: 0
- Fallback: không
- Model: Gemini 4 Hydrogen (High)
