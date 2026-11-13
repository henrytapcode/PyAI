# Dự đoán theo lô (batch)

**Ví dụ này cho thấy:** cách biến bảng xác suất 2D của mô hình thành nhãn dự đoán và đếm số mẫu có độ tin cậy cao.

**Từng bước**
1. Dòng 4–10 lưu ba tên lớp và bảng xác suất kích thước `(4, 3)` (4 mẫu × 3 lớp, mỗi hàng có tổng bằng `1.0`).
2. Dòng 12 chạy `probs.argmax(axis=1)` để chọn chỉ số cột có xác suất cao nhất cho từng hàng (`[2, 0, 1, 0]`).
3. Dòng 14 chuyển các chỉ số số nguyên đó thành chuỗi dễ đọc bằng list comprehension tra từ `labels`.
4. Dòng 16–19 lấy xác suất cao nhất của mỗi hàng bằng `.max(axis=1)` và đếm số mẫu đạt từ `0.8` trở lên bằng `(top_probs >= 0.8).sum()`.

**Để ý:** truyền `axis=1` bảo cả `argmax` lẫn `max` quét ngang qua các cột của mỗi hàng, cho ra đúng một kết quả cho từng mẫu.

**Tự thử:** hạ ngưỡng tin cậy `0.8` ở dòng 19 xuống `0.7`. Số mẫu tự tin sẽ tăng từ `2` lên `3`.
