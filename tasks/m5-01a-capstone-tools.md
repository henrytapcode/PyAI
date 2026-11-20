# M5 bước 1a: hạ tầng capstone phía tools (validate + build + schema)

## Mục tiêu
Capstone được viết như một bài học đủ cấu trúc, nằm ở `curriculum/capstones/<id>/` (meta.yaml, lesson.en/vi.md, examples, exercises, quiz.yaml, giống hệt layout bài thường trong `docs/CONTENT_GUIDE.md`). Bước này chỉ làm cho **tools** hiểu chúng. Chưa viết nội dung capstone, chưa sửa web.

Danh sách capstone vẫn ở `curriculum/syllabus.yaml`, mục `capstones:` (không thêm vào `phases`). Mỗi mục có cùng các trường như một lesson trong phase: `id`, `title`, `prerequisites`, `outcomes`, `runner` (tùy chọn), `kind` (tùy chọn). Thư mục chứa: `curriculum/capstones/`. Mã phase của capstone: `cap`.

## File được phép sửa/tạo
- `tools/validate.py`
- `tools/build_content.py`
- `tools/schema/meta.schema.json`, `tools/schema/exercise.schema.json`, `tools/schema/quiz.schema.json` (chỉ nếu pattern id cần mở rộng)
- `tools/test_validate.py`, và tạo `tools/test_build_content.py` nếu cần
- `curriculum/syllabus.yaml`: **chỉ** mục `capstones:` (thêm `prerequisites`, xem dưới)
- `tasks/m5-01a-capstone-tools.report.md`

## Không được đụng
- `apps/**`, `packages/**`, `docs/**`, `CLAUDE.md`, mọi nội dung trong `curriculum/` ngoài mục `capstones:` của syllabus.
- Không tạo thư mục `curriculum/capstones/` thật trong repo (test dùng thư mục tạm).
- Không đổi hành vi với các bài phase 1–8 hiện có.

## Việc cần làm
1. **Schema**
   - `meta.schema.json`: `id` chấp nhận thêm `^cap-[0-9]{2}-[a-z0-9-]+$`; `phase` chấp nhận thêm `cap`.
   - `exercise.schema.json`: `id` chấp nhận thêm `^cap-[0-9]{2}-ex[0-9]{2}$`. Thêm trường tùy chọn `runner` với `enum: ["local"]`.
   - Quiz: id câu hỏi/flashcard hiện là `^[a-z0-9-]+$`, đã đủ cho `cap-01-q01`; chỉ sửa nếu chỗ khác chặn.
2. **validate.py**
   - Tách một hàm dùng chung, ví dụ `lesson_groups(syllabus) -> list[dict]`, trả về các phase như cũ **cộng** một nhóm capstone `{"id": "cap", "dir": "capstones", "lessons": syllabus.get("capstones", [])}`. Dùng hàm này ở mọi chỗ đang lặp `syllabus["phases"]` để dựng `lesson_index`, kiểm `runner`/prerequisites ở syllabus, tìm thư mục bài, kiểm model HF (`check_missing_models`). Kiểm "phase-level runner bị cấm" vẫn chỉ áp cho phase thật.
   - Hệ quả mong muốn: portfolio `lesson: cap-01-rag-chatbot` hợp lệ khi id đó có trong `capstones:`; prerequisite của capstone phải là id bài có thật; meta `phase: cap` khớp.
   - Exercise có `runner: local` trong `exercise.yaml`: dùng timeout 60s như bài local cho starter/solution/alternatives của exercise đó (bài thường giữ 15s).
   - `--path curriculum/capstones/<id>` chạy được như với bài thường.
