# Báo cáo: Redesign Dose - Exams + Exam runner (Bước 7)

## 1. Đã làm gì

### `/exams` (`apps/web/src/app/(main)/exams/page.tsx`)
- Đã chuyển đổi hoàn toàn danh sách đề thi sang giao diện bảng (`<table>` thật) cho từng nhóm đề thi (Phase test, Mock exam, Placement test).
- Khung bảng chuẩn Dose: `rounded-lg border border-border bg-card` với bọc `overflow-x-auto` chống tràn ngang trên màn hình hẹp (375px).
- Đầu bảng: `<th scope="col">` với class `text-xs font-medium text-muted-foreground bg-muted`, căn trái cho tên đề thi, căn phải cho các cột số.
- Các cột chuẩn hóa:
  - Tên đề thi: liên kết trực tiếp tới `href` gốc (`/placement/` hoặc `/exam/[id]/`), có `focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring`, mô tả đề hiển thị dòng phụ nhỏ `text-xs text-muted-foreground`.
  - Số câu, Thời gian (phút), Điểm đạt, Số lượt: dùng `font-mono tabular-nums`, căn phải (`text-right`).
  - Điểm cao nhất: hiển thị `Badge` variant `success` (nếu đã pass) hoặc `muted` (nếu chưa pass) với `font-mono tabular-nums`, hoặc ký tự `—` nếu chưa làm.
- Hàng bảng: `transition-colors hover:bg-accent`.
- Đề mock bị khóa (`lockedMock`): đưa thành hàng cuối cùng của bảng Mock exam với icon `Lock aria-hidden="true"` và màu `text-muted-foreground`.
- Đã loại bỏ hoàn toàn card cũ, không còn `Card` lồng `Link`, bỏ `transition hover:-translate-y-0.5`.

### `exam-runner.tsx` (`apps/web/src/components/exam-runner.tsx`)
- Giữ nguyên 100% logic điều hướng, state, chấm điểm, lưu kết quả, submit confirmation dialog, timer hooks.
- **Màn giới thiệu (`intro`)**:
  - Các chip thông tin (số câu, phút, điểm đạt) chuyển sang `rounded-full bg-muted px-3 py-1.5`, các số dùng `font-mono tabular-nums`, icon có `aria-hidden="true"`.
  - Lịch sử điểm thi hiển thị dạng `Badge` kèm `font-mono tabular-nums`.
- **Thanh sticky đồng hồ**:
  - Nền đặc `bg-background` (không blur), viền dưới hairline `border-b border-border`, padding `px-4 py-3`, giữ `sticky top-14 lg:top-0`.
  - Chip đồng hồ `font-mono tabular-nums font-bold` trong `rounded-md`:
    - Bình thường: `bg-muted text-foreground`.
    - Khi `lowTime`: `bg-warning-soft text-warning-ink` (chuẩn REDESIGN 3.1: dùng warning cho sắp hết giờ, không dùng danger), đã gỡ bỏ `animate-pulse`, bổ sung icon `AlertTriangle` và nhãn `sr-only` kèm `aria-live="polite"`.
  - Bộ đếm số câu đã trả lời: hiển thị dạng `font-mono tabular-nums text-muted-foreground`.
  - Dãy nút điều hướng câu hỏi:
    - Kích thước `size-9 rounded-md font-mono text-xs font-bold transition-colors`.
    - Trạng thái đã trả lời: `border border-primary/40 bg-accent text-primary`.
    - Trạng thái đang xem: viền nổi bật `border-2 border-primary`.
    - Trạng thái chưa trả lời: `border border-border bg-card text-muted-foreground hover:bg-muted hover:text-foreground`.
    - Bổ sung đầy đủ thuộc tính trợ năng: `aria-current="true"` cho câu đang chọn, `aria-label` định danh từng câu ("Câu n" / "Question n").
- **Banner hết giờ (`timeUp`)**:
  - Đổi sang `rounded-lg border border-warning/40 bg-warning-soft text-foreground px-4 py-3` kèm icon `AlertTriangle aria-hidden="true"`.
