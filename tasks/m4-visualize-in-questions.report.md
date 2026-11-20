# Báo cáo M4 bước 9a: Visualize trong câu hỏi

## Đã làm gì
1. **`tools/build_content.py`:**
   - Thêm hằng `LOCAL_ONLY_MODULES = ("torch", "transformers", "fastapi", "uvicorn")` và regex `_LOCAL_IMPORT_RE` khớp `^\s*(?:import|from)\s+(?:torch|transformers|fastapi|uvicorn)\b` (multiline).
   - Thêm hàm `question_runner(q) -> str | None` ghép `q.get('code') or ''` với `"\n".join(q.get("lines") or [])` và trả `"local"` nếu khớp import local-only, ngược lại `None`.
   - Thêm hàm chung `attach_question_runners(questions)` gắn `q["runner"] = "local"` (chỉ khi khác `None`) và gọi tại cả hai đầu đọc câu hỏi: `build_lesson()` cho `quiz["questions"]` (tự động lan sang cả `lessons/<id>.json` và `review.json`) và `main()` cho `exam["questions"]` (phase test, placement, mock).
2. **`apps/web/src/lib/types.ts`:**
   - Thêm trường tùy chọn `runner?: "local";` vào interface `Question`.
3. **`apps/web/src/components/markdown.tsx`:**
   - Thêm prop tùy chọn `canVisualize?: boolean` (mặc định `true`) vào `Markdown` và truyền `canVisualize={isPython && canVisualize}` xuống `CodeBlock`.
   - Thêm prop tùy chọn `canVisualize?: boolean` (mặc định `true`) vào `StaticCode` và truyền xuống `Markdown`.
4. **`apps/web/src/components/question.tsx`:**
   - Thêm `canVisualize?: boolean` (mặc định `true`) vào helper `Inline`.
   - Trong `QuestionView`, đọc `inherited = useRunner()` từ `@/lib/local-runner`, bọc toàn bộ nội dung trong `<RunnerContext.Provider value={question.runner ?? inherited}>`.
   - Truyền `canVisualize={revealed}` vào `StaticCode` và mọi `Inline` (prompt, options, explanation) để ẩn hoàn toàn nút Visualize khi `revealed === false` (vẫn giữ nút Sao chép) và hiện lại khi `revealed === true`.
   - Giữ nguyên `FillCode` và `Parsons` (không dùng `StaticCode`/`Markdown` nên không có nút Visualize khi chưa reveal).

## File đã sửa / tạo
- `tools/build_content.py` (sửa)
- `apps/web/src/lib/types.ts` (sửa)
- `apps/web/src/components/markdown.tsx` (sửa)
- `apps/web/src/components/question.tsx` (sửa)
- `tasks/m4-visualize-in-questions.report.md` (tạo mới)

## Kết quả lệnh kiểm tra
- `uv run python tools/build_content.py`: **OK** (exit 0)
  `Built 39 lessons, 9 exams, 234 flashcards, 627 questions -> apps\web\src\generated`
- `uv run python tools/validate.py --fast`: **OK** (exit 0)
  `OK: 0 error(s), 0 warning(s). Checked 39 lessons, 301 markdown pairs, 115 examples, 78 exercises, 69 alternatives, 782 questions, 9 exams, 1 portfolio, 1 glossary, 1 interview.`
- `pnpm.cmd --filter web typecheck` (trên PowerShell dùng `pnpm.cmd` vì `pnpm.ps1` bị chặn bởi execution policy): **OK** (exit 0, `tsc --noEmit` sạch).
- `pnpm.cmd --filter web build`: **OK** (exit 0, `next build` compile thành công, generate 62/62 trang tĩnh).

### Output script đếm `"runner": "local"` theo từng file JSON
Script trong spec đếm mọi chuỗi `"runner": "local"` / `"runner":"local"` trong `apps/web/src/generated/**/*.json` (lưu ý: `catalog.json` và các file `lessons/p6-*.json` còn chứa `runner: "local"` ở metadata của lesson/summary bên cạnh các câu hỏi):
```text
apps/web/src/generated\catalog.json 6
apps/web/src/generated\exams\p6-phase-test.json 10
apps/web/src/generated\lessons\p6-01-tensors.json 14
apps/web/src/generated\lessons\p6-02-training-loop.json 10
apps/web/src/generated\lessons\p6-03-huggingface.json 11
apps/web/src/generated\lessons\p6-04-fine-tune.json 10
apps/web/src/generated\review.json 41
```

Kiểm tra riêng ở cấp độ câu hỏi (`q.get("runner") == "local"`):
- `apps/web/src/generated/exams/p6-phase-test.json`: **10** câu (`p6-test-q01`…`p6-test-q08`, `p6-test-q10`, `p6-test-q15`); các câu không import local-only (`p6-test-q09`, `p6-test-q11`…`q14`, `p6-test-q16`) không có trường `runner`.
- `apps/web/src/generated/lessons/p6-01-tensors.json`: **13** câu (`p6-01-q02`…`q06`, `q08`, `q09`, `q11`…`q16`).
- `apps/web/src/generated/lessons/p6-02-training-loop.json`: **9** câu (`p6-02-q02`, `q03`, `q05`, `q08`…`q10`, `q12`, `q14`, `q16`).
- `apps/web/src/generated/lessons/p6-03-huggingface.json`: **10** câu (`p6-03-q02`, `q04`, `q05`, `q07`…`q09`, `q11`, `q12`, `q14`, `q16`).
- `apps/web/src/generated/lessons/p6-04-fine-tune.json`: **9** câu (`p6-04-q02`, `q04`, `q05`, `q07`, `q08`, `q10`, `q12`, `q13`, `q15`).
- `apps/web/src/generated/review.json`: **41** câu (`13 + 9 + 10 + 9`).
- `apps/web/src/generated/exams/p5-phase-test.json` và các phase khác: **0** câu có trường `runner`.

## Điều còn chưa chắc
- Chưa mở trình duyệt / dev server để kiểm tra trực tiếp DOM lúc chưa reveal vs đã reveal ở từng màn (exam, lesson quiz, review) và chưa chạy thử nút Visualize thực tế trên câu có `import torch` với local runner đang bật (vì spec chỉ chạy build/typecheck/validate tĩnh và không chạy dev server).
- Trong `p6-phase-test.json`, ngoài `p6-test-q01`…`q08` và `q15` được nêu trong checklist, `p6-test-q10` cũng có `import torch` trong `code` nên cũng được gắn `"runner": "local"` (đúng theo rule regex của spec).
- Các câu hỏi nhắc tới `torch`/`transformers` bằng chữ trong câu chữ (không có dòng `import torch` trong `code`/`lines`) hoặc câu `p6-03-huggingface` chỉ dùng `pipeline`/`AutoTokenizer` dạng snippet không `import` rõ ràng sẽ không tự gắn `runner: "local"` nếu đứng ngoài bài học `runner: local` (theo đúng thiết kế regex hiện tại).
