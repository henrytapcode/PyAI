# M5 bước 2e: capstone 1 quiz + portfolio

## Mục tiêu
Hoàn tất capstone `cap-01-rag-chatbot`: thêm `quiz.yaml` (bộ câu hỏi + flashcard) để validate hết lỗi, và nối mục portfolio `cap-rag-chatbot` với bài, viết lại cho đúng những gì học viên thật sự làm.

Nội dung đã có (đọc trước): `curriculum/capstones/cap-01-rag-chatbot/lesson.en.md` (§3 lịch sử + ngân sách token, §4 viết lại câu nối tiếp, §5 eval hội thoại + baseline, §6 session TTL/LRU, §9 lỗi thường gặp) và 3 exercise `ex01-chatbot`, `ex02-dialog-eval`, `ex03-session-service`.

## File được phép sửa/tạo
- `curriculum/capstones/cap-01-rag-chatbot/quiz.yaml`
- `curriculum/portfolio.yaml`: **chỉ** mục `cap-rag-chatbot`
- `tasks/m5-cap01-quiz.report.md`

## Không được đụng
- Mọi file khác (lesson, examples, exercises, meta, syllabus, tools, apps, packages, phase khác, mục portfolio khác).

## Việc cần làm
### 1. `quiz.yaml` theo `docs/CONTENT_GUIDE.md` mục quiz.yaml
- 15–18 câu, mỗi loại `mcq`, `output`, `fill`, `parsons` **ít nhất 2**; độ khó khoảng 5 dễ / 7 vừa / 3 khó. Id `cap-01-q01`…, flashcard `cap-01-f01`…`f06` (6 flashcard).
- Tag có trong `curriculum/topics.yaml` (ví dụ `llm`, `rag`, `evaluation`, `production`, `apis`, `testing`).
- Phủ đều 4 ý mới của capstone (lịch sử/ngân sách token, viết lại câu nối tiếp, eval hội thoại + `fixed`/`broken`/cổng, session TTL/LRU/404) và các lỗi ở §9. Không hỏi lại kiến thức thuần p7-09/p8-05.
- Code trong câu `output`/`fill`/`parsons` chạy được trong **Pyodide**: thuần Python (có thể dùng `pyai_llm.count_tokens`), không fastapi, không mạng, không thời gian thật (dùng `FakeClock` chuẩn nếu cần). Output đúng tuyệt đối (validator chạy để kiểm). `parsons`: chỉ một thứ tự đúng.
- `mcq`: 4 lựa chọn, **độ dài các lựa chọn xấp xỉ nhau**, đáp án đúng không được là lựa chọn dài nhất duy nhất; không giấu lời giải thích trong đáp án; không "All of the above". Distractor là hiểu lầm thật (ví dụ: chỉ nhìn `pass_rate`; dùng câu đã viết lại làm "câu trước"; `>` thay `>=` ở TTL; một list lịch sử dùng chung).
- Mỗi câu có `explanation` en + vi nói **vì sao**.
- VI: tự nhiên, "bạn", không "ta"/"chúng ta", thuật ngữ giữ tiếng Anh, accuracy = "tỉ lệ đoán đúng".

### 2. `portfolio.yaml`, mục `cap-rag-chatbot`
- Thêm `lesson: cap-01-rag-chatbot`.
- Giữ `id`, `phase`, `difficulty` (thứ tự độ khó tăng dần phải còn đúng).
- Viết lại `pitch`, `cv_bullet`, `skills` (en + vi) cho đúng bài thật: chatbot nhiều lượt có viết lại câu nối tiếp và ngân sách token, citation + từ chối, bộ eval golden dialog có cổng hồi quy so baseline, dịch vụ FastAPI có session (TTL, giới hạn, 404), test bằng `TestClient` + `FakeClock`. **Bỏ** những gì bài không làm (cache, theo dõi chi phí/độ trễ: đó là p8-05).
- Thêm `stretch` (en + vi, 3 mục) giống dạng `rag-service`, khớp mục "Take it further" của lesson.
- Tags có trong topics.yaml.

## Tiêu chí hoàn thành (checklist)
- [ ] Validate capstone **0 lỗi, 0 cảnh báo**
- [ ] Validate toàn bộ nhanh (`--fast`) 0 lỗi (portfolio hợp lệ, thứ tự độ khó đúng)
- [ ] MCQ: trong report có bảng `id | độ dài đáp án đúng | độ dài lựa chọn dài nhất khác`, không câu nào đáp án đúng dài nhất mà dài hơn lựa chọn dài thứ hai quá 20%
- [ ] grep "ta"/"chúng ta" phần `vi:` của quiz ra 0 dòng

## Lệnh kiểm tra
Chạy từ gốc repo `D:\Proj\python-ai-platform`:
```bash
D=curriculum/capstones/cap-01-rag-chatbot
uv run python tools/validate.py --path $D
uv run python tools/validate.py --fast
uv run python -m pytest $D -q
uv run python tools/build_content.py
grep -nE "(^|[ .:(\"'])(Ta|ta|Chúng ta|chúng ta) " $D/quiz.yaml | grep -v "người ta"
git status --short
```

## Ghi chú cho worker
- Không chạy server hay dev server.
- Khuôn quiz: `curriculum/phase-07-llm/p7-09-mini-project-rag/quiz.yaml`.

## Trạng thái
- Bước hiện tại: 5 (đạt vòng 1; boss kiểm: validate capstone 0 lỗi 0 cảnh báo, MCQ cân độ dài, test tools + capstone pass, typecheck, build 80 trang, quiz 16 câu hiện trong app; chờ duyệt commit)
- Vòng: 1/3
- Số lần swap: 0
- Fallback: không
- Model: Gemini 4 Hydrogen (High)
