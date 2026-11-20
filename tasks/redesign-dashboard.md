# Redesign Dose: Dashboard + khay lộ trình (REDESIGN.md bước 4)

## Mục tiêu
Làm lại bố cục `/` (`app/(main)/page.tsx`) theo `docs/REDESIGN.md` mục 3.4 (signature "khay lộ trình") và
mục 4 hàng #2, theo hệ thống trong `apps/web/design.md`. Tạo component khay lộ trình dùng chung; bước này
chỉ dùng bản **thu gọn** trên Dashboard (bước 5 sẽ dùng bản đầy đủ ở `/learn`).

## File được phép sửa/tạo
- Sửa: `apps/web/src/app/(main)/page.tsx`
- Tạo: `apps/web/src/components/roadmap-tray.tsx`
- `apps/web/messages/en.json` + `vi.json`: chỉ **thêm** key nếu thật cần (cả hai file, cùng key). Không đổi/xóa key cũ.

## Không được đụng
- `curriculum/`, `tools/`, `supabase/`, `apps/web/src/lib/*` (dùng selector có sẵn, không sửa), `components/ui/*`,
  `tokens.css`, `globals.css`, `app/(main)/learn/page.tsx` (bước 5).
- Mọi `href` hiện có trên Dashboard phải còn (`/lesson/<id>/`, `/learn/`, `/review/`, `/exams/`).
- Không xóa file, không sửa test, không `git commit`. Không chạy `pnpm build` khi dev server đang chạy (xem Lệnh kiểm tra).

## Tiêu chí hoàn thành (checklist)
### Component `roadmap-tray.tsx`
- [ ] Export `RoadmapTray({ variant, nextId, className })`, `variant: "compact" | "full"`. Tự lấy dữ liệu bằng `useProgress()` + `catalog` + `lessonStatus` / `phaseProgress` (giống cách page.tsx đang làm). Không thêm logic tiến độ mới.
- [ ] Mỗi phase là một **dải** nền tint `var(--phase-N)` (N = thứ tự phase, quay vòng 1..7 theo REDESIGN 3.1: phase 8, 9 dùng lại tint 1, 2 — tức `((order - 1) % 7) + 1`, với phase 0 thì dùng order+1 để không ra 0; chọn cách map rõ ràng và ghi chú ở đầu file). Dải có tên phase (sentence case, `text-sm font-bold`) + `%` mono `tabular-nums` bên phải, bo `rounded-lg`, không viền, không shadow.
- [ ] Mỗi bài là một **ngăn** (`Link` tới `/lesson/<id>/` nếu `ready`, ngược lại `/learn/`), `rounded-md`, cỡ ≥ 36px (vùng bấm 44px qua pseudo-element nếu nhỏ hơn), hiển thị số thứ tự bài mono:
  - `completed`: nền `bg-success-soft`, icon `Check` (`aria-hidden`), chữ `text-primary-ink`.
  - bài kế tiếp (`id === nextId`): nền `bg-card`, viền 2px `border-primary`, chữ `text-primary font-bold`.
  - `in_progress`: nền `bg-card`, viền 1px `border-primary/50`.
  - `available`: nền `bg-card/80`, viền hairline `border-border`.
  - `locked`, `skipped`, `coming_soon`: nhạt (`opacity-60` hoặc `text-muted-foreground`), `coming_soon` viền dashed. Không dùng đỏ.
  - Mỗi ngăn có `title` + `aria-label` = `"<tên bài>: <trạng thái>"` (dùng `ts(status)` như code cũ). Trạng thái không chỉ dựa vào màu (completed có tick, next có viền dày).
  - `focus-visible:outline-2 outline-ring`; hover chỉ `transition-colors` hoặc `translate-y` (≤150ms, tắt khi reduced-motion qua class `motion-reduce:transform-none`).
