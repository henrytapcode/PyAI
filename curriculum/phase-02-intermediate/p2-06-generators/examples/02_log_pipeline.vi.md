# Pipeline xử lý log

**Ví dụ này cho thấy:** hai generator nhỏ nối với nhau để tìm các dòng `ERROR` trong một file. File được đọc từng dòng một.

**Từng bước**
1. Dòng 6–9 định nghĩa `read_lines`. Nó mở file và yield từng dòng sau khi đã bỏ dấu cách và ký tự xuống dòng.
2. Dòng 12–15 định nghĩa `only_errors`. Nó nhận bất kỳ iterable nào chứa các dòng và chỉ yield những dòng có chứa `ERROR`.
3. Dòng 18–25 tạo một thư mục tạm và ghi vào đó một file log năm dòng.
4. Dòng 27 nối hai công đoạn lại. Vẫn chưa đọc gì cả. Dòng 28 xin lỗi đầu tiên, nên chỉ hai dòng đầu của file được xử lý.
5. Dòng 29 gom phần còn lại vào một list. Dòng 31 tạo một pipeline **mới** để đếm số lỗi bằng `sum`.

**Lưu ý:** dòng 31 bắt đầu một pipeline mới thay vì dùng lại `errors`, vì `errors` đã bị dùng hết ở dòng 28–29.

**Thử tự làm:** thêm `f.write("ERROR gpu memory\n")` sau dòng 25. Số lỗi cuối cùng phải thành 3.
