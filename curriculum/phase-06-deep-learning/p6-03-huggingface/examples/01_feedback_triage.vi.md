# Phân loại phản hồi người dùng chatbot

**Điều cần thấy:** Nạp model cảm xúc đã ghim ở chế độ offline để phân loại sáu phản hồi của người dùng chatbot và đếm số phản hồi tiêu cực cần xử lý.

**Từng bước**
1. Dòng 4–10 nạp `tokenizer` và `model` từ cache cục bộ (`revision=REV, local_files_only=True`) rồi truyền cả hai object vào `pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)`.
2. Dòng 12–19 khai báo sáu câu phản hồi ngắn bằng tiếng Anh của người dùng.
3. Dòng 21–28 chạy `classifier(feedback)` một lượt, làm tròn mỗi score 3 chữ số, đếm số nhãn `"NEGATIVE"` và in từng dòng kết quả.
4. Dòng 30 in tổng số phản hồi tiêu cực (`negative count: 3/6`).

**Lưu ý:** Truyền trực tiếp hai object `model` và `tokenizer` vào `pipeline()` giúp đảm bảo không gọi mạng mà vẫn có đầu ra dạng dict gọn nhẹ (`'label'` và `'score'`).

**Thử tự sửa:** Thêm một câu trung tính như `"The chat window opened at 9 AM."` vào `feedback` và xem bộ phân loại hai lớp vẫn ép nó vào `POSITIVE` hay `NEGATIVE`.
