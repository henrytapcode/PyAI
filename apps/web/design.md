# Hệ thống thiết kế PyAI Path · Theme Dose

> Tài liệu chuẩn hóa hệ thống giao diện cho dự án PyAI Path sau đợt chuyển đổi từ theme Arcade sang theme **Dose** (REDESIGN.md bước 1 + 2).
> Mọi bước triển khai tiếp theo (Lesson, Dashboard, Learn, Review, Exams, Playground, v.v.) tuân thủ tuyệt đối các nguyên tắc trong tài liệu này.

---

## 1. Bản sắc & Đóng dấu (Stamp)

- **Theme:** Dose (modern-minimal).
- **Ground:**
  - Light mode: `white` (giấy sáng sớm ấm áp, mực xanh đen, hạt mộc mạc).
  - Dark mode: `night` (than chì ánh xanh đen `oklch(13% 0.01 170)`, nhựa bán trong 40% L, mực sáng `oklch(96% 0.01 160)`).
- **Signature:** **Khay lộ trình** (dải tint màu nhạt theo phase, chia ngăn bài học; ngăn đã xong chuyển mint có tick, bài kế tiếp viền xanh lá, bài khóa để mờ).
- **Stamp:**
  ```css
  /* Hallmark · shape: app screen · genre: modern-minimal · theme: Dose (deal 1/3, seed app-where-beginner-learns-bcc0·8cb9aa4e·2026-11-12·r0) · redesign: full
   * nav: sidebar of menu rows · signature: khay lộ trình · states: default hover active focus disabled busy selected correct wrong · dose: white/night
   * axes: light/clean/chromatic-green · posture: committed · contrast: pass · v2.1.0 */
  ```

---

## 2. Màu sắc & Tokens (`tokens.css`)

### 2.1 Bảng màu cốt lõi

| Token | Light (`:root`) | Dark (`:root.dark`) | Mục đích |
|---|---|---|---|
| `--background` | `oklch(97.6% 0.011 88)` | `oklch(13% 0.01 170)` | Nền trang |
| `--card`, `--popover` | `oklch(99.4% 0.006 88)` | `oklch(17% 0.012 170)` | Bề mặt card, menu nổi |
| `--muted`, `--secondary` | `oklch(96.5% 0.02 160)` | `oklch(21% 0.015 170)` | Sidebar, toolbar, container phụ |
| `--accent` | `oklch(93% 0.036 160)` | `oklch(26% 0.03 160)` | Nền hover, hàng menu đang chọn |
| `--foreground` | `oklch(21% 0.025 170)` | `oklch(96% 0.01 160)` | Chữ chính |
| `--muted-foreground` | `oklch(49% 0.024 165)` | `oklch(72% 0.02 165)` | Chữ phụ, nhãn, chú thích |
| `--border`, `--input` | `oklch(86.5% 0.022 140)` | `oklch(30% 0.02 165)` | Viền hairline |
| `--primary` | `oklch(50% 0.13 160)` | `oklch(72% 0.13 160)` | Màu tín hiệu chính, nút bấm, focus, bài hoàn thành |
| `--primary-foreground` | `oklch(99% 0.006 160)` | `oklch(15% 0.02 165)` | Chữ trên nền primary |
| `--primary-ink` | `oklch(42% 0.11 162)` | `oklch(85% 0.12 160)` | Chữ nhấn mạnh tông xanh |
| `--success` / `--success-soft` | = primary / `oklch(88% 0.08 160)` | = primary / `oklch(30% 0.06 160)` | Test pass, câu đúng, bài hoàn thành (mint) |
| `--danger` / `--danger-soft` | `oklch(52% 0.13 25)` / `oklch(94% 0.03 25)` | `oklch(72% 0.12 25)` / `oklch(27% 0.05 25)` | Test fail, câu sai |
| `--warning` / `--warning-soft` | `oklch(55% 0.09 75)` / `oklch(94% 0.04 85)` | `oklch(78% 0.1 80)` / `oklch(28% 0.04 80)` | Cảnh báo, sắp hết giờ |
| `--warning-ink` | `oklch(46% 0.09 75)` | = `--warning` | Chữ cảnh báo đạt tương phản ≥ 4.5:1 trên soft |
| `--ring` | `oklch(45% 0.14 160)` | `oklch(78% 0.13 160)` | Đường bao focus-visible |
| `--code-bg` | `oklch(96% 0.008 100)` | `oklch(16% 0.01 170)` | Nền khối code, terminal output |

