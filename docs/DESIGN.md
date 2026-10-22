# Nền tảng học Python for AI Engineer: Thiết kế & Hướng dẫn triển khai

> Phạm vi hiện tại: **sản phẩm cá nhân** (1 người dùng). Nếu phát hành sau này, bổ sung auth, backend, chi phí AI tutor ở mục 11.

## 1. Mục tiêu

- Lộ trình Python đầy đủ, hướng **AI Engineer**, từ người mới hoàn toàn đến mức làm được RAG và agent đơn giản.
- Đầu ra thuần thục: có example, exercise, quiz, mini-project, mock exam.
- **Không** nhắm trình độ pro/senior. Phần nâng cao để ở mục "Đọc thêm".
- Song ngữ **Việt/Anh**, có nút switch.
- Ưu tiên **web app** đẹp, dễ thao tác, trực quan.

## 2. Nguyên tắc cốt lõi

1. **Giáo trình là code.** Mỗi bài là một thư mục có test tự động. Example phải chạy được, starter phải fail, solution phải pass.
2. **Một nguồn nội dung, hai ngôn ngữ**, cùng ID và cấu trúc.
3. **Vertical slice trước.** Làm trọn chuỗi nội dung → build → UI → chạy code → chấm → i18n với khối lượng nhỏ, rồi mới mở rộng.
4. **Code không dịch**, chỉ dịch phần giải thích, đề bài, comment. Thuật ngữ giữ tiếng Anh, có glossary song ngữ.

## 3. Lộ trình nội dung (9 phase)

| Phase | Nội dung |
|---|---|
| 0 | Môi trường: uv/venv, Git, VS Code, terminal |
| 1 | Python core: kiểu dữ liệu, control flow, hàm, module, file I/O, exception |
| 2 | Python trung cấp: OOP, dataclass, typing cơ bản, generator, decorator, context manager |
| 3 | Chất lượng code: pytest, ruff, logging, debug |
| 4 | Data: NumPy, Pandas, Matplotlib, SQL cơ bản |
| 5 | ML: toán vừa đủ (có "cầu nối toán" bằng hình ảnh), scikit-learn, đánh giá mô hình |
| 6 | Deep learning: PyTorch cơ bản, training loop, Hugging Face, fine-tune nhỏ |
| 7 | LLM/GenAI: API, structured output, embeddings, vector DB, RAG, tool use, agent đơn giản, evals |
| 8 | Production: FastAPI, Docker cơ bản, cache, monitoring, cost/latency |

- Mỗi phase kết thúc bằng **mini-project + phase test**.
- Mini-project trọng yếu: data analysis, ML, RAG, agent đơn giản.
- Cuối lộ trình: **2 capstone** (RAG chatbot có eval; agent dùng tool) + **mock exam tổng**.
- **Rút gọn/bỏ:** async nâng cao, metaclass, C extension, toán chứng minh, Kubernetes, profiling sâu (đưa vào "Đọc thêm").

**Hai track:**
- **Track A (mới hoàn toàn):** bài nhỏ 5–10 phút, ví dụ từng bước, Parsons problem, code điền chỗ trống trước khi tự viết.
- **Track B (biết cơ bản):** placement test cho bỏ qua phase 0–1.

## 4. Cấu trúc repo nội dung

```
curriculum/
  phase-XX-name/
    lesson-YY/
      lesson.en.md   lesson.vi.md
      examples/              # code chạy được + output kỳ vọng
      exercises/
        starter.py
        test_exercise.py     # pytest
        solution.py          # ẩn khỏi UI cho tới khi thử đủ
        prompt.en.md  prompt.vi.md
      quiz.yaml              # mỗi câu có en: và vi:
      meta.yaml              # level, tags, prerequisites, thời lượng, ngày review
    phase-test.yaml
  capstones/
  exams/
  glossary.yaml              # thuật ngữ song ngữ
tools/                       # build, validate, parity check
apps/web/                    # web app
```

## 5. Kiến trúc web app (bản cá nhân)

| Lớp | Lựa chọn |
|---|---|
| Frontend | Next.js + TypeScript + Tailwind + shadcn/ui, dark/light mode |
| i18n | next-intl, không nhúng chuỗi cứng, fallback EN + nhãn "chưa dịch" |
| Editor | Monaco |
| Chạy Python | **Pyodide** trong trình duyệt (phase 0–5), lazy load + cache NumPy/Pandas |
| Chạy nặng (phase 6–8) | **Runner cục bộ**: FastAPI nhỏ chạy trên máy bạn, hoặc notebook có sẵn |
| Lưu tiến độ | localStorage/IndexedDB + nút export/import JSON. **Không backend, không auth** |
| Nội dung | Build từ `curriculum/` thành static pages, chạy hoàn toàn local |
| Gọi API LLM trong bài tập | Dùng mock/fixture có sẵn, không cần API key khi tập |

