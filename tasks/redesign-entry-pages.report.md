# Báo cáo: Redesign Onboarding, Placement, Login (Dose theme)

## 1. Đã làm gì

Đã triển khai đúng và đầy đủ theo đặc tả trong `tasks/redesign-entry-pages.md`:

### Onboarding (`apps/web/src/app/onboarding/page.tsx`)
- Khung bước: Sử dụng `rounded-lg border border-border bg-card p-6 sm:p-8` (không shadow).
- Thanh tiến độ: 3 đoạn `h-1.5 flex-1 rounded-full`, đoạn đã qua `bg-primary`, chưa qua `bg-muted`.
- Container lựa chọn: Bổ sung `role="radiogroup"` kèm `aria-label` lấy từ tiêu đề bước đã dịch (`chooseLanguage`, `chooseTrack`, `goal`).
- Lựa chọn "phím nhựa" (`Choice`):
  - Chuyển thành `type="button"`, `role="radio"`, `aria-checked={active}`.
  - Áp dụng class `.press` (mép dưới 3px, ấn lún) với `rounded-lg border p-4 text-left outline-none focus-visible:outline-2 outline-ring focus-visible:outline-ring`.
  - Mặc định: `bg-card text-foreground`.
  - Khi được chọn (mint): `border-primary bg-success-soft text-foreground [--press-edge:var(--primary-ink)]`.
  - Ô check: `size-5 rounded-md border`, khi chọn `border-primary bg-primary text-primary-foreground` + icon `Check aria-hidden`.
  - Không có `transition` trơn (`.press` đã tích hợp sẵn cơ chế transition).
- Ô code ngôn ngữ (VI/EN) và ô icon: `size-9 rounded-md bg-muted font-mono text-sm font-bold text-primary`, icon có `aria-hidden`.
- Gỡ bỏ toàn bộ `rounded-[4px]`, `rounded-[2px]`, `transition`, `transition-colors`.

### Placement (`apps/web/src/components/placement-view.tsx`)
- Card giới thiệu/kết quả: `Card` mặc định + `bg-accent` (gỡ bỏ `border-primary/30 bg-accent/40`).
- Icon: Bổ sung `aria-hidden` cho các icon trang trí `Compass`, `Rocket`, `ArrowRight`.
- Tiêu đề: Đảm bảo `text-2xl font-bold tracking-tight`, sentence case.

### Login (`apps/web/src/app/login/page.tsx`)
- Input: Chuyển sang `h-10 w-full rounded-md border border-border bg-card px-3 text-sm outline-none focus-visible:outline-2 focus-visible:outline-ring` (bỏ `ring-ring/50` và `rounded-[4px]`). Mỗi input có `<label>` hiển thị và thuộc tính `aria-label` đã dịch.
- Khung form và khung `notConfigured`: `rounded-lg border border-border bg-card`.
- Thông báo: Với lỗi hiển thị `rounded-md bg-danger-soft text-danger px-3 py-2 text-sm role="alert"` (thành công hiển thị `bg-success-soft text-foreground`).
- Nút Google: Giữ nguyên `Button variant="outline"` cùng logo Google 4 màu thương hiệu (`fill="#4285F4"`, `#34A853`, `#FBBC05`, `#EA4335`) và `aria-hidden`. Icon `Mail` có `aria-hidden`.

---

## 2. File đã sửa

Chỉ sửa đúng 3 file nằm trong danh sách cho phép:
1. `apps/web/src/app/onboarding/page.tsx`
2. `apps/web/src/app/login/page.tsx`
3. `apps/web/src/components/placement-view.tsx`

*(Không chỉnh sửa `en.json` và `vi.json` vì tất cả key i18n cần thiết đã có sẵn và khớp 100%).*

---

## 3. Kết quả lệnh kiểm tra

Tất cả các lệnh kiểm tra quy định trong spec đều đạt kết quả mong đợi (chạy từ gốc repo):

1. **Typecheck:**
   ```powershell
   pnpm.cmd --filter web typecheck
   ```
   **Kết quả:** 0 lỗi, TypeScript pass hoàn toàn.

2. **Kiểm tra forbidden token/class:**
   ```bash
   grep -nE "rounded-\[|border-2|font-black|font-semibold|uppercase|transition[ \"]|transition-all|text-hit|bg-hit|border-edge|shadow-\[|text-\[[0-9]+px\]|backdrop-blur|blur-|row-cursor|oklch\(" apps/web/src/app/onboarding/page.tsx apps/web/src/app/login/page.tsx apps/web/src/components/placement-view.tsx
   ```
   **Kết quả:** Rỗng (exit code 1, không tìm thấy bất kỳ chuỗi cấm nào).

3. **Đếm literal hex:**
   ```bash
   grep -cE "#[0-9a-fA-F]{6}" apps/web/src/app/login/page.tsx apps/web/src/app/onboarding/page.tsx apps/web/src/components/placement-view.tsx
   ```
   **Kết quả:**
   - `apps/web/src/app/login/page.tsx: 4` (chính xác 4 màu thương hiệu Google)
   - `apps/web/src/app/onboarding/page.tsx: 0`
   - `apps/web/src/components/placement-view.tsx: 0`

4. **Kiểm tra `aria-checked`:**
   ```bash
   grep -c "aria-checked" apps/web/src/app/onboarding/page.tsx
   ```
   **Kết quả:** `1` (đạt yêu cầu ≥ 1).

5. **Kiểm tra git diff scope:**
   ```bash
   git diff --stat
   ```
   **Kết quả:**
   ```
    apps/web/src/app/login/page.tsx            | 22 ++++++--
    apps/web/src/app/onboarding/page.tsx       | 90 ++++++++++++++++++++++++------
    apps/web/src/components/placement-view.tsx | 10 ++--
    3 files changed, 95 insertions(+), 27 deletions(-)
   ```
   Chỉ đúng 3 file được liệt kê trong spec.

6. **Kiểm tra i18n parity:**
   ```bash
   node -e "const a=require('./apps/web/messages/en.json'),b=require('./apps/web/messages/vi.json');const k=(o,p='')=>Object.entries(o).flatMap(([x,v])=>typeof v==='object'?k(v,p+x+'.'):[p+x]);const A=k(a),B=k(b);console.log('en-only',A.filter(x=>!B.includes(x)),'vi-only',B.filter(x=>!A.includes(x)))"
   ```
   **Kết quả:** `en-only [] vi-only []` (2 mảng đều rỗng).

---

## 4. Điều còn chưa chắc

- Mọi tiêu chí trong checklist và lệnh kiểm tra đều đã được xác minh tự động và pass 100%. Không có điều gì chưa chắc chắn.
- Lưu ý môi trường: Trên Windows PowerShell, thực thi `pnpm` có thể bị chặn bởi Execution Policy script nên cần gọi `pnpm.cmd`.
