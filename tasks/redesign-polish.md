# Redesign Dose: sửa sau kiểm tra tay (tiếp theo bước 11)

## Mục tiêu
Sửa 4 lỗi boss tìm thấy khi kiểm tra tay ở 768px, bản EN, light + dark (theo `tasks/PROGRESS.md` mục "Việc tiếp theo").
Chỉ sửa giao diện/a11y; không đổi logic.

## File được phép sửa/tạo
- `apps/web/src/components/roadmap-tray.tsx` — mục 1, 2
- `apps/web/src/app/(main)/learn/page.tsx` — mục 2
- `apps/web/src/components/markdown.tsx` — mục 3 (chỉ trong `MermaidDiagram`)
- `apps/web/src/app/onboarding/page.tsx` — mục 4

## Không được đụng
- Mọi file khác (`components/ui/*`, `tokens.css`, `globals.css`, `lib/*`, `curriculum/`, `tools/`).
- Logic, handler, href, i18n key. Không xóa file, không sửa test, không `git commit`.
- **Không chạy `pnpm --filter web build`** (dev server đang chạy; boss tự build).

## Tiêu chí hoàn thành (checklist)
1. [ ] **Vùng bấm ngăn khay** (`roadmap-tray.tsx`): ngăn "bài kế tiếp" (`border-2`) chỉ đạt 40px vì `after:absolute after:-inset-1` tính từ padding box. Trên **mọi** ngăn: bỏ `relative … after:absolute after:-inset-1 after:content-['']`, thay bằng class `hit` (utility có sẵn trong `globals.css`, mở rộng tối thiểu 44×44). Không đổi kích thước nhìn thấy (`size-9`).
2. [ ] **Tương phản badge trên dải tint phase** (light mode đo được 3.7–4.2:1, cần ≥ 4.5): badge "Coming soon"/"Sắp ra mắt", "Runs on your local Python runner"/runner cục bộ và "skipped" nằm trên nền `getPhaseTintClass(...)` đang dùng `text-muted-foreground` của `Badge variant="outline"`/`"muted"`. Trong `roadmap-tray.tsx` và `learn/page.tsx`, với mọi `Badge` nằm trên dải tint thêm `className="border-foreground/25 text-foreground"` (hoặc tương đương đạt ≥ 4.5:1). Không sửa `components/ui/badge.tsx`.
3. [ ] **Mermaid theo token Dose** (`markdown.tsx`, `MermaidDiagram`): hiện `theme: resolvedTheme === "dark" ? "dark" : "neutral"` → màu sơ đồ không theo Dose, nhãn cạnh ("yes"/"no") ở dark chỉ 4.43:1.
   - Đổi sang `theme: "base"` với `themeVariables` lấy từ CSS variable tại thời điểm render: đọc `getComputedStyle(document.documentElement).getPropertyValue("--card" | "--muted" | "--foreground" | "--muted-foreground" | "--border" | "--primary" | "--accent" | "--code-bg")`.
   - Mermaid (khroma) **không đọc được `oklch(...)`**: viết helper nhỏ trong file đổi màu CSS bất kỳ sang hex qua canvas 1×1 (`ctx.fillStyle = value; ctx.fillRect(0,0,1,1); getImageData` → `#rrggbb`). Không thêm dependency.
   - Gợi ý map: `background`=card, `primaryColor`=muted, `primaryBorderColor`=primary, `primaryTextColor`=foreground, `secondaryColor`=accent, `tertiaryColor`=card, `lineColor`=muted-foreground, `textColor`=foreground, `edgeLabelBackground`=card, `clusterBkg`=muted, `clusterBorder`=border, `fontFamily`="var(--font-sans)" (hoặc tên font đã tải). Giữ `securityLevel: "strict"`, `startOnLoad: false`.
   - Sơ đồ vẽ lại khi đổi theme (giữ dependency `resolvedTheme` của effect hiện có).
   - Kết quả mong đợi: chữ trong node và nhãn cạnh ≥ 4.5:1 ở cả hai mode.
4. [ ] **Tên truy cập lựa chọn ngôn ngữ ở onboarding**: `role="radio"` đang có tên "VITiếng Việt" / "ENEnglish" vì ô mã ngôn ngữ nằm trong nội dung. Thêm `aria-hidden="true"` cho ô mã (`code`) trong `Choice`, để tên còn "Tiếng Việt" / "English".
5. [ ] Lệnh kiểm tra xanh.

## Lệnh kiểm tra
Từ gốc repo `D:\Proj\python-ai-platform` (KHÔNG `pnpm build`):
```
pnpm --filter web typecheck
node ~/.claude/skills/hallmark/scripts/sloplint.mjs apps/web/src --genre modern-minimal --scope app --kept
grep -n "after:-inset" apps/web/src/components/roadmap-tray.tsx
grep -n "theme: \"base\"\|themeVariables" apps/web/src/components/markdown.tsx
git diff --stat
```
Mong đợi: typecheck 0 lỗi; sloplint 0 FAIL, `kept: links 20/20, fields 1/1, handlers 125/125`; grep `after:-inset` rỗng; grep mermaid có kết quả; diff chỉ 4 file trên.
Tự xem `http://localhost:3000/lesson/p1-03-loops/` (có sơ đồ mermaid) ở cả light và dark (HMR).

## Ghi chú cho worker
- Đọc `apps/web/design.md` trước. Utility `.hit` đã có trong `app/globals.css`.
- Windows: dùng `pnpm.cmd` nếu PowerShell chặn `pnpm`.

## Trạng thái
- Bước hiện tại: 2
- Vòng: 1/3
- Số lần swap: 0
- Fallback: không
