# Import trực tiếp các tên hàm

Cách này dùng `from statistics import mean, median, stdev` nên lời gọi ngắn hơn: `mean(values)` thay vì `statistics.mean(values)`. Đây là lựa chọn tốt khi bạn dùng vài tên nhiều lần. Đổi lại, người đọc không còn thấy ngay `mean` đến từ module nào, nên hãy giữ danh sách import ngắn và đặt ở đầu file.
