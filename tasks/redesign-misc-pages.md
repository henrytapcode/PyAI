# Redesign Dose: Glossary, Interview, Portfolio, Settings (REDESIGN.md bước 9)

## Mục tiêu
Đưa 4 trang `/glossary`, `/interview`, `/portfolio`, `/settings` sang theme Dose theo `docs/REDESIGN.md` mục 3 và
mục 4 hàng #7, theo `apps/web/design.md`:
"Glossary: ô tìm sticky nền đặc, danh sách dạng bảng. Portfolio: bỏ mũi tên dính chữ. Settings: nhóm theo mục,
xác nhận trước khi xóa tiến độ."

## File được phép sửa/tạo
- Sửa: `apps/web/src/app/(main)/glossary/page.tsx`, `interview/page.tsx`, `portfolio/page.tsx`, `settings/page.tsx`
- `apps/web/messages/en.json` + `vi.json`: chỉ **thêm** key nếu thật cần (cả hai file, cùng key).

## Không được đụng
- `components/*` (kể cả `ui/*`, `markdown.tsx`), `lib/*`, `tokens.css`, `globals.css`, `curriculum/`, `tools/`.
- Logic: tìm kiếm/lọc tag glossary, đánh dấu đã luyện ở interview, export/import/reset/redo onboarding ở settings, download/xem code ở portfolio. Chỉ sửa JSX markup + className; ngoại lệ duy nhất: Settings đổi `window.confirm` sang `Dialog` (xem dưới), vẫn gọi đúng `p.reset()` + `setMessage(...)` như cũ.
- Mọi `href`. Không xóa file, không sửa test, không `git commit`. **Không chạy `pnpm --filter web build`** (boss tự build).

## Tiêu chí hoàn thành (checklist)
### Chung (cả 4 file)
- [ ] Không còn: `rounded-[`, `border-2`, `font-black`, `font-semibold`, `uppercase`, `transition ` trơn / `transition"`, `transition-all`, `text-hit`, `bg-hit`, `decoration-hit`, `border-edge`, `shadow-[`, `text-[NNpx]`, `backdrop-blur`, `row-cursor`, literal màu, ký tự `→` trong JSX.
- [ ] Radius: control `rounded-md`, card/panel `rounded-lg`, tag/chip lọc `rounded-full`. Icon trang trí `aria-hidden="true"`; nút chỉ icon có `aria-label`. `focus-visible:outline-2 outline-ring` cho mọi phần tử bấm tự viết (không dùng `Button`).
- [ ] Chip lọc (TagButton ở glossary/interview): `type="button"`, `aria-pressed={active}`, `h-9 px-3 text-sm rounded-full border transition-colors`; đang chọn `border-primary bg-accent text-primary font-bold` (không tô đặc `bg-primary`); mặc định `border-border bg-card hover:bg-accent`.
- [ ] Trạng thái "xong/đã luyện" dùng `bg-success-soft text-primary-ink` (không `text-success` trên `bg-success-soft` — tương phản thấp).
- [ ] 375px: không cuộn ngang trang.

### Glossary
- [ ] Khối tìm kiếm sticky: nền đặc `bg-background`, viền dưới hairline, `py-3`, giữ `sticky top-14 lg:top-0`. Ô tìm `rounded-md border border-border bg-card h-10 px-3`, `focus-within:outline-2 outline-ring` (bỏ `ring-ring/40`); input có `aria-label={t("placeholder")}` hoặc `<label>` sr-only.
- [ ] Danh sách thuật ngữ **dạng bảng/danh sách hàng** thay lưới card: khung `rounded-lg border border-border bg-card divide-y divide-border`; mỗi hàng: cột trái thuật ngữ `font-mono text-sm font-bold` + tên VI `text-sm text-muted-foreground`; cột phải định nghĩa `text-sm` + ví dụ `pre` `rounded-md bg-code text-xs`. Ở `sm+` hai cột (`sm:grid sm:grid-cols-[14rem_1fr] gap-4`), `<sm` xếp dọc.

### Interview
- [ ] Câu hỏi dạng accordion: mỗi mục `rounded-lg border border-border bg-card`, nút mở có `aria-expanded`, `aria-controls` (nếu chưa có thì thêm, id dựa trên `q.id`), chevron `transition-transform motion-reduce:transition-none`.
- [ ] Nút "đã luyện": `Button variant="outline" size="sm"` hoặc class tương đương; trạng thái đã luyện như mục Chung.

### Portfolio
- [ ] Card dự án: `Card` mặc định; dự án xong thêm `border-primary/40` (không `border-success/40`). Ô icon phase `size-10 rounded-md bg-muted`, icon `aria-hidden`.
- [ ] Link "Tiếp tục" (`tc("continue")`) dùng `Button asChild variant="outline" size="sm"` thay link gạch chân `decoration-hit`. Không có mũi tên dính chữ; nếu cần mũi tên thì icon lucide `ArrowRight aria-hidden` có `gap`.
- [ ] Badge "đã nộp" khi `completedAt` rỗng không render chuỗi rỗng — chỉ hiện icon + nhãn có nghĩa (dùng key sẵn có nếu có; nếu không thì ẩn badge text, giữ icon có `aria-label`).

