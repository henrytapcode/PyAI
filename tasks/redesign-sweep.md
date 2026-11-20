# Redesign Dose: Sweep (REDESIGN.md bước 11)

## Mục tiêu
Dọn những gì còn sót sau bước 1–10 để sloplint 0 FAIL và qua checklist UI/UX (tương phản 4.5:1, focus-visible,
vùng bấm 44px, reduced-motion, không cuộn ngang ở 375px, không ký tự/emoji làm icon). Mọi thay đổi là
className/markup hoặc token CSS; không đổi logic.

## File được phép sửa/tạo
Chỉ các file sau, chỉ cho đúng mục ghi kèm:
- `apps/web/src/app/(main)/exams/page.tsx` — mục 1
- `apps/web/src/app/onboarding/page.tsx` — mục 2
- `apps/web/src/app/tokens.css`, `apps/web/src/app/globals.css` — mục 3
- `apps/web/src/components/providers.tsx` — mục 3 (chỉ thuộc tính `stroke` của `Logo`)
- `apps/web/src/components/app-shell.tsx` — mục 4
- `apps/web/src/lib/i18n.tsx` — mục 5 (chỉ `className` của `UntranslatedBadge` + `aria-hidden` cho icon)
- `apps/web/src/components/lesson/rag-chat.tsx` — mục 6 (chỉ class của chấm offline)
- `apps/web/src/components/visualizer.tsx` — mục 7
- `apps/web/src/app/(main)/page.tsx` — mục 8
- `apps/web/src/components/lesson/lesson-view.tsx` — mục 9
- `apps/web/messages/en.json` + `vi.json` — chỉ **thêm** key (mục 1).

## Không được đụng
- Mọi file khác; `lib/*` ngoài đúng `UntranslatedBadge`; logic, handler, prop, href.
- Không xóa file, không sửa test, không `git commit`. **Không chạy `pnpm --filter web build`** (boss tự build).

## Tiêu chí hoàn thành (checklist)
1. [ ] **sloplint FAIL `exams/page.tsx:127` dash "—"**: ô "điểm cao nhất" khi chưa làm đang in `—`. Thay bằng key mới `exam.notTaken` (en `"Not taken"`, vi `"Chưa làm"`), `text-muted-foreground`.
2. [ ] **sloplint FAIL `onboarding/page.tsx:178` card nested in card**: ô check trong `Choice` (`size-5 rounded-md border`) bị coi là card lồng card. Đổi thành chấm tròn không viền: `size-5 rounded-full` — chưa chọn `bg-muted`, đã chọn `bg-primary text-primary-foreground` + `Check aria-hidden`.
3. [ ] **Gỡ alias Arcade** (REDESIGN 8 / ghi chú các bước trước): xóa `--hit`, `--edge`, `--rule`, `--shade` khỏi cả hai mode trong `tokens.css`, xóa `--color-hit`, `--color-edge` khỏi `@theme` trong `globals.css`. Trước khi xóa: `grep -rnE "(text|bg|border|decoration|ring|outline|fill|stroke)-(hit|edge|rule|shade)\b|var\(--(hit|edge|rule|shade)\)" apps/web/src` phải chỉ còn `providers.tsx` (`stroke="var(--edge)"` của `Logo`) → đổi thành `stroke="var(--primary-ink)"`. Sau khi xóa grep đó phải rỗng.
4. [ ] `app-shell.tsx` dòng ~98, ~101: bỏ class `figure` thừa (đã có `font-mono tabular-nums`), thêm `font-bold leading-none`.
5. [ ] `UntranslatedBadge` (`lib/i18n.tsx`): `rounded-full bg-warning-soft px-2 py-0.5 text-xs font-medium text-warning-ink` (bỏ `rounded-[2px]`, `text-[10px]`, `text-warning` — tương phản 4.13 < 4.5); icon `Languages` thêm `aria-hidden="true"`.
6. [ ] `rag-chat.tsx` dòng ~372: chấm báo offline bỏ `animate-pulse` (nhấp nháy vô hạn là trang trí, REDESIGN 3.3). Giữ `animate-pulse`/`animate-spin` cho loader (workbench, providers) — không đụng.
7. [ ] `visualizer.tsx` dòng ~155: ký tự `"➜"` làm icon dòng đang chạy → `ArrowRight` của lucide `className="size-3.5 text-primary" aria-hidden="true"` (import thêm), giữ nguyên điều kiện `current ? … : n`.
8. [ ] `(main)/page.tsx` dòng ~131: thời lượng bài kế tiếp ("10 phút") bị xuống dòng ở 375px → bọc `whitespace-nowrap` cho span chứa icon + chữ.
9. [ ] `lesson-view.tsx`: ở 375px tab "Quiz" của `TabsList` (Bài học / Ví dụ / Bài tập / Quiz) bị khuất phải vuốt mới thấy. Dưới `sm`: `TabsList` `grid w-full grid-cols-4`, mỗi `TabsTrigger` `justify-center px-1.5 text-xs gap-1`, ẩn bộ đếm phụ (vd `0/2`) bằng `hidden sm:inline` nếu cần để vừa; từ `sm` giữ như hiện tại. Cả 4 tab phải thấy ở 375px, không cuộn ngang.
10. [ ] Lệnh kiểm tra xanh.