- [ ] `variant="compact"`: chỉ hiện phase đang học (phase của `nextId`) mở đầy đủ ngăn, các phase khác thu thành một dải một dòng (tên + `%` + thanh nhỏ `Progress`), dùng tối đa ~9 dải. `variant="full"`: mọi phase đều mở ngăn (để bước 5 dùng; chỉ cần render đúng, chưa gắn vào `/learn`).
- [ ] Ngăn trong dải xếp `flex flex-wrap gap-1.5`; ở 375px không tràn ngang.

### Dashboard `page.tsx`
- [ ] **Bỏ** `<h1>` "PyAI Path". `<h1>` mới là câu chào sẵn có (`t("greetingNew")` / `t("greeting")`), `text-2xl font-bold tracking-tight`.
- [ ] Ngay dưới: khối **bài kế tiếp** (không phải `Card` có shadow; dùng `Card` viền hairline mặc định): tag phase (`Badge`), tên bài `text-xl font-bold`, summary `line-clamp-2`, `Progress` + thời lượng mono, nút chính `Button size="lg"` "Bắt đầu/Tiếp tục". Bỏ ô icon có `shadow-[4px_4px_0_var(--hit)]`. Giữ nhánh `allCaughtUp`.
- [ ] Ngay dưới khối đó: `<RoadmapTray variant="compact" nextId={data.next?.id} />` trong một section có tiêu đề `t("skillTree")`, dòng phụ "bài đã xong / bài tập đã qua" (giữ chuỗi `tc("of", …)` hiện có) và link `t("openRoadmap")` → `/learn/`.
- [ ] **Hàng số liệu**: streak, XP hôm nay (`/goal`), thẻ cần ôn (link `/review/`), tổng XP gom thành **một hàng** số + nhãn: số `font-mono tabular-nums text-2xl font-bold text-foreground`, nhãn `text-xs text-muted-foreground` dưới số. Không ô icon, không `figure`, không `text-hit`, không `text-[44px]`. Ngăn cách bằng `divide-x divide-border` (desktop) / lưới 2×2 ở mobile. Ô "cần ôn" là `Link` có `focus-visible` và mũi tên `aria-hidden` khi `due > 0`.
- [ ] Bố cục: lưới `lg:grid-cols-3`: cột trái (`lg:col-span-2`) = bài kế tiếp + khay + hàng số; cột phải = "chủ đề cần củng cố" (`weakTopics`) và "tiêu chí thuần thục" (`mastery`). Heatmap hoạt động giữ lại ở dưới cùng, ô `rounded-[3px]` → dùng `rounded-sm`, mức 3 dùng `bg-primary-ink` (không `bg-hit`), bỏ `hover:scale-150`.
- [ ] `Criterion`: icon `aria-hidden`; mục đã xong không gạch ngang đậm màu (`line-through` bỏ `decoration-2 decoration-success`, dùng `text-muted-foreground` + icon check `text-primary`).
- [ ] Không còn trong `page.tsx` và `roadmap-tray.tsx`: `font-black`, `font-semibold`, `uppercase`, `figure`, `display`, `row-cursor`, `text-hit`, `bg-hit`, `border-edge`, `shadow-[`, `border-2` (trừ viền ngăn "bài kế tiếp"), `rounded-[`, `text-[NNpx]`, `transition-all`, `hover:scale`, literal màu.
- [ ] Mọi chuỗi qua next-intl; key mới (nếu có) ở cả en/vi.
- [ ] Lệnh kiểm tra xanh.

