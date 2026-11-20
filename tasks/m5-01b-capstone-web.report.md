# Báo cáo M5 bước 1b: web mở được capstone

## Đã làm gì
1. **`apps/web/src/lib/types.ts`**:
   - Cập nhật `Catalog.capstones` sang kiểu `LessonSummary[]`.
   - Thêm trường `runner?: "local"` cho `Exercise`.
2. **`apps/web/src/lib/content.ts`**:
   - Thêm `capstones` (map từ `catalog.capstones` kèm `phaseId: "cap"`), tách biệt hoàn toàn khỏi `allLessons` và `readyLessons` để không ảnh hưởng tổng số bài, tiến độ phase, dashboard hay `neighbours`.
   - Cập nhật `findLesson(id)` tìm trong cả `allLessons` và `capstones`.
   - Thêm `isCapstone(id)`.
3. **`apps/web/src/lib/content-server.ts`**:
   - Cập nhật `lessonIds()` bao gồm thêm các capstone có `ready: true` để trang `/lesson/<id>/` được tạo tĩnh khi có capstone sẵn sàng.
4. **`apps/web/src/components/lesson/lesson-view.tsx`**:
   - Khi `phase` là `undefined` (capstone), dòng trên tiêu đề hiển thị `t("capstoneBadge")` ("Capstone") thay vì tên phase và số thứ tự; các nút bài trước/sau (`prev`/`next` từ `neighbours`) tự tắt do capstone không nằm trong `readyLessons`.
   - Tính `runner = editingExercise ? (exercise.runner ?? meta.runner) : meta.runner` và truyền vào cả `RunnerContext.Provider` lẫn `Workbench` để Run/Test/Visualize, chip "Local runner" và khung hướng dẫn khi runner chưa chạy hoạt động theo từng exercise (giữ nguyên hành vi cho bài thường).
5. **`apps/web/src/app/(main)/learn/page.tsx`**:
   - Ở khu "Capstones": giữ nguyên giao diện khóa + tên cho capstone `ready: false`.
   - Với capstone `ready: true`: hiển thị thành link tới `/lesson/<id>/` kèm trạng thái từ `lessonStatus`/`lessonParts` (đã xong / đang làm / chưa bắt đầu / cần học bài trước), thanh tiến độ khi đang làm, và cảnh báo `prereqWarning` liệt kê các bài tiên quyết đã `ready` nhưng chưa hoàn thành/chưa skip (tra tên bài qua `findLesson`).
6. **`apps/web/src/app/(main)/portfolio/page.tsx`**:
   - Tách thẻ project thành component dùng chung `ProjectCard` trong cùng file.
   - Ở khu "Capstones": capstone `ready: true` dùng chung `ProjectCard` (tiến độ, nút tiếp tục, xem code, tải `.py` khi hoàn thành) với nhãn `"Capstone"` (`t("capstoneLabel")`) và icon `Trophy`; capstone `ready: false` giữ nguyên thẻ khóa nét đứt.
7. **`apps/web/messages/en.json` & `apps/web/messages/vi.json`**:
   - Thêm `lesson.capstoneBadge` (`"Capstone"`) và `portfolio.capstoneLabel` (`"Capstone"`) ở cả hai file.

## File đã sửa / tạo
- `apps/web/src/lib/types.ts`
- `apps/web/src/lib/content.ts`
- `apps/web/src/lib/content-server.ts`
- `apps/web/src/components/lesson/lesson-view.tsx`
- `apps/web/src/app/(main)/learn/page.tsx`
- `apps/web/src/app/(main)/portfolio/page.tsx`
- `apps/web/messages/en.json`
- `apps/web/messages/vi.json`
- `tasks/m5-01b-capstone-web.report.md` (tạo mới)

## Kết quả lệnh kiểm tra
Chạy tại `D:\Proj\python-ai-platform` (dùng `pnpm.cmd` do PowerShell chặn execution policy của `pnpm.ps1`):
- `pnpm.cmd --filter web typecheck`: **PASS** (exit code 0; `build_content.py` built 54 lessons, 11 exams, 324 flashcards, 866 questions; `tsc --noEmit` không lỗi).
- `pnpm.cmd --filter web build`: **PASS** ngay lần chạy đầu tiên (exit code 0; `Generating static pages using 17 workers (79/79)`).
- `git status --short`:
  ```text
   M apps/web/messages/en.json
   M apps/web/messages/vi.json
   M apps/web/src/app/(main)/learn/page.tsx
   M apps/web/src/app/(main)/portfolio/page.tsx
   M apps/web/src/components/lesson/lesson-view.tsx
   M apps/web/src/lib/content-server.ts
   M apps/web/src/lib/content.ts
   M apps/web/src/lib/types.ts
  ?? .hallmark/
  ?? tasks/
  ```
- `git diff --stat`:
  ```text
   apps/web/messages/en.json                      |   2 +
   apps/web/messages/vi.json                      |   2 +
   apps/web/src/app/(main)/learn/page.tsx         |  83 +++++++++--
   apps/web/src/app/(main)/portfolio/page.tsx     | 193 +++++++++++++++----------
   apps/web/src/components/lesson/lesson-view.tsx |   9 +-
   apps/web/src/lib/content-server.ts             |   8 +-
   apps/web/src/lib/content.ts                    |  11 +-
   apps/web/src/lib/types.ts                      |   3 +-
   8 files changed, 215 insertions(+), 96 deletions(-)
  ```

## Điều còn chưa chắc
- Do hiện tại chưa có capstone nào `ready: true` trong dữ liệu build thực tế (và không chạy dev server/trình duyệt theo hướng dẫn), giao diện runtime của capstone `ready: true` trên `/learn/`, `/portfolio/`, `/lesson/<id>/` (cũng như việc chuyển `exercise.runner ?? meta.runner` giữa các exercise khi tương tác thật với local runner) mới được kiểm tra qua đọc code và typecheck/build tĩnh, chưa test trực tiếp trên trình duyệt với dữ liệu capstone mẫu.
- Trong `apps/web/src/app/(main)/learn/page.tsx`, phần `prereqWarning` cho capstone lọc chỉ các bài tiên quyết đã `ready` và chưa hoàn thành/skip (thay vì liệt kê cả bài tiên quyết chưa `ready` như ở dòng bài thường); nếu sau này muốn hiện cả bài tiên quyết chưa `ready` thì có thể bỏ điều kiện `pl.ready` ở bộ lọc `missing`.
