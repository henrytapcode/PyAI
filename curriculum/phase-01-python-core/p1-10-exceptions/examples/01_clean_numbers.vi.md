# Làm sạch những con số lộn xộn

**Ví dụ này cho thấy:** một hàm trợ giúp nhỏ có thể dùng lại, `safe_int`, biến văn bản thành số hoặc trả về giá trị mặc định thay vì làm chương trình sập.

**Từng bước**
1. Dòng 2–6 định nghĩa `safe_int`. Lệnh có rủi ro `int(text)` là dòng duy nhất nằm trong `try`.
2. Dòng 5 bắt hai loại exception cùng lúc. `"twelve"` và `""` gây `ValueError`; `None` gây `TypeError` (`int(None)` vô nghĩa).
3. Dòng 9 là dữ liệu đầu vào lộn xộn. Lưu ý `" 7 "` vẫn ổn: `int()` bỏ qua khoảng trắng quanh các chữ số.
4. Dòng 14 truyền `default=None`. `None` không bao giờ bị nhầm với một số thật, nên dòng 15 có thể hỏi `value is None` để nhận ra giá trị lỗi.
5. Dòng 16 và 18 đếm giá trị lỗi và gom giá trị tốt. Chương trình kết thúc với `sum: 59` thay vì chết ở giá trị thứ ba.

**Để ý:** giá trị mặc định là lựa chọn của bạn cho từng tình huống. `0` ổn khi bạn chỉ cần tổng; `None` tốt hơn khi bạn phải biết là có chuyện không ổn.

**Tự thử:** thêm `"3.5"` vào `raw_values`. Nó có bị tính là lỗi không? (Có: `int("3.5")` gây `ValueError`, nên `bad values` thành `4`.)
