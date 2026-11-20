# Redesign Dose: nền móng (REDESIGN.md bước 1 + 2)

## Mục tiêu
Đổi theme Arcade/Dracula Soft sang theme **Dose** theo `docs/REDESIGN.md` (đọc kỹ mục 2, 3, 5, 6 bước 1–2).
Sau task này: tokens, font, CSS nền và component dùng chung đã là Dose; các trang còn lại vẫn build được
(chưa cần đẹp, các bước sau sẽ làm từng màn hình).

## File được phép sửa/tạo
Tất cả trong `apps/web/src/`:
- `app/tokens.css`, `app/globals.css`, `app/layout.tsx`, `app/base.css` (chỉ nếu scaffold sinh ra)
- `components/ui/badge.tsx`, `button.tsx`, `card.tsx`, `dialog.tsx`, `progress.tsx`, `tabs.tsx`, `tooltip.tsx`
- `components/app-shell.tsx`, `components/page-header.tsx`, `components/controls.tsx`, `components/count-up.tsx`
- Mọi file `.tsx` khác trong `apps/web/src/` **chỉ để** đổi class `font-pixel` → `font-mono tabular-nums`
  và gỡ class `crt` / `blink` (chỉ sửa chuỗi className, không đổi gì khác).
- Tạo `apps/web/design.md`.
- `apps/web/messages/en.json` + `vi.json`: chỉ thêm key nếu thật sự cần (thêm cả hai file).

## Không được đụng
- `curriculum/`, `tools/`, `supabase/`, `apps/web/src/lib/*`, `public/pyodide-worker.js`.
- Mọi route, `href`, handler, `id`, `name`, `key`, `type`, prop, luồng dữ liệu (REDESIGN mục 2).
- Không xóa key i18n, không xóa file, không sửa test.
- Không `git commit`.

## Tiêu chí hoàn thành (checklist)
- [ ] Chạy scaffold: `node ~/.claude/skills/hallmark/scripts/theme.mjs scaffold dose --dealt "1/3, seed app-where-beginner-learns-bcc0·8cb9aa4e·2026-11-12·r0" --redesign full --scope app --dir apps/web/src/app` (nếu lệnh lỗi, ghi lỗi vào report và làm tay theo REDESIGN 3.1).
- [ ] `tokens.css`: đúng **toàn bộ** giá trị bảng REDESIGN 3.1 cho light (`:root`) và dark (`:root.dark`); giữ tên token shadcn hiện có (`--card-foreground`, `--popover-foreground`, `--input`, `--accent-foreground`, `--secondary-foreground`, `--success-foreground`, `--primary-ink` … đặt giá trị hợp lý theo palette Dose). Thêm 7 tint phase `--phase-1`…`--phase-7` (dark: cùng hue, L 40%, alpha 62%), `--shadow-lift`, `--syn-*` theo Dose (xanh lá chủ đạo, đủ tương phản trên `--code-bg`). `--radius: 0.625rem`. Bỏ `--crt-r`, `--crt-c`, `--scan`, `--hit`, `--edge`, `--shade` nếu không còn dùng (grep trước).
- [ ] Không còn literal màu (`oklch(`, `#hex`, `rgb(`) ngoài `tokens.css`; `.hljs-*` trong `globals.css` dùng `var(--syn-*)`.
- [ ] `layout.tsx`: chỉ Be Vietnam Pro (400/500/700, subsets latin+vietnamese) + JetBrains Mono (400/500). Bỏ Bungee, Chivo, Silkscreen. `themeColor` khớp `--background` light/dark (hex tương đương được phép ở đây).
- [ ] `globals.css`: dòng 1–3 là stamp Hallmark mới (theme Dose, deal/seed ở trên, genre modern-minimal, signature "khay lộ trình"). `--font-sans` và `--font-display` cùng trỏ Be Vietnam Pro; bỏ `--font-pixel`. Radius map theo 3.3 (control 10px, card 14px). Gỡ `.crt`, `.blink`, text-shadow CRT, keyframe `boot`/`coin`/`flash`/`shake`/`pop` kiểu Arcade; giữ các class đang được dùng (`.display`, `.figure`, `.press`, `.well`, `.row-cursor`, `.meter`, `.animate-rise`, `.flash-hit`, `.shake`, `.xp-pop`, `.coin-drop`) nhưng restyle theo Dose: chỉ `transform`/`opacity`, 120–200ms, có nhánh `prefers-reduced-motion`. `.press` = nút "nhựa đúc" (viền 1px, mép dưới 3px, ấn lún 3px). `.meter` dùng `scaleX`, không animate width. `.display` không uppercase, 700, tracking -0.02em.
- [ ] Không còn `font-pixel`, `crt`, `blink`, `uppercase`, `transition-all`, `backdrop-blur` trong các file được phép sửa ở trên (trừ `rag-chat.tsx` — để bước 3).
- [ ] `components/ui/*`: đủ state default/hover/active/focus-visible/disabled; button cao 36–40px, vùng bấm ≥44px với size icon; card dùng viền hairline (không kèm shadow); dialog/tooltip dùng `--shadow-lift`, nền đặc; progress dùng `scaleX`.
- [ ] `app-shell.tsx`: sidebar nền `--muted`, mục đang chọn nền `--accent` + chữ `--primary` đậm (không tô đặc), header sticky nền đặc, logo "PyAI Path" sentence case. Giữ thu thành menu dưới `lg`. Nút chỉ có icon có `aria-label`, icon trang trí `aria-hidden`.
- [ ] `page-header.tsx`: heading sentence case, không eyebrow uppercase.
- [ ] `apps/web/design.md`: tóm tắt hệ thống (token, chữ, hình khối, motion, signature, quy tắc màu) đủ để các bước sau làm theo.
- [ ] Lệnh kiểm tra xanh.

