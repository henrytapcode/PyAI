# M5: capstone, portfolio, xuất PDF, đánh bóng (kế hoạch, 2026-11-18)

Nguồn: `docs/DESIGN.md` §3 (2 capstone + mock exam tổng), §6, §8 (Cowork chỉ dùng ở M5, phải hỏi trước), §10. Template bài: `docs/CONTENT_GUIDE.md`.
Quy trình như M4: `/delegate` (boss viết spec `tasks/<slug>.md`, Gemini làm, boss chạy lại cổng và xem trong app), mỗi bước một commit sau khi user duyệt. Capstone và mock exam: reviewer Opus soát 100% (DESIGN §7).

## Hiện trạng (đã kiểm 2026-11-18)
- `syllabus.yaml` có mục `capstones:` với 2 id (`cap-01-rag-chatbot`, `cap-02-tool-agent`), mới chỉ có title. Chưa có thư mục nội dung.
- `portfolio.yaml` có `cap-rag-chatbot`, `cap-tool-agent` chưa có `lesson`, nên app hiện "coming soon". Trang Learn và Portfolio đã có khu "Capstones".
- Mock exam: `mock-python-core` (phase 1–3), `mock-data-ml` (phase 4–5). Chưa có đề cho phase 6–8, chưa có đề tổng.
- Chưa có gì để xuất PDF.
- Còn lại từ M4: 33 cảnh báo "solution chép code bài học" của validator; picomatch có lỗ hổng chưa có bản vá.

## Quyết định cần user chốt (★ = đề xuất của boss)
1. ★ **Capstone là "bài" đủ cấu trúc**, nằm ở `curriculum/capstones/<id>/` (meta, lesson.en/vi.md, examples, exercises kind `project`, quiz ngắn). Build và validate coi chúng như lesson, nên dùng lại trang bài học, chấm bài, Visualize. Lesson của capstone là **brief + kiến trúc + tiêu chí chấm**, không dạy kiến thức mới.
   - Khác: thêm `phase-09-capstones` vào danh sách phase (ít sửa tool hơn, nhưng capstone lẫn vào lộ trình như phase thường).
2. ★ **Nội dung 2 capstone**, mỗi cái 3 exercise theo mốc, mỗi exercise yêu cầu phần mà bài cũ chưa làm (quy ước không chép bài học):
   - `cap-01-rag-chatbot`: (a) chatbot nhiều lượt có lịch sử hội thoại + citation + từ chối; (b) bộ eval (golden set, faithfulness/citation hit rate, hồi quy so với lần chạy trước); (c) dịch vụ FastAPI `/chat` + cache + `/metrics`. (a), (b) chạy Pyodide; (c) `runner: local` vì cần `TestClient`.
   - `cap-02-tool-agent`: (a) tool registry có phân quyền (allowlist theo request, tool nguy hiểm cần xác nhận); (b) retry có backoff với `FakeClock` + ngân sách token/chi phí mỗi request; (c) trace log từng bước + báo cáo tóm tắt (số bước, tool đã gọi, chi phí). Cả ba chạy Pyodide.
3. ★ **Mock exam:** thêm `mock-ai-engineer` (phase 6–8, 24 câu, 35 phút, giống 2 đề cũ) và `mock-final` (đề tổng, 40 câu trên phase 1–8, nặng phase 5–8, 60 phút, đạt 80%). Đề tổng là tiêu chí "thuần thục" của DESIGN §10.
4. **Xuất PDF** (DESIGN §8 nói dùng Cowork và phải hỏi bạn):
   - ★ Script `tools/export_pdf.py` trong repo: dựng HTML in được từ `apps/web/src/generated/` (giáo trình EN/VI, cheat sheet mỗi phase, đề thi in được kèm đáp án tách riêng) rồi in PDF bằng Chromium headless (Playwright). Lặp lại được mỗi khi nội dung đổi, không cần Cowork.
   - Khác: dùng Cowork như DESIGN viết (thủ công, mỗi lần đổi nội dung phải làm lại).
   - Bảng theo dõi tiến độ `.xlsx` (DESIGN §8): ★ bỏ, vì app đã có dashboard và export JSON.