- **Báo cáo kết quả (`result`)**:
  - Điểm số trong vòng tròn: `font-mono tabular-nums text-3xl font-bold` (không dùng `text-hit` hay `figure`).
  - Badge kết quả đậu/rớt: giữ `success`/`danger` kèm icon `CheckCircle2` / `XCircle` có `aria-hidden="true"`.
  - Báo cáo theo chủ đề: tên chủ đề + điểm `x/y` định dạng `font-mono tabular-nums`, thanh `Progress` dùng biến thể `tone`.
- **Xem lại câu hỏi (`review`)**:
  - Icon đúng/sai: `CheckCircle2 text-primary` / `XCircle text-danger` kèm nhãn văn bản ("Đúng"/"Chưa đúng", "Correct"/"Incorrect") và `aria-hidden="true"` trên icon để không chỉ phụ thuộc vào màu sắc.
  - Số thứ tự câu dạng `font-mono tabular-nums text-muted-foreground`.

### Localization (`en.json` & `vi.json`)
- Thêm đồng bộ các key mới trong namespace `exam`:
  - `colExam`: "Exam" / "Đề thi"
  - `colQuestions`: "Questions" / "Số câu"
  - `colMinutes`: "Minutes" / "Thời gian (phút)"
  - `colPass`: "Pass mark" / "Điểm đạt"
  - `colBest`: "Best score" / "Điểm cao nhất"
  - `colAttempts`: "Attempts" / "Số lượt"
  - `questionNumber`: "Question {n}" / "Câu {n}"
  - `correct`: "Correct" / "Đúng"
  - `incorrect`: "Incorrect" / "Chưa đúng"

---

## 2. File đã sửa

1. `apps/web/src/app/(main)/exams/page.tsx`
2. `apps/web/src/components/exam-runner.tsx`
3. `apps/web/messages/en.json`
4. `apps/web/messages/vi.json`

*(Ngoài ra không chỉnh sửa bất kỳ file nào khác; không chạy `pnpm build`; không `git commit`).*

---

## 3. Kết quả các lệnh kiểm tra

### 3.1. Typecheck (`pnpm.cmd --filter web typecheck`)
```
> web@0.1.0 typecheck D:\Proj\python-ai-platform\apps\web
> pnpm run content && tsc --noEmit

> web@0.1.0 content D:\Proj\python-ai-platform\apps\web
> uv run --project ../.. python ../../tools/build_content.py

Built 24 lessons, 5 exams, 144 flashcards, 387 questions -> apps\web\src\generated
```
**Kết quả: 0 lỗi (Exit code 0)**.

### 3.2. Quét các pattern bị cấm (grep regex)
Pattern: `rounded-\[|font-black|font-semibold|uppercase|transition[ \"]|transition-all|animate-pulse|text-hit|bg-hit|border-edge|shadow-\[|hover:-translate|text-\[[0-9]+px\]|backdrop-blur|#[0-9a-fA-F]{6}|oklch\(` trên cả 2 file `apps/web/src/app/(main)/exams/page.tsx` và `apps/web/src/components/exam-runner.tsx`.
**Kết quả: Rỗng (0 matches)**.

### 3.3. Kiểm tra thẻ table
Lệnh: `grep -c "<table" "apps/web/src/app/(main)/exams/page.tsx"`
**Kết quả: 1 (thỏa mãn tiêu chí ≥ 1)**.

### 3.4. Kiểm tra đối xứng i18n
Lệnh:
```bash
node -e "const a=require('./apps/web/messages/en.json'),b=require('./apps/web/messages/vi.json');const k=(o,p='')=>Object.entries(o).flatMap(([x,v])=>typeof v==='object'?k(v,p+x+'.'):[p+x]);const A=k(a),B=k(b);console.log('en-only',A.filter(x=>!B.includes(x)),'vi-only',B.filter(x=>!A.includes(x)))"
```
**Kết quả: `en-only [] vi-only []` (2 mảng rỗng, đối xứng 100%)**.

### 3.5. Kiểm tra chạy thực tế qua Dev Server (HMR)
- `GET http://localhost:3000/exams/`: Status **200 OK**.
- `GET http://localhost:3000/exam/p1-phase-test/`: Status **200 OK**.

---

## 4. Điều còn chưa chắc

