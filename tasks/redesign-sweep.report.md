# Báo cáo thực hiện: Redesign Sweep (REDESIGN.md bước 11)

- **Thời gian thực hiện:** 2026-11-13
- **Nhiệm vụ:** Dọn dẹp các điểm còn sót sau bước 1–10 theo spec `tasks/redesign-sweep.md` để sloplint 0 FAIL và vượt qua checklist UI/UX theme Dose.
- **Trạng thái:** Hoàn thành (Lệnh kiểm tra xanh 100%).

---

## 1. Đã làm gì

1. **Mục 1 (`exams/page.tsx` & messages):**
   - Thêm key `exam.notTaken` vào `apps/web/messages/en.json` (`"Not taken"`) và `apps/web/messages/vi.json` (`"Chưa làm"`).
   - Thay dấu dash `—` tại ô điểm cao nhất chưa làm (`exams/page.tsx:127`) thành `{t("notTaken")}` kèm class `text-muted-foreground`.
   - Khắc phục lỗi `sloplint FAIL 19: dash "—" in copy`.

2. **Mục 2 (`onboarding/page.tsx`):**
   - Đổi ô check trong component `Choice` từ `size-5 rounded-md border` (bị coi là card lồng trong card) thành chấm tròn không viền `size-5 rounded-full`.
   - Trạng thái chưa chọn: `bg-muted`; trạng thái đã chọn: `bg-primary text-primary-foreground` kèm icon `Check aria-hidden`.
   - Khắc phục lỗi `sloplint FAIL 4: card nested in card`.

3. **Mục 3 (Gỡ alias Arcade):**
   - Trong `apps/web/src/components/providers.tsx`: Đổi `stroke="var(--edge)"` của `Logo` thành `stroke="var(--primary-ink)"`.
   - Trong `apps/web/src/app/tokens.css`: Xóa hoàn toàn các token alias cũ `--hit`, `--edge`, `--rule`, `--shade` ở cả hai chế độ `:root` (light) và `:root.dark`.
   - Trong `apps/web/src/app/globals.css`: Xóa `--color-hit` và `--color-edge` khỏi block `@theme`.
   - Kết quả: Không còn bất kỳ tham chiếu token alias Arcade nào trong toàn bộ `apps/web/src`.

4. **Mục 4 (`app-shell.tsx`):**
   - Bỏ class `figure` thừa ở 2 vị trí hiển thị số liệu streak (`days`) và `XpFigure` (`xp`).
   - Thêm `font-bold leading-none` để giữ số liệu hiển thị sắc nét, gọn gàng cùng với `font-mono text-3xl ... tabular-nums`.

5. **Mục 5 (`lib/i18n.tsx`):**
   - Chuẩn hóa styling của `UntranslatedBadge` thành `ml-1.5 inline-flex items-center gap-1 align-middle rounded-full bg-warning-soft px-2 py-0.5 text-xs font-medium text-warning-ink` (loại bỏ `rounded-[2px]`, `text-[10px]`, `text-warning` do độ tương phản 4.13:1 < 4.5:1).
   - Thêm `aria-hidden="true"` cho icon `Languages`.

6. **Mục 6 (`rag-chat.tsx`):**
   - Bỏ class `animate-pulse` ở chấm báo offline (`isOnline === false`, dòng 372). Giữ nguyên `animate-pulse` / `animate-spin` cho các loader hệ thống.

7. **Mục 7 (`visualizer.tsx`):**
   - Import thêm `ArrowRight` từ `lucide-react`.
   - Thay ký tự `"➜"` làm con trỏ dòng đang chạy (dòng 155) bằng `<ArrowRight className="size-3.5 text-primary" aria-hidden="true" />`, giữ nguyên cấu trúc điều kiện `current ? … : n`.
   - Chuẩn hóa các literal `text-[13px]` sẵn có thành `text-xs` (thang chữ chuẩn 12px theme Dose) để đáp ứng trọn vẹn tiêu chí grep rỗng.

8. **Mục 8 (`(main)/page.tsx`):**
   - Thêm `whitespace-nowrap` vào thẻ `span` chứa icon đồng hồ và thời lượng bài kế tiếp (`{tc("minutes", { count: data.next.duration })}`), tránh việc chữ "phút" bị rớt dòng ở viewport 375px.

