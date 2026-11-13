# Làm sạch khảo sát người dùng bị thiếu dữ liệu

**Ví dụ này cho thấy:** cách đếm ô thiếu theo từng cột, bỏ hàng thiếu cột khóa bắt buộc (`user`), và điền điểm số bị thiếu bằng giá trị trung vị (median).

**Từng bước**
1. Dòng 5–14 nạp chuỗi CSV khảo sát vào `df` bằng `pd.read_csv(io.StringIO(csv_text))`.
2. Dòng 15–16 in `df.isna().sum()` để thấy mỗi cột thiếu bao nhiêu ô (`user`: 1, `score`: 2).
3. Dòng 18–20 bỏ hàng bị thiếu `user`, đánh lại index, tính trung vị điểm (`4.0`) rồi điền vào các ô `score` còn trống.
4. Dòng 22–24 in bảng đã làm sạch và điểm trung bình cuối cùng.

**Để ý:** `dropna(subset=["user"])` chạy trước `median()` để hàng không có `user` hợp lệ không làm ảnh hưởng giá trị dùng để điền.

**Tự thử:** đổi `cleaned["score"].median()` ở dòng 19 thành `cleaned["score"].mean()` rồi xem giá trị được điền có thay đổi không.
