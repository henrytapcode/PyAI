# Báo cáo: Redesign Dose cho Glossary, Interview, Portfolio, Settings (bước 9)

## 1. Đã làm gì

Đã hoàn thành chuyển đổi 4 trang `/glossary`, `/interview`, `/portfolio`, `/settings` sang theme Dose theo đúng thông số kỹ thuật trong `tasks/redesign-misc-pages.md`, `docs/REDESIGN.md` mục 3 & mục 4 hàng #7, và `apps/web/design.md`.

### Chung (cả 4 trang)
- Xóa bỏ toàn bộ các class và token cấm: không còn `rounded-[`, `border-2`, `font-black`, `font-semibold`, `uppercase`, `transition ` trơn, `transition-all`, `text-hit`, `bg-hit`, `decoration-hit`, `border-edge`, `shadow-[`, `text-[NNpx]`, `backdrop-blur`, `row-cursor`, ký tự `→` trong JSX, `window.confirm`, và literal màu.
- Quy chuẩn radius: controls dùng `rounded-md`, card/panel dùng `rounded-lg`, tag/chip lọc dùng `rounded-full`.
- Khả năng tiếp cận (a11y): các icon trang trí đều có `aria-hidden="true"`, các phần tử bấm tự viết đều có `outline-none focus-visible:outline-2 focus-visible:outline-ring`.
- Chip lọc (TagButton ở Glossary và Interview): `type="button"`, `aria-pressed={active}`, `h-9 px-3 text-sm rounded-full border transition-colors outline-none focus-visible:outline-2 focus-visible:outline-ring`. Khi active dùng `border-primary bg-accent font-bold text-primary` (không tô đặc `bg-primary`), mặc định `border-border bg-card text-foreground hover:bg-accent`.
- Trạng thái đã hoàn thành/đã luyện: dùng `bg-success-soft text-primary-ink` (đạt tương phản WCAG AA ≥ 4.5:1, không dùng `text-success` trên nền `bg-success-soft`).
- Responsive 375px: đảm bảo không có phần tử gây tràn ngang trang (`overflow-x-auto` cho khối code `pre`, cấu trúc flex-col ở màn nhỏ).

### Chi tiết từng trang
1. **Glossary (`apps/web/src/app/(main)/glossary/page.tsx`)**:
   - Khối tìm kiếm sticky: nền đặc `bg-background`, viền dưới hairline `border-b border-border`, `py-3`, giữ `sticky top-14 lg:top-0 z-10`.
   - Ô tìm kiếm: `rounded-md border border-border bg-card h-10 px-3`, `focus-within:outline-2 focus-within:outline-ring` (bỏ hoàn toàn `ring-ring/40`); input có `aria-label={t("placeholder")}`.
   - Danh sách thuật ngữ: chuyển từ lưới card sang dạng danh sách hàng/bảng với khung `rounded-lg border border-border bg-card divide-y divide-border`.
   - Mỗi hàng: cột trái hiển thị thuật ngữ `font-mono text-sm font-bold` và tên tiếng Việt `text-sm text-muted-foreground`; cột phải hiển thị định nghĩa `text-sm leading-relaxed` và code ví dụ `pre` `overflow-x-auto rounded-md bg-code p-3 font-mono text-xs`. Ở màn hình `sm+` hiển thị 2 cột (`sm:grid sm:grid-cols-[14rem_1fr] sm:gap-4 sm:p-5`), màn hình nhỏ hơn xếp dọc.

2. **Interview (`apps/web/src/app/(main)/interview/page.tsx`)**:
   - Accordion câu hỏi: mỗi mục là container `overflow-hidden rounded-lg border border-border bg-card`. Nút mở có `type="button"`, `aria-expanded={isOpen}`, `aria-controls={`accordion-panel-${q.id}`}`, chevron có `transition-transform motion-reduce:transition-none` và xoay 180 độ khi mở.
   - Nút "đã luyện": sử dụng component `Button` với `variant="outline"` và `size="sm"`. Khi đã luyện, áp dụng class `border-transparent bg-success-soft text-primary-ink hover:bg-success-soft/80`.
   - Nút trigger khi câu hỏi đã luyện có icon `CheckCircle2` mang màu `text-primary-ink` và `aria-hidden="true"`.
   - Tiến độ hiển thị số câu đã luyện dùng font mono `tabular-nums`.

