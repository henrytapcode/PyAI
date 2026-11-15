# Retry kèm phản hồi lỗi và fallback

**Ví dụ này minh họa:** Gửi ngược thông báo lỗi vào bản sao lịch sử `messages` để model tự sửa ở lượt sau, và trả về fallback an toàn nếu hết lượt vẫn hỏng.

**Từng bước**
1. Dòng 17–34 định nghĩa `validate_reply()` thu thập các lỗi thiếu khóa và sai kiểu dựa trên `TICKET_SCHEMA`.
2. Dòng 37–67 định nghĩa `get_structured()` sao chép `messages`, gọi `client.chat()`, parse và kiểm tra kết quả; nếu có lỗi thì nối phản hồi cũ cùng mô tả lỗi để thử lại.
3. Dòng 70–85 chạy hai lượt: lượt 1 hỏng 1 lần rồi đúng ở lần 2; lượt 2 hỏng cả 3 lần nên trả về fallback có `needs_review=True`.

**Điểm cần chú ý:** Sao chép `messages` ngay đầu `get_structured()` giúp danh sách gốc của người gọi không bị sửa đổi sau các lần retry.

**Tự thử:** Tăng `max_attempts=4` ở Run 2 và thêm một JSON hợp lệ thứ tư vào `script` của `failing_client` để xem nó phục hồi thay vì rơi vào fallback.
