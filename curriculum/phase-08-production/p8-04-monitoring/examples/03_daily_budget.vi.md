# Cảnh báo ngân sách và độ trễ hằng ngày

**Ví dụ này minh họa gì:** Tổng hợp dữ liệu request của ba ngày (`day_1` đến `day_3`) và kiểm tra các ngưỡng độ trễ, ngân sách sớm và tỉ lệ lỗi cho từng ngày.

**Từng bước**
1. Dòng 12–24 định nghĩa `summarize(records)` để tính `count`, `error_rate`, `p95_ms` (nearest-rank), `total_cost` và `cache_hit_rate`.
2. Dòng 27–39 định nghĩa `check_alerts(...)`, phát cảnh báo cứng `"budget exceeded"` khi chi phí vượt `budget` hoặc cảnh báo sớm `"budget warning"` khi chi tiêu chạm 80% `budget`.
3. Dòng 43–64 chuẩn bị bản ghi cố định cho ba ngày: `day_1` bình thường, `day_2` vượt cả độ trễ, chi phí lẫn tỉ lệ lỗi, còn `day_3` chạy nhanh và không lỗi nhưng đã tiêu `$17.00` (`85%` ngân sách `$20.00`).
4. Dòng 66–73 in tóm tắt và các cảnh báo của từng ngày.

**Điểm cần chú ý:** Ở `day_3`, độ trễ và tỉ lệ lỗi đều ổn và chi phí vẫn dưới `$20.00`, nhưng ngưỡng cảnh báo sớm 80% vẫn kịp báo `"budget warning: 85% of budget used"` trước khi chạm trần ngân sách.

**Tự thử thêm:** Hạ ngưỡng `0.8` trong `check_alerts` xuống `0.5` và xem ngày nào trước đó cũng bắt đầu nhận cảnh báo sớm.