## Lệnh kiểm tra
Từ gốc repo `D:\Proj\python-ai-platform`. **Không chạy `pnpm --filter web build`** (dev server đang chạy ở port 3000, build sẽ ghi đè `src/generated` làm nó hỏng). Boss sẽ tự build.
```
pnpm --filter web typecheck
grep -nE "font-black|font-semibold|uppercase|\bfigure\b|\bdisplay\b|row-cursor|text-hit|bg-hit|border-edge|shadow-\[|rounded-\[|text-\[[0-9]+px\]|transition-all|hover:scale|#[0-9a-fA-F]{6}|oklch\(" "apps/web/src/app/(main)/page.tsx" apps/web/src/components/roadmap-tray.tsx
node -e "const a=require('./apps/web/messages/en.json'),b=require('./apps/web/messages/vi.json');const k=(o,p='')=>Object.entries(o).flatMap(([x,v])=>typeof v==='object'?k(v,p+x+'.'):[p+x]);const A=k(a),B=k(b);console.log('en-only',A.filter(x=>!B.includes(x)),'vi-only',B.filter(x=>!A.includes(x)))"
```
Mong đợi: typecheck 0 lỗi; grep rỗng; hai mảng rỗng.

## Ghi chú cho worker
- Đọc `docs/REDESIGN.md` (3.1, 3.4, 4) và `apps/web/design.md` trước.
- Có thể xem `http://localhost:3000/` để tự kiểm tra (dev server đang chạy, HMR).
- Token: `bg-[var(--phase-1)]` … `bg-[var(--phase-7)]` (chưa map trong `@theme`, dùng arbitrary value; Tailwind cần chuỗi class tĩnh, nên khai báo một mảng 7 chuỗi class đầy đủ thay vì ghép chuỗi động).
- Font chỉ có 400/500/700. Windows: dùng `pnpm.cmd` nếu PowerShell chặn `pnpm`.

## Feedback vòng 1
Typecheck + grep xanh, khay chạy đúng. (Lượt trước bị rớt mạng ở cuối nhưng code đã ghi đủ; không cần làm lại.) Sửa:

1. **Phase 0 và phase 1 cùng tint 1** (`getPhaseTintClass`: order 0 → 1, order 1 → 1) nên hai dải đầu trùng màu. Đổi công thức thành `PHASE_TINT_CLASSES[order % 7]` (order 0..6 → tint 1..7, order 7, 8 → tint 1, 2 — đúng REDESIGN "phase 8 và 9 quay vòng lại hai tint đầu"). Sửa comment đầu file cho khớp.
2. **Tương phản ở light**: `text-muted-foreground` trên các tint phase chỉ 3.7–4.8:1 (< 4.5 ở tint 1, 2, 4, 5, 6, 7). Mọi chữ nằm trên dải tint (tên phase, `%`, số ngăn ở trạng thái thường) dùng `text-foreground`; trạng thái nhạt (locked/skipped/coming_soon) giữ `opacity-60` (là trạng thái không hoạt động, chấp nhận).
3. **Hàng số liệu bị đẩy quá sâu** (dưới 9 dải khay, ngoài màn hình 1440×900). Chuyển hàng số liệu lên **header**: một hàng `flex flex-wrap items-end justify-between gap-4` gồm `<h1>` câu chào bên trái và 4 số liệu bên phải (desktop); ở mobile số liệu xuống dòng dưới h1 dạng lưới 4 cột gọn (`grid-cols-4`, số `text-xl`). Giữ đúng thứ tự: bài kế tiếp → khay (không chen gì giữa).
4. Dải thu gọn của phase **chưa có bài** (`!prog.ready`): không hiện `Progress` và `0%`, chỉ tên + badge "Sắp ra mắt".
5. Chạy lại Lệnh kiểm tra (vẫn KHÔNG `pnpm build`), thêm mục "Vòng 2" vào report.

## Trạng thái
- Bước hiện tại: 5 (chờ user review + commit)
- Vòng: 2/3, đạt
- Boss đã kiểm: typecheck, build, validate, grep; desktop dark + light, 375px light, không cuộn ngang
- Ghi cho sweep (bước 11): "10 phút" ở khối bài kế tiếp bị xuống dòng ở 375px, cần `whitespace-nowrap`
- Số lần swap: 0
- Fallback: không