**Màn hình:** Onboarding + placement test, Dashboard (skill tree, streak, chủ đề yếu), Lesson view (chia đôi lý thuyết/editor), Exercise (test xanh/đỏ, hint 3 tầng), Quiz & flashcard (trắc nghiệm, đoán output, điền chỗ trống, Parsons), Mock exam (đếm giờ, báo cáo theo chủ đề), Review hằng ngày (spaced repetition), Portfolio.

**UI:** sạch, nhiều khoảng trắng, một màu nhấn, animation nhẹ. Lý thuyết/quiz/flashcard dùng tốt trên điện thoại, editor ưu tiên desktop.

## 6. Tính năng

**Làm ở bản đầu:** placement test, spaced repetition, mock exam có điểm theo chủ đề, debug challenge (sửa code có bug), dashboard tiến độ, ngân hàng câu hỏi phỏng vấn AI Engineer.

**Làm sau:** AI tutor (hint 3 tầng, dùng API key của bạn), AI code review theo rubric, portfolio tự động, eval chất lượng quiz.

## 7. Phân công model

| Model | Vai trò |
|---|---|
| **Opus** | Syllabus, dependency giữa bài, placement test, mock exam, kiến trúc web, review mẫu (100% capstone và mock exam, 15–20% còn lại) |
| **Sonnet** | Viết lesson, exercise + test + solution, UI component, dịch VI |
| **Haiku** | Quiz variants, flashcard, hint, tag metadata, kiểm tra parity VI/EN, lint nội dung |

Opus chỉ ở đầu (thiết kế) và cuối (review) pipeline. Phần lớn token chạy ở Sonnet và Haiku.

## 8. Phân công mode

- **Code:** toàn bộ repo, web app, Pyodide runner, autograder, CI, parity check. Đây là phần việc lớn nhất.
- **Cowork:** xuất PDF giáo trình song ngữ, cheat sheet, đề thi in được, bảng theo dõi tiến độ (xlsx). Chỉ dùng ở M5, và cần hỏi ý bạn trước.

## 9. Pipeline sản xuất nội dung

1. **Thiết kế** (Opus): syllabus, learning outcomes, prerequisite graph, template bài.
2. **Soạn** (Sonnet, song song theo lesson): EN trước, rồi dịch VI.
3. **Mở rộng** (Haiku): quiz variants, flashcard, hint, tag.
4. **Cổng tự động** (Code): chạy mọi example; starter fail, solution pass; ruff; validate schema; parity VI/EN (đủ field, cùng số câu, cùng code block, cùng đáp án).
5. **Review** (Opus, lấy mẫu).
6. **Đóng gói** (Code cho web, Cowork cho tài liệu).
7. **Vòng phản hồi:** câu nào bạn sai nhiều thì viết lại giải thích.

## 10. Lộ trình triển khai

| Mốc | Kết quả |
|---|---|
| **M0** | Chốt syllabus, template bài, schema nội dung, design system UI, bộ validate |
| **M1** | **Vertical slice:** phase 1 với 3–5 bài hoàn chỉnh, song ngữ, Pyodide, quiz, exercise, dashboard cơ bản |
| **M2** | Hoàn thiện phase 1–3, placement test, spaced repetition |
| **M3** | Phase 4–5, mock exam |
| **M4** | Phase 6–8, runner cục bộ, (tùy chọn) AI tutor + code review |
| **M5** | Capstone, portfolio, xuất PDF (Cowork), đánh bóng |

**Tiêu chí thuần thục:** hoàn thành exercise mỗi phase ≥ 80%, vượt phase test, nộp 4 mini-project trọng yếu, đạt ≥ 80% mock exam tổng.

## 11. Khi phát hành sau này (chưa làm)

Thêm auth (email/Google), Postgres + FastAPI cho tiến độ, sandbox server cho code nặng, giới hạn lượt AI tutor (Haiku cho hint tầng 1–2, Sonnet cho tầng 3), rate limit, analytics. Vì tiến độ đã tách thành lớp lưu trữ riêng ngay từ đầu, việc này chỉ cần đổi adapter lưu trữ.

## 12. Rủi ro

