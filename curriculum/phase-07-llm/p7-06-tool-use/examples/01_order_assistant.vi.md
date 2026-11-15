# Trợ lý đơn hàng với hai tool

**Điểm nổi bật:** Hai vòng tool hoàn chỉnh định tuyến câu hỏi sang `lookup_order` hoặc `estimate_delivery` rồi đưa kết quả JSON hoặc chuỗi trở lại `FakeLLM`.

**Từng bước**
1. Dòng 6–21 định nghĩa hai bảng dữ liệu dictionary cục bộ (`ORDERS` và `CARRIER_DAYS`) cùng hai hàm tra cứu Python thuần.
2. Dòng 24–39 khai báo schema (`TOOLS`) với mô tả ngắn không chứa từ đệm và đăng ký cả hai hàm vào `REGISTRY`.
3. Dòng 42–62 viết hàm `ask_assistant()`: tạo `FakeLLM()` mới, gọi `chat()` kèm `tools=TOOLS`, chạy hàm qua `REGISTRY[tc.name](**tc.arguments)`, đổi `dict` sang chuỗi bằng `json.dumps()`, nối lần lượt message `assistant` và `tool`, rồi gọi vòng 2.
4. Dòng 65–69 thử một câu hỏi đơn hàng và một câu ước tính giao hàng, in rõ tên tool, tham số, kết quả tool và câu trả lời cuối.

**Lưu ý:** Việc tạo `FakeLLM()` mới trong `ask_assistant()` giúp mỗi lượt chạy tất định, đồng thời kết quả `dict` của `lookup_order` luôn được chuyển sang chuỗi JSON trước khi đưa vào message `tool`.

**Tự thử:** Thêm câu hỏi `"Tell me a joke"` vào danh sách ở dòng 65–68 để xem `ask_assistant()` đi thẳng qua nhánh `if not resp.tool_calls:`.