## Lệnh kiểm tra
Từ gốc repo `D:\Proj\python-ai-platform` (KHÔNG `pnpm build`):
```
pnpm --filter web typecheck
node ~/.claude/skills/hallmark/scripts/sloplint.mjs apps/web/src --genre modern-minimal --scope app --kept
grep -rnE "(text|bg|border|decoration|ring|outline|fill|stroke)-(hit|edge|rule|shade)\b|var\(--(hit|edge|rule|shade)\)|--color-(hit|edge)" apps/web/src
grep -rnE "rounded-\[|text-\[[0-9]+px\]|➜" apps/web/src/lib/i18n.tsx apps/web/src/components/visualizer.tsx
git diff --stat
node -e "const a=require('./apps/web/messages/en.json'),b=require('./apps/web/messages/vi.json');const k=(o,p='')=>Object.entries(o).flatMap(([x,v])=>typeof v==='object'?k(v,p+x+'.'):[p+x]);const A=k(a),B=k(b);console.log('en-only',A.filter(x=>!B.includes(x)),'vi-only',B.filter(x=>!A.includes(x)))"
```
Mong đợi: typecheck 0 lỗi; sloplint `0 FAIL` và dòng `kept:` vẫn `links 20/20, fields 1/1, handlers 125/125`; hai grep rỗng; diff chỉ các file trên; hai mảng rỗng.

## Ghi chú cho worker
- Đọc `docs/REDESIGN.md` và `apps/web/design.md` trước.
- Hallmark script ở `C:\Users\Henry\.claude\skills\hallmark\scripts\` (đã được thêm vào workspace).
- Windows: dùng `pnpm.cmd` nếu PowerShell chặn `pnpm`.

## Feedback vòng 1
Đạt cả 9 mục (sloplint 0 FAIL, kept 20/125). Đổi `text-[13px]` → `text-xs` ở visualizer: chấp nhận.
Boss quét tự động ở 375px (10 route): không cuộn ngang, không phần tử thiếu tên. Còn **vùng bấm < 44px** (REDESIGN 3.3 "vùng bấm tối thiểu 44px"):

| Phần tử | Kích thước hiện tại | File |
|---|---|---|
| Nút VI / EN (mọi trang) | 32×24, 36×24 | `components/controls.tsx` (`LanguageSwitch`) |
| Link logo "PyAI Path" (header mobile) | 125×28 | `components/app-shell.tsx` |
| Tab Bài học/Ví dụ/Bài tập/Quiz (mobile) | 78×28 | `components/ui/tabs.tsx` (`TabsTrigger`) |
| Nút Sao chép / Chạy / Visualize trên khối code | ~90×24 | `components/markdown.tsx` |
| Tab Output / Test trong workbench | 83×24 | `components/workbench.tsx` |
| Segmented control Settings (track, XP) | ~65×32 | `app/(main)/settings/page.tsx` (`Segmented`) |
| Link "Từ bài: …" | 147×16 | `app/(main)/review/page.tsx` (`SourceLine`) |
| Chip lọc glossary/interview, nút Nội dung/Editor | h 36 | `glossary/page.tsx`, `interview/page.tsx`, `components/lesson/lesson-view.tsx` |

**Sửa bằng một utility chung, không phóng to phần nhìn thấy:**
1. Trong `globals.css` (`@layer components`) thêm:
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
   và ghi một dòng về `.hit` vào `apps/web/design.md` (mục a11y/hình khối). (Được phép sửa `apps/web/design.md` ở vòng này.)
2. Thêm class `hit` vào đúng các phần tử trong bảng (chỉ thêm class, không đổi gì khác). Ở những chỗ đã có `after:absolute after:-inset-*` thì không cần.
   File được phép sửa thêm ở vòng này: `components/controls.tsx`, `components/ui/tabs.tsx`, `components/markdown.tsx`, `components/workbench.tsx`, `app/(main)/settings/page.tsx`, `app/(main)/review/page.tsx`, `app/(main)/glossary/page.tsx`, `app/(main)/interview/page.tsx`, `apps/web/design.md` (ngoài các file đã liệt kê ở trên).
3. Không dùng `.hit` trên phần tử có `overflow-hidden` của chính nó (pseudo sẽ bị cắt); nếu gặp thì báo trong report.
4. Chạy lại Lệnh kiểm tra (KHÔNG `pnpm build`), sloplint vẫn phải 0 FAIL; thêm mục "Vòng 2" vào report.

## Feedback vòng 2
`.hit` chạy tốt (đo lại: VI/EN, tab, khối code, Output, segmented, glossary đều ≥ 44). Còn 2 chỗ:

1. **`components/ui/button.tsx`**: mọi `Button` size `default`/`sm`/`lg` cao 36–40px chưa mở rộng vùng bấm (vd "Mở lộ trình" 36, "Chạy" 36, "Export tiến độ" 40). Thêm `hit` vào chuỗi base của `buttonVariants`, và **gỡ** `after:absolute after:-inset-1 after:content-['']` / `after:-inset-[4px]` khỏi size `icon` và `icon-sm` (hai `::after` sẽ đánh nhau; `.hit` đã lo đủ). Base đã có `relative` thì để nguyên hoặc bỏ (`.hit` đã set).
2. **`components/controls.tsx`**: `ThemeSelect` (Sáng / Tối / Theo hệ thống, đang 32px) thêm `hit` vào từng nút; `ThemeToggle` thay `relative after:absolute after:-inset-[4px] after:content-['']` bằng `hit`.
File được phép sửa ở vòng này: `components/ui/button.tsx`, `components/controls.tsx`.
3. Chạy lại Lệnh kiểm tra (KHÔNG `pnpm build`), sloplint 0 FAIL; thêm `grep -n "after:-inset" apps/web/src/components/ui/button.tsx apps/web/src/components/controls.tsx` phải rỗng. Thêm mục "Vòng 3" vào report.

## Trạng thái
- Bước hiện tại: 2
- Vòng: 3/3
- Số lần swap: 0
- Fallback: không