## Lệnh kiểm tra
Chạy từ gốc repo `D:\Proj\python-ai-platform`:
```
pnpm --filter web typecheck
pnpm --filter web build
```
và grep xác nhận:
```
grep -rnE "font-pixel|\bcrt\b|\bblink\b|transition-all|backdrop-blur|Bungee|Silkscreen|Chivo" apps/web/src --include=*.tsx --include=*.css
grep -nE "oklch\(|#[0-9a-fA-F]{3,6}\b|rgb\(" apps/web/src/app/globals.css
```
(Kết quả mong đợi: lệnh 1 chỉ còn 3 dòng `transition-all` trong `rag-chat.tsx`; lệnh 2 rỗng.)

## Ghi chú cho worker
- Nguồn sự thật: `docs/REDESIGN.md`. Đọc file đó trước.
- Project dùng Tailwind v4 (`@theme inline` trong `globals.css`) và next-intl. Không nhúng chuỗi UI cứng.
- Là thay đổi giao diện: sửa className/CSS, không refactor logic.
- Windows + Git Bash/PowerShell. Dùng `pnpm`, không `npm`.

## Feedback vòng 1
Typecheck/build/grep đã xanh, phần lớn đạt. Sửa các điểm sau (chỉ trong file được phép):

1. **Viền + shadow cùng lúc** (vi phạm REDESIGN 3.3): `components/ui/dialog.tsx` (Content có `border border-border` + `shadow-[var(--shadow-lift)]`), `components/ui/tooltip.tsx` (như trên), `components/app-shell.tsx` popover "more" (`well` + shadow-lift). Bề mặt nổi: bỏ viền, giữ `--shadow-lift`. Popover "more" không dùng `.well`, dùng `rounded-lg bg-popover shadow-[var(--shadow-lift)]`.
2. **Tương phản < 4.5:1 ở light** (đã đo):
   - `text-primary` trên `bg-success-soft` = 3.96 → thêm vào `@theme` `--color-primary-ink: var(--primary-ink)` (nếu chưa có) và badge `success` dùng `text-primary-ink`.
   - `text-warning` trên `bg-warning-soft` = 4.13 → thêm token `--warning-ink` (light `oklch(46% 0.09 75)`, dark = `--warning`), map `--color-warning-ink` trong `@theme`, badge `warning` dùng `text-warning-ink`.