### Settings
- [ ] **Nhóm theo mục**: mỗi nhóm (ngôn ngữ/giao diện, mục tiêu học, dữ liệu: export/import, vùng nguy hiểm: làm lại onboarding/xóa tiến độ) là một section có `<h2 className="text-base font-bold">` + mô tả `text-sm text-muted-foreground`. Dùng key sẵn có; thiếu tiêu đề nhóm thì thêm key mới trong `settings` (cả en/vi).
- [ ] **Xác nhận xóa tiến độ bằng `Dialog`** (`components/ui/dialog.tsx`: `Dialog`, `DialogContent`, `DialogTitle`, `DialogDescription`) thay `window.confirm`: state `confirmReset` (boolean), `DialogTitle` = `t("reset")`, `DialogDescription` = `t("resetConfirm")`, hai nút `Button variant="outline"` = `tc("cancel")` và `Button variant="danger"` = `tc("confirm")`; bấm xác nhận → `p.reset(); setMessage({ ok: true, text: t("resetDone") }); setConfirmReset(false)`. Nút mở dialog: `Button variant="outline"` chữ `text-danger` (không tô đặc).
- [ ] Segmented control (dòng ~193): `rounded-md bg-muted p-0.5`, mục `rounded-sm px-3 py-1.5 text-sm`, đang chọn `bg-card text-primary font-bold`, có `role="radiogroup"`/`role="radio"` + `aria-checked` nếu chưa có.
- [ ] Thông báo import/reset (`message`): `rounded-md px-3 py-2 text-sm`, ok = `bg-success-soft text-primary-ink`, lỗi = `bg-danger-soft text-danger`, `role="status"`.

## Lệnh kiểm tra
Từ gốc repo `D:\Proj\python-ai-platform` (KHÔNG `pnpm build`):
```
pnpm --filter web typecheck
grep -nE "rounded-\[|border-2|font-black|font-semibold|uppercase|transition[ \"]|transition-all|text-hit|bg-hit|decoration-hit|border-edge|shadow-\[|text-\[[0-9]+px\]|backdrop-blur|row-cursor|window\.confirm|→|#[0-9a-fA-F]{6}|oklch\(" "apps/web/src/app/(main)/glossary/page.tsx" "apps/web/src/app/(main)/interview/page.tsx" "apps/web/src/app/(main)/portfolio/page.tsx" "apps/web/src/app/(main)/settings/page.tsx"
grep -c "aria-pressed" "apps/web/src/app/(main)/glossary/page.tsx" "apps/web/src/app/(main)/interview/page.tsx"
git diff --stat
node -e "const a=require('./apps/web/messages/en.json'),b=require('./apps/web/messages/vi.json');const k=(o,p='')=>Object.entries(o).flatMap(([x,v])=>typeof v==='object'?k(v,p+x+'.'):[p+x]);const A=k(a),B=k(b);console.log('en-only',A.filter(x=>!B.includes(x)),'vi-only',B.filter(x=>!A.includes(x)))"
```
Mong đợi: typecheck 0 lỗi; grep đầu rỗng; mỗi file `aria-pressed` ≥ 1; diff chỉ có 4 trang (+ messages); hai mảng rỗng.
Tự xem 4 trang trên `http://localhost:3000` (HMR).

## Ghi chú cho worker
- Đọc `docs/REDESIGN.md`, `apps/web/design.md`, `components/ui/button.tsx`, `components/ui/dialog.tsx` trước.
- Không cắt/ghép chuỗi đã dịch (`.replace`, nối dấu `:`); muốn chuỗi khác thì thêm key.
- Font chỉ 400/500/700. Windows: dùng `pnpm.cmd` nếu PowerShell chặn `pnpm`.

## Feedback vòng 1
Typecheck/grep/i18n xanh, handler còn đủ, dialog xóa tiến độ chạy đúng (Hủy giữ tiến độ). (Lượt trước rớt mạng ở cuối nhưng code đã ghi đủ.) Một lỗi:

1. **Glossary ở 375px**: ~30 chip tag nằm **trong** khối `sticky`, cao `h-9` và `flex-wrap` → khối sticky cao gần 600px, chiếm gần hết màn hình, cuộn danh sách gần như không thấy gì. Sửa trong `glossary/page.tsx`: hàng chip dưới `sm` thành **một dòng cuộn ngang trong chính nó** (`flex flex-nowrap gap-1.5 overflow-x-auto pb-1 [scrollbar-width:none] [&::-webkit-scrollbar]:hidden -mx-4 px-4` hoặc tương đương, chip `shrink-0 whitespace-nowrap`), từ `sm` trở lên giữ `flex-wrap`. Trang vẫn không được cuộn ngang. Kiểm tra `interview/page.tsx` có cùng vấn đề không (nếu chip của nó cũng nằm trong vùng sticky thì sửa y hệt).
2. Chạy lại Lệnh kiểm tra (KHÔNG `pnpm build`), thêm mục "Vòng 2" vào report.

## Trạng thái
- Bước hiện tại: 2
- Vòng: 2/3
- Số lần swap: 0
- Fallback: không