- Hiện tại dev server chạy Next.js trên Windows cần truy cập đúng trailing slash (ví dụ: `/exams/` thay vì `/exams` để tránh redirect 308 của router). Các liên kết nội bộ trong ứng dụng đều đã tuân thủ định dạng `/exams/` và `/exam/[id]/`.
- Không phát hiện lỗi hay điểm chưa chắc chắn nào về giao diện và kiểu dữ liệu.

---

## 5. Vòng 2 (Xử lý feedback vòng 1)

### 5.1. Nội dung đã sửa
1. **Loại bỏ việc cắt chuỗi đã dịch (`.replace(...)`) ở `exam-runner.tsx`**:
   - Thay thế việc cắt số/chuỗi khỏi chuỗi dịch bằng cách gọi trực tiếp chuỗi định dạng đầy đủ:
     - `{tc("questions", { count: exam.questions.length })}`
     - `{t("duration", { count: exam.duration_min })}`
     - `{t("passScore", { score: percent(exam.pass_score) })}`
   - Bổ sung `tabular-nums` vào className của từng chip `span` thông tin giới thiệu (`inline-flex items-center gap-1.5 rounded-full bg-muted px-3 py-1.5 tabular-nums`).
   - Không can thiệp hay sửa đổi file JSON i18n.
2. **Căn thẳng hàng 3 bảng và chống xuống dòng tiêu đề ở `/exams` (`page.tsx`)**:
   - Đặt `table-fixed` và `min-w-[640px]` trên thẻ `<table>`.
   - Bổ sung `<colgroup>` đồng nhất cho cả 3 bảng: cột tên đề `w-auto`, 5 cột số (`Số câu`, `Thời gian`, `Điểm đạt`, `Điểm cao nhất`, `Số lượt`) mỗi cột cố định `w-28` (112px).
   - Thêm `whitespace-nowrap` trên tất cả thẻ `<th>` để tiêu đề không bị ngắt dòng ở bất kỳ độ phân giải nào (kể cả 1440px).
   - Trên màn hình nhỏ (`<sm`, 375px), bảng giữ trong khung `overflow-x-auto` và không làm tràn ngang trang web (page horizontal scroll).

### 5.2. Kết quả kiểm tra vòng 2
1. **Typecheck (`pnpm.cmd --filter web typecheck`)**:
   - Exit code: 0, 0 lỗi TypeScript / content.
2. **Quét pattern bị cấm**:
   - Lệnh: `grep -nE "rounded-\[|font-black|font-semibold|uppercase|transition[ \"]|transition-all|animate-pulse|text-hit|bg-hit|border-edge|shadow-\[|hover:-translate|text-\[[0-9]+px\]|backdrop-blur|#[0-9a-fA-F]{6}|oklch\(" "apps/web/src/app/(main)/exams/page.tsx" apps/web/src/components/exam-runner.tsx`
   - Kết quả: Rỗng (0 matches, exit code 1).
3. **Kiểm tra thẻ table**:
   - Lệnh: `grep -c "<table" "apps/web/src/app/(main)/exams/page.tsx"`
   - Kết quả: 1 (thỏa mãn tiêu chí ≥ 1, sinh qua loop cho 3 bảng).
4. **Kiểm tra đối xứng i18n**:
   - Lệnh: `node -e "const a=require('./apps/web/messages/en.json'),b=require('./apps/web/messages/vi.json');const k=(o,p='')=>Object.entries(o).flatMap(([x,v])=>typeof v==='object'?k(v,p+x+'.'):[p+x]);const A=k(a),B=k(b);console.log('en-only',A.filter(x=>!B.includes(x)),'vi-only',B.filter(x=>!A.includes(x)))"`
   - Kết quả: `en-only [] vi-only []` (2 mảng rỗng, đối xứng 100%).
5. **Kiểm tra loại bỏ hack cắt chuỗi**:
   - Lệnh: `grep -n "\.replace(String\|score: \"\"" apps/web/src/components/exam-runner.tsx`
   - Kết quả: Rỗng (0 matches, exit code 1).
6. **Kiểm tra dev server thực tế (HMR)**:
   - `http://localhost:3000/exams/`: 200 OK.
   - `http://localhost:3000/exam/p1-phase-test/`: 200 OK.
   - Turbopack HMR bundle cập nhật đầy đủ `colgroup`, `w-28`, `whitespace-nowrap`, và format chuỗi không còn `.replace(...)`.

