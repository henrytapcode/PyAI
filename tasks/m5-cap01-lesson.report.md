# Báo cáo: M5 bước 2a (`cap-01-rag-chatbot` syllabus, meta, lesson, examples)

## 1. Đã làm gì

- Cập nhật mục `cap-01-rag-chatbot` trong [syllabus.yaml](file:///D:/Proj/python-ai-platform/curriculum/syllabus.yaml) (chỉ mục này trong `capstones:`): thêm `kind: project` và 4 `outcomes` song ngữ `en`/`vi`, giữ nguyên chạy trên Pyodide (không thêm `runner: local` ở cấp lesson).
- Tạo [meta.yaml](file:///D:/Proj/python-ai-platform/curriculum/capstones/cap-01-rag-chatbot/meta.yaml) với `id: cap-01-rag-chatbot`, `phase: cap`, `order: 1`, `kind: project`, `level: applied`, `tags: [llm, rag, evaluation, production]`, `prerequisites: [p7-08-evals, p7-09-mini-project-rag, p8-05-mini-project]`, `duration_min: 90`, `review_by: "2027-05-01"`, `title`/`outcomes` khớp `syllabus.yaml`, và 2 mục `further_reading` thực tế (RAGAS arXiv:2309.15217 và FastAPI Dependencies).
- Viết [lesson.en.md](file:///D:/Proj/python-ai-platform/curriculum/capstones/cap-01-rag-chatbot/lesson.en.md) và [lesson.vi.md](file:///D:/Proj/python-ai-platform/curriculum/capstones/cap-01-rag-chatbot/lesson.vi.md) theo giọng "brief" của quản lý, gồm:
  - Mở đầu không heading nêu 3 lý do bot một lượt chưa đủ.
  - `§1. The brief` (`Yêu cầu dự án`): 3 user story và kho 8 trang FAQ `docs` lấy nguyên văn từ `p7-09-mini-project-rag` §2.
  - `§2. Architecture` (`Kiến trúc hệ thống`): sơ đồ `mermaid` (`flowchart LR`, 9 node) và bảng ánh xạ tái sử dụng từ `p7-01`, `p7-05`, `p7-08`, `p7-09`, `p8-03`, `p8-05`.
  - `§3. Conversation history with a token budget`: hàm `trim_history` dùng `count_tokens` của `pyai_llm` + bảng trace 4 lượt.
  - `§4. Follow-up questions`: hàm `rewrite_query` tất định không gọi LLM (`<= 4` từ hoặc bắt đầu bằng `"what about"`, `"and"`, `"how about"`), khối code ngắn mời bấm **Visualize** (34 bước trên `tracer.py`), và khối + bảng so sánh điểm `cosine` + câu trả lời `FakeLLM.chat()` trước/sau viết lại.
  - `§5. Evaluating conversations`: minh họa chấm golden dialog và hàm `compare_to_baseline` trên dữ liệu giả (`fixed`, `broken`, `pass_rate`).
  - `§6. Sessions`: dict `session_id -> {"history", "last_seen"}` thuần Python dùng `FakeClock` chuẩn, hết hạn TTL và loại phiên ít dùng nhất (không `import fastapi`; ghi chú `ex03` sẽ bọc FastAPI và chạy `runner: local`).
  - `§7. Milestones`: bảng 3 mốc (`ex01`, `ex02`, `ex03`) kèm tiêu chí đo được và phần code trong bài học chưa làm.
  - `§8. Grading rubric`: bảng tiêu chí, cách đo và mức đạt.
  - `§9. Common mistakes` (`Lỗi thường gặp`): 4 lỗi thực tế kèm code sai, output sai và cách sửa (truy xuất bằng câu nối tiếp thô; cắt lịch sử làm mất `system` prompt; chỉ nhìn `pass_rate` bỏ qua `broken`; dùng chung một list lịch sử giữa các phiên).
  - `Recap` (`Tóm tắt`) và `Take it further` (`Mở rộng thêm`, có khối `bash` đọc key từ `.env` không in key).
- Tạo 3 bộ example đầy đủ (`.py`, `.out`, `.en.md`, `.vi.md`), cố tình lược bỏ yêu cầu cốt lõi của các mốc exercise sau này để không thành lời giải mẫu:
  - `01_follow_up_chat.py`: chạy hội thoại 4 lượt (1 câu nối tiếp, 1 câu ngoài FAQ). **Cố tình thiếu so với `ex01`:** dùng hàm rời với `history` không giới hạn token, chưa đóng gói thành class `ChatBot` có `.ask()` và chưa ghim `system` prompt khi cắt lịch sử theo ngân sách token.
  - `02_dialog_eval.py`: chấm 2 golden dialog (2 lượt/dialog) và đối chiếu giữa baseline (`rewrite=False, min_score=0.2`) với bản mới (`rewrite=True, min_score=0.35`) để lộ cả `fixed` (`d1#t2`) lẫn `broken` (`d2#t1`). **Cố tình thiếu so với `ex02`:** không nhận factory `make_bot` để cô lập từng dialog, gộp khóa thành chuỗi `"d1#t2"` thay vì báo cấu trúc `(dialog_id, turn_idx)`, và chưa cài cổng hồi quy fail khi có `broken` hoặc `pass_rate` dưới ngưỡng.
  - `03_session_store.py`: `SessionStore` thuần Python với `FakeClock`, TTL 60s và `max_sessions=2`, in trạng thái sau mỗi bước. **Cố tình thiếu so với `ex03`:** chưa bọc FastAPI `create_app` hay các route `/sessions`, `/sessions/{id}/messages`, chưa trả HTTP `404` cho phiên thiếu/hết hạn, và chưa nối `ChatBot` vào từng phiên.

## 2. File đã sửa / tạo

- Sửa:
  - [curriculum/syllabus.yaml](file:///D:/Proj/python-ai-platform/curriculum/syllabus.yaml) (chỉ mục `cap-01-rag-chatbot` trong `capstones:`)
- Tạo mới:
  - [curriculum/capstones/cap-01-rag-chatbot/meta.yaml](file:///D:/Proj/python-ai-platform/curriculum/capstones/cap-01-rag-chatbot/meta.yaml)
  - [curriculum/capstones/cap-01-rag-chatbot/lesson.en.md](file:///D:/Proj/python-ai-platform/curriculum/capstones/cap-01-rag-chatbot/lesson.en.md)
  - [curriculum/capstones/cap-01-rag-chatbot/lesson.vi.md](file:///D:/Proj/python-ai-platform/curriculum/capstones/cap-01-rag-chatbot/lesson.vi.md)
  - [curriculum/capstones/cap-01-rag-chatbot/examples/01_follow_up_chat.py](file:///D:/Proj/python-ai-platform/curriculum/capstones/cap-01-rag-chatbot/examples/01_follow_up_chat.py)
  - [curriculum/capstones/cap-01-rag-chatbot/examples/01_follow_up_chat.out](file:///D:/Proj/python-ai-platform/curriculum/capstones/cap-01-rag-chatbot/examples/01_follow_up_chat.out)
  - [curriculum/capstones/cap-01-rag-chatbot/examples/01_follow_up_chat.en.md](file:///D:/Proj/python-ai-platform/curriculum/capstones/cap-01-rag-chatbot/examples/01_follow_up_chat.en.md)
  - [curriculum/capstones/cap-01-rag-chatbot/examples/01_follow_up_chat.vi.md](file:///D:/Proj/python-ai-platform/curriculum/capstones/cap-01-rag-chatbot/examples/01_follow_up_chat.vi.md)
  - [curriculum/capstones/cap-01-rag-chatbot/examples/02_dialog_eval.py](file:///D:/Proj/python-ai-platform/curriculum/capstones/cap-01-rag-chatbot/examples/02_dialog_eval.py)
  - [curriculum/capstones/cap-01-rag-chatbot/examples/02_dialog_eval.out](file:///D:/Proj/python-ai-platform/curriculum/capstones/cap-01-rag-chatbot/examples/02_dialog_eval.out)
  - [curriculum/capstones/cap-01-rag-chatbot/examples/02_dialog_eval.en.md](file:///D:/Proj/python-ai-platform/curriculum/capstones/cap-01-rag-chatbot/examples/02_dialog_eval.en.md)
  - [curriculum/capstones/cap-01-rag-chatbot/examples/02_dialog_eval.vi.md](file:///D:/Proj/python-ai-platform/curriculum/capstones/cap-01-rag-chatbot/examples/02_dialog_eval.vi.md)
  - [curriculum/capstones/cap-01-rag-chatbot/examples/03_session_store.py](file:///D:/Proj/python-ai-platform/curriculum/capstones/cap-01-rag-chatbot/examples/03_session_store.py)
  - [curriculum/capstones/cap-01-rag-chatbot/examples/03_session_store.out](file:///D:/Proj/python-ai-platform/curriculum/capstones/cap-01-rag-chatbot/examples/03_session_store.out)
  - [curriculum/capstones/cap-01-rag-chatbot/examples/03_session_store.en.md](file:///D:/Proj/python-ai-platform/curriculum/capstones/cap-01-rag-chatbot/examples/03_session_store.en.md)
  - [curriculum/capstones/cap-01-rag-chatbot/examples/03_session_store.vi.md](file:///D:/Proj/python-ai-platform/curriculum/capstones/cap-01-rag-chatbot/examples/03_session_store.vi.md)
  - [tasks/m5-cap01-lesson.report.md](file:///D:/Proj/python-ai-platform/tasks/m5-cap01-lesson.report.md)

## 3. Kết quả lệnh kiểm tra

Chạy sau lần chỉnh sửa cuối cùng ở `D:\Proj\python-ai-platform`:

1. `uv run python tools/validate.py --path curriculum/capstones/cap-01-rag-chatbot`
   - Kết quả: thoát với đúng 2 lỗi mong đợi của bước 2a (`lesson has no exercises`, `missing quiz.yaml`), `0 warning(s)`:
     `FAILED: 2 error(s), 0 warning(s). Checked 1 lessons, 4 markdown pairs, 3 examples, 20 lesson output blocks.`
   - Tất cả kiểm tra schema, parity EN/VI, 20 output block trong lesson, 3 example + `tracer.py`, và `ruff` đều xanh.
2. Chạy từng example với `PYTHONPATH=packages/pyai_llm`, `uv run python -W error`, đối chiếu `.out`:
   - `ok 01_follow_up_chat.py`
   - `ok 02_dialog_eval.py`
   - `ok 03_session_store.py`
3. Kiểm tra đại từ `"ta"` / `"chúng ta"` (case-sensitive, loại trừ `"người ta"`) trong `curriculum/capstones/cap-01-rag-chatbot/*.vi.md` và `examples/*.vi.md`:
   - 0 dòng khớp.
4. `uv run python tools/build_content.py`
   - Kết quả: `Built 55 lessons, 11 exams, 324 flashcards, 866 questions -> apps\web\src\generated` (thoát mã `0`). Lưu ý bước 2a chưa có `exercises/` và `quiz.yaml` nên `build_lesson` vẫn build thành công lesson với `exercises=[]`, `quiz` rỗng.
5. `git status --short`
   - Hiển thị `M curriculum/syllabus.yaml`, `?? curriculum/capstones/`, `?? tasks/` (và `?? .hallmark/` đã có sẵn trước đó trên workspace).

## 4. Điều còn chưa chắc

- Chưa chạy `uv run pytest curriculum` trên toàn repo vì phạm vi bước 2a chỉ kiểm tra riêng `cap-01-rag-chatbot` (chưa tạo `exercises/` hay `quiz.yaml`).
- Chữ ký chính xác của `ex01`–`ex03` (`ChatBot`, `run_dialog_eval`, `compare_to_baseline`, `create_app`) bám theo mô tả trong `tasks/m5-cap01-lesson.md`; nếu ở bước 2b–2d bạn đổi tên tham số phụ (ví dụ tên field trong dict hoặc giá trị mặc định `min_score`), nên rà lại mục `§7. Milestones` cho khớp 100%.
- Không kiểm tra truy cập mạng trực tiếp tới hai URL `further_reading` (`arxiv.org/abs/2309.15217` và `fastapi.tiangolo.com/tutorial/dependencies/`); cả hai là URL tài liệu chuẩn đã biết.

## 5. Sửa theo Feedback vòng 2

- **Điểm 1 (`§6 open_session` trong [lesson.en.md](file:///D:/Proj/python-ai-platform/curriculum/capstones/cap-01-rag-chatbot/lesson.en.md) và [lesson.vi.md](file:///D:/Proj/python-ai-platform/curriculum/capstones/cap-01-rag-chatbot/lesson.vi.md)):** sửa `open_session` để khi `sid` đã tồn tại trong `sessions`, chỉ cập nhật `sessions[sid]["last_seen"] = now` và `return` sớm (giữ nguyên `history`), còn khi `sid` chưa tồn tại mới kiểm tra `max_sessions` và khởi tạo `{"history": [], "last_seen": now}`. Output của khối code và phần giải thích giữ nguyên.
- **Điểm 2 (`§4 rewrite_query` trong [lesson.en.md](file:///D:/Proj/python-ai-platform/curriculum/capstones/cap-01-rag-chatbot/lesson.en.md) và [lesson.vi.md](file:///D:/Proj/python-ai-platform/curriculum/capstones/cap-01-rag-chatbot/lesson.vi.md)):** đổi `low.startswith(("what about", "and", "how about"))` thành `low.startswith(("what about ", "and ", "how about "))` để kiểm theo từ, tránh khớp nhầm các từ như `"android..."` hoặc `"andy..."`. Kiểm tra mục `§7`, `Recap`/`Tóm tắt` vẫn khớp quy tắc; output của khối code giữ nguyên. *(Lưu ý: `examples/01_follow_up_chat.py` vẫn giữ nguyên `low.startswith(("what about", "and", "how about"))` vì feedback vòng 2 chỉ yêu cầu sửa 3 điểm này và giữ nguyên mọi thứ khác.)*
- **Điểm 3 ([03_session_store.vi.md](file:///D:/Proj/python-ai-platform/curriculum/capstones/cap-01-rag-chatbot/examples/03_session_store.vi.md) mục Lưu ý):** đổi `last_seen` của cô thành `last_seen` của `"alice"` để trung tính.
- **Kiểm tra lại sau khi sửa vòng 2:**
  1. `uv run python tools/validate.py --path curriculum/capstones/cap-01-rag-chatbot`: đúng 2 lỗi mong đợi (`lesson has no exercises`, `missing quiz.yaml`), `0 warning(s)`, `Checked 1 lessons, 4 markdown pairs, 3 examples, 20 lesson output blocks`.
  2. Chạy 3 file example với `PYTHONPATH=packages/pyai_llm` và `uv run python -W error`, so khớp `.out`: `ok 01_follow_up_chat.py`, `ok 02_dialog_eval.py`, `ok 03_session_store.py`.
  3. Kiểm tra đại từ `"ta"` / `"chúng ta"` (loại trừ `"người ta"`) trong `*.vi.md` và `examples/*.vi.md`: `0` dòng khớp.
  4. `uv run python tools/build_content.py`: `Built 55 lessons, 11 exams, 324 flashcards, 866 questions -> apps\web\src\generated` (exit code `0`).
  5. `git status --short`: `M curriculum/syllabus.yaml`, `?? .hallmark/`, `?? curriculum/capstones/`, `?? tasks/`.
