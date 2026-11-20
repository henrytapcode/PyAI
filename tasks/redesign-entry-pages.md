# Redesign Dose: Onboarding, Placement, Login (REDESIGN.md bước 10)

## Mục tiêu
Đưa `/onboarding`, `/placement`, `/login` sang theme Dose theo `docs/REDESIGN.md` mục 3 và mục 4 hàng #8
("Bỏ blur orb. Lựa chọn là 'phím nhựa', mint khi được chọn."), theo `apps/web/design.md`.

## File được phép sửa/tạo
- Sửa: `apps/web/src/app/onboarding/page.tsx`, `apps/web/src/app/login/page.tsx`, `apps/web/src/components/placement-view.tsx`
- `apps/web/messages/en.json` + `vi.json`: chỉ **thêm** key nếu thật cần (cả hai file).

## Không được đụng
- `app/placement/page.tsx`, `components/exam-runner.tsx`, `components/ui/*`, `lib/*` (gồm `lib/auth`), `tokens.css`, `globals.css`, `curriculum/`, `tools/`.
- Logic: các bước onboarding, `setLocale`/`setTrack`/`setDailyGoal`/`finishOnboarding`, điều hướng; login: form, handler đăng nhập/đăng ký, Google OAuth, trạng thái `notConfigured`; placement: kết quả/skip phase. Chỉ sửa JSX markup + className.
- **Logo Google** (`path fill="#4285F4"` … trong `login/page.tsx`) là màu thương hiệu bắt buộc của nút "Sign in with Google": **giữ nguyên**, đừng đổi sang token.
- Không xóa file, không sửa test, không `git commit`. **Không chạy `pnpm --filter web build`** (boss tự build).

## Tiêu chí hoàn thành (checklist)
### Onboarding
- [ ] Khung bước: `Card` mặc định hoặc `rounded-lg border border-border bg-card p-6 sm:p-8` (không shadow). Thanh tiến độ 3 đoạn: `h-1.5 flex-1 rounded-full`, đoạn đã qua `bg-primary`, chưa `bg-muted`.
- [ ] **Lựa chọn là "phím nhựa"** (component `Choice` hoặc tương đương ở dòng ~117): `type="button"` + `role="radio"` + `aria-checked={active}` trong một container `role="radiogroup"` có `aria-label` (dùng tiêu đề bước đã dịch); dùng class `.press` (mép dưới 3px, ấn lún) với `rounded-lg border p-4 text-left`; mặc định `bg-card`; **được chọn = mint**: `bg-success-soft border-primary [--press-edge:var(--primary-ink)]` + chữ `text-foreground`; ô check `size-5 rounded-md border`, khi chọn `border-primary bg-primary text-primary-foreground` + icon `Check aria-hidden`. Có `focus-visible:outline-2 outline-ring`. Không `transition` trơn (`.press` đã có transition riêng).
- [ ] Ô code ngôn ngữ (VI/EN) và ô icon: `size-9 rounded-md bg-muted font-mono text-sm font-bold text-primary`, icon `aria-hidden`.
- [ ] Không blur orb / `blur-` / `backdrop-blur` (nếu còn sót thì gỡ).

### Placement (`placement-view.tsx`)
- [ ] Banner/Card giới thiệu: `Card` mặc định + `bg-accent` (bỏ `border-primary/30 bg-accent/40`), icon `aria-hidden`. Tiêu đề `text-2xl font-bold tracking-tight`, sentence case.

### Login
- [ ] Input: `h-10 w-full rounded-md border border-border bg-card px-3 text-sm outline-none focus-visible:outline-2 focus-visible:outline-ring` (bỏ `ring-ring/50`). Mỗi input có `<label>` hiển thị hoặc `aria-label` đã dịch.
- [ ] Khung form và khung `notConfigured`: `rounded-lg border border-border bg-card`. Thông báo lỗi (nếu có) `rounded-md bg-danger-soft text-danger px-3 py-2 text-sm role="alert"`.
- [ ] Nút Google: `Button variant="outline"` giữ logo; logo có `aria-hidden`.

### Chung
- [ ] Không còn trong 3 file: `rounded-[`, `border-2`, `font-black`, `font-semibold`, `uppercase`, `transition ` trơn / `transition"`, `transition-all`, `text-hit`, `bg-hit`, `border-edge`, `shadow-[`, `text-[NNpx]`, `backdrop-blur`, `blur-`, `row-cursor`, `oklch(`; literal hex chỉ được còn 4 `fill="#..."` của logo Google.
- [ ] 375px: không cuộn ngang; lựa chọn onboarding xếp 1 cột.
- [ ] Lệnh kiểm tra xanh.

## Lệnh kiểm tra
Từ gốc repo `D:\Proj\python-ai-platform` (KHÔNG `pnpm build`):
```
pnpm --filter web typecheck
grep -nE "rounded-\[|border-2|font-black|font-semibold|uppercase|transition[ \"]|transition-all|text-hit|bg-hit|border-edge|shadow-\[|text-\[[0-9]+px\]|backdrop-blur|blur-|row-cursor|oklch\(" apps/web/src/app/onboarding/page.tsx apps/web/src/app/login/page.tsx apps/web/src/components/placement-view.tsx
grep -cE "#[0-9a-fA-F]{6}" apps/web/src/app/login/page.tsx apps/web/src/app/onboarding/page.tsx apps/web/src/components/placement-view.tsx
grep -c "aria-checked" apps/web/src/app/onboarding/page.tsx
git diff --stat
node -e "const a=require('./apps/web/messages/en.json'),b=require('./apps/web/messages/vi.json');const k=(o,p='')=>Object.entries(o).flatMap(([x,v])=>typeof v==='object'?k(v,p+x+'.'):[p+x]);const A=k(a),B=k(b);console.log('en-only',A.filter(x=>!B.includes(x)),'vi-only',B.filter(x=>!A.includes(x)))"
```
Mong đợi: typecheck 0 lỗi; grep đầu rỗng; đếm hex = login 4, hai file kia 0; `aria-checked` ≥ 1; diff chỉ 3 file (+ messages); hai mảng rỗng.

## Ghi chú cho worker
- Đọc `docs/REDESIGN.md`, `apps/web/design.md`, `components/ui/button.tsx`, phần `.press` trong `app/globals.css` trước.
- Không cắt/ghép chuỗi đã dịch; muốn chuỗi khác thì thêm key.
- Font chỉ 400/500/700. Windows: dùng `pnpm.cmd` nếu PowerShell chặn `pnpm`.

## Trạng thái
- Bước hiện tại: 2
- Vòng: 1/3
- Số lần swap: 0
- Fallback: không
