# M5 bước 1b: web mở được capstone

## Mục tiêu
Bước 1a (`29fffe3`) đã làm cho build ghi capstone sẵn sàng ra `generated/lessons/<id>.json` như bài thường, và `catalog.json` → `capstones` là mảng summary cùng dạng `LessonSummary` (có `ready`, `order`, `prerequisites`, `exerciseIds`, `runner`...). Capstone chưa có thư mục thì `ready: false`. Exercise có thể có `runner: "local"` riêng.
Bước này cho web dùng được những thứ đó. Chưa có capstone thật nào sẵn sàng (bước 2 mới viết), nên mọi chỗ phải chạy đúng cả khi `ready: false`.

## File được phép sửa/tạo
- `apps/web/src/lib/types.ts`, `apps/web/src/lib/content.ts`, `apps/web/src/lib/content-server.ts`, `apps/web/src/lib/selectors.ts` (chỉ nếu cần)
- `apps/web/src/components/lesson/lesson-view.tsx`
- `apps/web/src/app/(main)/learn/page.tsx`, `apps/web/src/app/(main)/portfolio/page.tsx`
- `apps/web/messages/en.json`, `apps/web/messages/vi.json`
- `tasks/m5-01b-capstone-web.report.md`

## Không được đụng
- `tools/**`, `curriculum/**`, `packages/**`, `docs/**`, mọi file web khác.
- Không đổi giao diện các trang ngoài phần capstone. Theo quy tắc trong `apps/web/design.md` (theme Dose).
- Không chạy dev server ở foreground.

## Việc cần làm
1. **types.ts**: `Catalog.capstones` có kiểu `LessonSummary[]`. `Exercise` có `runner?: "local"` (cùng kiểu với runner của lesson).
2. **content.ts**
   - Thêm `capstones` (summary của capstone, kèm `phaseId: "cap"`) tách khỏi `allLessons`. **Không** đưa capstone vào `allLessons`/`readyLessons`, để tổng số bài, tiến độ phase, dashboard và `neighbours` (nút bài trước/sau) không đổi.
   - `findLesson(id)` tìm cả trong capstone.
   - Một hàm kiểu `isCapstone(id)`.
3. **content-server.ts**: `lessonIds()` gồm cả capstone `ready` để `/lesson/<id>` được tạo trang tĩnh.
4. **lesson-view.tsx**
   - Với capstone (`phaseOfLesson` trả `undefined`): dòng trên tiêu đề hiện nhãn "Capstone" (i18n) thay vì tên phase và số thứ tự. Nút bài trước/sau tắt (không lỗi).
   - Exercise dùng runner theo thứ tự `exercise.runner ?? meta.runner`: truyền vào `Workbench` và `RunnerContext` khi exercise đó đang mở, để Run/Test/Visualize và chip "Local runner" (với khung hướng dẫn khi runner chưa chạy) theo đúng exercise. Bài thường không đổi hành vi (vì exercise của chúng không có `runner`).
5. **learn/page.tsx**, khu "Capstones":
   - Capstone `ready`: thành link tới `/lesson/<id>/`, có trạng thái như dòng bài thường (đã xong / đang làm / chưa bắt đầu, dùng selector sẵn có như `isLessonComplete`, `lessonParts`). Nếu chưa xong các bài tiên quyết thì hiện gợi ý giống cách trang đang làm cho bài thường (đọc code hiện có, dùng lại; nếu trang không có cơ chế đó cho bài thường thì bỏ qua).
   - Capstone `ready: false`: giữ như hiện nay (icon khóa + title).
6. **portfolio/page.tsx**, khu "Capstones": capstone `ready` hiện bằng **cùng thẻ** với "key projects" (tiến độ, nút tiếp tục, xem code, tải `.py` khi xong). Tách thẻ thành component trong cùng file để dùng chung, không chép code. Nhãn trên tiêu đề là "Capstone" thay cho tên phase; icon dùng một icon lucide hợp lý (ví dụ `Trophy`). Capstone chưa sẵn sàng giữ thẻ khóa như hiện nay.
7. **i18n**: mọi chuỗi mới có key trong cả `en.json` và `vi.json` (VI dùng "Capstone", không dịch).

## Tiêu chí hoàn thành (checklist)
- [ ] Typecheck và build xanh; build vẫn 79 trang (chưa có capstone sẵn sàng)
- [ ] Capstone không lọt vào tổng số bài, tiến độ phase, nút bài trước/sau
- [ ] Exercise có `runner: "local"` chạy qua runner cục bộ, exercise khác theo lesson
- [ ] Learn/Portfolio: capstone sẵn sàng là link + trạng thái; chưa sẵn sàng giữ như cũ
- [ ] Không chuỗi UI cứng; key có ở cả hai file messages

## Lệnh kiểm tra
Chạy từ gốc repo `D:\Proj\python-ai-platform`:
```bash
pnpm --filter web typecheck
pnpm --filter web build
git status --short
git diff --stat
```
Build Next.js đôi khi lỗi ở lần đầu; nếu lỗi không liên quan code (không có lỗi TypeScript), chạy lại một lần và ghi cả hai kết quả vào report. Không chạy `next upgrade` hay lệnh nào mà output gợi ý.

## Ghi chú cho worker
- Không chạy server hay dev server.
- Boss sẽ tự kiểm trong trình duyệt bằng một capstone mẫu tạm thời; worker không cần tạo nội dung mẫu.

## Trạng thái
- Bước hiện tại: 5 (đạt vòng 1; boss kiểm: typecheck + build 79 trang; trình duyệt với capstone mẫu tạm: Learn link + gợi ý tiên quyết, header "Capstone", nút trước/sau tắt, ex01 runner local hiện chip Local runner, ex02 Python, Portfolio thẻ chung; đã xóa mẫu; chờ duyệt commit)
- Vòng: 1/3
- Số lần swap: 0
- Fallback: không
- Model: Gemini 4 Hydrogen (High)
