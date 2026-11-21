# Dùng hàm chuẩn `posixpath.normpath`

Thay vì tự quản lý ngăn xếp (stack) từng đoạn đường dẫn, cách này giao việc gộp `.` và `..` cho hàm chuẩn `posixpath.normpath` của Python. Có một chi tiết nhỏ theo chuẩn POSIX: `normpath("//a")` giữ nguyên hai dấu gạch chéo đầu `//a`, nên vòng lặp `while` cắt bớt dấu `/` thừa ở đầu. Cả hai cách đều cho kết quả giống hệt nhau.
