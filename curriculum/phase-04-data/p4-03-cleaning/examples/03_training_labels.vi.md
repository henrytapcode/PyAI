# Làm sạch nhãn cho tập huấn luyện phân loại

**Ví dụ này cho thấy:** cách chuẩn hóa văn bản và nhãn bằng `.str`, loại bỏ dòng có text rỗng, bỏ mẫu bị trùng lặp và kiểm tra phân bố nhãn cuối bằng `value_counts()`.

**Từng bước**
1. Dòng 4–23 tạo một dataset `(text, label)` nhỏ có khoảng trắng thừa, chữ hoa thường lẫn lộn, dấu `_` và `-`, text rỗng và câu bị lặp.
2. Dòng 25–33 copy bảng, cắt khoảng trắng hai đầu của `text`, và chuẩn hóa `label` bằng strip, viết thường, rồi đổi `_` và `-` thành dấu cách.
3. Dòng 35–36 bỏ các hàng có `text` rỗng và loại dòng trùng theo `text` với `keep="last"`.
4. Dòng 38–41 in dataset sạch và `value_counts()` cuối cùng của từng nhãn.

**Để ý:** việc `strip()` cột `text` trước khi lọc `df["text"] != ""` và loại trùng giúp phát hiện `"   "` là rỗng và gộp `" Reset password "` với `"Reset password"`.

**Tự thử:** đổi `keep="last"` ở dòng 36 thành `keep="first"` rồi xem thứ tự hàng của `Reset password` thay đổi thế nào.
