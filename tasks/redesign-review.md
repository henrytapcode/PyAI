# Redesign Dose: trang Review (REDESIGN.md bước 6)

## Mục tiêu
Đưa `/review` (`app/(main)/review/page.tsx`) sang theme Dose theo `docs/REDESIGN.md` mục 3 và mục 4 hàng #4
("Thẻ flashcard ở giữa, bộ đếm mono. Empty state: nói rõ chưa có thẻ nào đến hạn và nút sang bài học"),
theo `apps/web/design.md`.

## File được phép sửa/tạo
- Sửa: `apps/web/src/app/(main)/review/page.tsx`
- `apps/web/messages/en.json` + `vi.json`: **thêm** key mới trong namespace `review` nếu cần (cả hai file, cùng key). Không đổi/xóa key cũ.

## Không được đụng
- `curriculum/`, `tools/`, `supabase/`, `apps/web/src/lib/*` (srs, quiz, selectors…), `components/*` (kể cả `question.tsx`, `markdown.tsx`, `ui/*`), `tokens.css`, `globals.css`.
- Logic: `queue`, `pos`, `reviewed`, `onGrade`, `practice`, `resolve`, `initialDue`, `previewInterval`, `suggest`, cách gọi `reviewCard`. Chỉ sửa JSX markup + className, và thêm một nút/link ở empty state.
- Không xóa file, không sửa test, không `git commit`. **Không chạy `pnpm --filter web build`** (dev server đang chạy; boss tự build).

## Tiêu chí hoàn thành (checklist)
- [ ] **Bộ đếm**: `pos/queue` hiển thị `font-mono tabular-nums` (`text-sm font-medium text-foreground`), cạnh `Progress`. Badge "Bộ thẻ" dùng `font-mono tabular-nums` cho số; icon `aria-hidden`.
- [ ] **Thẻ ở giữa**: khung thẻ `Card` viền hairline (không shadow), `max-w-2xl mx-auto` như cũ, padding `p-6 sm:p-8`. Mặt trước `text-xl font-bold`; mặt sau ngăn bằng `border-t border-border pt-5`. Lật thẻ chỉ dùng `animate-rise` sẵn có (opacity/transform), không thêm animation khác.
- [ ] **Nút chấm điểm** (`GradeButtons`): 4 nút cùng kiểu "phím nhựa" trung tính — dùng `Button variant="outline"` (đã có `.press`) hoặc class tương đương, `h-auto flex-col py-2.5`, nhãn `text-sm font-medium`, khoảng ngày `text-xs font-mono tabular-nums text-muted-foreground`. **Không dùng màu đỏ/vàng** cho "Quên"/"Khó" (REDESIGN 3.1: đỏ chỉ cho đúng/sai của code/quiz; ôn tập dùng xám). Nút được gợi ý (`suggest === g`) nổi bật bằng `border-primary bg-accent text-primary` (không `ring-current`). Thêm `type="button"` và `aria-label` gộp nhãn + khoảng ngày (vd `"Ổn · 3 ngày"`, ghép từ chuỗi đã dịch, không chuỗi cứng). Có `focus-visible`.
- [ ] **Empty state** (không có thẻ đến hạn, `reviewed === 0`):
  - Icon `CheckCircle2` dùng `text-primary` (bỏ `text-success`), `aria-hidden`, `size-8`.
  - Tiêu đề `t("due", { count: 0 })`, dòng phụ `t("empty")` (giữ nguyên).
  - **Thêm** nút chính `Button asChild` → `Link href="/learn/"` với key mới `review.goToLessons` (en: `"Go to lessons"`, vi: `"Sang lộ trình bài học"`). Nếu `deckSize > 0` thì nút "Vẫn luyện thêm" là `variant="outline"` đặt cạnh nút chính.
- [ ] **Hết phiên** (`reviewed > 0`): bỏ `PartyPopper text-warning` (không dùng vàng làm trang trí); dùng `CheckCircle2 text-primary`. Số đã ôn (`t("reviewed")`) giữ nguyên chuỗi. Có cùng nút `goToLessons`.
- [ ] `SourceLine`: link "Từ bài" có `focus-visible:outline-2 outline-ring rounded-sm`, `hover:text-foreground underline-offset-4`.
- [ ] Không còn trong file: `rounded-[`, `border-2`, `font-black`, `font-semibold`, `uppercase`, `transition ` trơn / `transition"`, `transition-all`, `ring-current`, `text-[NNpx]`, `text-danger`, `text-warning`, `border-danger`, `border-warning`, `text-success`, `PartyPopper`, literal màu.
- [ ] Ở 375px: 4 nút chấm điểm vẫn nằm một hàng (`grid-cols-4 gap-1.5`), chữ không tràn; không cuộn ngang.
- [ ] Lệnh kiểm tra xanh.

## Lệnh kiểm tra
Từ gốc repo `D:\Proj\python-ai-platform` (KHÔNG `pnpm build`):
```
pnpm --filter web typecheck
grep -nE "rounded-\[|border-2|font-black|font-semibold|uppercase|transition[ \"]|transition-all|ring-current|text-\[[0-9]+px\]|text-danger|text-warning|border-danger|border-warning|text-success|PartyPopper|#[0-9a-fA-F]{6}|oklch\(" "apps/web/src/app/(main)/review/page.tsx"
node -e "const a=require('./apps/web/messages/en.json'),b=require('./apps/web/messages/vi.json');const k=(o,p='')=>Object.entries(o).flatMap(([x,v])=>typeof v==='object'?k(v,p+x+'.'):[p+x]);const A=k(a),B=k(b);console.log('en-only',A.filter(x=>!B.includes(x)),'vi-only',B.filter(x=>!A.includes(x)),'goToLessons',A.includes('review.goToLessons'))"
```
Mong đợi: typecheck 0 lỗi; grep rỗng; hai mảng rỗng và `goToLessons true`.
Tự xem `http://localhost:3000/review/` (HMR). Tài khoản mới thường rơi vào empty state; muốn thấy thẻ thì vào một bài, bấm "đánh dấu đã đọc" để thêm flashcard, rồi bấm "Vẫn luyện thêm".

## Ghi chú cho worker
- Đọc `docs/REDESIGN.md` và `apps/web/design.md` trước. Xem `components/ui/button.tsx` để dùng lại variant.
- Font chỉ 400/500/700. Windows: dùng `pnpm.cmd` nếu PowerShell chặn `pnpm`.

## Feedback vòng 1
Đạt gần hết. Một lỗi:

1. `review/page.tsx` dòng ~72: `t.rich("deckSize", { count: <span …>{deckSize}</span> as unknown as string })` là ép kiểu lách TypeScript; message `deckSize` không có tag nên next-intl không hỗ trợ giá trị là element. Console báo `Each child in a list should have a unique "key" prop … Check the render method of span. It was passed a child from ReviewPage`, và số bị tách xuống dòng riêng. Sửa: bỏ `t.rich`, dùng `{t("deckSize", { count: deckSize })}` bình thường, thêm `tabular-nums` vào `className` của `Badge`. Không đổi message JSON.
2. Chạy lại Lệnh kiểm tra (KHÔNG `pnpm build`), thêm mục "Vòng 2" ngắn vào report.

## Trạng thái
- Bước hiện tại: 5 (chờ user review + commit)
- Vòng: 2/3, đạt
- Boss đã kiểm: typecheck, build, validate, grep; empty state + thẻ + 4 nút chấm điểm ở 375px dark, aria-label đúng, console sạch
- Số lần swap: 0
- Fallback: không
