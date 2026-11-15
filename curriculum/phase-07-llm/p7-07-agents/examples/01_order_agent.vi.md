# Agent hỗ trợ đơn hàng với ba tool chỉ đọc

**Điểm nổi bật:** Vòng lặp observe-think-act có giới hạn giải quyết yêu cầu tra cứu đơn hàng nhiều bước bằng `FakeLLM(script=...)` và ghi lại trace từng bước.

**Từng bước**
1. Dòng 6–34 khai báo ba bảng dữ liệu chỉ đọc cục bộ (`ORDERS`, `DELIVERY_DAYS`, `POLICIES`) cùng các hàm tra cứu Python thuần.
2. Dòng 37–57 định nghĩa ba schema trong `TOOLS` và ánh xạ tên sang hàm trong `REGISTRY`.
3. Dòng 60–84 cài đặt `dispatch()` và `run_agent()`, lặp tối đa `max_steps` lần, nối cặp message `assistant` (`tool_calls`) và `tool`, đồng thời ghi từng bước vào `trace`.
4. Dòng 87–97 chạy một tác vụ 3 bước dùng `script` (`lookup_order` -> `estimate_delivery` -> câu trả lời cuối) rồi in lý do dừng, các dòng trace và câu trả lời cuối.

**Lưu ý:** Mỗi tool call luôn nối cả yêu cầu `assistant` lẫn quan sát `tool` vào `messages` trước khi gọi `chat()` kế tiếp để model thấy được kết quả bước trước.

**Tự thử:** Đổi bước thứ hai trong `script` sang `check_policy` với `{"status": "shipped"}` và xem dòng trace thay đổi mà không cần sửa `run_agent()`.
