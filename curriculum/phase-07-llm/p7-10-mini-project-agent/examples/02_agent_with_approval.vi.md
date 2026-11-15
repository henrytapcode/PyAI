# Agent có giới hạn và cổng duyệt hành động

**Ví dụ này minh họa:** Chạy `run_support_agent()` trên ba tác vụ—tra cứu chỉ đọc, hoàn tiền được duyệt và hoàn tiền vượt mức bị `policy_gate` chặn—đồng thời ghi đủ cả `trace` lẫn nhật ký `audit`.

**Từng bước một**
1. Dòng 5–35 khai báo đơn hàng, ba tool (`issue_refund` gắn cờ `True` cho side effect) và schema.
2. Dòng 38–60 cài đặt `run_support_agent()` với giới hạn `max_steps`, phát hiện `repeat` và bước gọi `approve(name, args)` trước khi chạy tool có tác dụng phụ.
3. Dòng 63–65 viết `policy_gate()` chỉ cho phép hoàn tiền khi `days_late >= 3` và `amount <= 20%` tổng đơn.
4. Dòng 68–97 chạy cả ba kịch bản rồi in `stopped_reason`, `pending`, từng bước trace, `audit` và sổ `REFUNDS`.

**Điểm đáng chú ý:** Ở yêu cầu hoàn `$50` bị từ chối cho đơn `1044`, `run_support_agent()` dừng với `needs_approval`, trả về `pending`, ghi `ok=False by=policy_gate`, và `REFUNDS` chỉ có mỗi đơn `1042`.

**Tự thử:** Đổi số tiền trong kịch bản `"rejected "` từ `50.0` xuống `24.0` (đúng 20% của `$120.0`) và thêm một câu trả lời cuối vào script để thấy `policy_gate` cho qua êm đẹp.