3. **Portfolio (`apps/web/src/app/(main)/portfolio/page.tsx`)**:
   - Card dự án: `Card` mặc định; dự án đã xong thêm viền `border-primary/40` (thay vì `border-success/40`).
   - Ô icon phase: `size-10 rounded-md bg-muted`, bọc icon với `aria-hidden="true"`.
   - Link "Tiếp tục" (`tc("continue")`): sử dụng `Button asChild variant="outline" size="sm"` thay vì link gạch chân `decoration-hit`. Kèm icon `ArrowRight aria-hidden="true"` có khoảng cách tự nhiên từ `Button`.
   - Badge "đã nộp": khi `completedAt` rỗng không render chuỗi rỗng mà hiển thị icon + nhãn `tc("done")` ("Done" / "Hoàn thành") có ý nghĩa; khi có `completedAt` hiển thị `t("submitted", { date: completedAt.slice(0, 10) })`.

4. **Settings (`apps/web/src/app/(main)/settings/page.tsx`)**:
   - Nhóm theo mục: chia thành các section rõ ràng:
     - Giao diện / Ngôn ngữ (`t("appearance")` + `t("appearanceDesc")`)
     - Học tập / Mục tiêu (`t("learning")` + `t("learningDesc")`)
     - Dữ liệu sao lưu (`t("data")` + `t("dataDesc")`)
     - Vùng nguy hiểm (`t("dangerZone")` + `t("dangerZoneDesc")`)
     - Giới thiệu (`t("about")`)
     - Tài khoản (`AccountCard` nếu `authEnabled`)
     Mỗi nhóm có `<h2 className="text-base font-bold">` + mô tả `text-sm text-muted-foreground`.
   - Dialog xác nhận xóa tiến độ: thay thế hoàn toàn `window.confirm` bằng `Dialog` từ `components/ui/dialog.tsx` (`Dialog`, `DialogContent`, `DialogTitle`, `DialogDescription`).
     - State `confirmReset` (boolean).
     - `DialogTitle`: `t("reset")`.
     - `DialogDescription`: `t("resetConfirm")`.
     - Nút Hủy: `Button variant="outline"` (`tc("cancel")`).
     - Nút Xác nhận: `Button variant="danger"` (`tc("confirm")`).
     - Khi xác nhận gọi: `p.reset(); setMessage({ ok: true, text: t("resetDone") }); setConfirmReset(false);`.
     - Nút mở dialog: `Button variant="outline"` mang class `text-danger hover:bg-danger-soft hover:text-danger` (không tô nền đặc).
   - Segmented control: container `rounded-md bg-muted p-0.5` với `role="radiogroup"`, từng nút có `role="radio"`, `aria-checked={checked}`, `rounded-sm px-3 py-1.5 text-sm transition-colors outline-none focus-visible:outline-2 focus-visible:outline-ring`. Mục đang chọn có class `bg-card font-bold text-primary`.
   - Thông báo import/reset (`message`): bọc trong container `role="status"`, `rounded-md px-3 py-2 text-sm`, thành công dùng `bg-success-soft text-primary-ink`, lỗi dùng `bg-danger-soft text-danger`. Hiển thị ngữ cảnh phù hợp theo thao tác (import ở mục Dữ liệu, reset ở mục Vùng nguy hiểm).

5. **i18n Messages (`apps/web/messages/en.json`, `apps/web/messages/vi.json`)**:
   - Thêm đồng bộ 5 key phục vụ chia nhóm trong `settings`:
     - `appearanceDesc`: `"Language and theme preferences"` / `"Tùy chọn ngôn ngữ và giao diện"`
     - `learningDesc`: `"Learning track and daily XP target"` / `"Lộ trình học và mục tiêu XP mỗi ngày"`
     - `dataDesc`: `"Backup and restore your progress on this device"` / `"Sao lưu và khôi phục tiến độ trên thiết bị này"`
     - `dangerZone`: `"Danger zone"` / `"Vùng nguy hiểm"`
     - `dangerZoneDesc`: `"Reset progress or restart onboarding"` / `"Làm lại màn hình chào hoặc xóa toàn bộ tiến độ"`

---

## 2. File đã sửa

Chỉ sửa đúng 4 file trang và 2 file từ điển i18n theo đúng phạm vi cho phép:
1. `apps/web/src/app/(main)/glossary/page.tsx`
2. `apps/web/src/app/(main)/interview/page.tsx`
3. `apps/web/src/app/(main)/portfolio/page.tsx`
4. `apps/web/src/app/(main)/settings/page.tsx`
5. `apps/web/messages/en.json`
6. `apps/web/messages/vi.json`

---

## 3. Kết quả lệnh kiểm tra

Tất cả lệnh kiểm tra trong spec đều được thực thi và đạt 100% mong đợi:

### 3.1. Typecheck (`pnpm --filter web typecheck` / `pnpm.cmd --filter web typecheck`)
```
> web@0.1.0 typecheck D:\Proj\python-ai-platform\apps\web
> pnpm run content && tsc --noEmit

> web@0.1.0 content D:\Proj\python-ai-platform\apps\web
> uv run --project ../.. python ../../tools/build_content.py

Built 24 lessons, 5 exams, 144 flashcards, 387 questions -> apps\web\src\generated
```
=> Kết quả: **0 lỗi typecheck, exit code 0.**

