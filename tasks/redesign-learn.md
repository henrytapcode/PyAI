# Redesign Dose: trang Learn (REDESIGN.md bước 5)

## Mục tiêu
Đưa `/learn` (`app/(main)/learn/page.tsx`) sang theme Dose với signature **khay lộ trình bản đầy đủ**
(REDESIGN 3.4, mục 4 hàng #3; `apps/web/design.md`). Khay đã có ở `components/roadmap-tray.tsx` (bước 4).
Trang Learn cần hiện tên bài, thời lượng, trạng thái, cảnh báo prerequisite và link phase test, nên **giữ dạng
danh sách hàng** cho từng bài, nhưng mỗi phase vẽ thành một "khay": dải tint phase + các hàng bài là "ngăn".

## File được phép sửa/tạo
- Sửa: `apps/web/src/app/(main)/learn/page.tsx`
- Sửa: `apps/web/src/components/roadmap-tray.tsx` — **chỉ** để tách ra và export dùng chung: `getPhaseTintClass` (đã export) và một hàm mới `trayCellClass(status: LessonStatus, isNext: boolean): string` trả về đúng chuỗi class trạng thái ngăn đang dùng trong `RoadmapTray` (rồi `RoadmapTray` gọi lại hàm này). Không đổi giao diện Dashboard.
- `apps/web/messages/en.json` + `vi.json`: chỉ **thêm** key nếu thật cần (cả hai file).

## Không được đụng
- `curriculum/`, `tools/`, `supabase/`, `apps/web/src/lib/*`, `components/ui/*`, `tokens.css`, `globals.css`, `app/(main)/page.tsx`.
- **Điều hướng bàn phím** của Learn (`useEffect` j/k/ArrowUp/ArrowDown): giữ nguyên code, và mọi `Link` bài học vẫn phải có `data-lesson-row` + `data-live={l.id === next?.id}`.
- Mọi `href` (`/lesson/<id>/`, `/exam/<id>/`, `/placement/`), mọi logic hiển thị (track B placement, prereqWarning, local runner, skipped, comingSoon, project badge, capstones, furtherReading).
- Không xóa file, không sửa test, không `git commit`. **Không chạy `pnpm --filter web build`** (dev server đang chạy ở port 3000; boss tự build).

## Tiêu chí hoàn thành (checklist)
- [ ] Bỏ hẳn `STATUS_DOT` (dùng `trayCellClass` thay thế) — ô số/tick của mỗi bài trông y như ngăn trên Dashboard (`size-9 rounded-md font-mono`), completed có `Check`, coming_soon có `Lock`, icon `aria-hidden="true"`.
- [ ] Mỗi phase là một khối `rounded-lg` **nền tint** `getPhaseTintClass(phase.order)`, không viền, không shadow (không dùng `Card`):
  - Đầu khối: tên phase `<h2 className="text-lg font-bold">`, nhãn "Phase N" gộp vào cùng dòng dạng chữ nhỏ trước tên (`text-sm font-medium`, sentence case — không còn eyebrow tách dòng), summary `text-sm text-foreground/80`… **lưu ý tương phản**: mọi chữ trên tint dùng `text-foreground` (không `text-muted-foreground`, không `opacity-75` cho chữ thường). Bên phải: badges + `Progress` + `%` mono `tabular-nums`.
  - Bỏ ô icon phase `size-12 rounded-[4px] bg-primary` (giữ `PhaseIcon` nhỏ `size-5` cạnh tên, `aria-hidden`).
  - Các hàng bài nằm trong một khay con `rounded-md bg-card/70` (dark: vẫn token, không literal), phân cách `divide-y divide-border`.
- [ ] **Hàng bài** (`Link` khi `ready`): `flex items-center gap-4 px-4 py-3`, hover `bg-accent` + `text-foreground` (`transition-colors`), `focus-visible:outline-2 outline-ring -outline-offset-2`; bài kế tiếp (`data-live=true`) có nền `bg-accent` và vạch trái 3px `border-l-primary` (thay cho tam giác svg; xóa svg). Hàng chưa ready: `div` với `opacity-60`.
  - Dòng phụ (thời lượng, trạng thái, prereq) `text-xs text-foreground/80`, icon `aria-hidden`; thời lượng `whitespace-nowrap`.
  - Mũi tên cuối hàng `aria-hidden`, chỉ `transition-transform group-hover:translate-x-0.5 motion-reduce:transform-none`.
- [ ] **Phase test** là hàng cuối khay con, ô icon dùng `trayCellClass("completed", false)` khi đã qua, ngược lại kiểu `available`.
- [ ] Banner track B (placement): `Card` viền hairline mặc định, nền `bg-accent`, icon `aria-hidden`. Không `border-primary/30 bg-accent/40`.
- [ ] Capstones / Đọc thêm: `Card` mặc định, tiêu đề `text-base font-bold`, chữ đủ tương phản.
- [ ] Không còn trong `learn/page.tsx`: `row-cursor`, `rounded-[`, `border-2`, `border-edge`, `font-black`, `font-semibold`, `uppercase`, `opacity-75`, `text-hit`, `bg-hit`, `shadow-[`, `transition-all`, `hover:scale`, literal màu.
- [ ] Ở 375px: không cuộn ngang; khối đầu phase xếp dọc (badges/progress xuống dưới tên).
- [ ] Lệnh kiểm tra xanh.

## Lệnh kiểm tra
Từ gốc repo `D:\Proj\python-ai-platform` (KHÔNG `pnpm build`):
```
pnpm --filter web typecheck
grep -nE "row-cursor|rounded-\[|border-2|border-edge|font-black|font-semibold|uppercase|opacity-75|text-hit|bg-hit|shadow-\[|transition-all|hover:scale|STATUS_DOT|#[0-9a-fA-F]{6}|oklch\(" "apps/web/src/app/(main)/learn/page.tsx"
grep -c "data-lesson-row" "apps/web/src/app/(main)/learn/page.tsx"
node -e "const a=require('./apps/web/messages/en.json'),b=require('./apps/web/messages/vi.json');const k=(o,p='')=>Object.entries(o).flatMap(([x,v])=>typeof v==='object'?k(v,p+x+'.'):[p+x]);const A=k(a),B=k(b);console.log('en-only',A.filter(x=>!B.includes(x)),'vi-only',B.filter(x=>!A.includes(x)))"
```
Mong đợi: typecheck 0 lỗi; grep đầu rỗng; `data-lesson-row` ≥ 1; hai mảng rỗng.
Tự xem `http://localhost:3000/learn/` (HMR), thử phím `j`/`k`.

## Ghi chú cho worker
- Đọc `docs/REDESIGN.md`, `apps/web/design.md` và `components/roadmap-tray.tsx` trước.
- Font chỉ 400/500/700. Windows: dùng `pnpm.cmd` nếu PowerShell chặn `pnpm`.

## Trạng thái
- Bước hiện tại: 5 (chờ user review + commit)
- Vòng: 1/3, đạt
- Boss đã kiểm: typecheck, build, validate, grep, logic còn đủ; desktop dark, 375px dark, phím j/k, không cuộn ngang
- Số lần swap: 0
- Fallback: không
