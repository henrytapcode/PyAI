# Quét một lượt sau khi sắp xếp

Thay vì quét lại toàn bộ mảng `scores` cho từng ngưỡng ứng viên (`O(n^2)`), phiên bản này sắp xếp các cặp `(score, label)` một lần rồi duyệt từ thấp đến cao bằng vòng lặp Python thuần (`O(n log n)`). Tại mỗi giá trị `t` riêng biệt, tổng `left_zeros + right_ones` cho ngay số lượng dự đoán đúng mà không phải tạo lại mảng dự đoán ở từng bước. Với mảng nhỏ vài chục phần tử, vòng lặp NumPy ở `solution.py` ngắn gọn và đủ nhanh, còn với hàng chục nghìn điểm thì cách quét sau khi sắp xếp này tránh được chi phí bậc hai.
