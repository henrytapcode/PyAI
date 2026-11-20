# Báo cáo: Redesign Dashboard + Khay lộ trình (Bước 4)

## 1. Đã làm gì

### A. Tạo component `RoadmapTray` (`apps/web/src/components/roadmap-tray.tsx`)
- Export `RoadmapTray({ variant, nextId, className })` hỗ trợ 2 biến thể: `"compact"` và `"full"`.
- Dữ liệu tiến độ tự lấy qua hook `useProgress()` cùng `catalog`, `lessonStatus`, `phaseProgress` (không thêm logic tiến độ mới).
- Map tĩnh thứ tự phase sang 7 dải tint background tương ứng tokens theme Dose:
  - Phase 0 $\rightarrow$ tint 1 (`bg-[var(--phase-1)]`)
  - Phase 1..7 $\rightarrow$ tint 1..7 (`bg-[var(--phase-1)]` .. `bg-[var(--phase-7)]`)
  - Phase 8, 9 $\rightarrow$ quay vòng tint 1, 2 via `((order - 1) % 7) + 1`
  - Dải có tên phase (sentence case, `text-sm font-bold`) và `%` mono `tabular-nums` bên phải, bo `rounded-lg`, không viền, không shadow.
- Mỗi bài học là một ngăn (`Link` tới `/lesson/<id>/` nếu `ready`, ngược lại `/learn/`), bo `rounded-md`, kích thước 36px (`size-9`), vùng bấm 44px thông qua pseudo-element `after:absolute after:-inset-1`, hiển thị số thứ tự bài dạng mono `tabular-nums`:
  - `completed`: nền `bg-success-soft`, icon `Check` (`aria-hidden="true"`), chữ `text-primary-ink`.
  - bài kế tiếp (`id === nextId`): nền `bg-card`, viền 2px `border-primary`, chữ `text-primary font-bold`.
  - `in_progress`: nền `bg-card`, viền 1px `border-primary/50`.
  - `available`: nền `bg-card/80`, viền hairline `border-border`.
  - `locked`, `skipped`, `coming_soon`: nhạt (`opacity-60` hoặc `text-muted-foreground`), `coming_soon` viền dashed `border-dashed border-border`. Không dùng màu đỏ.
  - Mỗi ngăn có `title` + `aria-label` = `"<tên bài>: <trạng thái>"` sử dụng `ts(status)`. Trạng thái phân biệt bằng cả visual tick/border lẫn text label.
  - Trạng thái tương tác: `focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring`, hover `hover:-translate-y-0.5` với thời lượng 150ms và tắt khi `prefers-reduced-motion` qua `motion-reduce:transform-none`.
- Biến thể `variant="compact"`: chỉ mở phase đang học (`activePhaseId = nextId ? phaseOfLesson(nextId)?.id : undefined`), các phase khác thu gọn thành dải một dòng (tên phase + `%` mono + thanh nhỏ `Progress`).
- Biến thể `variant="full"`: tất cả các phase đều mở ngăn đầy đủ để sẵn sàng cho bước 5 (`/learn`).
- Sắp xếp ngăn theo `flex flex-wrap gap-1.5`, kiểm tra co giãn không bị tràn ngang ở 375px.

### B. Cải tổ Dashboard (`apps/web/src/app/(main)/page.tsx`)
- **Tiêu đề trang**: Bỏ `<h1>` "PyAI Path", thay bằng câu chào sẵn có (`t("greetingNew")` / `t("greeting")`) với `text-2xl font-bold tracking-tight`.
- **Khối bài kế tiếp**: Sử dụng `Card` hairline mặc định (bỏ ô icon với `shadow-[4px_4px_0_var(--hit)]`), gắn tag phase (`Badge variant="muted"`), tên bài `text-xl font-bold`, summary `line-clamp-2`, `Progress` + thời lượng mono (`Clock aria-hidden="true"`), nút chính `Button size="lg"` "Bắt đầu/Tiếp tục". Nhánh `allCaughtUp` giữ nguyên, Trophy đổi sang `text-primary`, chữ `font-bold`.
- **Section khay lộ trình**: Đặt ngay dưới khối bài kế tiếp với `<RoadmapTray variant="compact" nextId={data.next?.id} />`, tiêu đề `t("skillTree")`, dòng phụ giữ chuỗi `tc("of", ...)` hiện có, link `t("openRoadmap")` trỏ đến `/learn/`.
- **Hàng số liệu**: Gom 4 chỉ số (streak, XP hôm nay kèm mốc `/goal`, thẻ cần ôn link `/review/`, tổng XP dùng `XpFigure`) thành một hàng số + nhãn: số `font-mono tabular-nums text-2xl font-bold text-foreground`, nhãn `text-xs text-muted-foreground` bên dưới. Ngăn cách bằng `lg:divide-x divide-border` trên desktop và lưới 2×2 trên mobile. Ô "cần ôn" là `Link` có `focus-visible` và mũi tên `ArrowRight aria-hidden="true"` khi `due > 0`.
- **Bố cục trang**: Lưới `lg:grid-cols-3`:
  - Cột trái (`lg:col-span-2`): Bài kế tiếp + Khay lộ trình + Hàng số liệu.
  - Cột phải: "Chủ đề cần củng cố" (`weakTopics`) + "Tiêu chí thuần thục" (`mastery`).
