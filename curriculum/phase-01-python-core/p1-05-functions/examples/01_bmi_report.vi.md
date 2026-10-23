# Báo cáo BMI: hàm gọi hàm

**Ví dụ này cho thấy:** ba hàm nhỏ, mỗi hàm làm một việc, ghép lại thành một bản báo cáo. Chương trình thật được xây dựng như vậy.

**Từng bước**
1. Dòng 2–4 định nghĩa `bmi`. Hàm nhận hai tham số và **trả về** một con số. Ở đây không in gì cả.
2. Dòng 7–13 định nghĩa `bmi_category`. Mỗi `return` kết thúc hàm, nên `if` kế tiếp chỉ chạy khi `if` trước không khớp. Vì vậy `value < 25` thực chất nghĩa là "từ 18.5 đến dưới 25".
3. Dòng 16–19 định nghĩa `report`. Dòng 17 gọi `bmi(...)` và lưu kết quả trả về vào `value`. Dòng 18 đưa `value` cho `bmi_category`. Dòng 19 ghép thành câu cuối cùng. Trong f-string, `:.1f` nghĩa là "hiện 1 chữ số thập phân".
4. Dòng 22–24 gọi `report` ba lần với các đối số khác nhau. Trước dòng 22 không có gì được in: các dòng `def` chỉ *định nghĩa*.

**Để ý:** `report` không lặp lại công thức BMI. Nếu công thức thay đổi, bạn chỉ sửa `bmi` ở một chỗ.

**Tự thử:** bấm **Visualize** và xem một khung (frame) mới xuất hiện cho `report`, rồi thêm một khung cho `bmi` bên trong, và biến mất khi `return` chạy. Sau đó thêm `print(report("You", 60, 1.70))`.
