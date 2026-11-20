# Redesign Dose: Exams + exam runner (REDESIGN.md bước 7)

## Mục tiêu
Đưa `/exams` (`app/(main)/exams/page.tsx`) và `/exam/[id]` (`components/exam-runner.tsx`) sang theme Dose theo
`docs/REDESIGN.md` mục 3 và mục 4 hàng #5: "Danh sách đề dạng bảng. Thanh sticky đồng hồ nền đặc; báo cáo theo
chủ đề dùng thanh ngang `scaleX`". Theo `apps/web/design.md`.

## File được phép sửa/tạo
- Sửa: `apps/web/src/app/(main)/exams/page.tsx`, `apps/web/src/components/exam-runner.tsx`
- `apps/web/messages/en.json` + `vi.json`: chỉ **thêm** key trong namespace `exam` nếu thật cần (cả hai file).

## Không được đụng
- `curriculum/`, `tools/`, `supabase/`, `apps/web/src/lib/*`, `components/question.tsx`, `components/ui/*`, `tokens.css`, `globals.css`, `app/(main)/exam/[id]/page.tsx`, `placement-view.tsx`.
- Logic exam-runner: timer, `timeUp`, `lowTime`, chấm điểm, `confirm` dialog, lưu kết quả, điều hướng câu hỏi, các handler. Chỉ sửa JSX markup + className.
- Mọi `href` (`/exam/<id>/`, `/placement/`). Không xóa file, không sửa test, không `git commit`.
- **Không chạy `pnpm --filter web build`** (dev server đang chạy; boss tự build).

## Tiêu chí hoàn thành (checklist)
### `/exams`
- [ ] Mỗi nhóm (phase test / mock / placement) là một section: tiêu đề `<h2 className="text-lg font-bold">` + icon `aria-hidden`, rồi **một bảng** (`<table>` thật, `w-full text-sm`, trong khung `rounded-lg border border-border bg-card overflow-hidden`; trên mobile bọc `overflow-x-auto` hoặc chuyển sang danh sách xếp dọc ở `<sm` — không cuộn ngang trang).
  - Cột: tên đề (link tới `href` cũ, là phần tử bấm được của hàng), số câu, thời gian (phút), điểm đạt, điểm tốt nhất (Badge success nếu `passed`, muted nếu chưa), số lượt. Số dùng `font-mono tabular-nums`, căn phải.
  - Đầu bảng: `<th scope="col">` `text-xs font-medium text-muted-foreground`, sentence case, không uppercase, nền `bg-muted`.
  - Hàng: `hover:bg-accent transition-colors`, link có `focus-visible:outline-2 outline-ring`. Mô tả đề (`exam.description`) dòng phụ nhỏ dưới tên.
  - Cần nhãn cột → thêm key mới trong `exam` (vd `colExam`, `colQuestions`, `colMinutes`, `colPass`, `colBest`, `colAttempts`) ở cả en/vi, hoặc dùng lại key có sẵn nếu khớp. Không chuỗi cứng.
- [ ] Ô "mock bị khóa" (`lockedMock`) thành hàng cuối bảng mock (hoặc dòng ghi chú ngay dưới bảng), chữ `text-muted-foreground`, icon `Lock aria-hidden`.
- [ ] Bỏ `transition hover:-translate-y-0.5` của card cũ; không còn `Card` lồng `Link` cho từng đề.

### `exam-runner.tsx`
- [ ] **Màn giới thiệu**: các chip thông tin (số câu / phút / điểm đạt) `rounded-full bg-muted px-3 py-1.5`, số `font-mono tabular-nums`, icon `aria-hidden`. Lịch sử điểm dạng Badge mono.
- [ ] **Thanh sticky đồng hồ**: nền đặc `bg-background` (không blur), viền dưới hairline, padding `px-4 py-3`, vẫn `sticky top-14 lg:top-0`. Đồng hồ `font-mono tabular-nums font-bold` trong chip `rounded-md`:
  - bình thường: `bg-muted text-foreground`;
  - `lowTime`: `bg-warning-soft text-warning-ink` (REDESIGN 3.1: warning dùng cho "sắp hết giờ thi" — **không** dùng danger), **bỏ `animate-pulse`**; thêm icon cảnh báo nhỏ hoặc chữ sr-only để không chỉ dựa vào màu (có thể dùng `aria-live="polite"` ở chip).
  - Bộ đếm "đã trả lời" mono. Dãy ô điều hướng câu hỏi: `size-9 rounded-md font-mono text-xs`, đã trả lời = `bg-accent text-primary border-primary/40`, đang xem = viền `border-2 border-primary`, chưa = `border border-border bg-card`; có `aria-label`/`aria-current` (nếu đã có thì giữ).
