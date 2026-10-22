Tạo lesson mới: $ARGUMENTS
1. Kiểm tra lesson có trong curriculum/syllabus.yaml (thêm nếu chưa có).
2. Dùng subagent content-writer soạn lesson + examples + 2 exercise.
3. Dùng subagent quiz-factory sinh quiz.yaml (8 câu, 5 flashcard).
4. Chạy `uv run python tools/validate.py --path <lesson>` và `uv run pytest <lesson>`.
5. Báo kết quả ngắn gọn.
