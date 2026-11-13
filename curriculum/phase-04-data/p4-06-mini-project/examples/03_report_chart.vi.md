# Vẽ biểu đồ lượng token theo model

**Ví dụ này cho thấy:** cách biến bảng báo cáo SQL đã sắp xếp thành biểu đồ cột có đầy đủ nhãn và in một dòng tóm tắt model tốn nhiều token nhất.

**Từng bước**
1. Dòng 23–40 làm sạch log, đưa vào SQLite và truy vấn `model` cùng `total_tokens` theo thứ tự giảm dần.
2. Dòng 42–48 vẽ biểu đồ cột bằng `ax.bar(...)`, đặt tiêu đề và nhãn hai trục, rồi gọi `plt.show()`.
3. Dòng 50–52 in tên model tiêu thụ nhiều token nhất cùng tổng số token ra stdout.

**Để ý:** gọi `.tolist()` giúp truyền list chuỗi và số Python thuần cho Matplotlib, tránh lẫn định dạng scalar của NumPy cả khi vẽ lẫn khi in tóm tắt.

**Tự thử:** đổi sang vẽ `avg_latency` thay cho `total_tokens` (kèm cập nhật tiêu đề và nhãn trục y) để so sánh trực quan tốc độ phản hồi giữa các model.
