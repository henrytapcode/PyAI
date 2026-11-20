# Báo cáo thực hiện: Redesign Dose - Trang Learn (`tasks/redesign-learn.md`)

## 1. Đã làm gì

- **Tách hàm `trayCellClass` dùng chung tại `apps/web/src/components/roadmap-tray.tsx`**:
  - Export hàm `trayCellClass(status: LessonStatus, isNext: boolean): string` trả về đúng chuỗi class trạng thái cell mà `RoadmapTray` đang dùng.
  - Cập nhật `RoadmapTray` gọi lại hàm này, giao diện Dashboard được giữ nguyên 100%.

- **Redesign trang Learn (`apps/web/src/app/(main)/learn/page.tsx`) theo chuẩn theme Dose**:
  - **Bỏ `STATUS_DOT`**: Thay bằng `trayCellClass(st, isNext)` từ `roadmap-tray.tsx`. Ô số/tick có kích thước `size-9 rounded-md font-mono text-xs tabular-nums`, trạng thái `completed` hiển thị `<Check className="size-4" aria-hidden="true" />`, `coming_soon` hiển thị `<Lock className="size-3.5" aria-hidden="true" />`.
  - **Khối Phase nền tint**:
    - Mỗi phase là một khối `rounded-lg p-3 sm:p-4` có nền tint từ `getPhaseTintClass(phase.order)`, không viền, không shadow (không dùng `Card`).
    - Bỏ ô icon phase `size-12 rounded-[4px] bg-primary`. Giữ `PhaseIcon` kích thước `size-5 text-foreground` đặt cạnh tiêu đề, bọc trong `<span aria-hidden="true">`.
    - Tiêu đề phase: thẻ `<h2 className="text-lg font-bold text-foreground">`, nhãn phase "Phase N" gộp vào cùng dòng dạng `<span className="mr-2 text-sm font-medium">{t("phase", { n: phase.order })}</span>` (sentence case, không còn eyebrow tách dòng).
    - Summary phase: `text-sm text-foreground/80` đảm bảo tương phản trên nền tint.
    - Bên phải: Badges (`localRunner` có icon `aria-hidden="true"`, `skipped`, `comingSoon`) + `Progress` bar + tỷ lệ `%` dạng `font-mono text-xs font-bold tabular-nums text-foreground`.
    - Responsive 375px: header phase xếp dọc (`flex flex-col sm:flex-row`), không tràn ngang.
  - **Khay con chứa các bài học**:
    - Sử dụng container `rounded-md bg-card/70 divide-y divide-border overflow-hidden`.
    - Hàng bài `Link` khi `ready`: `group flex items-center gap-4 px-4 py-3 transition-colors hover:bg-accent hover:text-foreground focus-visible:outline-2 focus-visible:outline-ring focus-visible:-outline-offset-2`.
    - Bài kế tiếp (`data-live=true`): nền `bg-accent`, vạch trái 3px `border-l-[3px] border-l-primary`. Xóa bỏ hoàn toàn SVG tam giác.
    - Hàng bài khi chưa `ready`: hiển thị dạng `div` với `opacity-60`.
    - Dòng phụ: thời lượng (`whitespace-nowrap`), trạng thái, prereq warning dùng `text-xs text-foreground/80`; các icon có `aria-hidden="true"`.
    - Mũi tên cuối hàng: `ArrowRight` với `aria-hidden="true"` và `transition-transform group-hover:translate-x-0.5 motion-reduce:transform-none`.
  - **Phase test**:
    - Đặt làm hàng cuối cùng trong khay con.
    - Ô icon dùng `trayCellClass(prog.phaseTestPassed ? "completed" : "available", false)` cùng `<ClipboardCheck className="size-4" aria-hidden="true" />`.
    - Chữ tiêu đề phụ hiển thị `text-sm text-foreground/80` (thay thế `opacity-75`).
  - **Banner Track B (Placement)**:
    - `Card` với viền hairline mặc định, nền `bg-accent`, icon `Trophy` có `aria-hidden="true"` (bỏ `border-primary/30 bg-accent/40`).
  - **Capstones & Đọc thêm**:
    - `Card` mặc định viền hairline, tiêu đề `text-base font-bold text-foreground`, các mục danh sách dùng `text-foreground/80` và icon `aria-hidden="true"`.
  - **Điều hướng bàn phím**:
    - Giữ nguyên toàn bộ logic phím `j`/`k`/`ArrowUp`/`ArrowDown`/`Enter`.
    - Giữ `data-lesson-row` và `data-live={isNext}` trên tất cả các `Link` bài học.
  - **Làm sạch class**:
    - Loại bỏ hoàn toàn: `row-cursor`, `rounded-[`, `border-2`, `border-edge`, `font-black`, `font-semibold`, `uppercase`, `opacity-75`, `text-hit`, `bg-hit`, `shadow-[`, `transition-all`, `hover:scale`, literal màu (`#hex`, `oklch`).