### 2.2 Tint nhận diện Phase (Khay lộ trình)

7 dải tint nhạt dùng cho dải phase (chỉ là nhận diện thương hiệu, không mang nghĩa trạng thái; phase 8 và 9 quay vòng lại phase 1 và 2):

- `--phase-1`: `oklch(85% 0.052 22)` (Dark: `oklch(40% 0.052 22 / 62%)`)
- `--phase-2`: `oklch(87.5% 0.058 64)` (Dark: `oklch(40% 0.058 64 / 62%)`)
- `--phase-3`: `oklch(91.5% 0.064 98)` (Dark: `oklch(40% 0.064 98 / 62%)`)
- `--phase-4`: `oklch(86.5% 0.075 160)` (Dark: `oklch(40% 0.075 160 / 62%)`)
- `--phase-5`: `oklch(87% 0.048 210)` (Dark: `oklch(40% 0.048 210 / 62%)`)
- `--phase-6`: `oklch(84% 0.045 270)` (Dark: `oklch(40% 0.045 270 / 62%)`)
- `--phase-7`: `oklch(84% 0.048 322)` (Dark: `oklch(40% 0.048 322 / 62%)`)

### 2.3 Syntax Highlighting (`--syn-*`)

Bộ token cú pháp lấy tông xanh lá pharmacy làm chủ đạo, tương phản cao trên `--code-bg`:
- `--syn-keyword`: `oklch(44% 0.13 160)` (Dark: `oklch(76% 0.13 160)`)
- `--syn-string`: `oklch(48% 0.11 135)` (Dark: `oklch(78% 0.11 135)`)
- `--syn-number`: `oklch(50% 0.11 60)` (Dark: `oklch(80% 0.1 75)`)
- `--syn-title`: `oklch(38% 0.12 165)` (Dark: `oklch(82% 0.12 165)`)
- `--syn-meta`: `oklch(52% 0.06 165)` (Dark: `oklch(70% 0.06 165)`)

### 2.4 Quy tắc màu

1. **Một màu xanh lá tín hiệu duy nhất (`--primary`):** Nút chính, mục đang chọn, focus ring, bài đã hoàn thành. Không dùng màu thương hiệu thứ hai.
2. **Đỏ (`--danger`):** Chỉ dùng cho test fail và câu trả lời sai. Thẻ ôn tập quá hạn dùng màu xám (`--muted-foreground`), không dùng màu đỏ.
3. **Không literal màu:** Tuyệt đối không viết `#hex`, `rgb(...)`, `oklch(...)` trong component `.tsx` hay `globals.css`. Mọi màu phải trỏ tới `var(--token)`.
4. **Độ tương phản (WCAG AA ≥ 4.5:1):** Luôn đảm bảo tỷ lệ tương phản chữ thường ≥ 4.5:1 ở cả light và dark mode. Badge `success` bắt buộc dùng `text-primary-ink` trên nền `bg-success-soft`; Badge `warning` dùng `text-warning-ink` trên nền `bg-warning-soft`.

---

## 3. Chữ (Typography)

- **Display & Body Font:** **Be Vietnam Pro** (chỉ nạp 3 weights: 400, 500, 700; subsets: `latin`, `vietnamese`). Cả hai biến `--font-sans` và `--font-display` đều trỏ vào font này. Không dùng weight 600 (`font-semibold`) hay 900 (`font-black`) — toàn bộ chuyển sang `font-bold` (700) hoặc `font-medium` (500).
- **Code, Số liệu, Đồng hồ:** **JetBrains Mono** (weights: 400, 500; subsets: `latin`, `vietnamese`), luôn đi kèm `tabular-nums` cho số XP, streak, đồng hồ đếm ngược.
- **Thang chữ cố định (12 / 14 / 16 / 19 / 23 / 28 / 33px):**
  - `--text-xs`: `0.75rem` (12px)
  - `--text-sm`: `0.875rem` (14px)
  - `--text-base`: `1rem` (16px)
  - `--text-lg`: `1.1875rem` (19px)
  - `--text-xl`: `1.4375rem` (23px)
  - `--text-2xl`: `1.75rem` (28px)
  - `--text-3xl` / `--text-4xl` / `--text-5xl`: `2.0625rem` (33px)
