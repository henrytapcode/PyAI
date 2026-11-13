# Chi phí API từ CSV

**Ví dụ này cho thấy:** cách đọc chuỗi CSV bằng `io.StringIO`, tạo thêm các cột tính toán và tìm ba lượt gọi tốn kém nhất.

**Từng bước**
1. Dòng 5–10 lưu năm bản ghi gọi API dưới dạng chuỗi CSV nhiều dòng.
2. Dòng 12 đọc chuỗi CSV thành DataFrame bằng `pd.read_csv(io.StringIO(csv_data))`.
3. Dòng 13–14 tính `total_tokens` từ hai cột có sẵn và tính `cost` làm tròn tới 4 chữ số thập phân.
4. Dòng 16 sắp xếp theo `cost` giảm dần, đánh lại index và lấy 3 hàng đầu bằng `.head(3)`.
5. Dòng 18–19 in ra 3 hàng đắt nhất (chọn 3 cột cho gọn) và tổng chi phí của cả bảng.

**Để ý:** bọc `df["cost"].sum()` trong `float(...)` trước khi `round(...)` giúp in ra số `float` thuần của Python thay vì kiểu scalar của NumPy.

**Tự thử:** đổi đơn giá `0.002` ở dòng 14 thành `0.005` và xem chi phí top 3 cùng tổng chi phí thay đổi thế nào.
