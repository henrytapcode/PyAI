# Dự án: Python for AI Engineer platform
Thiết kế đầy đủ: @docs/DESIGN.md
Template nội dung: @docs/CONTENT_GUIDE.md

## Quy tắc
- Bản cá nhân: KHÔNG auth, KHÔNG backend. Tiến độ lưu localStorage qua storage adapter
  (`apps/web/src/lib/storage.ts`). Đổi backend sau này = viết adapter mới.
- Nội dung song ngữ: mọi lesson/quiz/exercise có bản en và vi, cùng ID.
- Code không dịch (chỉ comment được dịch); thuật ngữ kỹ thuật giữ tiếng Anh.
- Không nhúng chuỗi UI cứng: dùng next-intl, thêm key vào cả `apps/web/messages/en.json` và `vi.json`.
- Mọi exercise: starter fail, solution pass (pytest VÀ runner trình duyệt `tools/pyrunner/runner.py`).
- Test exercise chỉ dùng: assert, pytest.raises, pytest.approx, pytest.mark.parametrize, capsys.

## Kiến trúc nhanh
- `curriculum/` nội dung (YAML + MD + .py) → `tools/build_content.py` → `apps/web/src/generated/` (gitignored).
- `apps/web`: Next.js (App Router, static export), Tailwind v4, shadcn-style UI trong `src/components/ui`,
  Monaco editor, Pyodide chạy trong Web Worker (`public/pyodide-worker.js`).
- Locale chuyển phía client (không routing theo locale) để switch VI/EN tức thì.

## Lệnh
- Validate nội dung: `uv run python tools/validate.py` (`--path <lesson dir>`, `--fast`)
- Test nội dung: `uv run pytest curriculum`
- Build nội dung cho web: `uv run python tools/build_content.py`
- Web dev: `pnpm --filter web dev` (tự build nội dung trước)
- Web build/typecheck: `pnpm --filter web build` / `pnpm --filter web typecheck`

## Quy trình
- Làm theo mốc M0→M5 trong docs/DESIGN.md. Hiện tại: M1 xong (vertical slice phase 1). Kế tiếp: M2.
- Trước khi báo xong: chạy validate + pytest + typecheck + build.
- Commit nhỏ, mỗi commit một việc.
