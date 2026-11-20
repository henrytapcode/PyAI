# Báo cáo: M3 bước 15c — xáo thứ tự lựa chọn trắc nghiệm (`mcq`)

## 1. Đã làm gì

- **`apps/web/src/components/question.tsx`** (`QuestionView`):
  - Tính `order: number[]` bằng `useMemo` phụ thuộc `[question.id, question.shuffle_options, optionCount]` (với `optionCount = question.type === "mcq" ? (qt.options ?? []).length : 0`):
    - Nếu `question.shuffle_options === false`: giữ nguyên `[0, 1, ..., optionCount - 1]`.
    - Ngược lại: `shuffle(indices, seedOf(question.id))` dùng lại `shuffle` từ `@/lib/utils` và `seedOf` có sẵn trong file.
  - Render lựa chọn theo `order.map((i, pos) => ...)`:
    - Nội dung hiển thị lấy `options[i]`, `key={i}`, `chosen = answer.choice === i`, `isRight = i === question.answer`, `onClick` vẫn gửi `{ type: "mcq", choice: i }` (chỉ số gốc trong YAML).
    - Nhãn chữ cái hiển thị theo vị trí hiển thị `String.fromCharCode(65 + pos)` (`A`, `B`, `C`, `D` từ trên xuống).
  - Cập nhật `useEffect` phím tắt (`A`–`D` / `1`–`4`): tính vị trí hiển thị `pos`, khi hợp lệ (`pos >= 0 && pos < order.length`) gửi `{ type: "mcq", choice: order[pos] }`; thêm `order` vào dependency array.
- **`docs/CONTENT_GUIDE.md`** (mục `## quiz.yaml: a question bank`):
  - Sửa đúng một câu `"Options are shuffled, so never write ..."` thành mô tả hành vi mới: lựa chọn được hiển thị theo thứ tự xáo cố định theo `question id`, giữ nguyên lời khuyên không viết `"All of the above"`, `"Both A and B"` hoặc nội dung phụ thuộc vị trí, và giữ nguyên phần `shuffle_options: false`. Các câu khác giữ nguyên.

## 2. File đã sửa

- `apps/web/src/components/question.tsx`
- `docs/CONTENT_GUIDE.md`
- Báo cáo mới tạo: `tasks/m3-mcq-shuffle.report.md`

Lưu ý: `docs/` nằm trong `.gitignore` (dòng 20: `docs/`), nên `git diff --stat` chỉ hiển thị `apps/web/src/components/question.tsx`.

## 3. Kết quả lệnh kiểm tra

1. `pnpm.cmd --filter web typecheck` (sau lần sửa cuối): **PASS** (exit code 0)
   - `build_content.py`: `Built 30 lessons, 6 exams, 180 flashcards, 483 questions -> apps\web\src\generated`
   - `tsc --noEmit`: 0 lỗi.
2. `node "$env:USERPROFILE\.claude\skills\hallmark\scripts\sloplint.mjs" apps/web/src --genre modern-minimal --scope app --kept`:
   - **Trước khi sửa**: `sloplint: clean. 0 FAIL, 0 REFLEX, 0 WARN across 45 file(s).` / `kept: links 20/20, fields 1/1, handlers 125/125; before 3 FAIL, 0 REFLEX, now 0 FAIL, 0 REFLEX` (exit code 0).
   - **Sau lần sửa cuối**: `sloplint: clean. 0 FAIL, 0 REFLEX, 0 WARN across 45 file(s).` / `kept: links 20/20, fields 1/1, handlers 125/125; before 3 FAIL, 0 REFLEX, now 0 FAIL, 0 REFLEX` (exit code 0, không giảm số `kept`).
3. `git diff --stat` (sau lần sửa cuối):
   - `apps/web/src/components/question.tsx | 18 ++++++++++++------`
   - `1 file changed, 12 insertions(+), 6 deletions(-)`

## 4. Điều còn chưa chắc / chưa kiểm tra runtime

- **Chưa kiểm tra trên trình duyệt**: không mở trình duyệt chạy thực tế trong lượt này. Cần kiểm tra thủ công trong app:
  - Quiz bài học, phase test, review/mock exam/placement có xáo cố định theo `question.id` và giữ nguyên thứ tự gốc khi `shuffle_options: false`.
  - Khi đã trả lời (`revealed`), ô đúng/sai tô màu đúng theo chỉ số gốc trong khi nhãn chữ cái vẫn là `A`, `B`, `C`, `D` từ trên xuống.
  - Phím tắt `A`–`D` / `1`–`4` chọn đúng lựa chọn ở vị trí hiển thị tương ứng.
  - Đổi ngôn ngữ `VI ↔ EN` giữ nguyên thứ tự hiển thị (dựa trên giả định số `options` giữa `en` và `vi` bằng nhau theo spec `CONTENT_GUIDE.md`).
- Trong `docs/CONTENT_GUIDE.md` dòng 142 vẫn còn câu `"The app draws 10 per attempt and shuffles questions and options every time."` — giữ nguyên theo chỉ dẫn `"chỉ câu nói về việc xáo lựa chọn ... Giữ nguyên mọi câu khác"`, chưa rõ có cần chỉnh thêm cụm `"every time"` ở dòng 142 hay không.
