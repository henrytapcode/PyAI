<div align="center">

# PyAI Path

**Learn Python the way an AI engineer needs it.**
**Học Python theo đúng hướng của một AI Engineer.**

[![Deploy](https://github.com/henrytapcode/PyAI/actions/workflows/pages.yml/badge.svg)](https://github.com/henrytapcode/PyAI/actions/workflows/pages.yml)
![Next.js](https://img.shields.io/badge/Next.js-static_export-000?logo=nextdotjs)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![Pyodide](https://img.shields.io/badge/Pyodide-in--browser-F7C948)
![i18n](https://img.shields.io/badge/lang-EN%20%7C%20VI-6c5ce7)

**[Live demo](https://henrytapcode.github.io/PyAI/)** · [English](#english) · [Tiếng Việt](#tiếng-việt)

</div>

---

## English

PyAI Path is a bilingual (EN/VI) interactive Python course for people who want to become AI engineers. Everything runs in your browser: write code, run tests, take quizzes and track progress. No install, no account, no server.

### Highlights

- **Run Python in the browser.** Pyodide runs in a Web Worker, with a Stop button for infinite loops.
- **Split lesson view.** Theory with mermaid diagrams and trace tables on the left, Monaco editor on the right. A **Visualize** button steps through code and shows variables changing.
- **Real exercises.** Write code, fill in blanks, debug, or build a mini-project. Tests show green/red with actual vs. expected values, 3-tier hints, and the solution unlocks after 3 attempts.
- **Quizzes.** Multiple choice, predict-the-output, fill-in, and Parsons problems (reorder code). Wrong answers go to your review queue.
- **Spaced repetition (SM-2)** for flashcards and missed questions.
- **Assessment.** Phase tests, a placement test (Track B skips phases 0–1), timed mock exams with per-topic reports.
- **Dashboard.** Streak, daily XP goal, due cards, 9-phase skill tree, weak topics, activity heatmap.
- **Extras.** Code playground, bilingual glossary, interview question bank, portfolio, JSON export/import of your progress.
- **Bilingual and themed.** Switch EN/VI instantly; missing translations fall back to EN with a label. Dark and light mode.

### Curriculum

| Phase | Topic | Status |
|---|---|---|
| 0 | Environment: uv, Git, VS Code, terminal | Planned |
| 1 | Python core | Available |
| 2 | Intermediate Python: OOP, dataclasses, typing, generators, decorators | Available |
| 3 | Code quality: pytest, ruff, logging, debugging | Available |
| 4–5 | Data (NumPy, Pandas, SQL) and ML basics | Planned |
| 6–8 | Deep learning, LLM/GenAI, production | Planned |

### Quick start

Requirements: Node 20+, pnpm (via corepack), Python 3.11+, [uv](https://docs.astral.sh/uv/).

```bash
pnpm install
uv sync
pnpm dev            # http://localhost:3000 (builds content first)
```

Static build:

```bash
pnpm build                    # outputs apps/web/out
pnpm --filter web start       # serves out/ at http://localhost:3000
```

The first visit needs internet to download Pyodide and the Monaco editor; the browser caches them afterwards.

### Quality gates

Every lesson is code: examples run, starters fail, solutions pass, EN and VI stay in parity.

```bash
uv run python tools/validate.py   # schema, EN/VI parity, examples, starter fail / solution pass, quiz answers, ruff
uv run pytest curriculum          # every exercise's tests against its solution
pnpm typecheck                    # TypeScript + en.json/vi.json key parity
```

### Project layout

```text
curriculum/                 content: YAML + Markdown + .py
tools/validate.py           automated content gate
tools/build_content.py      curriculum -> apps/web/src/generated (JSON)
tools/pyrunner/runner.py    pytest-compatible runner for Pyodide and CPython
apps/web/                   Next.js (static export), Tailwind v4, next-intl, Monaco, Pyodide
.github/workflows/pages.yml validate, build, deploy to GitHub Pages
```

### Deployment

Pushes to `main` run `.github/workflows/pages.yml`: validate content, build the static site with the repository name as base path, deploy to GitHub Pages. In **Settings → Pages**, set the source to **GitHub Actions**.

### Contributing a lesson

Follow the lesson template (folder layout, tone, quiz rules), then run the quality gates above. All three must be green before a lesson is considered done.

---

## Tiếng Việt

PyAI Path là khóa học Python tương tác song ngữ (EN/VI) cho người muốn trở thành AI Engineer. Mọi thứ chạy ngay trong trình duyệt: viết code, chạy test, làm quiz và theo dõi tiến độ. Không cần cài đặt, không cần tài khoản, không cần server.

### Điểm nổi bật

- **Chạy Python trong trình duyệt.** Pyodide chạy trong Web Worker, có nút Dừng cho vòng lặp vô hạn.
- **Lesson view chia đôi.** Lý thuyết có sơ đồ mermaid và bảng trace bên trái, Monaco editor bên phải. Nút **Visualize** chạy từng bước và cho thấy biến thay đổi.
- **Bài tập thực chiến.** Viết code, điền chỗ trống, debug hoặc làm mini-project. Test xanh/đỏ kèm giá trị thực tế so với kỳ vọng, hint 3 tầng, lời giải mở sau 3 lần thử.
- **Quiz.** Trắc nghiệm, đoán output, điền chỗ trống và Parsons (sắp xếp code). Câu sai vào bộ ôn tập.
- **Ôn tập ngắt quãng (SM-2)** cho flashcard và các câu từng làm sai.
- **Kiểm tra.** Phase test, placement test (Track B bỏ qua phase 0–1), mock exam đếm giờ có báo cáo theo chủ đề.
- **Dashboard.** Streak, mục tiêu XP mỗi ngày, thẻ cần ôn, cây kỹ năng 9 phase, chủ đề yếu, heatmap hoạt động.
- **Tiện ích.** Sân chơi code, thuật ngữ song ngữ, ngân hàng phỏng vấn, portfolio, export/import tiến độ bằng JSON.
- **Song ngữ và giao diện.** Chuyển EN/VI tức thì; nội dung thiếu bản dịch tự hiển thị EN kèm nhãn. Có dark/light mode.

### Lộ trình

| Phase | Chủ đề | Trạng thái |
|---|---|---|
| 0 | Môi trường: uv, Git, VS Code, terminal | Sắp ra mắt |
| 1 | Python core | Đã có |
| 2 | Python trung cấp: OOP, dataclass, typing, generator, decorator | Đã có |
| 3 | Chất lượng code: pytest, ruff, logging, debug | Đã có |
| 4–5 | Dữ liệu (NumPy, Pandas, SQL) và nền tảng ML | Sắp ra mắt |
| 6–8 | Deep learning, LLM/GenAI, production | Sắp ra mắt |

### Chạy nhanh

Cần: Node 20+, pnpm (qua corepack), Python 3.11+, [uv](https://docs.astral.sh/uv/).

```bash
pnpm install
uv sync
pnpm dev            # http://localhost:3000 (tự build nội dung trước)
```

Bản tĩnh:

```bash
pnpm build                    # xuất ra apps/web/out
pnpm --filter web start       # phục vụ out/ tại http://localhost:3000
```

Lần đầu truy cập cần mạng để tải Pyodide và Monaco editor; sau đó trình duyệt cache lại.

### Cổng chất lượng

Mỗi bài học là code: example chạy được, starter fail, solution pass, EN và VI luôn khớp nhau.

```bash
uv run python tools/validate.py   # schema, parity EN/VI, example, starter fail / solution pass, đáp án quiz, ruff
uv run pytest curriculum          # test của mọi exercise với solution
pnpm typecheck                    # TypeScript + kiểm tra en.json/vi.json cùng khóa
```

### Cấu trúc dự án

```text
curriculum/                 nội dung: YAML + Markdown + .py
tools/validate.py           cổng kiểm tra nội dung tự động
tools/build_content.py      curriculum -> apps/web/src/generated (JSON)
tools/pyrunner/runner.py    test runner tương thích pytest, chạy trong Pyodide và CPython
apps/web/                   Next.js (static export), Tailwind v4, next-intl, Monaco, Pyodide
.github/workflows/pages.yml validate, build, deploy lên GitHub Pages
```

### Triển khai

Mỗi lần push lên `main`, `.github/workflows/pages.yml` sẽ validate nội dung, build site tĩnh với tên repo làm base path, rồi deploy lên GitHub Pages. Trong **Settings → Pages**, đặt Source là **GitHub Actions**.

### Đóng góp bài học

Làm theo template bài học (cấu trúc thư mục, giọng văn, quy tắc quiz), rồi chạy ba cổng chất lượng ở trên. Cả ba phải xanh thì bài mới được coi là xong.
