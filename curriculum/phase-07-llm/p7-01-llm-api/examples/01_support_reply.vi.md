# Trợ lý hỗ trợ và tính chi phí token

**Điều cần thấy:** Gửi system message cùng ba câu hỏi của khách hàng tới `FakeLLM`, gửi lại lịch sử hội thoại qua từng lượt, rồi ước lượng tổng chi phí từ số token sử dụng.

**Từng bước**
1. Dòng 4–9 đặt đơn giá giả định theo mỗi triệu token, khởi tạo `FakeLLM()` và tạo `history` bắt đầu bằng một `system` message đặt giọng điệu cho trợ lý.
2. Dòng 10–14 liệt kê ba câu hỏi của khách: hai câu khớp kiến thức có sẵn của fake model và một câu rơi vào nhánh phản hồi lặp lại mặc định.
3. Dòng 19–25 thêm từng câu hỏi vào `history`, gọi `client.chat(history)`, lưu câu trả lời `assistant` lại vào `history`, và cộng dồn `prompt_tokens` cùng `completion_tokens`.
4. Dòng 27–37 in câu trả lời và số token của từng lượt, rồi tính và in tổng token (`223`) cùng chi phí ví dụ (`$0.000168`).

**Lưu ý:** Dù câu hỏi mới rất ngắn, `prompt_tokens` vẫn tăng từ `21` lên `55` rồi `91` vì toàn bộ lịch sử hội thoại đều được gửi lại ở mỗi lượt.

**Thử tự sửa:** Thêm một câu hỏi thứ tư vào `questions` và xem `prompt_tokens` tăng thêm bao nhiêu so với lượt 1.