- [ ] **Banner hết giờ** (`timeUp`): `rounded-lg bg-warning-soft text-foreground` + icon `aria-hidden`.
- [ ] **Báo cáo kết quả**: điểm lớn `font-mono tabular-nums text-3xl font-bold` (không `text-hit`, không `figure`); Badge đậu/rớt giữ `success`/`danger` (đây là kết quả đúng/sai, đỏ được phép). "Theo chủ đề": mỗi chủ đề là tên + `x/y` mono + `Progress` (đã dùng `scaleX`), tone success khi ≥ 70% như logic hiện có nếu có.
- [ ] **Xem lại câu**: icon đúng/sai `CheckCircle2 text-primary` / `XCircle text-danger` + chữ (không chỉ màu), `aria-hidden` cho icon.
- [ ] Không còn trong 2 file: `rounded-[`, `border-2` (trừ ô câu đang xem), `font-black`, `font-semibold`, `uppercase`, `transition ` trơn / `transition"`, `transition-all`, `animate-pulse`, `text-hit`, `bg-hit`, `border-edge`, `shadow-[`, `hover:-translate`, `text-[NNpx]`, `backdrop-blur`, literal màu.
- [ ] 375px: không cuộn ngang trang; thanh đồng hồ xếp gọn (nút Nộp bài vẫn thấy).
- [ ] Lệnh kiểm tra xanh.

## Lệnh kiểm tra
Từ gốc repo `D:\Proj\python-ai-platform` (KHÔNG `pnpm build`):
```
pnpm --filter web typecheck
grep -nE "rounded-\[|font-black|font-semibold|uppercase|transition[ \"]|transition-all|animate-pulse|text-hit|bg-hit|border-edge|shadow-\[|hover:-translate|text-\[[0-9]+px\]|backdrop-blur|#[0-9a-fA-F]{6}|oklch\(" "apps/web/src/app/(main)/exams/page.tsx" apps/web/src/components/exam-runner.tsx
grep -c "<table" "apps/web/src/app/(main)/exams/page.tsx"
node -e "const a=require('./apps/web/messages/en.json'),b=require('./apps/web/messages/vi.json');const k=(o,p='')=>Object.entries(o).flatMap(([x,v])=>typeof v==='object'?k(v,p+x+'.'):[p+x]);const A=k(a),B=k(b);console.log('en-only',A.filter(x=>!B.includes(x)),'vi-only',B.filter(x=>!A.includes(x)))"
```
Mong đợi: typecheck 0 lỗi; grep đầu rỗng; `<table` ≥ 1; hai mảng rỗng.
Tự xem `http://localhost:3000/exams/` và mở một phase test (HMR).

## Ghi chú cho worker
- Đọc `docs/REDESIGN.md` và `apps/web/design.md` trước.
- Token: `bg-warning-soft`, `text-warning-ink`, `bg-accent`, `text-primary`, `bg-muted`, `text-danger`.
- Font chỉ 400/500/700. Windows: dùng `pnpm.cmd` nếu PowerShell chặn `pnpm`.

## Feedback vòng 1
Typecheck/grep/i18n xanh, logic giữ nguyên, bảng và thanh đồng hồ đạt. Sửa:

1. **Cắt chuỗi đã dịch** ở `exam-runner.tsx` dòng ~121, ~126, ~130:
   `tc("questions", …).replace(String(n), "").trim()`, `t("duration", …).replace(…)`, `t("passScore", { score: "" }).trim()`.
   Cách này phụ thuộc vị trí số trong câu (vd EN "Pass {score}" khác thứ tự VI/plural) và sẽ vỡ khi ai đó đổi bản dịch. Trả về gọi bình thường: `{tc("questions", { count })}`, `{t("duration", { count })}`, `{t("passScore", { score: percent(...) })}` trong chip, chip thêm `tabular-nums` (không cần tách span mono cho số). Không đổi JSON.
2. **Ba bảng ở `/exams` lệch cột nhau** và đầu cột "Số câu" bị xuống dòng ở 1440px. Dùng `table-fixed` + `<colgroup>` cùng độ rộng cho cả ba bảng (vd cột tên `w-auto`, 5 cột số mỗi cột `w-28` ở `sm+`), `<th>` thêm `whitespace-nowrap`. Ở `<sm` giữ cách hiện tại (ẩn bớt cột hoặc xếp dọc) sao cho không cuộn ngang trang.
3. Chạy lại Lệnh kiểm tra (KHÔNG `pnpm build`), thêm mục "Vòng 2" vào report. Grep thêm để chắc đã bỏ hack: `grep -n "\.replace(String\|score: \"\"" apps/web/src/components/exam-runner.tsx` phải rỗng.

## Trạng thái
- Bước hiện tại: 5 (chờ user review + commit)
- Vòng: 2/3, đạt
- Boss đã kiểm: typecheck, build, validate, grep; /exams 1440 (3 bảng thẳng cột) + 375 (không cuộn ngang), exam intro + đang thi ở desktop dark
- Số lần swap: 0
- Fallback: không