- Pyodide + thư viện nặng tải chậm lần đầu → lazy load và cache.
- Chất lượng bản dịch → bạn đọc mẫu, không chỉ dựa kiểm tra tự động.
- Nội dung LLM/AI lỗi thời nhanh → phase 7 tách module, gắn ngày review trong `meta.yaml`.
- Phình scope → luôn hoàn tất vertical slice trước.

---

# Hướng dẫn triển khai bằng Claude Code

## A. Chuẩn bị

1. Cài Claude Code theo hướng dẫn chính thức (docs.claude.com), rồi đăng nhập.
2. Cài Node 20+, Python 3.11+, `uv`, Git, pnpm.
3. Tạo thư mục dự án và khởi tạo git:
   ```bash
   mkdir python-ai-platform && cd python-ai-platform
   git init
   ```
4. Chép file này vào repo thành `docs/DESIGN.md`. Đây là nguồn sự thật cho mọi phiên làm việc.
5. Mở Claude Code trong thư mục: `claude`.

## B. Thiết lập "bộ nhớ" dự án

Chạy `/init` để Claude tạo `CLAUDE.md`, rồi chỉnh để có các mục sau (ngắn, dưới ~100 dòng):

```markdown
# Dự án: Python for AI Engineer platform
Thiết kế đầy đủ: @docs/DESIGN.md

## Quy tắc
- Bản cá nhân: KHÔNG auth, KHÔNG backend. Tiến độ lưu localStorage/IndexedDB qua lớp storage adapter.
- Nội dung song ngữ: mọi lesson/quiz/exercise có bản en và vi, cùng ID.
- Code không dịch; thuật ngữ kỹ thuật giữ tiếng Anh.
- Không nhúng chuỗi UI cứng, dùng next-intl.
- Mọi exercise: starter fail, solution pass.

## Lệnh
- Validate nội dung: `uv run python tools/validate.py`
- Test nội dung: `uv run pytest curriculum`
- Web dev: `pnpm --filter web dev`
- Web build/lint/typecheck: `pnpm --filter web build|lint|typecheck`

## Quy trình
- Làm theo mốc M0→M5 trong docs/DESIGN.md. Chỉ làm mốc hiện tại.
- Trước khi báo xong: chạy validate + test + typecheck.
- Commit nhỏ, mỗi commit một việc.
```

## C. Subagent theo model

Tạo các file trong `.claude/agents/` (định dạng markdown có frontmatter; kiểm tra tên trường mới nhất bằng `/agents` hoặc docs):

`.claude/agents/content-writer.md`
```markdown
---
name: content-writer
description: Viết lesson, example, exercise + pytest + solution cho một lesson. Dùng khi cần soạn nội dung bài học.
model: sonnet
---
Bạn viết nội dung theo template trong docs/DESIGN.md mục 4. Viết EN trước, rồi VI tự nhiên.
Mỗi exercise có starter.py, test_exercise.py, solution.py. Chạy pytest để xác nhận:
starter fail, solution pass. Giữ giọng văn đơn giản cho người mới.
```

`.claude/agents/quiz-factory.md`
```markdown
---
name: quiz-factory
description: Sinh quiz.yaml, flashcard, hint 3 tầng, tag metadata cho lesson đã có. Việc khối lượng lớn.
model: haiku
---
Sinh quiz song ngữ theo schema trong tools/schema. Đa dạng: trắc nghiệm, đoán output,
điền chỗ trống, Parsons. Chạy validate sau khi tạo.
```

`.claude/agents/reviewer.md`
```markdown
---
name: reviewer
description: Review độ chính xác, độ khó, lỗi sư phạm và parity VI/EN của nội dung. Dùng trước khi chốt một phase.
model: opus
tools: Read, Grep, Glob, Bash
---
Chỉ đọc và báo cáo, không sửa. Liệt kê lỗi theo mức nghiêm trọng, kèm đường dẫn file và đề xuất sửa.
```

Phiên chính nên dùng **Opus cho M0 (thiết kế)** và **Sonnet cho phần code web**. Đổi model bằng `/model`.

## D. Lệnh tùy chỉnh (tùy chọn)

`.claude/commands/new-lesson.md`:
```markdown
Tạo lesson mới: $ARGUMENTS
1. Dùng subagent content-writer soạn lesson + exercise.
2. Dùng subagent quiz-factory sinh quiz.
3. Chạy `uv run python tools/validate.py` và `uv run pytest` cho lesson đó.
4. Báo kết quả ngắn gọn.
```
Dùng: `/new-lesson phase-01/lesson-03 vòng lặp for`.