- **Heading:** Font weight 700 (`font-bold`), letter-spacing `-0.02em`, sentence case (chữ cái đầu viết hoa, không viết hoa toàn bộ `uppercase`), `text-wrap: balance`. Display = `text-3xl`, thường = `text-2xl`.
- **Nhãn, Tag, Nav, Nút:** Body font, sentence case, không tracking rộng, không eyebrow uppercase.
- **Lesson Prose:** Cỡ chữ 16–17px, line-height 1.6 (hỗ trợ dấu tiếng Việt chồng), measure tối đa 65–72ch.

---

## 4. Hình khối, Bề mặt & Controls

- **Radius:**
  - Controls (button, input, select, tabs list): 10px (`--radius: 0.625rem`, Tailwind `rounded-md`).
  - Card & Panels: 14px (Tailwind `rounded-lg`, class `.well`).
  - Tags & Badges: 999px (Tailwind `rounded-full`).
- **Quy tắc Elevation (Viền hairline HOẶC Shadow - không dùng cả hai):**
  - Card thường: dùng viền hairline 1px (`border border-border`), không kèm shadow.
  - Bề mặt nổi (Dialog, Popover "more", Tooltip): dùng nền đặc (`bg-popover`) + shadow (`shadow-[var(--shadow-lift)]`), **bỏ viền** (`border-0` hoặc không khai báo border).
- **Không Glassmorphism / Không Blur:**
  - Tuyệt đối không dùng `backdrop-blur`, blur orb, hoặc nền kính mờ.
  - Sticky header dùng nền đặc (`bg-background` hoặc `bg-card`).
- **Nút bấm kiểu "Nhựa đúc" (`.press`):**
  - Viền 1px, mép dưới 3px (`box-shadow: 0 3px 0 0 var(--press-edge)`).
  - Biến `--press-edge`: mặc định `var(--border)`; variant `default` và `success` dùng `var(--primary-ink)`; variant `danger` dùng `color-mix(in oklch, var(--danger) 75%, var(--foreground))`.
  - Hover: nhấc nhẹ lên 1px (`translateY(-1px)`, mép 4px).
  - Active: ấn lún xuống 3px (`translateY(3px)`, mép 0px).
  - Chiều cao nút nhìn thấy 36–40px. Vùng bấm mở rộng đạt ≥ 44px bằng pseudo-element (`relative after:absolute after:-inset-1` hoặc `after:-inset-[4px]`) mà không làm phình kích thước icon.
- **Trạng thái Control:**
  Mọi control phải đủ các trạng thái tương tác: `default`, `hover`, `active`, `focus-visible`, `disabled`, `busy`, `selected`, `correct`/`wrong`.

---

## 5. Chuyển động (Motion)

- **Triết lý:** Motion là trạng thái phản hồi, không dùng để trang trí rườm rà.
- **Thuộc tính được phép:** Chỉ áp dụng `transform` và `opacity`.
- **Thời lượng:** 120ms – 200ms (nhanh, dứt khoát, cảm giác nhựa cơ học).
- **Cấm tuyệt đối:**
  - Không dùng `transition-all`.
  - Không animate thuộc tính kích thước (`width`, `height`). Thanh tiến độ (`Progress`, `.meter`) bắt buộc sử dụng `transform: scaleX(...)` với `transform-origin: left center`.
  - Không dùng hiệu ứng CRT, scanline, flicker, blink.
- **Trợ năng (Accessibility - Reduced Motion):**
  - Mọi hiệu ứng chuyển động và animation phải tắt hoặc đưa về tức thì khi `prefers-reduced-motion: reduce`.

---

## 6. Trợ năng (A11y Standards)

- Mọi nút bấm chỉ có icon bắt buộc phải có `aria-label` mô tả hành động (ví dụ: nút đóng modal, nút chuyển theme).
- Các icon minh họa/trang trí đi kèm chữ bắt buộc có `aria-hidden="true"`.
- Bàn phím: outline rõ nét với `focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring`.
- Không tràn ngang (no horizontal overflow) ở kích thước màn hình nhỏ 375px.
