# Class với `__enter__` và `__exit__`

Cũng là `edit_expenses` đó, nhưng viết theo cách dài như trong bài về context manager. `__enter__` đọc list (hoặc bắt đầu bằng `[]`) và trả về nó, để nó trở thành tên sau `as`. `__exit__` nhận thông tin về lỗi: khi `exc_type` là `None` thì khối đã chạy xong tốt, nên nó lưu; ngược lại nó không làm gì, và `return False` để lỗi tiếp tục đi. Nếu một khoản chi sai, `save_expenses` raise `ValueError` bên trong `__exit__` và file giữ nguyên như cũ.

Class là lựa chọn tốt hơn khi manager cần giữ nhiều trạng thái hơn hoặc có nhiều method. Với việc ngắn kiểu "chuẩn bị, yield, dọn dẹp" như thế này, generator `@contextmanager` trong lời giải chính ngắn hơn và dễ đọc hơn.