## E. Hook (tùy chọn, nên có)

Trong `.claude/settings.json`, thêm hook chạy validate sau khi sửa file trong `curriculum/` để lỗi schema/parity lộ ra ngay. Dùng `/hooks` để cấu hình qua giao diện.

## F. Lộ trình prompt theo từng mốc

Luôn bắt đầu bằng **Plan mode** (nhấn `Shift+Tab` để chuyển) và duyệt kế hoạch trước khi cho sửa file. Mỗi mốc: một nhánh git, xong thì merge.

### M0: Nền móng (model: Opus, Plan mode trước)
```
Đọc @docs/DESIGN.md. Thực hiện M0:
1. Syllabus chi tiết: danh sách bài cho phase 0–3 (phase 4–8 chỉ cần outline), kèm learning outcomes và prerequisite.
2. Template bài học và JSON Schema cho meta.yaml, quiz.yaml.
3. Dựng monorepo: curriculum/, tools/, apps/web (Next.js + TS + Tailwind + shadcn/ui + next-intl).
4. tools/validate.py: kiểm schema, parity VI/EN, chạy starter-fail/solution-pass.
5. Design system UI cơ bản (màu, typography, dark/light).
Chưa viết nội dung bài học. Đưa kế hoạch cho tôi duyệt trước.
```

### M1: Vertical slice (Sonnet làm chính)
```
Thực hiện M1 theo docs/DESIGN.md:
- Dùng subagent content-writer viết 3 bài phase 1 (biến & kiểu dữ liệu, điều kiện, vòng lặp), mỗi bài có example + 2 exercise.
- Dùng quiz-factory sinh quiz cho 3 bài.
- Web: trang Dashboard, Lesson view (chia đôi), Monaco + Pyodide chạy code, chạy pytest-style test trong browser, Quiz, nút switch VI/EN, lưu tiến độ localStorage qua storage adapter.
Xong thì chạy validate, build, typecheck. Dùng subagent reviewer review kết quả.
```
**Kiểm thu M1:** tự học thử 3 bài như người dùng thật, ghi lại điểm vướng. Đây là bước quyết định trước khi mở rộng.

### M2 → M5
Mỗi mốc dùng cấu trúc: *đọc DESIGN.md mục tương ứng → Plan mode → duyệt → triển khai → validate/test → reviewer → commit*.

- **M2:** phase 1–3 (song song nhiều lesson bằng subagent), placement test, spaced repetition.
- **M3:** phase 4–5, mock exam (đếm giờ, báo cáo theo chủ đề). Opus thiết kế bộ đề.
- **M4:** phase 6–8, runner Python cục bộ (FastAPI) cho code nặng; AI tutor và code review nếu muốn (dùng API key của bạn, lưu `.env` cục bộ, không commit).
- **M5:** capstone, portfolio, rồi xuất PDF/cheat sheet/đề in (Cowork hoặc script). Cowork sẽ hỏi bạn trước khi dùng.

## G. Mẹo làm việc hiệu quả

- **Một phiên, một mục tiêu.** Dùng `/clear` giữa các nhiệm vụ để khỏi tràn ngữ cảnh. Kiến thức dự án nằm ở `CLAUDE.md` và `docs/DESIGN.md`, không cần nhớ trong chat.
- **Chạy song song:** nhờ Claude giao nhiều lesson cho `content-writer` cùng lúc. Có thể dùng git worktree nếu muốn nhiều phiên độc lập.
- **Cổng chất lượng là test, không phải niềm tin.** Luôn yêu cầu chạy `validate` và `pytest` trước khi nhận kết quả.
- **Cập nhật DESIGN.md** mỗi khi đổi quyết định, để các phiên sau không lệch hướng.
- **Commit thường xuyên**, dễ quay lại khi Claude đi sai hướng. `Esc` để dừng, `Esc Esc` để quay lại bước trước.
- **Kiểm soát chi phí:** Haiku cho việc hàng loạt, Sonnet cho viết/code, Opus chỉ cho thiết kế và review.
- **Đọc mẫu bản dịch VI** của từng phase, vì kiểm tra tự động không bắt được văn phong gượng.

## H. Việc đầu tiên nên làm hôm nay

1. Tạo repo, chép file này thành `docs/DESIGN.md`.
2. Chạy `claude`, `/init`, chỉnh `CLAUDE.md` theo mục B.
3. Tạo 3 subagent ở mục C.
4. Chuyển Opus + Plan mode, dán prompt M0.
