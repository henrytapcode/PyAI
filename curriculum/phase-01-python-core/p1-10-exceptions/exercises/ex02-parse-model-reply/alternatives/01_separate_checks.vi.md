# Các khối except riêng và return sớm

Phiên bản này đặt `json.JSONDecodeError` trong một khối `except` riêng và xử lý `KeyError` cùng `TypeError` ở khối khác. Nó kiểm tra khoảng của score bằng `return` sớm thay vì `raise`. Nó dùng một dict `UNKNOWN` chung và `sum(...)` với generator, một cách viết ngắn bạn sẽ gặp ở phần sau của khóa học. Tách thành nhiều khối là lựa chọn tốt khi bạn muốn phản ứng khác nhau với từng vấn đề, ví dụ in thông báo khác nhau. Khi mọi lỗi đều dùng cùng một giá trị dự phòng, một tuple (như lời giải chính) sẽ ngắn hơn.
