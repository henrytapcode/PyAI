# Một class với `__enter__` và `__exit__`

Cùng hành vi nhưng viết thành class (§3). `__enter__` nhớ giá trị cũ rồi đặt giá trị mới, còn `__exit__` trả mọi thứ về như cũ và trả về `False` để lỗi không bị giấu. Hàm nhỏ ở cuối chỉ có để test vẫn gọi được `temporary_setting(...)` như trước. Cách này dài hơn generator, nhưng là lựa chọn tốt hơn khi manager phải giữ thêm trạng thái mà bạn đọc lại sau đó.
