# PyAI Path: Python for AI Engineers

Nền tảng học Python cá nhân, song ngữ VI/EN, hướng AI Engineer. Thiết kế: [docs/DESIGN.md](docs/DESIGN.md).

**Trạng thái:** M0 + M1 (vertical slice) xong: Phase 1 có 6 bài (5 bài + mini-project), phase test,
placement test, mock exam, 30 câu phỏng vấn, 49 thuật ngữ. Phase 0, 2–8 đã có trong syllabus (hiển thị
"Sắp ra mắt").

## Chạy

Cần: Node 20+, pnpm (qua corepack), Python 3.11+, uv.

```bash
pnpm install
uv sync
pnpm dev            # http://localhost:3000 (tự build nội dung trước)
```

Bản tĩnh (không cần server Node):

```bash
pnpm build                       # -> apps/web/out
pnpm --filter web start          # phục vụ out/ tại http://localhost:3000
```

Lần đầu mở cần mạng để tải Pyodide (Python trong trình duyệt) và Monaco editor từ CDN; sau đó trình duyệt cache lại.

## Cổng chất lượng nội dung

```bash
uv run python tools/validate.py   # schema, parity VI/EN, chạy example, starter fail / solution pass, đáp án quiz, ruff
uv run pytest curriculum          # test của mọi exercise với solution
pnpm typecheck                    # TypeScript + kiểm tra en.json/vi.json cùng khóa
```

## Tính năng

- **Dashboard**: tiếp tục bài đang học, streak, XP theo mục tiêu ngày, thẻ cần ôn, cây kỹ năng 9 phase,
  chủ đề yếu, heatmap hoạt động, tiêu chí thuần thục.
- **Lesson view chia đôi**: lý thuyết (callout, code có nút "Chạy thử") | Monaco + Python (Pyodide trong Web
  Worker, nút Dừng cho vòng lặp vô hạn). Kéo thanh giữa để đổi tỉ lệ. Mobile: chuyển Nội dung / Editor.
- **Bài tập**: viết code, điền chỗ trống (highlight `___`), debug challenge, project. Test xanh/đỏ kèm giá trị
  thực tế vs kỳ vọng, hint 3 tầng, lời giải mở sau 3 lần thử. Code tự lưu.
- **Quiz**: trắc nghiệm, đoán output, điền chỗ trống, Parsons (sắp xếp code). Câu sai vào bộ ôn tập.
- **Ôn tập** (spaced repetition, SM-2): flashcard + câu từng làm sai.
- **Kiểm tra**: phase test, placement test (Track B bỏ qua phase 0–1), mock exam đếm giờ, báo cáo theo chủ đề.
- **Sân chơi code**, **Thuật ngữ** song ngữ, **Ngân hàng phỏng vấn**, **Portfolio**, **Cài đặt** (export/import JSON).
- Song ngữ VI/EN chuyển tức thì; nội dung thiếu bản dịch tự hiển thị EN kèm nhãn. Dark/light mode.

## Cấu trúc

```
curriculum/           nội dung (YAML + Markdown + .py), xem docs/CONTENT_GUIDE.md
tools/validate.py     cổng tự động
tools/build_content.py  curriculum -> apps/web/src/generated (JSON)
tools/pyrunner/runner.py  test runner tương thích pytest, chạy cả trong Pyodide lẫn CPython
apps/web/             Next.js (static export), Tailwind v4, next-intl, Monaco, Pyodide
.claude/agents/       content-writer (Sonnet), quiz-factory (Haiku), reviewer (Opus)
```

Thêm bài mới: `/new-lesson p2-01-comprehensions` trong Claude Code, hoặc làm theo docs/CONTENT_GUIDE.md.