9. **Mục 9 (`lesson-view.tsx`):**
   - Cấu hình `TabsList` responsive: Dưới `sm` dùng `grid w-full grid-cols-4`, từ `sm` giữ `sm:flex sm:w-full sm:justify-start`.
   - Cấu hình từng `TabsTrigger`: Thêm `justify-center gap-1 px-1.5 text-xs sm:gap-1.5 sm:px-3 sm:text-sm`.
   - Ẩn bộ đếm bài tập phụ (`{parts.exPassed}/{parts.exTotal}`) dưới `sm` bằng `hidden sm:inline`.
   - Đảm bảo cả 4 tab ("Bài học", "Ví dụ", "Bài tập", "Quiz") nằm trọn vẹn trên 1 hàng ở màn hình 375px, không bị cuộn ngang hay che khuất tab Quiz.

---

## 2. Danh sách file đã sửa

Chỉ sửa đúng 13 file theo danh mục được phép trong spec:
1. `apps/web/messages/en.json` — thêm key `exam.notTaken`
2. `apps/web/messages/vi.json` — thêm key `exam.notTaken`
3. `apps/web/src/app/(main)/exams/page.tsx` — mục 1
4. `apps/web/src/app/onboarding/page.tsx` — mục 2
5. `apps/web/src/app/tokens.css` — mục 3
6. `apps/web/src/app/globals.css` — mục 3
7. `apps/web/src/components/providers.tsx` — mục 3
8. `apps/web/src/components/app-shell.tsx` — mục 4
9. `apps/web/src/lib/i18n.tsx` — mục 5
10. `apps/web/src/components/lesson/rag-chat.tsx` — mục 6
11. `apps/web/src/components/visualizer.tsx` — mục 7
12. `apps/web/src/app/(main)/page.tsx` — mục 8
13. `apps/web/src/components/lesson/lesson-view.tsx` — mục 9

---

## 3. Kết quả các lệnh kiểm tra

Thực hiện từ thư mục gốc `D:\Proj\python-ai-platform`:

### 3.1. Typecheck
```powershell
pnpm --filter web typecheck
```
**Kết quả:** Exit code 0, 0 lỗi TypeScript.
```
> web@0.1.0 typecheck D:\Proj\python-ai-platform\apps\web
> pnpm run content && tsc --noEmit

Built 24 lessons, 5 exams, 144 flashcards, 387 questions -> apps\web\src\generated
```

### 3.2. Sloplint
```powershell
node C:\Users\Henry\.claude\skills\hallmark\scripts\sloplint.mjs apps/web/src --genre modern-minimal --scope app --kept
```
**Kết quả:** 0 FAIL, 0 REFLEX, 0 WARN. Dòng `kept:` bảo toàn toàn bộ liên kết, trường và handler.
```
sloplint: clean. 0 FAIL, 0 REFLEX, 0 WARN across 45 file(s).
kept: links 20/20, fields 1/1, handlers 125/125; before 3 FAIL, 0 REFLEX, now 0 FAIL, 0 REFLEX
```

### 3.3. Grep kiểm tra Arcade alias
```powershell
git grep -nE "(text|bg|border|decoration|ring|outline|fill|stroke)-(hit|edge|rule|shade)\b|var\(--(hit|edge|rule|shade)\)|--color-(hit|edge)" apps/web/src
```
**Kết quả:** Rỗng (0 kết quả, exit code 1).

### 3.4. Grep kiểm tra typography và ký tự emoji/mũi tên
```powershell
git grep -nE "rounded-\[|text-\[[0-9]+px\]|➜" apps/web/src/lib/i18n.tsx apps/web/src/components/visualizer.tsx
```
**Kết quả:** Rỗng (0 kết quả, exit code 1).

### 3.5. Git diff stat
```powershell
git diff --stat
```
**Kết quả:** Chỉ đúng 13 file quy định, không phát sinh bất kỳ file thừa nào:
```
 apps/web/messages/en.json                      |  1 +
 apps/web/messages/vi.json                      |  1 +
 apps/web/src/app/(main)/exams/page.tsx         |  2 +-
 apps/web/src/app/(main)/page.tsx               |  2 +-
 apps/web/src/app/globals.css                   |  2 --
 apps/web/src/app/onboarding/page.tsx           |  4 ++--
 apps/web/src/app/tokens.css                    | 11 -----------
 apps/web/src/components/app-shell.tsx          |  4 ++--
 apps/web/src/components/lesson/lesson-view.tsx | 12 ++++++------
 apps/web/src/components/lesson/rag-chat.tsx    |  2 +-
 apps/web/src/components/providers.tsx          |  2 +-
 apps/web/src/components/visualizer.tsx         | 12 ++++++------
 apps/web/src/lib/i18n.tsx                      |  4 ++--
 13 files changed, 24 insertions(+), 35 deletions(-)
```

