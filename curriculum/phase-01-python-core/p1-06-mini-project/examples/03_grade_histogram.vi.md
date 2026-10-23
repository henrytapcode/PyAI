# Biểu đồ phân bố xếp loại

**Ví dụ này cho thấy:** đếm bằng dict, rồi biến số đếm thành một biểu đồ chữ đơn giản. Đây cũng là ý tưởng của `grade_counts` trong `class_stats`.

**Từng bước**
1. Dòng 2 là list các chữ cái xếp loại, như thể `letter_grade` đã chạy xong cho bảy học sinh.
2. Dòng 4 tạo dict đếm với mọi loại bằng `0`. Có đủ năm khóa ngay từ đầu nghĩa là loại nào không ai đạt vẫn hiện ra với số `0`.
3. Dòng 5–6 duyệt qua các chữ cái. `counts[letter] += 1` tìm đúng khóa rồi cộng thêm một.
4. Dòng 8 in cả dict.
5. Dòng 9–10 lặp bằng `.items()`, cho ta từng khóa và giá trị cùng lúc. `'#' * how_many` lặp ký tự `#` bấy nhiêu lần, tạo thành thanh biểu đồ.

**Để ý:** nếu bắt đầu bằng dict rỗng `{}`, thì `counts["A"] += 1` sẽ báo lỗi `KeyError` ngay lần đầu, vì khóa chưa tồn tại. Bắt đầu với đủ năm khóa giúp tránh lỗi đó.

**Tự thử:** thêm `"D"` vào list rồi chạy lại. Hãy đoán dòng `D` mới trước khi chạy (phải là `D: # (1)`).
