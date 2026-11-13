# Chi phí API theo từng mô hình

**Ví dụ này cho thấy:** cách gom nhóm chi phí API theo mô hình bằng pandas, sắp xếp giảm dần, vẽ biểu đồ cột bằng `ax.bar()` và in tổng chi phí theo định dạng gọn.

**Từng bước**
1. Dòng 5–8 tạo một DataFrame gồm sáu dòng request API thuộc ba mô hình.
2. Dòng 10 cộng tổng `cost` theo từng `model` bằng `.groupby("model")["cost"].sum()` rồi sắp xếp từ cao xuống thấp.
3. Dòng 12–17 tạo `(fig, ax)`, vẽ cột từ `totals.index.tolist()` và `totals.tolist()`, gắn nhãn rồi gọi `plt.show()`.
4. Dòng 19–20 duyệt qua `totals.items()` (trả về từng cặp `(nhãn, giá trị)` của Series) và in tổng chi phí của từng mô hình làm tròn hai chữ số thập phân.

**Để ý:** dùng `.tolist()` giúp chuyển Index và giá trị pandas thành list Python thuần, tránh in ra các kiểu scalar của NumPy.

**Tự thử:** đổi `ax.bar(...)` ở dòng 13 thành `ax.barh(...)` (và đổi chỗ hai nhãn trục x/y) để xem biểu đồ cột nằm ngang hiển thị ra sao.
