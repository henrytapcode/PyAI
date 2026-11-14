# Chuyển cột giá dạng chữ sang số

**Ví dụ này cho thấy:** cách xóa dấu phẩy hàng nghìn ở cột giá dạng chữ, ép các ô không đọc được thành `NaN` bằng `pd.to_numeric(..., errors="coerce")`, rồi chuyển các dòng hợp lệ sang `int64`.

**Từng bước**
1. Dòng 4–7 tạo `orders` chứa cột giá lộn xộn (`"1,200"`, `"N/A"`, `" 350 "`, `"free"`, `"890"`).
2. Dòng 9–10 xóa dấu phẩy bằng `.str.replace(",", "", regex=False)` rồi ép cột về kiểu số.
3. Dòng 12–13 đếm xem có bao nhiêu ô biến thành `NaN` (`2`) và in dưới dạng `int` Python thuần.
4. Dòng 15–18 bỏ các hàng `NaN`, ép `price` sang `"int64"`, rồi in bảng sạch cùng tổng doanh thu.

**Để ý:** nếu không có `errors="coerce"`, `pd.to_numeric` sẽ báo lỗi `ValueError` ngay khi gặp `"N/A"` hoặc `"free"`.

**Tự thử:** đổi `"free"` ở dòng 6 thành `" 450 "` rồi xem `Unreadable prices` giảm từ `2` xuống `1`.
