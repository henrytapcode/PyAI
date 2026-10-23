# Sắp xếp trực tiếp các học sinh

Ở đây không có list `rows`. Hàm key `student_key` nhận một dict học sinh và tự tính điểm trung bình, nên `sorted(students, key=student_key)` sắp xếp ngay các dict gốc. Sau đó vòng lặp tính điểm trung bình lần thứ hai để tạo từng dòng.

Cách này ngắn hơn, nhưng `average` chạy hai lần cho mỗi học sinh. Với lớp 30 người thì không đáng kể; với dữ liệu lớn bạn nên tính mỗi điểm trung bình một lần như lời giải chính. Cách dùng rows cũng dễ debug hơn, vì bạn có thể `print(rows)` và thấy chính xác cái gì đang được sắp xếp.
