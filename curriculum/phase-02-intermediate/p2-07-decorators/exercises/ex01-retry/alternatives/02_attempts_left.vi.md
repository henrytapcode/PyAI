# Đếm ngược số lần thử còn lại

Vòng `while True` giữ một biến đếm `attempts_left`. Mỗi vòng giảm nó đi rồi thử gọi hàm. Khi lời gọi raise lỗi mà không còn lần nào, `raise error` chuyển lỗi ra ngoài; nếu còn thì vòng lặp đơn giản là chạy tiếp. Cách này làm ý "còn mấy lần thử" rất rõ ràng và cũng tiện nếu sau này bạn muốn log từng lần thử, nhưng bạn phải cẩn thận để vòng lặp luôn kết thúc: nếu quên giảm biến đếm thì nó không bao giờ dừng.
