# Class quản lý trạng thái theo từng bước

Cách tiếp cận này tách toàn bộ trạng thái một lượt chạy vào `_AgentSession` với phương thức `step()` trả về mã dừng hoặc `None`, đồng thời gom các kiểm tra kỳ vọng thành bảng `(label, failed)`. Tách từng lượt thành `step()` giúp bạn dễ dàng tạm dừng, đọc trạng thái giữa chừng hoặc chạy tiếp sau khi có người duyệt trong các ứng dụng lớn hơn.
