# Đo thời gian một bước embedding

**Ví dụ này cho thấy:** decorator `timed` đo một hàm và lưu thời gian vào một dict, không in ra gì và không đổi thứ hàm trả về.

**Từng bước**
1. Dòng 5 tạo dict `timings`. Wrapper sẽ điền vào đó.
2. Dòng 8–16 định nghĩa `timed`. Wrapper đọc đồng hồ bấm giờ, gọi hàm gốc với mọi đối số của nó, đọc đồng hồ lần nữa, rồi lưu hiệu số dưới tên của hàm.
3. Dòng 9 đặt `@wraps(func)` lên wrapper, để hàm được decorate giữ nguyên tên và docstring.
4. Dòng 19–22 decorate `embed`, một bước embedding giả biến mỗi văn bản thành `[độ dài, số từ]`.
5. Dòng 25 gọi `embed` như bình thường. Dòng 26–29 in các vector, tên hàm, các key của `timings`, và kiểm tra thời gian không âm.

**Để ý:** thời gian cụ thể không bao giờ được in, vì nó đổi sau mỗi lần chạy. Chỉ in những gì ổn định, và kiểm tra phần còn lại bằng phép so sánh như `>= 0`.

**Tự thử:** gọi `embed(["a", "b", "c"])` thêm một lần nữa trước các dòng print. Dict vẫn chỉ có một key, vì thời gian mới thay thế thời gian cũ dưới cùng một tên.
