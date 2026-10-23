# Cùng việc đó bằng class thường

Không có dataclass ở đây: `__init__`, `__repr__` và `__eq__` đều viết tay, và `tags` bị thiếu được thay trong `__init__` để mỗi message có list riêng. (Mẹo `tags=None` là cách quen thuộc để tránh list mặc định dùng chung trong class thường.) Cách này vượt qua cùng các test, nhưng dài gấp khoảng ba lần, và đó chính là lý do dataclass ra đời. Chỉ dùng class thường khi object cần logic khởi tạo thực sự.
