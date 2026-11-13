# Lặp từng hàng

Cách này duyệt qua từng hàng của `probs`, gọi `row.argmax()` để lấy chỉ số lớp tốt nhất rồi kiểm tra trực tiếp `row[best_idx]` thay vì tính riêng mảng `max(axis=1)`. Cách viết này rất dễ đọc và tiện khi bạn cần ghi log hoặc xử lý hòa điểm riêng cho từng hàng, dù `argmax(axis=1)` kết hợp `max(axis=1)` sẽ nhanh hơn khi một lô có hàng nghìn hàng.
