# Chọn ngưỡng lọc ticket spam

**Ví dụ này cho thấy:** Thử năm ngưỡng khác nhau trên 12 ticket đã gắn nhãn và chọn ngưỡng cho accuracy cao nhất.

**Từng bước**
1. Dòng 4–5 tạo mảng `scores` (điểm nghi ngờ spam) và `labels` (`0` là bình thường, `1` là spam) cho 12 ticket.
2. Dòng 7–8 khởi tạo `best_t` và `best_acc` để ghi lại ngưỡng tốt nhất.
3. Dòng 10–16 duyệt qua năm ngưỡng thử nghiệm, đổi `scores >= t` thành dự đoán `0`/`1` bằng `.astype("int64")`, tính accuracy và cập nhật kết quả tốt nhất khi accuracy cao hơn.
4. Dòng 18 in ra ngưỡng tốt nhất cùng accuracy đã làm tròn.

**Để ý:** Có một ticket mang `score = 0.34` nhưng `label = 1`, nên `threshold = 0.55` vẫn đoán sai một ca (`11 / 12 = 0.917`) — dữ liệu thực tế hiếm khi phân tách hoàn toàn đạt `1.0`.

**Tự thử:** Thêm `0.34` vào danh sách ngưỡng thử nghiệm và xem việc hạ ngưỡng làm accuracy chung tăng hay giảm.
