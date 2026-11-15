# Bộ kiểm thử kịch bản tất định và báo cáo tổng kết

**Ví dụ này minh họa:** Chạy bảy kịch bản—gồm đường vui, tự xử lý lỗi, `repeat`, `max_steps`, hoàn tiền được duyệt, hoàn tiền bị chặn và `budget`—mỗi kịch bản dùng một client `FakeLLM` mới, rồi in bảng kết quả và báo cáo token.

**Từng bước một**
1. Dòng 5–42 thiết lập dữ liệu đơn hàng, tool và schema.
2. Dòng 45–67 cài đặt `run_agent()` kiểm tra theo đúng thứ tự `budget`, `final`, `repeat` và quyền duyệt side effect.
3. Dòng 75–158 định nghĩa bảy `SCENARIOS` kèm quỹ đạo chuẩn `tools` và kiểm tra `answer_contains`.
4. Dòng 160–198 chạy từng kịch bản bằng một `FakeLLM(script=sc["script"])` riêng, in bảng `PASS`/`FAIL` và thống kê theo `stopped_reason` cùng tổng token.

**Điểm đáng chú ý:** Mỗi kịch bản đều tạo mới một đối tượng `FakeLLM(script=sc["script"])` ngay trong vòng lặp nên không bao giờ bị cạn script giữa chừng hay lệch `ToolCall.id` giữa các ca.

**Tự thử:** Đảo vị trí hai phần tử trong `expect["tools"]` của `happy_lookup` rồi chạy lại để xem dòng `FAIL` hiện ra ngay trong bảng tổng kết.