### 3.2. Quét các pattern / token bị cấm
Lệnh:
```bash
grep -nE "rounded-\[|border-2|font-black|font-semibold|uppercase|transition[ \"]|transition-all|text-hit|bg-hit|decoration-hit|border-edge|shadow-\[|text-\[[0-9]+px\]|backdrop-blur|row-cursor|window\.confirm|→|#[0-9a-fA-F]{6}|oklch\(" "apps/web/src/app/(main)/glossary/page.tsx" "apps/web/src/app/(main)/interview/page.tsx" "apps/web/src/app/(main)/portfolio/page.tsx" "apps/web/src/app/(main)/settings/page.tsx"
```
=> Kết quả: **Rỗng (0 dòng match, grep exit code 1 - hoàn toàn sạch các token cấm).**

### 3.3. Đếm `aria-pressed` ở Glossary và Interview
Lệnh:
```bash
grep -c "aria-pressed" "apps/web/src/app/(main)/glossary/page.tsx" "apps/web/src/app/(main)/interview/page.tsx"
```
Output:
```
apps/web/src/app/(main)/glossary/page.tsx:1
apps/web/src/app/(main)/interview/page.tsx:1
```
=> Kết quả: **Cả 2 file đều có `aria-pressed` = 1 (đạt yêu cầu ≥ 1).**

### 3.4. Git diff stat
Lệnh:
```bash
git diff --stat
```
Output:
```
 apps/web/messages/en.json                  |   5 +
 apps/web/messages/vi.json                  |   5 +
 apps/web/src/app/(main)/glossary/page.tsx  |  53 +++--
 apps/web/src/app/(main)/interview/page.tsx | 114 ++++++---
 apps/web/src/app/(main)/portfolio/page.tsx |  39 +--
 apps/web/src/app/(main)/settings/page.tsx  | 367 +++++++++++++++++++----------
 6 files changed, 384 insertions(+), 199 deletions(-)
```
=> Kết quả: **Chỉ có 4 file trang và 2 file i18n messages.** Không chạm vào bất kỳ file nào khác ngoài phạm vi.

### 3.5. Kiểm tra đối xứng key i18n (en vs vi)
Lệnh:
```bash
node -e "const a=require('./apps/web/messages/en.json'),b=require('./apps/web/messages/vi.json');const k=(o,p='')=>Object.entries(o).flatMap(([x,v])=>typeof v==='object'?k(v,p+x+'.'):[p+x]);const A=k(a),B=k(b);console.log('en-only',A.filter(x=>!B.includes(x)),'vi-only',B.filter(x=>!A.includes(x)))"
```
Output:
```
en-only [] vi-only []
```
=> Kết quả: **Hai mảng rỗng, đối xứng 100%.**

---

## 4. Điều còn chưa chắc

1. **Vị trí hiển thị `message` sau khi reset tiến độ**: Trong code cũ, cả import và reset đều nằm chung một card. Hiện tại, đã tách thành 2 card riêng biệt (Dữ liệu và Vùng nguy hiểm). Để trải nghiệm mượt mà nhất, thông báo `resetDone` được hiển thị ngay bên trong card Vùng nguy hiểm (nơi người dùng vừa bấm nút xác nhận xóa), trong khi thông báo `importOk` / `importFail` hiển thị bên trong card Dữ liệu.
2. **Khối sticky header trên màn hình lớn**: Khối tìm kiếm ở trang `/glossary` có class `-mx-4 px-4 sm:-mx-6 sm:px-6 lg:-mx-10 lg:px-10` để nền đặc tràn vừa khít với padding của `main` container, tạo hiệu ứng viền hairline ngăn cách sạch sẽ khi cuộn.

---

## 5. Vòng 2: Xử lý Feedback vòng 1

### 5.1. Các thay đổi đã thực hiện

