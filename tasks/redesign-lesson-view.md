# Redesign Dose: Lesson view (REDESIGN.md bước 3)

## Mục tiêu
Đưa màn `/lesson/[id]` (màn dùng nhiều nhất) sang theme Dose theo `docs/REDESIGN.md` mục 3, mục 4 hàng #1,
và `apps/web/design.md` (đã có từ bước 1–2, đọc trước). Tokens và `components/ui/*` đã xong; task này chỉ
sửa markup/className của các component trong lesson view.

## File được phép sửa/tạo
Trong `apps/web/src/`:
- `components/lesson/lesson-view.tsx`, `exercise-panel.tsx`, `lesson-quiz.tsx`, `rag-chat.tsx`
- `components/workbench.tsx`, `code-editor.tsx`, `markdown.tsx`, `visualizer.tsx`, `question.tsx`
- `app/(main)/lesson/[id]/page.tsx`
- `app/globals.css`: chỉ phần CSS của lesson prose / callout / mermaid / `.hljs` nếu cần (không literal màu).
- `apps/web/messages/en.json` + `vi.json`: chỉ **thêm** key nếu thật cần (cả hai file, cùng key).

## Không được đụng
- `curriculum/`, `tools/`, `supabase/`, `apps/web/src/lib/*`, `public/pyodide-worker.js`, `components/ui/*`, `tokens.css`.
- Prop, state, handler, hook, luồng dữ liệu của Monaco / Pyodide / RAG / quiz / exercise (REDESIGN mục 2). Chỉ sửa JSX markup và className.
- Không xóa key i18n, không xóa file, không sửa test. Không `git commit`.
- `question.tsx` cũng được dùng ở exam/placement: chỉ đổi giao diện, giữ nguyên API.

## Tiêu chí hoàn thành (checklist)
- [ ] **Bố cục** giữ chia đôi. Cột trái: prose trên `bg-card`/`bg-background`, measure 65–72ch, 16–17px, line-height 1.6. Cột phải: editor + output là **một mặt phẳng** `bg-code`, toolbar gọn (nút cao 36px, icon có `aria-label` khi không có chữ).
- [ ] **Không còn** trong các file trên: `rounded-[2px]`, `rounded-[4px]`, `border-2`, `font-black`, `font-semibold`, `uppercase`, `transition-all`, `transition ` trơn (dùng `transition-colors` / `transition-transform` / `transition-opacity`), `shadow-xl`, `shadow-2xl`, `hover:scale-*`, `text-hit`, `bg-hit`, `border-edge`, `text-[NNpx]` lệch thang (dùng `text-xs`/`text-sm`/…; riêng code/output được `text-[13px]`).
  Radius: control `rounded-md` (10px), card/panel `rounded-lg` (14px), tag `rounded-full`.
- [ ] **Monaco theme** (`code-editor.tsx`): hex được phép **chỉ ở file này** (Monaco bắt buộc hex). Dùng đúng các giá trị (đã quy đổi từ token):
  - light `pyai-light`: background/gutter `#f3f2ec`, lineHighlight `#ebeae1`, lineNumber `#7c8a83`, comment `#596f65` italic, keyword `#006738`, string `#416b25`, number `#905211`, type/function `#005532`.
  - dark `pyai-dark`: background/gutter `#090f0d`, lineHighlight `#111815`, lineNumber `#54615b`, comment `#768c82` italic, keyword `#5aca94`, string `#99c77f`, number `#e4b572`, type/function `#70ddb1`.
  Giữ cơ chế đổi theme theo `resolvedTheme` hiện có.