3. **build_content.py**
   - Với từng mục trong `capstones:`, nếu `curriculum/capstones/<id>/meta.yaml` tồn tại thì `build_lesson` và ghi `generated/lessons/<id>.json` như bài thường (kể cả `runner` của mục syllabus, flashcard/câu hỏi vào `review.json` với `lessonId`).
   - `catalog.json` → `capstones`: mỗi phần tử có cùng dạng summary như lesson trong phase (`id`, `order`, `kind`, `title`, `outcomes`, `prerequisites`, `ready`, và khi ready thì `summary`, `duration`, `tags`, `exerciseIds`, `questionCount`, `runner` nếu có). Capstone chưa có thư mục → `ready: false`, giữ `id`, `title` như hiện nay để web không vỡ.
   - Exercise có `runner` trong yaml thì trường đó có trong JSON (đã có nhờ `**meta`, chỉ cần xác nhận).
   - Tránh lặp code: tách phần dựng summary của một lesson thành hàm dùng chung cho phase và capstone.
4. **syllabus.yaml, mục `capstones:`** thêm `prerequisites`:
   - `cap-01-rag-chatbot`: `[p7-08-evals, p7-09-mini-project-rag, p8-05-mini-project]`
   - `cap-02-tool-agent`: `[p7-07-agents, p7-10-mini-project-agent, p8-04-monitoring]`
   Chưa thêm `outcomes` (bước 2a làm).
5. **Test** (chỉ dùng thư mục tạm, không ghi vào repo):
   - `lesson_groups` trả về nhóm `cap` với đúng `dir` và lessons.
   - Schema meta/exercise chấp nhận id `cap-01-rag-chatbot`, `cap-01-ex01`, phase `cap`, exercise `runner: local`; vẫn từ chối `runner: remote` và id sai dạng như `cap-1-x`.
   - Build: dựng một curriculum giả tối thiểu trong `tmp_path` (một phase với một bài, một capstone có meta + 1 exercise + quiz) hoặc tách hàm để test được mà không cần cả repo; kiểm `catalog["capstones"][0]["ready"] is True` và file `lessons/<cap id>.json` tồn tại; capstone không có thư mục thì `ready` là `False`. Nếu `build_content.py` dùng hằng `CURRICULUM`/`OUT` cố định, thêm tham số (mặc định như cũ) để test truyền thư mục tạm.

## Tiêu chí hoàn thành (checklist)
- [ ] Schema nhận id/phase capstone và exercise `runner: local`
- [ ] validate và build dùng chung một nguồn nhóm bài (phase + capstone), không lặp logic
- [ ] Portfolio trỏ `lesson` tới capstone sẽ hợp lệ khi capstone có trong syllabus
- [ ] `catalog.json` hiện tại: `capstones` có 2 phần tử `ready: false`, phase không đổi
- [ ] Test mới pass; toàn bộ test cũ pass
- [ ] Validate toàn bộ vẫn 0 lỗi (không có cảnh báo mới ngoài 33 cảnh báo chép code cũ)

## Lệnh kiểm tra
Chạy từ gốc repo `D:\Proj\python-ai-platform`:
```bash
uv run python -m pytest tools -q
uv run ruff check tools/validate.py tools/build_content.py tools/test_validate.py
uv run python tools/build_content.py
uv run python -c "import json;c=json.load(open('apps/web/src/generated/catalog.json',encoding='utf-8'));print([(x['id'],x['ready']) for x in c['capstones']], len(c['phases']))"
uv run python tools/validate.py --fast
git status --short
```
Mong đợi: pytest xanh; ruff không lỗi mới (so với `main`); dòng in ra `[('cap-01-rag-chatbot', False), ('cap-02-tool-agent', False)] 9`; validate 0 lỗi.
Validate đầy đủ (khoảng 6 phút) boss sẽ tự chạy; worker chỉ cần `--fast`.

## Ghi chú cho worker
- Không chạy server hay dev server. Không chạy `pnpm`.
- Giữ code ngắn, theo phong cách sẵn có của hai file. Không đổi format output của validate.

## Trạng thái
- Bước hiện tại: 5 (đạt vòng 1; boss kiểm: pytest tools 46 pass, ruff không lỗi mới, validate toàn bộ 0 lỗi, catalog 2 capstone ready false; chờ duyệt commit)
- Vòng: 1/3
- Số lần swap: 0
- Fallback: không
- Model: Gemini 4 Hydrogen (High)
