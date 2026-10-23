# Đếm và dựng dict bằng tay

Phiên bản này đếm từ bằng vòng lặp (mẫu bộ cộng dồn) và dựng dict bằng cách viết ra từng key. Nó làm cùng việc với `len(...)` và `asdict`, nhưng dài hơn và bạn phải nhớ sửa `to_dict` mỗi khi thêm field. `asdict` còn xử lý được cả field chứa dataclass khác, nên lời giải chính là lựa chọn tốt hơn cho code thật. Còn một khác biệt nữa: `to_dict` ở đây trả về đúng cái list `tags` mà object đang giữ, còn `asdict` trả về một bản sao, nên sửa list trong dict cũng sẽ sửa luôn message.
