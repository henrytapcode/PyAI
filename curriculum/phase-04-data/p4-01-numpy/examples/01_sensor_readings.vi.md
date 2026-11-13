# Dữ liệu cảm biến nhiệt độ

**Ví dụ này cho thấy:** cách tính các số đo tổng hợp và dùng boolean mask để tách giá trị bất thường khỏi dữ liệu cảm biến sạch.

**Từng bước**
1. Dòng 4 đưa bảy lần đo nhiệt độ (độ C) vào một mảng NumPy 1D.
2. Dòng 5–7 in giá trị nhỏ nhất, lớn nhất và trung bình chung bằng `.min()`, `.max()` và `.mean()`.
3. Dòng 9 tạo mask bằng `|` (hoặc) để bắt các giá trị nằm ngoài đoạn `[10, 35]` và lọc ra hai điểm bất thường (`41.8` và `-5.0`).
4. Dòng 12 dùng `&` (và) kèm ngoặc đơn quanh mỗi phép so sánh để chỉ giữ lại năm lần đo bình thường, rồi in số lượng và trung bình sau khi lọc.

**Để ý:** mỗi điều kiện nối bằng `&` hoặc `|` phải đặt trong ngoặc đơn `( ... )`, và phép lọc tạo ra mảng mới mà không làm đổi `temps_c`.

**Tự thử:** đổi ngưỡng dưới `10` ở dòng 9 và 12 thành `20`. `normal count` sẽ giảm từ `5` xuống `4` và `clean mean` sẽ tăng từ `22.26` lên `22.98`.