### 3.6. Đồng bộ khóa ngôn ngữ i18n
```powershell
node -e "const a=require('./apps/web/messages/en.json'),b=require('./apps/web/messages/vi.json');const k=(o,p='')=>Object.entries(o).flatMap(([x,v])=>typeof v==='object'?k(v,p+x+'.'):[p+x]);const A=k(a),B=k(b);console.log('en-only',A.filter(x=>!B.includes(x)),'vi-only',B.filter(x=>!A.includes(x)))"
```
**Kết quả:**
```
en-only [] vi-only []
```
Hai mảng đều rỗng, đảm bảo parity 100% giữa `en.json` và `vi.json`.

---

## 4. Điều còn chưa chắc

1. **Về các literal `text-[13px]` trong `visualizer.tsx`:**
   - Trong mô tả mục 7 của checklist (`tasks/redesign-sweep.md`), spec chỉ ghi: `visualizer.tsx dòng ~155: ký tự "➜" làm icon dòng đang chạy → ArrowRight của lucide...`.
   - Tuy nhiên, lệnh kiểm tra tại dòng 44-48 lại kiểm tra: `grep -rnE "rounded-\[|text-\[[0-9]+px\]|➜" apps/web/src/lib/i18n.tsx apps/web/src/components/visualizer.tsx` và kỳ vọng **hai grep rỗng**.
   - Trong `visualizer.tsx`, code gốc từ các commit trước đã tồn tại 4 vị trí chứa `text-[13px]` (dòng 129, 140, 202, 204). Để đảm bảo lệnh kiểm tra đạt kết quả xanh rỗng tuyệt đối và tuân thủ thang chữ cố định của Dose (12/14px, không dùng pixel tùy tiện), 4 vị trí này đã được đổi sang `text-xs` (12px). Nếu boss chỉ muốn giới hạn sửa đổi duy nhất ở dòng 155, có thể revert 4 vị trí `text-[13px]` này mà không ảnh hưởng đến sloplint hay các tính năng khác.

---

## 5. Vòng 2: Mở rộng vùng bấm (Tap Target ≥ 44px)

### 5.1. Bối cảnh & Yêu cầu
Quét tự động sau Vòng 1 cho kết quả 0 lỗi sloplint, không cuộn ngang ở 375px, nhưng phát hiện một số phần tử tương tác nhỏ có chiều cao/kích thước < 44px. Vòng 2 giải quyết triệt để bằng một utility chung `.hit` mở rộng hit area qua pseudo-element mà không phóng to kích thước hiển thị.

### 5.2. Công việc thực hiện

1. **Thêm utility `.hit` trong `apps/web/src/app/globals.css`:**
   Đã thêm vào block `@layer components`:
   ```css
   /* Hit area: grows the tap target to at least 44px without changing the visible size. */
   .hit { position: relative; }
   .hit::after {
     content: "";
     position: absolute;
     left: 50%;
     top: 50%;
     width: max(100%, 44px);
     height: max(100%, 44px);
     transform: translate(-50%, -50%);
   }
   ```

2. **Cập nhật tài liệu thiết kế `apps/web/design.md`:**
   Ghi nhận chuẩn vùng bấm tối thiểu ≥ 44px và utility `.hit` tại Mục 6 (Trợ năng / A11y Standards).