3. **Thang chữ cố định** (REDESIGN 3.2: 12/14/16/19/23/28/33px): trong `@theme inline` của `globals.css` khai báo `--text-xs: 0.75rem; --text-sm: 0.875rem; --text-base: 1rem; --text-lg: 1.1875rem; --text-xl: 1.4375rem; --text-2xl: 1.75rem; --text-3xl: 2.0625rem; --text-4xl: 2.0625rem; --text-5xl: 2.0625rem` (kèm `--text-*--line-height` hợp lý). Trong `app-shell.tsx` đổi `text-[32px]` → `text-3xl`; `page-header.tsx` bỏ cỡ `sm:text-4xl` thừa (display = `text-3xl`, thường = `text-2xl`).
4. **Weight không được load**: chỉ có 400/500/700. Thay mọi `font-semibold` (controls.tsx, tabs.tsx, …) bằng `font-bold`; `font-black` nếu còn trong file được phép → `font-bold`.
5. **`uppercase` trong `controls.tsx`** (LanguageSwitch) — checklist cấm. Bỏ class, render `{l.toUpperCase()}`.
6. **Mép nút "nhựa đúc"**: `.press` hiện lấy mép dưới = `--border` cho mọi variant, nút xanh trông bị viền xám. Cho `.press` dùng biến `--press-edge` (mặc định `var(--border)`); variant `default`/`success` đặt `[--press-edge:var(--primary-ink)]` và `border-color` theo cùng biến; `danger` đặt edge là `color-mix(in oklch, var(--danger) 75%, var(--foreground))`. `.press` dùng `border-color: var(--press-edge)` và `box-shadow: 0 3px 0 0 var(--press-edge)`.
7. **Vùng bấm 44px mà không phóng to icon**: `button.tsx` size `icon-sm` hiện = `size-9 min-h-[44px] min-w-[44px]` nên thực tế bằng `icon`. Bỏ `min-h/min-w`, giữ kích thước nhìn thấy (`size-10` / `size-9`) và mở rộng vùng bấm bằng pseudo-element: thêm vào base `relative` và cho size icon `after:absolute after:-inset-1 after:content-['']` (icon-sm: `after:-inset-[4px]` để đạt 44px). Làm tương tự cho `ThemeToggle` trong `controls.tsx`.
8. `button.tsx` variant `danger` dùng `text-danger-foreground` (token đã có) thay vì `text-primary-foreground`; map `--color-danger-foreground` trong `@theme` nếu chưa có.

Sau khi sửa: chạy lại toàn bộ Lệnh kiểm tra, thêm mục "Vòng 2" vào report.

## Feedback vòng 2
Vòng 2 đạt hết 8 mục. Còn 1 lỗi hồi quy thấy khi mở app:

1. `tokens.css` đặt alias `--hit: transparent` (cả light và dark). Các trang chưa redesign vẫn dùng `text-hit` / `bg-hit` / `decoration-hit` / `shadow-[...var(--hit)]` (`app/(main)/page.tsx` dòng 74, 105, 265, 277, 291; `workbench.tsx:250`; `portfolio/page.tsx:75`) → trên Dashboard số "XP hôm nay" và "Tổng XP" **biến mất** (chữ trong suốt). Đổi alias thành `--hit: var(--primary);` ở cả hai mode. Không sửa các trang đó (để các bước sau).
2. Chạy lại Lệnh kiểm tra, thêm mục "Vòng 3" ngắn vào report.

## Trạng thái
- Bước hiện tại: 5 (chờ user review + commit)
- Vòng: 3/3, đạt
- Boss đã kiểm: typecheck, build, validate --fast, grep, xem app ở 1440/375, light/dark
- Số lần swap: 0
- Fallback: không
