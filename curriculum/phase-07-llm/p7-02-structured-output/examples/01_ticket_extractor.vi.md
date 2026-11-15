# Trích xuất ticket từ email khách hàng

**Ví dụ này minh họa:** Yêu cầu `FakeLLM` trả JSON theo schema, kiểm tra khóa và kiểu dữ liệu, rồi dựng dataclass `Ticket` đồng thời loại bỏ các giá trị rỗng giả.

**Từng bước**
1. Dòng 7–15 định nghĩa `TICKET_SCHEMA` yêu cầu `name` (`string`), `order_id` (`integer`) và `urgent` (`boolean`).
2. Dòng 18–28 định nghĩa dataclass `Ticket` có `__post_init__` để từ chối tên rỗng và `order_id` không dương.
3. Dòng 31–48 định nghĩa `validate_ticket_dict()` để bắt thiếu khóa bắt buộc và sai kiểu (kiểm `bool` trước `int`).
4. Dòng 58–73 lặp qua ba email khách hàng, parse JSON, validate dict rồi in ra `Ticket` hoặc lý do bị loại.

**Điểm cần chú ý:** Email 2 vẫn cho ra JSON hợp lệ (`{"name": "", "order_id": 0, "urgent": false}`) qua được bước kiểm kiểu, nên chỉ kiểm tra nghiệp vụ trong `Ticket.__post_init__` mới phát hiện email này thiếu thông tin.

**Tự thử:** Đổi Email 2 thành `"name: Hoa, order_id: 99, urgent: yes"` rồi chạy lại để thấy cả ba email đều tạo được ticket.
