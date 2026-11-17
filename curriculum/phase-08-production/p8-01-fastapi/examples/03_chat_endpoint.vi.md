# Endpoint chat LLM kèm đếm token

**Ví dụ này cho thấy:** Bọc `FakeLLM` phía sau endpoint `POST /chat`, cộng dồn trường `tokens` qua nhiều request và để Pydantic tự chặn `temperature` ngoài ngưỡng.

**Từng bước**
1. Dòng 8–9 tạo `app` và khởi tạo `llm = FakeLLM(seed=0)` một lần ở mức module.
2. Dòng 12–14 định nghĩa `ChatRequest` yêu cầu `message` không rỗng và `temperature` nằm trong `[0.0, 1.0]`.
3. Dòng 17–23 chuyển tiếp `message` và `temperature` đã kiểm tra vào `llm.chat(...)` rồi trả về cả `answer` lẫn `tokens`.
4. Dòng 26–44 gửi ba câu hỏi hợp lệ, cộng tổng `total_tokens` (`82`), rồi gửi thêm một request có `temperature=2` để thấy lỗi `422` tự động.

**Để ý:** Trả kèm `tokens` trong JSON giúp phía gọi và hệ thống monitoring theo dõi chi phí LLM mà không phải đếm lại, còn khi `temperature=2` sai ngay ở Pydantic thì `FakeLLM` không bị gọi.

**Tự thử:** Truyền `"temperature": 0.5` ở ba request đầu và kiểm tra xem `answer` hay `tokens` có đổi với `FakeLLM(seed=0)` không.
