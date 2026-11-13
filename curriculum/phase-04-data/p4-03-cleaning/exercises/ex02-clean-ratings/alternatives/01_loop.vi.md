# Vòng lặp từng dòng với dictionary theo user

Cách này duyệt từng cặp `(user, rating)` theo từng hàng, tự phân tích và kiểm tra khoảng hợp lệ bằng Python thuần, rồi lưu điểm hợp lệ mới nhất vào một `dict` có khóa là `user` đã chuẩn hóa (dùng `.pop()` xóa khóa cũ trước khi ghi để thứ tự hàng khớp `keep="last"`). Cách viết này dễ mở rộng khi mỗi dòng cần kiểm tra phức tạp hoặc ghi log riêng, nhưng chạy chậm hơn nhiều so với các phép vector hóa của pandas trên bảng lớn.
