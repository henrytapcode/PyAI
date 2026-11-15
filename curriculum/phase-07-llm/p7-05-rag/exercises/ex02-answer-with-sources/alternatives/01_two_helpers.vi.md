# Tách thành hai hàm phụ `_retrieve` và `_build_messages` cùng một lần embed gộp

Thay vì viết toàn bộ pipeline trong một hàm, cách này tách riêng `_retrieve()` và `_build_messages()`, embed cả các chunk lẫn câu hỏi trong một lần gọi `client.embed(...)` duy nhất, và khử trùng nguồn trích dẫn bằng `dict.fromkeys(...)`. Tách riêng bước truy xuất và bước dựng prompt giúp dễ viết unit test hoặc thay thế từng phần độc lập, còn gộp câu hỏi vào chung lô embed tiết kiệm một lượt gọi khi chạy thử nghiệm (dù ở production bạn thường embed sẵn các chunk từ trước và chỉ embed câu hỏi lúc truy vấn).
