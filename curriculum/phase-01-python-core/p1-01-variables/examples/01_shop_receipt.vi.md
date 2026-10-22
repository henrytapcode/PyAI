# Hóa đơn mua hàng

**Ví dụ này cho thấy:** biến, phép tính và f-string phối hợp với nhau trong một chương trình nhỏ có thật.

**Từng bước**
1. Dòng 2–4 lưu tên món (`str`), đơn giá (`float`) và số lượng (`int`).
2. Dòng 6–8 tính giá trị mới từ giá trị cũ: `subtotal` trước, rồi `tax` từ `subtotal`, rồi `total` từ cả hai. Mỗi dòng chỉ dùng được những biến đã tạo ở phía trên nó.
3. Dòng 10–13 in hóa đơn bằng f-string. `round(tax, 2)` làm tròn số tới 2 chữ số thập phân để tiền trông đúng là tiền.
4. Dòng 14 in kiểu của `total`: là `float`, vì `float` nhân `int` cho ra `float`.

**Để ý:** máy tính không "nhớ" công thức. `total` giữ con số `8.25`, chứ không phải "subtotal + tax". Nếu bạn đổi `quantity` sau dòng 8, `total` sẽ không tự cập nhật.

**Tự thử:** đổi `quantity` thành `4` rồi chạy lại. Hãy đoán tổng tiền trước khi bấm Run (kết quả phải là `11.0`).