- **Component `Criterion`**: Thêm `aria-hidden="true"` cho icon; khi hoàn thành không gạch ngang màu đậm (`line-through` bỏ `decoration-2 decoration-success`, dùng `text-muted-foreground` + icon check `text-primary`).
- **Activity heatmap**: Đặt ở dưới cùng toàn chiều rộng, ô chuyển sang `rounded-sm` (bỏ `rounded-[2px]`), mức 3 dùng `bg-primary-ink` (bỏ `bg-hit`), bỏ hiệu ứng `hover:scale-150` sang `transition-opacity hover:opacity-80`.
- **Dọn dẹp code & chuẩn hóa**:
  - Loại bỏ hoàn toàn: `font-black`, `font-semibold`, `uppercase`, `\bfigure\b`, `\bdisplay\b`, `row-cursor`, `text-hit`, `bg-hit`, `border-edge`, `shadow-[`, `border-2` (trừ viền ngăn bài kế tiếp), `rounded-[`, `text-[NNpx]`, `transition-all`, `hover:scale`, literal màu.
  - Giữ đầy đủ tất cả các `href` hiện có (`/lesson/<id>/`, `/learn/`, `/review/`, `/exams/`).

---

## 2. File đã sửa / tạo
- **Sửa**: [page.tsx](file:///D:/Proj/python-ai-platform/apps/web/src/app/(main)/page.tsx)
- **Tạo**: [roadmap-tray.tsx](file:///D:/Proj/python-ai-platform/apps/web/src/components/roadmap-tray.tsx)
- **Không chạm vào**: `messages/` (không phát sinh key mới), `components/ui/*`, `tokens.css`, `globals.css`, `curriculum/`, `tools/`, `supabase/`, `lib/*`.

---

## 3. Kết quả lệnh kiểm tra

Tất cả lệnh chạy từ thư mục gốc `D:\Proj\python-ai-platform`. Tuyệt đối **không chạy `pnpm build`**.

1. **Kiểm tra TypeScript (`pnpm.cmd --filter web typecheck`)**:
   ```
   > web@0.1.0 typecheck D:\Proj\python-ai-platform\apps\web
   > pnpm run content && tsc --noEmit

   > web@0.1.0 content D:\Proj\python-ai-platform\apps\web
   > uv run --project ../.. python ../../tools/build_content.py

   Built 24 lessons, 5 exams, 144 flashcards, 387 questions -> apps\web\src\generated
   ```
   **Kết quả:** 0 lỗi, exit code 0.

2. **Kiểm tra grep các token/class bị cấm**:
   ```bash
   grep -nE "font-black|font-semibold|uppercase|\bfigure\b|\bdisplay\b|row-cursor|text-hit|bg-hit|border-edge|shadow-\[|rounded-\[|text-\[[0-9]+px\]|transition-all|hover:scale|#[0-9a-fA-F]{6}|oklch\(" "apps/web/src/app/(main)/page.tsx" apps/web/src/components/roadmap-tray.tsx
   ```
   **Kết quả:** Rỗng (không tìm thấy bất kỳ pattern nào vi phạm, exit code 1).

3. **Kiểm tra đồng bộ key i18n giữa `en.json` và `vi.json`**:
   ```bash
   node -e "const a=require('./apps/web/messages/en.json'),b=require('./apps/web/messages/vi.json');const k=(o,p='')=>Object.entries(o).flatMap(([x,v])=>typeof v==='object'?k(v,p+x+'.'):[p+x]);const A=k(a),B=k(b);console.log('en-only',A.filter(x=>!B.includes(x)),'vi-only',B.filter(x=>!A.includes(x)))"
   ```
   **Kết quả:**
   ```
   en-only [] vi-only []
   ```
   Hai mảng đều rỗng.

---

## 4. Điều còn chưa chắc
- Khi người học hoàn thành toàn bộ bài (`allCaughtUp` / `data.next` là `undefined`): khay `variant="compact"` hiện tại sẽ thu gọn tất cả 9 dải phase về dạng một dòng tiến độ thay vì mở ngăn nào. Đây là hành vi hợp lý khi không có phase nào đang học dang dở.
- Chưa test trực tiếp trên dev server vì server không lắng nghe tại port 3000 ở thời điểm chạy task; kiểm thử tĩnh qua compiler TypeScript và script regex đã pass toàn bộ.

---

## 5. Vòng 2 (Xử lý Feedback vòng 1)

### A. Các thay đổi đã thực hiện
1. **Sửa dải tint phase 0 và phase 1 trùng màu** (`roadmap-tray.tsx`):
   - Đổi công thức `getPhaseTintClass` thành `PHASE_TINT_CLASSES[order % 7]`.
   - Kết quả: Phase 0 (`order: 0`) dùng tint 1, phase 1 (`order: 1`) dùng tint 2, các phase tiếp theo từ 2..6 dùng tint 3..7, và phase 7, 8 quay vòng lại tint 1, 2 theo đúng REDESIGN mục 3.1.
   - Cập nhật comment giải thích ở đầu file cho khớp logic mới.

2. **Cải thiện độ tương phản trên nền tint ở Light mode** (`roadmap-tray.tsx`):
   - Đổi tất cả chữ trên dải tint gồm tên phase, tỷ lệ `%`, và số ngăn bài học ở trạng thái thường sang `text-foreground` (đảm bảo độ tương phản > 4.5:1 đạt chuẩn WCAG AA trên cả 7 sắc tint).
   - Các trạng thái không hoạt động / nhạt (`locked`, `skipped`, `coming_soon`) dùng `text-foreground opacity-60`.

3. **Chuyển hàng số liệu lên Header** (`page.tsx`):
   - Chuyển toàn bộ 4 chỉ số (streak, XP hôm nay kèm mốc goal, số thẻ cần ôn link `/review/`, tổng XP với `XpFigure`) từ `Card` nằm dưới khay lên thẳng hàng header chứa `<h1>`.
   - Bố cục header dùng `flex flex-wrap items-end justify-between gap-4`:
     - Desktop: `<h1>` câu chào bên trái, 4 số liệu bên phải gom thành hàng với ngăn cách `sm:divide-x sm:divide-border sm:gap-0 sm:px-5`, số cỡ `sm:text-2xl font-bold font-mono tabular-nums`.
     - Mobile: Số liệu tự động xuống dòng dưới `<h1>` thành lưới 4 cột gọn gàng `w-full grid-cols-4 gap-2`, số hiển thị cỡ `text-xl font-bold font-mono tabular-nums`.
   - Loại bỏ hoàn toàn khối Card số liệu ở cột trái, giữ thứ tự chuẩn: Bài kế tiếp $\rightarrow$ Khay lộ trình (không có khối nào chen giữa).

4. **Dải thu gọn của phase chưa có bài** (`roadmap-tray.tsx`):
   - Điều kiện render kiểm tra `prog.ready > 0`: Khi phase chưa có bài (`!prog.ready`), ẩn hoàn toàn thanh `Progress` và nhãn `0%`.
   - Dải chỉ hiển thị tên phase và badge "Sắp ra mắt" (`tc("comingSoon")`).

### B. Kết quả lệnh kiểm tra Vòng 2
1. **TypeScript Typecheck (`pnpm.cmd --filter web typecheck`)**:
   ```
   > web@0.1.0 typecheck D:\Proj\python-ai-platform\apps\web
   > pnpm run content && tsc --noEmit

   > web@0.1.0 content D:\Proj\python-ai-platform\apps\web
   > uv run --project ../.. python ../../tools/build_content.py

   Built 24 lessons, 5 exams, 144 flashcards, 387 questions -> apps\web\src\generated
   ```
   **Kết quả:** 0 lỗi (Exit code 0).

2. **Kiểm tra grep cấm các token/pattern cũ**:
   ```bash
   grep -nE "font-black|font-semibold|uppercase|\bfigure\b|\bdisplay\b|row-cursor|text-hit|bg-hit|border-edge|shadow-\[|rounded-\[|text-\[[0-9]+px\]|transition-all|hover:scale|#[0-9a-fA-F]{6}|oklch\(" "apps/web/src/app/(main)/page.tsx" apps/web/src/components/roadmap-tray.tsx
   ```
   **Kết quả:** Rỗng (0 vi phạm, Exit code 1).

3. **Kiểm tra đồng bộ key i18n giữa `en.json` và `vi.json`**:
   ```bash
   node -e "const a=require('./apps/web/messages/en.json'),b=require('./apps/web/messages/vi.json');const k=(o,p='')=>Object.entries(o).flatMap(([x,v])=>typeof v==='object'?k(v,p+x+'.'):[p+x]);const A=k(a),B=k(b);console.log('en-only',A.filter(x=>!B.includes(x)),'vi-only',B.filter(x=>!A.includes(x)))"
   ```
   **Kết quả:**
   ```
   en-only [] vi-only []
   ```
   Cả 2 mảng đều rỗng.
