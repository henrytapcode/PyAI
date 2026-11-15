# Tách riêng hàm hỗ trợ `_dispatch_call` và `_assistant_tool_message`

Thay vì lồng toàn bộ phần điều phối, bắt lỗi và tạo message vào bên trong vòng `for`, cách này tách `_dispatch_call()` và `_assistant_tool_message()` thành các hàm độc lập. Tách riêng phần xử lý một tool call khỏi vòng lặp giúp kiểm thử đơn vị logic bắt lỗi dễ dàng hơn và tái sử dụng thuận tiện khi sang bài agent nhiều bước ở `p7-07-agents`, đổi lại thêm vài hàm phụ với các script nhỏ.
