# Tiến độ redesign Dose (cập nhật 2026-11-13)

Nhánh: `redesign/dose`, đã merge vào `main` (`c415e3a`) và đã push (2026-11-13). Spec gốc: `docs/REDESIGN.md` (mục 6 = các bước, mục 7–8 = việc treo + handoff).

## Đã xong (mỗi bước một commit)

| Bước | Nội dung | Commit |
|---|---|---|
| 1–2 | Tokens, font, CSS nền, component dùng chung | `e79a7e8` |
| 3 | Lesson view, workbench, Monaco theme, quiz, RAG chat | `03d6bbe` |
| 4 | Dashboard + khay lộ trình (`components/roadmap-tray.tsx`) | `506a022` |
| 5 | Learn (khay đầy đủ) | `dddadee` |
| 6 | Review | `4dfa4c5` |
| 7 | Exams + exam runner | `f0eef4e` |
| 8 | Playground | `58f8172` |
| 9 | Glossary, Interview, Portfolio, Settings (dialog xóa tiến độ) | `979ea1b` |
| 10 | Onboarding, Placement, Login | `a40881a` |
| 11 | Sweep: sloplint 0 FAIL, `.hit` 44px, gỡ alias Arcade | `5a98470` |
| 12 | Handoff: ghi vào `docs/REDESIGN.md` §7–8, `CLAUDE.md`, `docs/DESIGN.md` §5 (các file này bị gitignore, chỉ có trên máy) | không commit |
| Sửa sau kiểm tra tay | Mermaid theo token Dose, vùng bấm ngăn khay 44px, tương phản badge trên dải tint, tên truy cập lựa chọn ngôn ngữ ở onboarding (`tasks/redesign-polish.md`) | `c2021ea` |

Chủ dự án đã chốt (2026-11-13): **giữ** bước 10–11.

Kiểm tra tay đã làm (2026-11-13): quét tự động 11 route ở 768px, bản EN, light + dark: không cuộn ngang, không chữ nào dưới 4.5:1 (sau khi sửa), vùng bấm ≥ 44px. Đã xem màn báo cáo kết quả thi (768px, light, EN).

## Việc tiếp theo

1. Chủ dự án review các commit trên `redesign/dose`.
2. Còn chưa xem tận mắt: trạng thái sắp hết giờ thi (`lowTime` trong `exam-runner.tsx`, phải chờ đồng hồ gần hết); đã soát code: dùng `bg-warning-soft text-warning-ink`, có icon + chữ sr-only.
3. ~~Merge vào `main`~~: đã merge ở `c415e3a` và push lên `origin/main` (2026-11-13).

## Cách làm tiếp (quy trình boss/worker)

- Claude viết spec `tasks/<slug>.md` → giao Gemini qua MCP `consult_agy` → tự chạy lại kiểm tra + xem app trong browser pane → feedback tối đa 3 vòng → commit.
- Lệnh kiểm tra: `uv run python tools/validate.py` · `uv run python -m pytest curriculum` (không dùng `uv run pytest`, bị lỗi launcher) · `pnpm --filter web typecheck` · `pnpm --filter web build` · `node ~/.claude/skills/hallmark/scripts/sloplint.mjs apps/web/src --genre modern-minimal --scope app --kept`.
- **Tắt dev server trước khi build**, build xong bật lại (build dựng lại `src/generated`, dev server đang chạy sẽ lỗi 500).
- Prompt để chạy lại: `Đọc tasks/PROGRESS.md và docs/REDESIGN.md, làm tiếp mục "Việc tiếp theo".`

---

# M3 (bắt đầu 2026-11-13) — xem `tasks/M3-PLAN.md`

Đã commit: bước 1 nền tảng `8493356`, p4-01 NumPy `67492fc`, p4-02 Pandas `b8e334d`, p4-03 Cleaning `1d52b9b`.
**Bước 5 `325ec3d`, bước 6 `0f1b004` đã commit. Bước 7 `53d9f44` đã commit.** Reviewer đã soát phase 4 (2026-11-13): 0 blocker, 11 major, 14 minor; boss đã xác minh các điểm chính. Sửa review đã commit `12bbc47`. Phase test 4 `0febc7a`, xáo lựa chọn mcq `7cf05bc` đã commit. Bước 9 p5-01 `0b54b49` đã commit. Bước 10 p5-02 `d2416cf` đã commit. Ghim scipy `67a7aba`, bước 11 p5-03 `6bcb761` đã commit. Bước 12 p5-04 `7cd65aa` đã commit. Bước 13 p5-05 `8612c8f` đã commit. Reviewer đã soát phase 5 (2026-11-14): 1 blocker, 10 major, 27 minor, xem `tasks/m3-p5-review.md`; bước 13b sửa cả 38 điểm đã commit `e0a633b`. Bước 14 phase test 5 `44d05fa` đã commit. Bước 15 mock exam Data & ML `d9b7437` đã commit. Bước 15b bảng Visualize `bc7ba47` đã commit. Bước 16 tài liệu + đọc mẫu VI (3 bài, 55 chỗ sửa) đã commit `80f9579`. **M3 xong (2026-11-14); kế tiếp M4.**
Lệnh commit gợi ý:
`git add curriculum/phase-04-data/p4-04-matplotlib curriculum/glossary.yaml tools/validate.py curriculum/conftest.py && git commit -m "Add p4-04 plotting lesson; default matplotlib to Agg in validate and pytest"`

Tiếp theo: bước 6 `m3-p4-05-sql` (SQLite) theo `/delegate`. Quy tắc output phase 4–5 nằm đầu `tasks/M3-PLAN.md` (Pyodide wasm32: NumPy int là int32).
Worker không có trình duyệt: boss tự kiểm tra trong app (Visualize, chấm ex02 trên Pyodide).
Prompt để chạy lại: `Đọc tasks/PROGRESS.md và tasks/M3-PLAN.md, commit bước 5 nếu user đồng ý rồi /delegate bước 6.`
