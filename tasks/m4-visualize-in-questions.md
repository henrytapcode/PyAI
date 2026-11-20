# M4 bước 9a: Visualize trong câu hỏi (ẩn khi đang làm, chạy đúng runner khi xem lại)

## Mục tiêu
Hai lỗi trong `QuestionView` (`apps/web/src/components/question.tsx`). Component này được dùng ở bài thi (`exam-runner.tsx`), quiz trong bài (`lesson/lesson-quiz.tsx`) và trang ôn tập (`app/(main)/review/page.tsx`).
1. **Lộ đáp án:** khối code của câu hỏi (qua `StaticCode` → `Markdown` → `CodeBlock`) luôn có nút **Visualize**. Đang làm câu "đoán output" mà bấm Visualize là thấy luôn kết quả in ra. Phải ẩn Visualize khi câu chưa `revealed`.
2. **Sai runner:** ngoài trang bài học không có `RunnerContext`, nên Visualize luôn chạy bằng Pyodide. Câu có `import torch` (phase test 6) báo `ModuleNotFoundError: No module named 'torch'`. Câu cần thư viện chỉ có ở runner cục bộ phải chạy qua runner cục bộ.

## File được phép sửa/tạo
- `tools/build_content.py`
- `apps/web/src/lib/types.ts`
- `apps/web/src/components/markdown.tsx`
- `apps/web/src/components/question.tsx`
- `tasks/m4-visualize-in-questions.report.md`

## Không được đụng
- `curriculum/**`, `tools/validate.py`, `tools/localrunner/**`, `tools/pyrunner/**`, các component khác, `messages/*.json` (không cần chuỗi UI mới).
- Không `git commit`, không chạy dev server ở foreground.
- **Không chạy `pnpm --filter web build` khi dev server đang chạy.**

## Thiết kế (boss chốt)
1. **`tools/build_content.py`:**
   - Thêm hằng `LOCAL_ONLY_MODULES = ("torch", "transformers", "fastapi", "uvicorn")`.
   - Thêm hàm `question_runner(q) -> str | None`. Hàm ghép `q.get("code", "")` với `"\n".join(q.get("lines", []))`, rồi trả `"local"` nếu có dòng khớp regex `^\s*(?:import|from)\s+(torch|transformers|fastapi|uvicorn)\b` (multiline), ngược lại trả `None`.
   - Gắn `q["runner"] = "local"` (chỉ khi khác None) cho **mọi** câu hỏi được ghi ra: quiz của từng bài (gồm cả bản trong danh sách `review`) và câu hỏi của mọi exam (phase test, placement, mock). Làm ở một chỗ chung để không sót.
2. **`apps/web/src/lib/types.ts`:** thêm `runner?: "local";` vào interface `Question`.
3. **`apps/web/src/components/markdown.tsx`:**
   - `Markdown` nhận thêm prop tùy chọn `canVisualize?: boolean` (mặc định `true`) và truyền xuống `CodeBlock` là `canVisualize={isPython && canVisualize}`.
   - `StaticCode` nhận thêm `canVisualize?: boolean` (mặc định `true`) và truyền cho `Markdown`.
   - Hành vi hiện tại ở lesson và example không đổi.
4. **`apps/web/src/components/question.tsx`:**
   - Khi `revealed === false`: không khối code nào trong `QuestionView` có nút Visualize. Điều này gồm `StaticCode` của câu hỏi và mọi `Markdown` qua `Inline` (prompt, option). Nút Sao chép vẫn giữ.
   - Khi `revealed === true`: hiện Visualize như bây giờ.
   - Bọc nội dung `QuestionView` trong `<RunnerContext.Provider value={question.runner ?? inherited}>`, với `inherited = useRunner()` để quiz trong bài `runner: local` vẫn kế thừa runner của bài. Import từ `@/lib/local-runner`.
   - Câu `fill` và `parsons` hiện không dùng `StaticCode` cho phần code chính. Giữ nguyên, chỉ cần chắc chắn chúng không lộ nút Visualize khi chưa reveal.

## Tiêu chí hoàn thành (checklist)
- [ ] `uv run python tools/build_content.py` chạy được. Trong `apps/web/src/generated/`:
  - Các câu `p6-test-q01`…`q08` và `q15` (những câu có `import torch` trong `code`/`lines`) có `"runner": "local"`.
  - Câu phase 5 và câu không import torch không có trường `runner`.
  - Report ghi số câu được gắn `runner` theo từng file JSON (lấy bằng script).
- [ ] Đang làm bài thi, quiz hoặc ôn tập (chưa reveal): DOM không có nút Visualize trong câu hỏi.
- [ ] Sau khi nộp hoặc reveal: có nút Visualize. Câu phase 6 có torch truyền `runner="local"` vào `visualize(...)`.
- [ ] `pnpm --filter web typecheck` và `pnpm --filter web build` xanh.
- [ ] `uv run python tools/validate.py --fast` 0 lỗi.
- [ ] Chỉ sửa đúng các file được phép.

## Lệnh kiểm tra
```
uv run python tools/build_content.py
uv run python tools/validate.py --fast
pnpm --filter web typecheck
pnpm --filter web build
git status --short
```
Đếm câu có runner (in theo file):
```
uv run python -c "
import json,glob
for f in sorted(glob.glob('apps/web/src/generated/**/*.json', recursive=True)):
    s=open(f,encoding='utf-8').read()
    n=s.count('\"runner\": \"local\"')+s.count('\"runner\":\"local\"')
    if n: print(f,n)
"
```

## Ghi chú cho worker
- Đọc `apps/web/src/lib/local-runner.ts` (`RunnerContext`, `useRunner`) và `apps/web/src/components/visualizer.tsx` để hiểu cách `visualize(code, runner)` chọn backend.
- Đọc `apps/web/src/components/exam-runner.tsx` (QuestionView dùng `revealed` lúc làm bài và lúc xem lại) và `lesson/lesson-quiz.tsx`.
- Không thêm chuỗi UI cứng.
- Boss sẽ tự kiểm trong app, có bật runner cục bộ.

## Trạng thái
- Bước hiện tại: 5 (đạt vòng 1; boss đổi lại line ending LF cho build_content.py; kiểm trong app: đang làm bài thi 0 nút Visualize ở 16 câu, sau khi nộp có 7 nút, câu torch chạy qua runner cục bộ ra đúng output; quiz trong bài ẩn Visualize; typecheck, build, validate --fast xanh, ruff không thêm lỗi; đã commit `7f5b668`)
- Vòng: 1/3
- Số lần swap: 0
- Fallback: không
- Model: Gemini 4 Hydrogen (High)
