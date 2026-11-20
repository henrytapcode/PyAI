# Báo cáo: Redesign Dose - Playground (`tasks/redesign-playground.md` · Bước 8)

## 1. Đã làm gì

### `apps/web/src/app/(main)/playground/page.tsx`
- **Header trang (thanh trên editor)**:
  - Cập nhật nền đặc `bg-muted`, viền dưới hairline `border-b border-border`, padding `px-4 py-3 sm:px-6`.
  - Tiêu đề dùng `<h1 className="text-lg font-bold tracking-tight">` với nội dung `{t("playgroundTitle")}`.
  - Phụ đề chuyển sang `line-clamp-2 text-sm text-muted-foreground` (loại bỏ `truncate text-xs`, cho phép xuống dòng tối đa 2 dòng trên mobile).
  - Thêm `shrink-0` để header giữ chiều cao tự nhiên, không bị co lại khi `Workbench` co dãn.

- **Nhóm nút chọn template**:
  - Bọc trong container có `role="group"` và `aria-label={t("templates")}`.
  - Layout responsive: `flex flex-wrap items-center gap-1.5`.
  - Nhãn hiển thị dùng `text-sm text-muted-foreground`, dùng key bản dịch `{t("templatesLabel")}` (không hardcode dấu `:` trong JSX).
  - Các nút chọn template:
    - Bổ sung `type="button"`.
    - Trạng thái chọn: `aria-pressed={code === TEMPLATES[k]}`.
    - Định dạng chip: `h-9 rounded-md border px-3 font-mono text-xs transition-colors`.
    - Vùng bấm cảm ứng ≥ 44px thông qua pseudo-element: `relative after:absolute after:-inset-1 after:content-['']`.
    - Kiểu dáng:
      - Mặc định: `border-border bg-card text-foreground hover:bg-accent`.
      - Đang chọn: `border-primary bg-accent font-bold text-primary`.
    - Trợ năng bàn phím: `focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring`.

- **Responsive ở 375px**:
  - Header xếp dọc: `flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between`. Tiêu đề nằm trên, nhóm template nằm dưới.
  - Nhóm nút template có `flex-wrap gap-1.5`, tự động xuống hàng khi không đủ chiều ngang, đảm bảo **trang không bị cuộn ngang**.
  - Chiều cao trang giữ nguyên: `h-[calc(100dvh-3.5rem-4rem)] lg:h-dvh`.

- **`Workbench` title**:
  - Cập nhật nhãn tên file `playground.py` trong prop `title` thành `font-mono text-sm text-muted-foreground` (bổ sung `text-sm`).

- **Bảo toàn logic**:
  - Giữ nguyên 100% `TEMPLATES` (từng ký tự trong code mẫu không đổi).
  - Giữ nguyên `KEY`, `useEffect` đọc localStorage và hàm `update`.

### Localization (`en.json` & `vi.json`)
- Thêm đồng bộ key `templatesLabel` trong namespace `editor`:
  - `apps/web/messages/en.json`: `"templatesLabel": "Templates:"`
  - `apps/web/messages/vi.json`: `"templatesLabel": "Mẫu:"`
- Giữ nguyên toàn bộ các key hiện có, bao gồm `templates` ("Templates" / "Mẫu") dùng cho `aria-label`.

---

## 2. File đã sửa

1. `apps/web/src/app/(main)/playground/page.tsx`
2. `apps/web/messages/en.json`
3. `apps/web/messages/vi.json`

*(Không chỉnh sửa bất kỳ file nào khác; không đụng `components/*`, `lib/*`, `tokens.css`; không git commit, không chạy `pnpm build`).*

---

## 3. Kết quả lệnh kiểm tra

### Lệnh 1: `pnpm --filter web typecheck` (chạy qua `pnpm.cmd` trên Windows)
```
> web@0.1.0 typecheck D:\Proj\python-ai-platform\apps\web
> pnpm run content && tsc --noEmit

> web@0.1.0 content D:\Proj\python-ai-platform\apps\web
> uv run --project ../.. python ../../tools/build_content.py

Built 24 lessons, 5 exams, 144 flashcards, 387 questions -> apps\web\src\generated
Exit code: 0
```

### Lệnh 2: Kiểm tra class cấm bằng grep
```
grep -nE "rounded-\[|border-2|font-black|font-semibold|uppercase|transition-all|text-\[[0-9]+px\]|backdrop-blur|#[0-9a-fA-F]{6}|oklch\(" "apps/web/src/app/(main)/playground/page.tsx"
```
- **Kết quả**: Rỗng (không tìm thấy class cấm, exit code 1 - sạch hoàn toàn).

### Lệnh 3: Kiểm tra `aria-pressed`
```
grep -c "aria-pressed" "apps/web/src/app/(main)/playground/page.tsx"
```
- **Kết quả**: `1` (đạt yêu cầu ≥ 1).

### Lệnh 4: `git diff --stat`
```
 apps/web/messages/en.json                   |  1 +
 apps/web/messages/vi.json                   |  1 +
 apps/web/src/app/(main)/playground/page.tsx | 32 ++++++++++++++++++++++-------
 3 files changed, 27 insertions(+), 7 deletions(-)
```
- **Kết quả**: Chỉ thay đổi đúng `playground/page.tsx` và 2 file `messages`.

### Lệnh 5: Đối chiếu tính đối xứng i18n
```
node -e "const a=require('./apps/web/messages/en.json'),b=require('./apps/web/messages/vi.json');const k=(o,p='')=>Object.entries(o).flatMap(([x,v])=>typeof v==='object'?k(v,p+x+'.'):[p+x]);const A=k(a),B=k(b);console.log('en-only',A.filter(x=>!B.includes(x)),'vi-only',B.filter(x=>!A.includes(x)))"
```
- **Kết quả**: `en-only [] vi-only []` (đối xứng 100%, 0 key lệch).

---

## 4. Điều còn chưa chắc

- Hiện tại nhóm template chip ở mobile sử dụng `flex-wrap gap-1.5`. Với 4 template mặc định (`hello`, `numpy`, `pandas`, `words`) cùng nhãn "Templates:" / "Mẫu:", trên màn hình 375px các chip có thể nằm trên cùng 1 hàng hoặc ngắt thành 2 hàng vừa vặn mà không cuộn ngang. Nếu sau này có thêm nhiều template dài hơn, có thể cân nhắc chuyển sang thanh cuộn ngang `overflow-x-auto no-scrollbar` nếu muốn giữ chiều cao header cố định.
