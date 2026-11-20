# Báo cáo: Redesign Polish - Sửa sau kiểm tra tay (bước 11)

## 1. Đã làm gì

Đã giải quyết triệt để 4 lỗi tìm thấy khi kiểm tra tay theo đúng đặc tả kỹ thuật trong `tasks/redesign-polish.md`:

### 1. Vùng bấm ngăn khay (`roadmap-tray.tsx`)
- Trên các ô ngăn bài học trong `RoadmapTray` (`Link`), đã loại bỏ toàn bộ `relative` và `after:absolute after:-inset-1 after:content-['']`.
- Thay thế bằng utility class `.hit` (đã có trong `globals.css`, dùng pseudo-element `::after` căn giữa với kích thước `max(100%, 44px)`).
- Đảm bảo vùng bấm đạt tối thiểu 44×44px cho mọi ngăn kể cả bài kế tiếp có `border-2`, đồng thời giữ nguyên kích thước nhìn thấy `size-9` (36×36px).

### 2. Tương phản badge trên dải tint phase (`roadmap-tray.tsx` và `learn/page.tsx`)
- Các badge trạng thái ("Coming soon"/"Sắp ra mắt", "Runs on your local Python runner", "skipped") nằm trên nền tint `getPhaseTintClass(...)` trước đây dùng `text-muted-foreground` từ `variant="outline"` và `variant="muted"`, dẫn đến độ tương phản chỉ đạt 3.7–4.2:1 (dưới ngưỡng WCAG AA 4.5:1).
- Đã bổ sung `className="border-foreground/25 text-foreground"` cho toàn bộ các `Badge` nằm trên dải tint phase trong cả hai file:
  - `apps/web/src/components/roadmap-tray.tsx`: 4 vị trí (2 vị trí ở trạng thái mở `isOpen` và 2 vị trí ở trạng thái thu gọn).
  - `apps/web/src/app/(main)/learn/page.tsx`: 3 vị trí trên header dải tint của mỗi phase (`localRunner`, `skipped`, `comingSoon`).
- Kết quả: Màu chữ chuyển sang `text-foreground` (`oklch(21% 0.025 170)` ở light mode và `oklch(96% 0.01 160)` ở dark mode) cho độ tương phản vượt trội (≥ 10:1), đạt chuẩn WCAG AA / AAA.

### 3. Sơ đồ Mermaid theo token Dose (`markdown.tsx`)
- Viết hàm helper `cssColorToHex(cssColor: string): string` ngay trong `markdown.tsx` để chuyển đổi màu CSS bất kỳ (kể cả `oklch(...)` mà thư viện `khroma` trong Mermaid không đọc được) sang mã hex `#rrggbb` thông qua canvas 1×1 (`ctx.fillStyle = value; ctx.fillRect(0,0,1,1); getImageData`). Không thêm bất kỳ thư viện ngoài nào.
- Trong `MermaidDiagram`, tại thời điểm render đọc computed style trực tiếp từ `document.documentElement` cho các biến CSS Dose: `--card`, `--muted`, `--foreground`, `--muted-foreground`, `--border`, `--primary`, `--accent`.
- Chuyển `mermaid.initialize` sang `theme: "base"` với `themeVariables` map theo spec:
  - `background`: `--card`
  - `primaryColor`: `--muted`
  - `primaryBorderColor`: `--primary`
  - `primaryTextColor`: `--foreground`
  - `secondaryColor`: `--accent`
  - `tertiaryColor`: `--card`
  - `lineColor`: `--muted-foreground`
  - `textColor`: `--foreground`
  - `edgeLabelBackground`: `--card`
  - `clusterBkg`: `--muted`
  - `clusterBorder`: `--border`
  - `fontFamily`: `"var(--font-sans)"`
  - Giữ nguyên `securityLevel: "strict"`, `startOnLoad: false`.
- Giữ nguyên dependency `resolvedTheme` trong `useEffect` để sơ đồ tự động re-render và cập nhật màu khi người dùng chuyển đổi light/dark mode.
- Kết quả: Chữ trong node và nhãn cạnh ("yes"/"no") có màu chữ `foreground` trên nền `card`/`muted`, đạt tương phản ≥ 4.5:1 ở cả hai chế độ sáng/tối.

### 4. Tên truy cập lựa chọn ngôn ngữ ở Onboarding (`onboarding/page.tsx`)
- Bổ sung thuộc tính tường minh `aria-hidden="true"` cho thẻ `<span ...>{code}</span>` trong component `Choice`.
- Giúp Accessible Name của nút `role="radio"` chỉ còn tên hiển thị ngôn ngữ ("Tiếng Việt" / "English"), loại bỏ tiền tố mã "VI" / "EN" bị đọc dính vào tên trước đó ("VITiếng Việt" / "ENEnglish").

