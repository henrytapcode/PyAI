# Biểu đồ phân tán số token và độ trễ

**Ví dụ này cho thấy:** cách vẽ từng cặp điểm đo `(tokens, latency_ms)` bằng `ax.scatter()` để xem mối quan hệ giữa hai đại lượng và in hệ số tương quan.

**Từng bước**
1. Dòng 5–6 tạo hai mảng NumPy chứa số token đầu vào và độ trễ phản hồi của 8 request.
2. Dòng 8–14 tạo `(fig, ax)`, vẽ biểu đồ phân tán bằng `ax.scatter(tokens, latency_ms)`, đặt nhãn trục, bật lưới rồi gọi `plt.show()`.
3. Dòng 16–17 tính hệ số tương quan bằng `np.corrcoef(...)`, ép sang `float`, làm tròn hai chữ số rồi in ra.

**Để ý:** `ax.scatter` chấm các điểm rời rạc thay vì nối dây giữa chúng — đúng với trường hợp các điểm đo độc lập nhau.

**Tự thử:** sửa giá trị cuối của `latency_ms` từ `790` thành `250` (giả lập một request trúng cache nên trả lời nhanh) để xem biểu đồ và hệ số tương quan thay đổi ra sao.