5. ★ **Đánh bóng** (làm cuối, mỗi mục một bước nhỏ): giảm 33 cảnh báo chép code (sửa exercise cho có phần mới, hoặc ghi lý do giữ); soát luồng học đầu-cuối trong app (onboarding → bài → quiz → review → exam → portfolio) trên desktop và mobile; README cho người dùng; cập nhật DESIGN/CLAUDE.md "M5 xong".

## Quyết định đã chốt (user 2026-11-18: "chia nhỏ M5 ra và tiến hành theo thứ tự")
Theo các đề xuất ★ ở trên. Thêm: exercise được ghi `runner: local` riêng (cap-01 ex03 cần FastAPI `TestClient`), các exercise khác của capstone vẫn chạy Pyodide.

## Các bước (chia nhỏ)
| Bước | Slug | Nội dung | Trạng thái |
|---|---|---|---|
| 1a | `m5-01a-capstone-tools` | Schema (id `cap-NN-...`, phase `cap`), validate + build coi `syllabus.capstones` là bài trong `curriculum/capstones/`; `runner: local` ở mức exercise; test | `29fffe3` |
| 1b | `m5-01b-capstone-web` | Trang bài mở được capstone; thẻ capstone ở Learn/Portfolio dẫn tới bài khi sẵn sàng; Run/Test theo runner của exercise; i18n | `7f46770` |
| 2a | `m5-cap01-lesson` | cap-01: syllabus outcomes, meta, lesson EN+VI (brief, kiến trúc, 3 ý mới, mốc, tiêu chí chấm), 3 examples | `7f4a002` |
| 2b | `m5-cap01-ex01` | cap-01 ex01 `ChatBot`: lịch sử có ngân sách token, viết lại câu nối tiếp, citation, từ chối | `8cec468` |
| 2c | `m5-cap01-ex02` | cap-01 ex02: eval theo hội thoại + so baseline (fixed/broken) | `b594a95` |
| 2d | `m5-cap01-ex03` | cap-01 ex03: dịch vụ FastAPI có session (TTL, giới hạn số session, 404) (`runner: local`); p8-05 đã có cache + metrics nên không làm lại | `c429894` |
| 2e | `m5-cap01-quiz` | cap-01 quiz + portfolio `lesson`, cập nhật pitch | `cfc94c5` |
| 2f | `m5-cap01-review` | Reviewer Opus 100%, sửa | `dcb33c8` |
| 3a–3f | `m5-cap02-*` | cap-02 tool agent, cùng nhịp 2a–2f (ex01 phân quyền tool, ex02 retry + ngân sách, ex03 trace + báo cáo) | `85c22f1` |
| 4 | `m5-mock-ai` | Mock exam phase 6–8 (24 câu) | `85c22f1` |
| 5 | `m5-mock-final` | Mock exam tổng (40 câu) | `85c22f1` |
| 5b | `m5-mock-review` | Reviewer Opus/Argon 100% cả 2 đề, sửa | `85c22f1` |
| 6a | `m5-pdf-book` | `tools/export_pdf.py`: giáo trình EN/VI (pure stdlib + Chrome/Edge headless) | `75c032e` |
| 6b | `m5-pdf-sheets` | Cheat sheet mỗi phase + đề in được, đáp án tách riêng | `75c032e` |
| 7a–7c | `m5-overlap-*` | 33 cảnh báo chép code, chia theo nhóm phase | Wave 2B (done — M5 100%) |
| 8 | `m5-polish` | Soát luồng/route tĩnh trong `apps/web/out/`, README | `75c032e` |
| 9 | `m5-docs` | DESIGN/CONTENT_GUIDE/M5-PLAN: cập nhật Wave 2A & Wave 2B (M5 xong) | `75c032e` + Wave 2B |

Cổng mỗi bước: validate (`--path` hoặc toàn bộ), `uv run python -m pytest`, `EXERCISE_TARGET=starter` (mọi test fail), ruff, typecheck + build (tắt dev server trước), xem trong trình duyệt của app.
