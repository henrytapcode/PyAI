# Lọc và loại trùng trong Python

Cách thay thế này lấy toàn bộ các dòng `(user, rating)` bằng `SELECT user, rating FROM feedback`, lọc `rating <= max_rating` bằng `set` comprehension trong Python để loại trùng rồi sắp xếp bằng `sorted(...)`. Cách này chạy ổn với bảng nhỏ, nhưng khi dữ liệu lớn thì để SQL lọc bằng `WHERE rating <= ?`, `DISTINCT` và `ORDER BY` tốt hơn nhiều vì chỉ các tên user khớp điều kiện mới đi ra khỏi database thay vì nạp hàng triệu dòng vào bộ nhớ Python.