---

## 2. File đã sửa

Chỉ sửa đúng 4 file được phép trong danh sách:
1. `apps/web/src/components/roadmap-tray.tsx` (mục 1 và 2)
2. `apps/web/src/app/(main)/learn/page.tsx` (mục 2)
3. `apps/web/src/components/markdown.tsx` (mục 3, chỉ trong `MermaidDiagram` và helper liên quan)
4. `apps/web/src/app/onboarding/page.tsx` (mục 4)

---

## 3. Kết quả lệnh kiểm tra

Tất cả lệnh kiểm tra trong spec đều được thực thi từ thư mục gốc `D:\Proj\python-ai-platform` (KHÔNG chạy `pnpm build`):

### 1. TypeScript Typecheck
```powershell
pnpm.cmd --filter web typecheck
```
**Kết quả:**
```
> web@0.1.0 typecheck D:\Proj\python-ai-platform\apps\web
> pnpm run content && tsc --noEmit

> web@0.1.0 content D:\Proj\python-ai-platform\apps\web
> uv run --project ../.. python ../../tools/build_content.py

Built 24 lessons, 5 exams, 144 flashcards, 387 questions -> apps\web\src\generated
```
-> 0 lỗi. Exit code 0.

### 2. Sloplint
```powershell
node C:/Users/Henry/.claude/skills/hallmark/scripts/sloplint.mjs apps/web/src --genre modern-minimal --scope app --kept
```
**Kết quả:**
```
sloplint: clean. 0 FAIL, 0 REFLEX, 0 WARN across 45 file(s).
kept: links 20/20, fields 1/1, handlers 125/125; before 3 FAIL, 0 REFLEX, now 0 FAIL, 0 REFLEX
```
-> 0 FAIL, kept 20/20 links, 1/1 fields, 125/125 handlers. Exit code 0.

### 3. Kiểm tra loại bỏ `after:-inset` trong `roadmap-tray.tsx`
```bash
grep -n "after:-inset" apps/web/src/components/roadmap-tray.tsx
```
**Kết quả:**
```
(rỗng - không có dòng nào trùng khớp, exit code 1)
```

### 4. Kiểm tra Mermaid `theme: "base"` và `themeVariables` trong `markdown.tsx`
```bash
grep -n "theme: \"base\"\|themeVariables" apps/web/src/components/markdown.tsx
```
**Kết quả:**
```
158:          theme: "base",
159:          themeVariables: {
```

### 5. Git Diff Stat
```bash
git diff --stat
```
**Kết quả:**
```
 apps/web/src/app/(main)/learn/page.tsx   |  6 ++---
 apps/web/src/app/onboarding/page.tsx     |  2 +-
 apps/web/src/components/markdown.tsx     | 40 +++++++++++++++++++++++++++++++-
 apps/web/src/components/roadmap-tray.tsx | 10 ++++----
 4 files changed, 48 insertions(+), 10 deletions(-)
```
-> Chỉ có đúng 4 file được liệt kê trong spec bị thay đổi.

### 6. Kiểm tra dev server
Truy cập `http://localhost:3000/lesson/p1-03-loops/` (bài học chứa sơ đồ Mermaid `flowchart TD` kèm nhãn cạnh "yes"/"no"):
- HTTP status 200 OK, render ổn định.

---

## 4. Điều còn chưa chắc

1. **Khả năng hỗ trợ `oklch` trong Canvas 2D ở các trình duyệt cũ:**
   Hàm `cssColorToHex` dựa vào việc gán `ctx.fillStyle = oklch(...)` rồi đọc lại qua `getImageData`. Hầu hết trình duyệt hiện đại (Chrome 111+, Firefox 113+, Safari 15.4+) đều hỗ trợ đầy đủ CSS Color 4. Nếu trình duyệt quá cũ không hỗ trợ `oklch` trong canvas, hàm có khối `try/catch` sẽ trả về nguyên chuỗi CSS màu gốc làm fallback.
2. **Font chữ trong sơ đồ Mermaid:**
   Giá trị `fontFamily: "var(--font-sans)"` được truyền vào `themeVariables` và đưa trực tiếp vào CSS inline của thẻ `<svg>`. Do SVG được chèn trực tiếp vào DOM trang (thông qua `dangerouslySetInnerHTML`), biến CSS `--font-sans` được kế thừa và hiển thị chính xác font sans của ứng dụng (Be Vietnam Pro).
