# Xoay vòng một bản sao của các reply

Cách này giữ một bản sao của list trong `self.queue`. Mỗi lần gọi, nó lấy reply đầu tiên ra bằng `pop(0)` rồi đặt vào cuối bằng `append`, nên hàng đợi xoay vòng như một bánh xe và không cần bộ đếm hay `%`. List gốc `self.replies` không bao giờ bị đổi, nhờ vậy `describe` vẫn đếm được. Cách này gọn với list ngắn, nhưng bản dùng bộ đếm dễ theo dõi hơn khi debug, và `pop(0)` chậm dần với list rất dài.