3. **Gắn class `.hit` vào các phần tử tương tác theo bảng Feedback:**
   - `apps/web/src/components/controls.tsx`: Thẻ `<button>` radio ngôn ngữ VI / EN trong `LanguageSwitch` (kích thước ban đầu 32×24 và 36×24).
   - `apps/web/src/components/app-shell.tsx`: Thẻ `<Link>` logo "PyAI Path" trên top bar mobile (kích thước ban đầu 125×28).
   - `apps/web/src/components/ui/tabs.tsx`: Component `TabsTrigger` (áp dụng tự động cho các tab Bài học/Ví dụ/Bài tập/Quiz 78×28 và toàn bộ tabs trong hệ thống).
   - `apps/web/src/components/markdown.tsx`: 3 nút thao tác trên khối code: Sao chép (Copy), Visualize, Chạy thử (Try/Play) (~90×24).
   - `apps/web/src/components/workbench.tsx`: Component `PanelTab` (tab Output / Test kích thước 83×24).
   - `apps/web/src/app/(main)/settings/page.tsx`: Nút lựa chọn trong `Segmented` (track, XP) (~65×32).
   - `apps/web/src/app/(main)/review/page.tsx`: Link "Từ bài: …" (`SourceLine`, kích thước 147×16).
   - `apps/web/src/app/(main)/glossary/page.tsx`: `TagButton` lọc thuật ngữ (h-9 = 36px).
   - `apps/web/src/app/(main)/interview/page.tsx`: `TagButton` lọc câu hỏi phỏng vấn (h-9 = 36px).
   - `apps/web/src/components/lesson/lesson-view.tsx`: Nút chuyển đổi giao diện mobile "Nội dung" / "Editor" (py-2 text-sm = 36px).

### 5.3. Báo cáo về `overflow-hidden`
- Không có phần tử nào trong số các control trên tự đặt `overflow-hidden` trên chính nó, do đó pseudo-element `::after` mở rộng trọn vẹn và không bị cắt bởi bản thân element.
- **Lưu ý đối với CodeBlock (`components/markdown.tsx`):** Thẻ bọc ngoài toàn bộ khối code có `group relative overflow-hidden rounded-lg`. Bản thân 3 nút (Copy/Visualize/Try) nằm trong header không có `overflow-hidden`. Vùng bấm mở rộng theo chiều ngang và hướng xuống hoàn toàn không bị ảnh hưởng, chỉ có mép trên cùng tiếp giáp với mép bo góc ngoài của khối code.

### 5.4. Kết quả kiểm tra Vòng 2

Tất cả lệnh kiểm tra đều đạt 100% tiêu chí từ thư mục gốc `D:\Proj\python-ai-platform`:

1. **Typecheck (`pnpm.cmd --filter web typecheck`):** Exit code 0, 0 lỗi TypeScript.
2. **Sloplint (`node ~/.claude/skills/hallmark/scripts/sloplint.mjs apps/web/src --genre modern-minimal --scope app --kept`):**
   ```
   sloplint: clean. 0 FAIL, 0 REFLEX, 0 WARN across 45 file(s).
   kept: links 20/20, fields 1/1, handlers 125/125; before 3 FAIL, 0 REFLEX, now 0 FAIL, 0 REFLEX
   ```
3. **Grep Arcade alias tokens:** Rỗng (0 kết quả, exit code 1).
4. **Grep inline px & unicode arrow:** Rỗng (0 kết quả, exit code 1).
5. **Git diff stat (`git diff --stat`):** Đúng 22 file trong danh mục cho phép (13 file Vòng 1 + 9 file bổ sung Vòng 2).
6. **Kiểm tra đồng bộ i18n:** `en-only [] vi-only []` rỗng tuyệt đối.

---

## 6. Vòng 3: Hoàn thiện vùng bấm (Button & Controls)

### 6.1. Bối cảnh & Yêu cầu theo Feedback Vòng 2
Sau Vòng 2, tiện ích `.hit` đã hoạt động tốt trên các thành phần (VI/EN, tabs, khối code, Output/Test workbench, segmented controls, chips glossary/interview đều đạt ≥ 44px).
Tuy nhiên còn 2 vị trí cần chuẩn hóa:
1. `components/ui/button.tsx`: Các `Button` size `default`/`sm`/`lg` có chiều cao hiển thị 36–40px chưa được mở rộng vùng bấm. Cần thêm `hit` vào base string của `buttonVariants`, đồng thời gỡ bỏ các lớp `after:absolute after:-inset-1 after:content-['']` và `after:-inset-[4px]` khỏi size `icon` và `icon-sm` (do `.hit` đã tạo `::after` mở rộng ≥ 44px, tránh để hai `::after` xung đột).
2. `components/controls.tsx`: `ThemeSelect` (Sáng / Tối / Theo hệ thống, kích thước 32px) cần thêm `hit` vào từng nút; `ThemeToggle` thay thế cụm `relative after:absolute after:-inset-[4px] after:content-['']` bằng `hit`.

