# Chuyển kiểu dữ liệu từ form

**Ví dụ này cho thấy:** vì sao văn bản đến từ bên ngoài phải được chuyển kiểu trước khi tính toán.

**Từng bước**
1. Dòng 2–3 giữ giá trị đúng như một form web gửi lên: dạng văn bản, dù trông giống số.
2. Dòng 5 cộng hai chuỗi. Với văn bản, `+` nghĩa là "nối", nên bạn được `2121` chứ không phải `42`.
3. Dòng 6–7 chuyển kiểu: `int()` cho số nguyên, `float()` cho số thập phân.
4. Dòng 8 cộng hai số thật và in ra `42`. Dòng 9–10 dùng các giá trị đã chuyển trong f-string.
5. Dòng 11 chứng minh việc chuyển kiểu đã thành công: `<class 'int'> <class 'float'>`.

**Để ý:** `1.68 * 100` in ra `168.0` chứ không phải `168`. Float vẫn là float kể cả khi kết quả là số tròn.

**Tự thử:** sửa dòng 6 thành `age = int(height_text)` rồi chạy. Đọc thông báo `ValueError`: nó cho biết chính xác đoạn văn bản nào không chuyển được.
