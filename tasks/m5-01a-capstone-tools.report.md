# Báo cáo M5 bước 1a: hạ tầng capstone phía tools

## Đã làm gì
1. **Schema**
   - `tools/schema/meta.schema.json`: mở rộng pattern `id` chấp nhận `^(p[0-9]|cap)-[0-9]{2}-[a-z0-9-]+$` và `phase` chấp nhận `^(p[0-9]|cap)$`.
   - `tools/schema/exercise.schema.json`: mở rộng pattern `id` chấp nhận `^(p[0-9]|cap)-[0-9]{2}-ex[0-9]{2}$` và thêm trường tùy chọn `runner` (`enum: ["local"]`).
   - `tools/schema/quiz.schema.json`: giữ nguyên vì pattern `^[a-z0-9-]+$` ở câu hỏi (`common.schema.json`) và flashcard đã chấp nhận id dạng `cap-01-q01`.
2. **Nhóm bài dùng chung & `tools/build_content.py`**
   - Tách `lesson_groups(syllabus)` trả về danh sách `syllabus["phases"]` kèm nhóm capstone `{"id": "cap", "dir": "capstones", "lessons": syllabus.get("capstones") or []}`.
   - Tách `build_lesson_summary(...)` dùng chung cho cả lesson trong phase và capstone trong `capstones:`.
   - Mở rộng `main(curriculum=CURRICULUM, out=OUT, web=WEB)` để hỗ trợ test bằng thư mục tạm mà vẫn giữ hành vi mặc định khi chạy CLI.
   - Khi capstone chưa có thư mục `curriculum/capstones/<id>/meta.yaml`, `catalog.json` ghi `ready: false` với cùng dạng summary (`id`, `order`, `kind`, `title`, `outcomes`, `prerequisites`, `ready`, `runner` nếu có). Khi có thư mục hợp lệ, build `lessons/<id>.json`, đính kèm `runner` (cả ở `meta` và exercise nhờ `**meta`), và đưa flashcard/câu hỏi vào `review.json` kèm `lessonId`.
3. **`tools/validate.py`**
   - Dùng `lesson_groups(syllabus)` từ `tools.build_content` ở mọi chỗ duyệt nhóm bài: dựng `lesson_index`, `check_missing_models`, và vòng duyệt thư mục bài học (`--path curriculum/capstones/<id>` hoạt động như bài thường).
   - Kiểm tra phase-level `runner` bị cấm vẫn chỉ áp dụng cho `syllabus["phases"]`.
   - Thêm `exercise_timeout(meta, lesson_timeout=15)` trả về `60` khi `exercise.yaml` có `runner: local` (ngược lại giữ `lesson_timeout`), và truyền `timeout=code_timeout` vào `check_exercise`.
4. **`curriculum/syllabus.yaml`**
   - Chỉ thêm `prerequisites` cho mục `capstones:`:
     - `cap-01-rag-chatbot`: `[p7-08-evals, p7-09-mini-project-rag, p8-05-mini-project]`
     - `cap-02-tool-agent`: `[p7-07-agents, p7-10-mini-project-agent, p8-04-monitoring]`
5. **Tests**
   - `tools/test_validate.py`: thêm test cho `lesson_groups`, schema `meta`/`exercise` (hợp lệ & từ chối `runner: remote`, `cap-1-x`, `cap1`), `exercise_timeout`, và validate toàn bộ + `--path` + `portfolio.lesson` trỏ tới capstone trên curriculum giả trong `tmp_path`.
   - `tools/test_build_content.py`: thêm test build curriculum giả trong `tmp_path` có cả capstone `ready: true` (kèm exercise `runner: local` và quiz) và capstone chưa có thư mục (`ready: false`).

## File đã sửa / tạo
- `tools/schema/meta.schema.json` (sửa)
- `tools/schema/exercise.schema.json` (sửa)
- `tools/build_content.py` (sửa)
- `tools/validate.py` (sửa)
- `curriculum/syllabus.yaml` (sửa mục `capstones:`)
- `tools/test_validate.py` (sửa)
- `tools/test_build_content.py` (tạo mới)
- `tasks/m5-01a-capstone-tools.report.md` (tạo mới)

## Kết quả lệnh kiểm tra
- `uv run python -m pytest tools -q` -> **46 passed** (exit code 0).
- `uv run ruff check tools/validate.py tools/build_content.py tools/test_validate.py tools/test_build_content.py` -> còn **38 lỗi sẵn có** (chỉ là `E501`, `B905`, `B007`, `E713` có từ trước trên `validate.py`/`build_content.py`, giảm từ 45 xuống 38; **0 lỗi mới** ở các dòng vừa sửa/thêm và ở hai file test).
- `uv run python tools/build_content.py` -> `Built 54 lessons, 11 exams, 324 flashcards, 866 questions -> apps\web\src\generated` (exit code 0).
- `uv run python -c "import json;c=json.load(open('apps/web/src/generated/catalog.json',encoding='utf-8'));print([(x['id'],x['ready']) for x in c['capstones']], len(c['phases']))"` -> `[('cap-01-rag-chatbot', False), ('cap-02-tool-agent', False)] 9` (exit code 0).
- `uv run python tools/validate.py --fast` -> `OK: 0 error(s), 33 warning(s). Checked 54 lessons, 409 markdown pairs, 160 examples, 108 exercises, 87 alternatives, 1057 questions, 574 lesson output blocks, 11 exams, 1 portfolio, 1 glossary, 1 interview.` (exit code 0).

## Điều còn chưa chắc
- **Timeout cho `starter`/`solution`/`alternatives` trong `check_exercise`**: `run_tests` (`tools/pyrunner/runner.py`, không thuộc danh sách file được phép sửa) chạy in-process và không nhận tham số `timeout`. Khi chạy `pytest` (không có `--fast`), `validate.py` trước đây dùng cứng `timeout=120` (vì các bài nặng như `p6-04-fine-tune` chạy nhiều epoch). Do đó `check_exercise` hiện tính `ex_timeout = exercise_timeout(meta, timeout)` (60s khi `runner: local`, mặc định theo bài 15s/60s) và giữ `timeout=max(120, ex_timeout)` cho `pytest` để không đổi hành vi hay làm chậm/gãy phase 1–8; chưa có cơ chế ngắt `run_tests` in-process ở mốc 15s/60s nếu một file exercise treo vô hạn.
- **Validate đầy đủ (không `--fast`)**: theo spec chưa chạy validate đầy đủ (~6 phút), chỉ mới chạy `--fast`.
- **`check_missing_models` khi chỉ exercise có `runner: local`**: nếu một capstone không đặt `runner: local` ở `syllabus.yaml` mà chỉ đặt trong `exercise.yaml` và có dùng model HF local, `check_missing_models` hiện mới lọc theo `les.get("runner") == "local"` ở cấp syllabus như hiện tại.