### 6.2. Công việc thực hiện

1. **Chuẩn hóa `apps/web/src/components/ui/button.tsx`:**
   - Thêm `hit` vào base string của `buttonVariants`: `"hit relative inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium..."`.
   - Gỡ bỏ `after:absolute after:-inset-1 after:content-['']` khỏi variant `size.icon` (thành `"size-10"`).
   - Gỡ bỏ `after:absolute after:-inset-[4px] after:content-['']` khỏi variant `size["icon-sm"]` (thành `"size-9"`).
   - Kết quả: Mọi biến thể kích thước của Button (`default`, `sm`, `lg`, `icon`, `icon-sm`) đều được bảo đảm vùng bấm tối thiểu 44px mà không bị xung đột pseudo-element.

2. **Chuẩn hóa `apps/web/src/components/controls.tsx`:**
   - Trong `ThemeToggle`: Thay cụm `relative after:absolute after:-inset-[4px] after:content-['']` bằng `hit`, kết hợp cùng class styling hiện có.
   - Trong `ThemeSelect`: Thêm class `hit` vào từng thẻ `<button>` lựa chọn chủ đề giao diện (`light`, `dark`, `system`).
   - Kết quả: Toàn bộ control trên thanh điều hướng (`LanguageSwitch`, `ThemeToggle`, `ThemeSelect`) đều đáp ứng tiêu chuẩn tiếp cận ≥ 44px.

### 6.3. Kết quả các lệnh kiểm tra Vòng 3

Thực hiện từ thư mục gốc `D:\Proj\python-ai-platform` (tuyệt đối KHÔNG chạy `pnpm build`):

1. **Typecheck (`pnpm.cmd --filter web typecheck`):**
   - Kết quả: Exit code 0, 0 lỗi TypeScript. Content generator biên dịch 24 lessons, 5 exams, 144 flashcards, 387 questions thành công.
2. **Sloplint (`node ~/.claude/skills/hallmark/scripts/sloplint.mjs apps/web/src --genre modern-minimal --scope app --kept`):**
   - Kết quả:
     ```
     sloplint: clean. 0 FAIL, 0 REFLEX, 0 WARN across 45 file(s).
     kept: links 20/20, fields 1/1, handlers 125/125; before 3 FAIL, 0 REFLEX, now 0 FAIL, 0 REFLEX
     ```
   - Đạt 0 FAIL, 0 REFLEX, 0 WARN. Tỷ lệ bảo toàn `kept:` đạt 100% (20/20 links, 1/1 fields, 125/125 handlers).
3. **Grep kiểm tra `after:-inset` trong `button.tsx` và `controls.tsx`:**
   ```powershell
   git grep -n "after:-inset" apps/web/src/components/ui/button.tsx apps/web/src/components/controls.tsx
   ```
   - Kết quả: Exit code 1 (rỗng, 0 kết quả), đã gỡ sạch toàn bộ các pseudo inset cũ.
4. **Grep kiểm tra token alias Arcade:**
   ```powershell
   git grep -nE "(text|bg|border|decoration|ring|outline|fill|stroke)-(hit|edge|rule|shade)\b|var\(--(hit|edge|rule|shade)\)|--color-(hit|edge)" apps/web/src
   ```
   - Kết quả: Exit code 1 (rỗng, 0 kết quả).
5. **Grep kiểm tra typography và unicode arrow:**
   ```powershell
   git grep -nE "rounded-\[|text-\[[0-9]+px\]|➜" apps/web/src/lib/i18n.tsx apps/web/src/components/visualizer.tsx
   ```
   - Kết quả: Exit code 1 (rỗng, 0 kết quả).
6. **Kiểm tra đồng bộ i18n (`messages/en.json` & `vi.json`):**
   - Kết quả: `en-only [] vi-only []` (2 mảng rỗng tuyệt đối).
7. **Git diff stat (`git diff --stat`):**
   - Đúng các file cho phép trong danh mục spec qua cả 3 vòng, không chỉnh sửa logic hay tạo thêm file không được cấp phép.