1. **Khắc phục chiều cao sticky header Glossary ở 375px (`apps/web/src/app/(main)/glossary/page.tsx`)**:
   - **Vấn đề vòng 1**: ~30 chip tag nằm trong khối `sticky top-14`, do dùng `flex-wrap` nên bị ngắt thành nhiều dòng, khiến khối sticky cao ~600px chiếm gần hết màn hình 375px (iPhone SE cao 667px), người dùng cuộn gần như không thấy danh sách thuật ngữ.
   - **Giải pháp**:
     - Container chip tag ở màn hình nhỏ (`< sm`) chuyển sang **một hàng cuộn ngang độc lập**: `flex flex-nowrap gap-1.5 overflow-x-auto pb-1 [scrollbar-width:none] [&::-webkit-scrollbar]:hidden -mx-4 px-4`.
     - Ở màn hình lớn hơn (`sm+`): phục hồi về cấu hình bọc dòng thông thường `sm:mx-0 sm:px-0 sm:flex-wrap sm:overflow-visible sm:pb-0`.
     - Từng `TagButton` được bổ sung `shrink-0 whitespace-nowrap` để nút không bị co lại hay gãy dòng chữ khi cuộn ngang.
   - **Kết quả**: Chiều cao toàn bộ khối sticky ở 375px giảm từ ~600px xuống còn ~116px (gồm padding 24px + ô tìm kiếm 40px + khoảng cách 12px + hàng chip 40px). Danh sách thuật ngữ hiển thị thông thoáng ngay bên dưới, trang không xuất hiện thanh cuộn ngang toàn trang.

2. **Kiểm tra `interview/page.tsx`**:
   - Đã rà soát chi tiết cấu trúc `apps/web/src/app/(main)/interview/page.tsx`.
   - Khối chip tag lọc chủ đề của Interview (`<div className="mb-6 flex flex-wrap gap-1.5">`) **không nằm trong bất kỳ container `sticky` nào**; khối này trôi theo luồng văn bản thông thường và cuộn lên khi người dùng duyệt xuống danh sách câu hỏi. Vì vậy không gây hiện tượng che khuất nội dung như Glossary.

### 5.2. Kết quả chạy lại các lệnh kiểm tra

Tất cả lệnh kiểm tra trong spec đều được thực thi lại từ đầu (tuyệt đối không chạy `pnpm build`):

1. **Typecheck (`pnpm.cmd --filter web typecheck`)**:
   ```
   > web@0.1.0 typecheck D:\Proj\python-ai-platform\apps\web
   > pnpm run content && tsc --noEmit

   > web@0.1.0 content D:\Proj\python-ai-platform\apps\web
   > uv run --project ../.. python ../../tools/build_content.py

   Built 24 lessons, 5 exams, 144 flashcards, 387 questions -> apps\web\src\generated
   ```
   => **0 lỗi typecheck, exit code 0.**

2. **Quét các pattern / token bị cấm**:
   ```bash
   grep -nE "rounded-\[|border-2|font-black|font-semibold|uppercase|transition[ \"]|transition-all|text-hit|bg-hit|decoration-hit|border-edge|shadow-\[|text-\[[0-9]+px\]|backdrop-blur|row-cursor|window\.confirm|→|#[0-9a-fA-F]{6}|oklch\(" "apps/web/src/app/(main)/glossary/page.tsx" "apps/web/src/app/(main)/interview/page.tsx" "apps/web/src/app/(main)/portfolio/page.tsx" "apps/web/src/app/(main)/settings/page.tsx"
   ```
   => **Rỗng (0 dòng match, grep exit code 1 - hoàn toàn sạch các token cấm).**

3. **Đếm `aria-pressed`**:
   ```bash
   grep -c "aria-pressed" "apps/web/src/app/(main)/glossary/page.tsx" "apps/web/src/app/(main)/interview/page.tsx"
   ```
   Output:
   ```
   apps/web/src/app/(main)/glossary/page.tsx:1
   apps/web/src/app/(main)/interview/page.tsx:1
   ```
   => **Cả hai file đều có `aria-pressed` = 1 (đạt yêu cầu ≥ 1).**

4. **Git diff stat**:
   ```bash
   git diff --stat
   ```
   Output:
   ```
    apps/web/messages/en.json                  |   5 +
    apps/web/messages/vi.json                  |   5 +
    apps/web/src/app/(main)/glossary/page.tsx  |  55 +++--
    apps/web/src/app/(main)/interview/page.tsx | 114 ++++++---
    apps/web/src/app/(main)/portfolio/page.tsx |  39 +--
    apps/web/src/app/(main)/settings/page.tsx  | 367 +++++++++++++++++++----------
    6 files changed, 385 insertions(+), 200 deletions(-)
   ```
   => **Chỉ sửa đúng 4 file trang và 2 file i18n messages.**

5. **Kiểm tra đối xứng i18n**:
   ```bash
   node -e "const a=require('./apps/web/messages/en.json'),b=require('./apps/web/messages/vi.json');const k=(o,p='')=>Object.entries(o).flatMap(([x,v])=>typeof v==='object'?k(v,p+x+'.'):[p+x]);const A=k(a),B=k(b);console.log('en-only',A.filter(x=>!B.includes(x)),'vi-only',B.filter(x=>!A.includes(x)))"
   ```
   Output:
   ```
   en-only [] vi-only []
   ```
   => **Hai mảng rỗng, đối xứng 100%.**

