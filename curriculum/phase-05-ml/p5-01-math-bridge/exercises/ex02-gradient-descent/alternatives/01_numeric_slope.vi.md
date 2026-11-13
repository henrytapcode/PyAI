# Ước lượng độ dốc bằng số

Thay vì lắp vào công thức `grad_w` và `grad_b` cho sẵn, phiên bản này tự ước lượng từng độ dốc trực tiếp từ `mse` bằng cách nhích `w` và `b` lên xuống một khoảng rất nhỏ `h = 0.001`, giống hệt §4 trong bài học. Nhờ vậy bạn chỉ cần viết đúng hàm loss mà không phải nhớ công thức gradient cho từng dạng hàm. Đổi lại là tốc độ: mỗi bước phải gọi `mse` thêm bốn lần, vẫn rất nhẹ với hai tham số ở đây nhưng sẽ quá chậm khi mô hình có hàng nghìn hoặc hàng triệu trọng số.
