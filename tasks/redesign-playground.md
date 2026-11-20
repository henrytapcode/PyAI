# Redesign Dose: Playground (REDESIGN.md bước 8)

## Mục tiêu
Đưa `/playground` (`app/(main)/playground/page.tsx`) sang theme Dose theo `docs/REDESIGN.md` mục 4 hàng #6
("Editor toàn chiều rộng, output bên dưới hoặc bên phải; trạng thái đang tải Pyodide") và `apps/web/design.md`.
`Workbench` (editor + output + chấm trạng thái Pyodide) đã redesign ở bước 3; task này chỉ làm phần vỏ trang.

## File được phép sửa/tạo
- Sửa: `apps/web/src/app/(main)/playground/page.tsx`
- `apps/web/messages/en.json` + `vi.json`: chỉ **thêm** key trong namespace `editor` nếu thật cần (cả hai file).

## Không được đụng
- `components/workbench.tsx`, `code-editor.tsx`, mọi `components/*`, `lib/*`, `tokens.css`, `globals.css`, `curriculum/`, `tools/`.
- Logic trang: `TEMPLATES` (nội dung code giữ nguyên từng ký tự), `KEY`, `useEffect` đọc localStorage, `update`. Chỉ sửa JSX markup + className.
- Không xóa file, không sửa test, không `git commit`. **Không chạy `pnpm --filter web build`** (boss tự build).

## Tiêu chí hoàn thành (checklist)
- [ ] **Header trang** (thanh trên editor): nền đặc `bg-muted`, viền dưới hairline `border-b border-border`, `px-4 py-3 sm:px-6`. Tiêu đề `<h1 className="text-lg font-bold tracking-tight">`, phụ đề `text-sm text-muted-foreground` (không `truncate` ở mobile; cho xuống dòng, `line-clamp-2`).
- [ ] **Chọn template** là một nhóm nút: bọc `role="group"` với `aria-label={t("templates")}`; nhãn "Templates:" hiển thị `text-sm text-muted-foreground` (bỏ dấu `:` cứng trong JSX — nếu cần dấu, thêm vào bản dịch, không ghép cứng). Mỗi nút:
  - `type="button"`, `aria-pressed={code === TEMPLATES[k]}`;
  - kiểu chip `h-9 rounded-md border px-3 font-mono text-xs transition-colors`, vùng bấm ≥ 44px (pseudo-element `relative after:absolute after:-inset-1 after:content-['']` hoặc tương đương);
  - mặc định `border-border bg-card text-foreground hover:bg-accent`; đang chọn `border-primary bg-accent text-primary font-bold`;
  - `focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring`.
- [ ] Ở 375px: header xếp dọc (tiêu đề trên, nhóm template dưới), nhóm template `flex-wrap gap-1.5` hoặc cuộn ngang trong chính nó (`overflow-x-auto`), **trang không cuộn ngang**. Chiều cao trang vẫn tính như cũ để editor lấp đầy (`h-[calc(100dvh-3.5rem-4rem)] lg:h-dvh` giữ nguyên).
- [ ] Tên file `playground.py` trong `title` của `Workbench`: `font-mono text-sm text-muted-foreground`.
- [ ] Không còn trong file: `rounded-[`, `border-2`, `font-black`, `font-semibold`, `uppercase`, `transition-all`, `text-\[NNpx\]`, `backdrop-blur`, literal màu.
- [ ] Lệnh kiểm tra xanh.

## Lệnh kiểm tra
Từ gốc repo `D:\Proj\python-ai-platform` (KHÔNG `pnpm build`):
```
pnpm --filter web typecheck
grep -nE "rounded-\[|border-2|font-black|font-semibold|uppercase|transition-all|text-\[[0-9]+px\]|backdrop-blur|#[0-9a-fA-F]{6}|oklch\(" "apps/web/src/app/(main)/playground/page.tsx"
grep -c "aria-pressed" "apps/web/src/app/(main)/playground/page.tsx"
git diff --stat
node -e "const a=require('./apps/web/messages/en.json'),b=require('./apps/web/messages/vi.json');const k=(o,p='')=>Object.entries(o).flatMap(([x,v])=>typeof v==='object'?k(v,p+x+'.'):[p+x]);const A=k(a),B=k(b);console.log('en-only',A.filter(x=>!B.includes(x)),'vi-only',B.filter(x=>!A.includes(x)))"
```
Mong đợi: typecheck 0 lỗi; grep đầu rỗng; `aria-pressed` ≥ 1; `git diff --stat` chỉ có playground (+ messages nếu thêm key); hai mảng rỗng.
Tự xem `http://localhost:3000/playground/` (HMR).

## Ghi chú cho worker
- Đọc `docs/REDESIGN.md` và `apps/web/design.md` trước.
- Font chỉ 400/500/700. Windows: dùng `pnpm.cmd` nếu PowerShell chặn `pnpm`.

## Trạng thái
- Bước hiện tại: 5 (chờ user review + commit)
- Vòng: 1/3, đạt
- Boss đã kiểm: typecheck, build, validate, grep; 375px dark không cuộn ngang; chạy code ra đúng output
- Số lần swap: 0
- Fallback: không
