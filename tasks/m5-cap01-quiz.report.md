# Báo cáo M5 bước 2e: `cap-01-rag-chatbot` quiz + portfolio

## 1. Đã làm gì

1. **Tạo `curriculum/capstones/cap-01-rag-chatbot/quiz.yaml`**:
   - Gồm **16 câu hỏi** (`cap-01-q01` đến `cap-01-q16`) và **6 flashcard** (`cap-01-f01` đến `cap-01-f06`) song ngữ `en` + `vi`.
   - Cơ cấu loại câu hỏi: **8 `mcq`**, **3 `output`**, **2 `fill`**, **3 `parsons`** (mỗi loại đều >= 2).
   - Cơ cấu độ khó: **5 dễ (`1`)**, **8 vừa (`2`)**, **3 khó (`3`)**.
   - Nội dung phủ đều 4 trụ cột của capstone và các lỗi §9:
     - Lịch sử hội thoại + ngân sách token (`count_tokens`), giữ cố định `system` prompt bên ngoài `self.history` và giữ lại ít nhất cặp lượt mới nhất (`len(kept) > 2`).
     - Viết lại câu hỏi nối tiếp tất định (`<= 4` từ, `"what about "`, `"and "`, `"how about "`), dùng câu hỏi `user` gốc trong `history` (không dùng chuỗi đã viết lại), từ chối không gọi `client.chat` khi `retrieve` trả rỗng.
     - Đánh giá hội thoại nhiều lượt (`run_dialog_eval` gọi `make_bot()` mới cho từng dialog, thứ tự ưu tiên `score_turn`), đối chiếu baseline theo `(dialog, turn)` (`fixed`, `broken`, `new`, `gate_ok = not broken and pass_rate >= min_pass_rate`, lỗi chỉ nhìn `pass_rate`).
     - Quản lý phiên (`FakeClock`, `now - last_seen >= ttl`, loại LRU theo `last_seen`, tránh aliasing chung list `history`, trả `404` khi phiên hết hạn hoặc không tồn tại).
   - Toàn bộ code trong `output`, `fill`, `parsons` chạy bằng Python thuần / `pyai_llm.count_tokens` (tương thích Pyodide, không dùng `fastapi`, không mạng, không thời gian thật). Các câu `parsons` đều có <= 7 dòng, không dùng `while`, và đã được kiểm tra chỉ có duy nhất 1 hoán vị chạy ra đúng output.
   - Phần tiếng Việt dùng `"bạn"`, không dùng `"ta"`/`"chúng ta"`, mỗi câu đều có `explanation` giải thích vì sao.

2. **Cập nhật `curriculum/portfolio.yaml` (chỉ mục `cap-rag-chatbot`)**:
   - Thêm `lesson: cap-01-rag-chatbot`, giữ nguyên `id: cap-rag-chatbot`, `phase: p8`, `difficulty: 5`.
   - Cập nhật `tags: [rag, evaluation, production, apis, testing]` (đều có trong `curriculum/topics.yaml`).
   - Viết lại `pitch`, `cv_bullet` (`en` + `vi`) và `skills` phản ánh đúng nội dung thật của capstone (multi-turn RAG, viết lại câu nối tiếp, ngân sách token, trích dẫn `[n]` và từ chối, golden dialog eval + cổng hồi quy, dịch vụ FastAPI session với TTL/LRU/404, kiểm thử bằng `TestClient` + `FakeClock`), bỏ các mục thuộc `p8-05` (TTL cache phản hồi, theo dõi chi phí/độ trễ).
   - Thêm `stretch` (`en` + `vi`, 3 mục) khớp mục "Take it further" của bài học (LLM contextualizer qua `.env`, lưu phiên bằng Redis hash + `EXPIRE`, stream SSE từ `POST /sessions/{id}/messages`).

## 2. File đã sửa / tạo

- Tạo mới: `curriculum/capstones/cap-01-rag-chatbot/quiz.yaml`
- Chỉnh sửa: `curriculum/portfolio.yaml` (chỉ mục `cap-rag-chatbot`)
- Tạo mới: `tasks/m5-cap01-quiz.report.md`

