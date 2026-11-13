# Tổng hợp feedback theo model với GROUP BY và HAVING

**Ví dụ này cho thấy:** cách gom nhóm đánh giá người dùng theo từng model với `AVG` và `COUNT(*)`, loại các nhóm quá ít mẫu bằng `HAVING` và làm tròn trung bình tới 2 chữ số thập phân.

**Từng bước**
1. Dòng 4–11 tạo bảng `feedback` gồm cột `model` và `rating`.
2. Dòng 13–26 chèn bảy lượt đánh giá của bốn model bên trong `with conn:`.
3. Dòng 28–37 gom nhóm theo `model`, chỉ giữ các model có `COUNT(*) >= 2`, làm tròn `AVG(rating)` còn 2 chữ số rồi sắp theo `avg_rating DESC, model ASC`.
4. Dòng 39–42 in điểm trung bình cùng số lượt đánh giá của từng model đạt ngưỡng, rồi đóng kết nối.

**Để ý:** `local-7b` chỉ có 1 lượt đánh giá nên bị `HAVING COUNT(*) >= 2` loại *sau khi* gom nhóm, còn `model ASC` phá thế hòa 4.5 giữa `claude` và `gpt-4o`.

**Tự thử:** thêm một lượt `("local-7b", 5)` vào `rows` rồi xem `local-7b` đứng ở vị trí nào trong kết quả.