- [ ] **Kết quả test** (`workbench.tsx`): mỗi test là một hàng có icon (lucide `CheckCircle2` / `XCircle`, `aria-hidden`) + chữ tên test + màu; không chỉ dựa vào màu. Ô tóm tắt pass/total dùng `font-mono tabular-nums` cỡ `text-3xl` (bỏ `figure text-[48px]`, bỏ `display`). Trạng thái loading Pyodide / running / error / timeout vẫn hiển thị như cũ, đổi style sang Dose (`bg-danger-soft text-danger`, `bg-warning-soft text-warning-ink`).
- [ ] **Exercise panel**: danh sách bài tập là các hàng chọn (selected = `bg-accent text-primary` + viền `border-primary`), chấm độ khó `rounded-full`, hint tầng 1–3: nút số tròn, hint đã mở là card `bg-warning-soft` viền hairline, chữ `text-foreground`.
- [ ] **Question / quiz**: lựa chọn là "phím nhựa" (dùng `.press` hoặc `Button variant="outline"` phong cách tương đương), state selected (`bg-accent border-primary`), correct (`bg-success-soft` + icon check + chữ), wrong (`bg-danger-soft` + icon X + chữ). Có `focus-visible`. Parsons/fill giữ hành vi.
- [ ] **Markdown** (`markdown.tsx`): code block `rounded-lg bg-code` viền hairline, nút Copy/Run/Visualize cỡ `text-xs` có focus-visible; callout TIP/NOTE/WARNING dùng token (`--accent`/`--muted`/`--warning-soft`), viền trái 3px thay vì viền 4 phía; mermaid container `rounded-lg`. Không literal màu.
- [ ] **Visualizer**: dòng đang chạy highlight `bg-accent` + vạch trái `border-primary`; frame/biến dạng bảng gọn, `font-mono`.
- [ ] **RAG chat** (`rag-chat.tsx`): sửa 3 chỗ `transition-all` (dòng ~366, ~381, ~589) sang thuộc tính cụ thể; nút nổi bỏ `hover:scale-105` + `shadow-xl`, dùng `.press` hoặc `shadow-[var(--shadow-lift)]` (chọn một, không kèm viền); panel chat: `rounded-lg bg-popover shadow-[var(--shadow-lift)]` **không viền**; select/textarea `rounded-md` có `focus-visible:outline-ring`. State "đang trả lời / lỗi / offline" giữ logic, đổi style.
- [ ] Mọi nút chỉ có icon có `aria-label` (dùng key i18n có sẵn hoặc thêm key mới vào cả en/vi); icon trang trí `aria-hidden="true"`.
- [ ] Motion chỉ `transform`/`opacity`, 120–200ms. `animate-pulse`/`animate-spin` trên loader được giữ.
- [ ] Không cuộn ngang ở 375px: cột phải xuống dưới cột trái trên mobile như hiện tại.
- [ ] Lệnh kiểm tra xanh.

## Lệnh kiểm tra
Từ gốc repo `D:\Proj\python-ai-platform`:
```
pnpm --filter web typecheck
pnpm --filter web build
uv run python tools/validate.py --fast
```
Grep (mong đợi: rỗng):
```
grep -nE "rounded-\[(2|4)px\]|border-2|font-black|font-semibold|uppercase|transition-all|transition |shadow-xl|shadow-2xl|hover:scale|text-hit|bg-hit|border-edge|backdrop-blur" apps/web/src/components/lesson/*.tsx apps/web/src/components/workbench.tsx apps/web/src/components/code-editor.tsx apps/web/src/components/markdown.tsx apps/web/src/components/visualizer.tsx apps/web/src/components/question.tsx
grep -nE "#[0-9a-fA-F]{6}\b|oklch\(|rgb\(" apps/web/src/components/lesson/*.tsx apps/web/src/components/workbench.tsx apps/web/src/components/markdown.tsx apps/web/src/components/visualizer.tsx apps/web/src/components/question.tsx
node -e "const a=require('./apps/web/messages/en.json'),b=require('./apps/web/messages/vi.json');const k=(o,p='')=>Object.entries(o).flatMap(([x,v])=>typeof v==='object'?k(v,p+x+'.'):[p+x]);const A=k(a),B=k(b);console.log('en-only',A.filter(x=>!B.includes(x)),'vi-only',B.filter(x=>!A.includes(x)))"
```
(lệnh cuối: cả hai mảng phải rỗng)

## Ghi chú cho worker
- Đọc `docs/REDESIGN.md` và `apps/web/design.md` trước. Xem `components/ui/button.tsx`, `badge.tsx` để dùng lại variant có sẵn thay vì viết class mới.
- Token có sẵn: `bg-code`, `bg-accent`, `text-primary`, `text-primary-ink`, `bg-success-soft`, `bg-danger-soft`, `bg-warning-soft`, `text-warning-ink`, `shadow-[var(--shadow-lift)]`.
- Font chỉ có weight 400/500/700 (`font-normal`/`font-medium`/`font-bold`).
- Windows: dùng `pnpm.cmd` nếu PowerShell chặn `pnpm`.

## Trạng thái
- Bước hiện tại: 5 (chờ user review + commit)
- Vòng: 1/3, đạt
- Boss đã kiểm: gates xanh; desktop dark, 375px light (nội dung + editor, Monaco đổi theme), không cuộn ngang
- Số lần swap: 0
- Fallback: không