## 3. Kiểm tra độ dài lựa chọn MCQ

Không có câu MCQ nào có đáp án đúng là lựa chọn dài nhất duy nhất hoặc dài hơn lựa chọn dài nhất còn lại quá 20%.

### Tiếng Anh (`en`)

| id | độ dài đáp án đúng | độ dài lựa chọn dài nhất khác | chênh lệch |
|---|---|---|---|
| `cap-01-q01` | 61 | 69 | -11.6% |
| `cap-01-q04` | 69 | 69 | +0.0% |
| `cap-01-q05` | 64 | 64 | +0.0% |
| `cap-01-q08` | 63 | 69 | -8.7% |
| `cap-01-q09` | 63 | 68 | -7.4% |
| `cap-01-q10` | 63 | 67 | -6.0% |
| `cap-01-q13` | 56 | 57 | -1.8% |
| `cap-01-q16` | 68 | 69 | -1.4% |

### Tiếng Việt (`vi`)

| id | độ dài đáp án đúng | độ dài lựa chọn dài nhất khác | chênh lệch |
|---|---|---|---|
| `cap-01-q01` | 58 | 68 | -14.7% |
| `cap-01-q04` | 67 | 67 | +0.0% |
| `cap-01-q05` | 69 | 73 | -5.5% |
| `cap-01-q08` | 68 | 69 | -1.4% |
| `cap-01-q09` | 68 | 69 | -1.4% |
| `cap-01-q10` | 68 | 68 | +0.0% |
| `cap-01-q13` | 60 | 67 | -10.4% |
| `cap-01-q16` | 65 | 68 | -4.4% |

## 4. Kết quả lệnh kiểm tra

- `uv run python tools/validate.py --path curriculum/capstones/cap-01-rag-chatbot`:
  - Exit code `0`: `OK: 0 error(s), 0 warning(s). Checked 1 lessons, 10 markdown pairs, 3 examples, 20 lesson output blocks, 3 alternatives, 3 exercises, 16 questions.`
- `uv run python tools/validate.py --fast`:
  - Exit code `0`: `OK: 0 error(s), 33 warning(s). Checked 55 lessons, 419 markdown pairs, 163 examples, 111 exercises, 90 alternatives, 1073 questions, 594 lesson output blocks, 11 exams, 1 portfolio, 1 glossary, 1 interview.` (33 cảnh báo đều thuộc các bài phase 1–8 có sẵn, không có cảnh báo nào ở `cap-01-rag-chatbot` hay `portfolio.yaml`).
- `uv run python -m pytest curriculum/capstones/cap-01-rag-chatbot -q`:
  - Exit code `0`: `42 passed` (`.......................................... [100%]`).
- `uv run python tools/build_content.py`:
  - Exit code `0`: `Built 55 lessons, 11 exams, 330 flashcards, 882 questions -> apps\web\src\generated`.
- Kiểm tra `"ta"` / `"chúng ta"` trong `curriculum/capstones/cap-01-rag-chatbot/quiz.yaml` (regex `(^|[ .:(\"'])(Ta|ta|Chúng ta|chúng ta) `, loại trừ `"người ta"`):
  - `0` dòng khớp (`matches: 0 []`).
- `git status --short`:
  - Chỉ có `M curriculum/portfolio.yaml`, `?? curriculum/capstones/cap-01-rag-chatbot/quiz.yaml`, và `?? tasks/` (cùng thư mục `.hallmark/` đã có sẵn trước đó).

## 5. Điều còn chưa chắc

- Chưa chạy `uv run python tools/validate.py` (chế độ đầy đủ không `--fast` trên toàn repo, vì spec yêu cầu `--path $D` đầy đủ và toàn repo `--fast`), và chưa mở ứng dụng web để kiểm tra hiển thị giao diện thực tế sau `build_content.py` (do không chạy dev server theo yêu cầu).
