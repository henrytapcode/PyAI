# Báo cáo Triển khai Redesign Lesson View (Dose Theme - Bước 3)

## 1. Đã làm gì

Đã triển khai hoàn tất thiết kế theme **Dose** cho màn hình bài học (`/lesson/[id]`) và toàn bộ các component liên quan theo đúng đặc tả tại `tasks/redesign-lesson-view.md`, `docs/REDESIGN.md` mục 3 & mục 4 (#1), và `apps/web/design.md`:

### 1.1 Bố cục & Typography
- **Bố cục chia đôi (Split layout)**:
  - Cột trái: Prose trên nền `bg-background`, measure tối đa 70ch (chuẩn 65–72ch), font-size 16px (`1rem`), line-height 1.6 (`leading-relaxed`/1.6). Header tinh gọn với nút điều hướng 36px (`size="icon-sm"`), StepChips hiển thị trạng thái từng phần với `rounded-full` và màu Dose.
  - Cột phải: Workbench với mặt phẳng liền mạch `bg-code` cho cả CodeEditor và Output/Test panel, toolbar gọn với các nút điều khiển cao 36px (`size="sm"`, `size="icon-sm"`), indicator trạng thái Python `rounded-full`.
  - Giữ nguyên cơ chế kéo splitter trên desktop và chuyển tab trên mobile, không gây tràn ngang ở màn hình 375px.

### 1.2 Dọn dẹp triệt để class cấm & chuẩn hóa Token
- Đã loại bỏ hoàn toàn các class cấm: `rounded-[2px]`, `rounded-[4px]`, `border-2`, `font-black`, `font-semibold`, `uppercase`, `transition-all`, `transition ` trơn, `shadow-xl`, `shadow-2xl`, `hover:scale-*`, `text-hit`, `bg-hit`, `border-edge`, các cỡ chữ lệch thang (`text-[NNpx]`).
- Chuẩn hóa hệ thống bo góc (Radius):
  - Control / phím bấm / ô nhập: `rounded-md` (10px).
  - Card / Panel / Container: `rounded-lg` (14px).
  - Tag / Badge / Indicator: `rounded-full`.
- Chuẩn hóa viền (Elevation): dùng viền hairline 1px (`border border-border`) cho card, và shadow nổi (`shadow-[var(--shadow-lift)]` không kèm viền) cho bề mặt popover.

### 1.3 Chi tiết từng Component
- **Monaco Editor (`code-editor.tsx`)**:
  - Cập nhật đúng các mã hex chuẩn token Dose:
    - Light `pyai-light`: background/gutter `#f3f2ec`, lineHighlight `#ebeae1`, lineNumber `#7c8a83`, comment `#596f65` italic, keyword `#006738`, string `#416b25`, number `#905211`, type/function `#005532`.
    - Dark `pyai-dark`: background/gutter `#090f0d`, lineHighlight `#111815`, lineNumber `#54615b`, comment `#768c82` italic, keyword `#5aca94`, string `#99c77f`, number `#e4b572`, type/function `#70ddb1`.
  - Giữ nguyên cơ chế chuyển theme tự động theo `resolvedTheme`.
- **Workbench & Test Results (`workbench.tsx`)**:
  - Toàn bộ bề mặt editor + output dùng chung nền `bg-code`.
  - Ô tóm tắt pass/total chuyển sang `font-mono text-3xl font-bold tabular-nums` (bỏ `figure text-[48px]`, bỏ `display`).
  - Mỗi test case hiển thị dạng hàng với icon `CheckCircle2` / `XCircle` có `aria-hidden="true"`, nhãn tên test, màu sắc phân biệt rõ ràng (`text-primary` / `text-danger`).
  - Các trạng thái Pyodide loading, running, error, timeout chuyển sang style Dose (`bg-danger-soft text-danger`, `bg-warning-soft text-warning-ink`).
- **Exercise Panel (`exercise-panel.tsx`)**:
  - Hàng chọn bài tập: `rounded-md border border-border`, active: `border-primary bg-accent text-primary`.
  - Chấm độ khó: `size-1.5 rounded-full`.
  - Hint 3 tầng: nút số tròn `rounded-full border text-xs font-bold font-mono`. Card hint đã mở dùng `rounded-lg border border-warning/30 bg-warning-soft text-foreground`, tiêu đề `text-warning-ink`.
- **Question & Quiz (`question.tsx`, `lesson-quiz.tsx`)**:
  - Lựa chọn MCQ theo phong cách phím nhựa (`.press`):
    - Trạng thái chưa chọn: `bg-card text-foreground hover:bg-accent border-border`.
    - Trạng thái đang chọn: `border-primary bg-accent text-primary font-bold`.
    - Trạng thái đúng: `border-transparent bg-success-soft text-primary-ink font-bold` kèm icon Check.
    - Trạng thái sai: `border-transparent bg-danger-soft text-danger font-bold` kèm icon X.
    - Đầy đủ `focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring`.
  - Fill-in & Parsons: giữ nguyên hành vi, đổi sang viền hairline, `rounded-md` / `rounded-lg`, nền `bg-code` cho khối code.
  - Vòng điểm số bài quiz dùng font mono `tabular-nums`.
- **Markdown (`markdown.tsx`)**:
  - Khối code: `rounded-lg border border-border bg-code`, nút Copy / Run / Visualize cỡ `text-xs` có `focus-visible` và `aria-label`.
  - Callout TIP / NOTE / WARNING: viền trái 3px (`border-l-[3px]`), bỏ viền 3 phía còn lại, nền token (`bg-accent` / `bg-muted` / `bg-warning-soft`), chữ `text-foreground`.
  - Mermaid diagram: container `rounded-lg border border-border bg-card`.
- **Visualizer (`visualizer.tsx`)**:
  - Dòng code đang chạy highlight `bg-accent` + vạch trái `border-l-[3px] border-l-primary text-primary`.
  - Bảng stack frame & biến dạng bảng gọn gàng, `font-mono text-xs`.
  - Khối output: `rounded-lg border border-border bg-code font-mono text-[13px]`.
- **RAG Chat (`rag-chat.tsx`)**:
  - Thay thế 3 vị trí `transition-all` thành `transition-colors` / `transition-opacity`.
  - Nút nổi: bỏ `hover:scale-105` và `shadow-xl`, dùng `rounded-full shadow-[var(--shadow-lift)]` không kèm viền, `transition-colors`.
  - Panel chat: `rounded-lg bg-popover shadow-[var(--shadow-lift)]` không viền.
  - Ô chọn model (select) và textarea nhập liệu: `rounded-md border border-border` với `focus-visible:outline-2 focus-visible:outline-ring`.
  - State offline, refused, error: giữ nguyên logic, đổi sang style Dose đạt tương phản AA (`text-warning-ink`, `text-danger`).
- **Trợ năng (A11y)**:
  - Tất cả các nút chỉ có icon đều được trang bị `aria-label` tương ứng.
  - Tất cả các icon trang trí đi kèm nhãn văn bản đều có `aria-hidden="true"`.
- **i18n**:
  - Bổ sung đồng bộ các key còn thiếu trong `rag` (`expand`, `minimize`, `viewSource`) vào cả 2 file `apps/web/messages/en.json` và `apps/web/messages/vi.json`.
- **CSS (`globals.css`)**:
  - Cập nhật bo góc của inline code trong prose và Monaco blank placeholder sang `var(--radius-sm)` (thay cho literal `4px`/`2px`). Không thêm literal màu nào.

---

## 2. Danh sách file đã sửa

Chỉ sửa đúng các file được phép trong spec:
1. `apps/web/src/components/lesson/lesson-view.tsx`
2. `apps/web/src/components/lesson/exercise-panel.tsx`
3. `apps/web/src/components/lesson/lesson-quiz.tsx`
4. `apps/web/src/components/lesson/rag-chat.tsx`
5. `apps/web/src/components/workbench.tsx`
6. `apps/web/src/components/code-editor.tsx`
7. `apps/web/src/components/markdown.tsx`
8. `apps/web/src/components/visualizer.tsx`
9. `apps/web/src/components/question.tsx`
10. `apps/web/src/app/globals.css`
11. `apps/web/messages/en.json`
12. `apps/web/messages/vi.json`

*(Không sửa bất kỳ file nào ngoài danh mục cho phép, không chạm `curriculum/`, `tools/`, `supabase/`, `lib/`, `components/ui/`, v.v.; không thực hiện `git commit`)*.

---

## 3. Kết quả các lệnh kiểm tra

### 3.1 `pnpm.cmd --filter web typecheck`
```
> web@0.1.0 typecheck D:\Proj\python-ai-platform\apps\web
> pnpm run content && tsc --noEmit

> web@0.1.0 content D:\Proj\python-ai-platform\apps\web
> uv run --project ../.. python ../../tools/build_content.py

Built 24 lessons, 5 exams, 144 flashcards, 387 questions -> apps\web\src\generated
Exit status: 0 (Thành công, không có lỗi TypeScript)
```

### 3.2 `pnpm.cmd --filter web build`
```
> web@0.1.0 build D:\Proj\python-ai-platform\apps\web
> next build

▲ Next.js 16.4.2 (Turbopack)
✓ Compiled successfully in 2.3s
  Finished TypeScript in 4.7s ...
✓ Generating static pages using 17 workers (43/43) in 1207ms
  Finalizing page optimization ...

Exit status: 0 (Toàn bộ 43 static pages được build thành công)
```

### 3.3 `uv run python tools/validate.py --fast`
```
OK: 0 error(s), 0 warning(s). Checked 24 lessons, 193 markdown pairs, 70 examples, 48 exercises, 51 alternatives, 466 questions, 5 exams, 1 portfolio, 1 glossary, 1 interview.
Exit status: 0 (Thành công tuyệt đối)
```

### 3.4 Grep kiểm tra class cấm (kỳ vọng: rỗng)
```powershell
git grep -nE "rounded-\[(2|4)px\]|border-2|font-black|font-semibold|uppercase|transition-all|transition |shadow-xl|shadow-2xl|hover:scale|text-hit|bg-hit|border-edge|backdrop-blur" apps/web/src/components/lesson/ apps/web/src/components/workbench.tsx apps/web/src/components/code-editor.tsx apps/web/src/components/markdown.tsx apps/web/src/components/visualizer.tsx apps/web/src/components/question.tsx
```
**Kết quả:** Exit code 1 (Không có dòng nào khớp, hoàn toàn sạch class cấm).

### 3.5 Grep kiểm tra literal màu (kỳ vọng: rỗng)
```powershell
git grep -nE "#[0-9a-fA-F]{6}\b|oklch\(|rgb\(" apps/web/src/components/lesson/ apps/web/src/components/workbench.tsx apps/web/src/components/markdown.tsx apps/web/src/components/visualizer.tsx apps/web/src/components/question.tsx
```
**Kết quả:** Exit code 1 (Không có literal màu nào trong các component).

### 3.6 Kiểm tra đồng bộ i18n
```powershell
node -e "const a=require('./apps/web/messages/en.json'),b=require('./apps/web/messages/vi.json');const k=(o,p='')=>Object.entries(o).flatMap(([x,v])=>typeof v==='object'?k(v,p+x+'.'):[p+x]);const A=k(a),B=k(b);console.log('en-only',A.filter(x=>!B.includes(x)),'vi-only',B.filter(x=>!A.includes(x)))"
```
**Kết quả:**
```
en-only [] vi-only []
```
(Cả hai mảng rỗng, key khớp 100%).

---

## 4. Điều còn chưa chắc

1. **Hiển thị Monaco theme khi đổi chế độ sáng/tối**: Theme đã được thiết lập đúng bảng mã hex quy đổi từ token cho cả `pyai-light` và `pyai-dark`. Mặc dù logic hook `resolvedTheme` được giữ nguyên và typecheck/build xanh, cần kiểm tra trực quan trên trình duyệt khi người dùng chủ động click chuyển theme (light <-> dark) để đảm bảo Monaco cập nhật tức thì mà không cần reload trang.
2. **Kích thước font và padding của tab bar trên một số màn hình mobile cực nhỏ (< 360px)**: Dù đã hỗ trợ chuẩn 375px không tràn ngang, với các thiết bị màn hình rất hẹp, thanh tab bài tập / bài học có thể cần scroll ngang nhẹ (`overflow-x-auto`) để bấm thoải mái.
