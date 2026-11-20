# M3 bước 15c: xáo thứ tự lựa chọn trắc nghiệm (mcq)

## Mục tiêu
App hiện hiển thị lựa chọn mcq đúng thứ tự trong yaml (`apps/web/src/components/question.tsx`, dòng ~74–116 chỉ `map` theo thứ tự gốc; chỉ parsons được xáo ở dòng ~196–205). `docs/CONTENT_GUIDE.md` lại nói lựa chọn được xáo, nên tác giả không để ý vị trí đáp án (vd phase 4 test bản đầu 5/8 đáp án là A).
Sửa để mọi câu mcq (quiz bài học, review, phase test, mock exam, placement — tất cả đều đi qua `QuestionView`) hiển thị lựa chọn theo **thứ tự xáo cố định theo id câu hỏi**, trừ câu có `shuffle_options: false`.

## File được phép sửa
- `apps/web/src/components/question.tsx`
- `docs/CONTENT_GUIDE.md`: **chỉ** câu nói về việc xáo lựa chọn trong mục quiz.yaml (xem mục 5).

## Không được đụng
- `apps/web/src/lib/quiz.ts` (hàm `grade`, `correctAnswerText`), `lib/types.ts`, `lib/storage.ts`, `lib/utils.ts`, mọi component khác, nội dung `curriculum/`, `tools/`.
- Không đổi hình dạng `UserAnswer` hay dữ liệu lưu trong localStorage.
- Không `git commit`, **không chạy `pnpm --filter web build`** (dev server đang chạy).

## Thiết kế (boss chốt)
1. **Chỉ đổi thứ tự hiển thị.** `answer.choice` vẫn là **chỉ số gốc** trong `options` của yaml. Nhờ vậy `grade()`, tiến độ đã lưu, báo cáo bài thi và review không cần đổi.
2. Trong `QuestionView`, tính `order: number[]` bằng `useMemo`:
   - `question.shuffle_options === false` → `[0, 1, ..., n-1]`.
   - ngược lại → `shuffle([0..n-1], seedOf(question.id))` (dùng lại `shuffle` từ `lib/utils` và `seedOf` có sẵn trong file).
   - n lấy từ `qt.options.length` (EN và VI cùng số option, nên đổi ngôn ngữ không đổi thứ tự).
3. Render: `order.map((orig, pos) => ...)`:
   - nhãn chữ cái theo **vị trí hiển thị** `String.fromCharCode(65 + pos)`;
   - `chosen = answer.choice === orig`, `isRight = orig === question.answer`;
   - `onClick` gửi `{ type: "mcq", choice: orig }`;
   - `key` dùng `orig`.
4. Phím tắt A–D / 1–4 (useEffect dòng ~45–56): phím chọn **vị trí hiển thị** `pos`, gửi `choice: order[pos]`. Thêm `order` vào dependency của effect.
5. `docs/CONTENT_GUIDE.md` mục quiz.yaml: sửa câu "Options are shuffled, so never write ..." cho đúng hành vi mới: lựa chọn được hiển thị theo thứ tự xáo cố định theo id câu (giữ nguyên lời khuyên không viết "All of the above", và `shuffle_options: false` để giữ thứ tự). Giữ nguyên mọi câu khác.

## Tiêu chí hoàn thành (checklist)
1. [ ] Đúng thiết kế trên; không có file nào ngoài danh sách bị sửa.
2. [ ] Câu có `shuffle_options: false` hiển thị đúng thứ tự gốc.
3. [ ] Sau khi trả lời (revealed), ô đúng/sai tô đúng màu theo chỉ số gốc; nhãn chữ cái vẫn A, B, C, D từ trên xuống.
4. [ ] Đổi VI ↔ EN không đổi thứ tự lựa chọn của cùng một câu.
5. [ ] Lệnh kiểm tra xanh.

## Lệnh kiểm tra
Từ gốc repo `D:\Proj\python-ai-platform`:
```
pnpm --filter web typecheck
node ~/.claude/skills/hallmark/scripts/sloplint.mjs apps/web/src --genre modern-minimal --scope app --kept
git diff --stat
```
Mong đợi: typecheck 0 lỗi; sloplint 0 FAIL và dòng `kept:` không giảm so với trước khi sửa (chạy một lần trước khi sửa để có số so sánh, ghi cả hai vào report); diff chỉ 2 file trên.
Không có trình duyệt thì ghi rõ trong report; boss tự kiểm tra trong app (quiz bài học, phase test, phím tắt).

## Ghi chú cho worker
- Windows: dùng `pnpm.cmd` nếu PowerShell chặn `pnpm`.
- Đọc `apps/web/design.md` nếu chạm vào class (không cần đổi class nào).

## Trạng thái
- Bước hiện tại: xong (commit 7cf05bc)
- Vòng: 1/3
- Số lần swap: 0
- Fallback: không
- Model: Gemini 4 Hydrogen (High)