---

## 2. File đã sửa

1. `apps/web/src/components/roadmap-tray.tsx`
2. `apps/web/src/app/(main)/learn/page.tsx`

*(Không chỉnh sửa bất kỳ file nào khác; file i18n giữ nguyên do các key đã có sẵn đầy đủ).*

---

## 3. Kết quả lệnh kiểm tra

Tất cả các lệnh kiểm tra chạy từ thư mục gốc `D:\Proj\python-ai-platform`:

### 3.1. Typecheck (`pnpm --filter web typecheck`)
```
> web@0.1.0 typecheck D:\Proj\python-ai-platform\apps\web
> pnpm run content && tsc --noEmit

> web@0.1.0 content D:\Proj\python-ai-platform\apps\web
> uv run --project ../.. python ../../tools/build_content.py

Built 24 lessons, 5 exams, 144 flashcards, 387 questions -> apps\web\src\generated
```
**Kết quả**: 0 lỗi, build content thành công, `tsc --noEmit` hoàn toàn xanh.

### 3.2. Grep kiểm tra các từ khóa cấm trong `learn/page.tsx`
```bash
grep -nE "row-cursor|rounded-\[|border-2|border-edge|font-black|font-semibold|uppercase|opacity-75|text-hit|bg-hit|shadow-\[|transition-all|hover:scale|STATUS_DOT|#[0-9a-fA-F]{6}|oklch\(" "apps/web/src/app/(main)/learn/page.tsx"
```
**Kết quả**: Không có dòng nào vi phạm (grep exit code 1 / 0 matches).

### 3.3. Kiểm tra số lượng `data-lesson-row`
```bash
grep -c "data-lesson-row" "apps/web/src/app/(main)/learn/page.tsx"
```
**Kết quả**: `2` (thỏa mãn yêu cầu ≥ 1: 1 vị trí query trong `useEffect` và 1 vị trí attribute trên `Link`).

### 3.4. Kiểm tra đối ứng i18n en - vi
```bash
node -e "const a=require('./apps/web/messages/en.json'),b=require('./apps/web/messages/vi.json');const k=(o,p='')=>Object.entries(o).flatMap(([x,v])=>typeof v==='object'?k(v,p+x+'.'):[p+x]);const A=k(a),B=k(b);console.log('en-only',A.filter(x=>!B.includes(x)),'vi-only',B.filter(x=>!A.includes(x)))"
```
**Kết quả**:
```
en-only [] vi-only []
```
Hai mảng rỗng, độ cân đối key 100%.

---

## 4. Điều còn chưa chắc

- Dev server (Next.js) ở port 3000 hiện tại chưa khởi chạy trong môi trường agent, nên việc kiểm tra visual HMR trực tiếp trên trình duyệt chưa thực hiện được trực tiếp qua HTTP. Tuy nhiên, toàn bộ markup, Tailwind token classes, a11y attributes và cấu trúc DOM đã được rà soát đối chiếu từng dòng theo design spec.
- Không phát sinh key i18n mới nên không cần sửa `en.json` và `vi.json`.
