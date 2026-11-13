# Đường cong training loss và validation loss

**Ví dụ này cho thấy:** cách vẽ hai đường (`train_loss` và `val_loss`) trên cùng một `Axes` kèm điểm đánh dấu, nhãn trục, chú thích và lưới, rồi in ra epoch có validation loss thấp nhất.

**Từng bước**
1. Dòng 4–6 khai báo sáu epoch cùng giá trị training loss và validation loss tương ứng.
2. Dòng 8–10 tạo cặp `(fig, ax)` bằng `plt.subplots()` và vẽ cả hai đường với `marker="o"` cùng tên `label=`.
3. Dòng 11–16 đặt tiêu đề, nhãn hai trục, chú thích, bật lưới rồi gọi `plt.show()`.
4. Dòng 18–19 tìm vị trí của `min(val_loss)` và in ra epoch tốt nhất.

**Để ý:** mỗi lời gọi `ax.plot(...)` phải truyền `label=` trước khi gọi `ax.legend()`, nếu không hộp chú thích sẽ trống rỗng.

**Tự thử:** thêm epoch thứ 7 với `train_loss` là `0.21` và `val_loss` là `0.49` rồi xem biểu đồ và epoch tốt nhất được in ra thay đổi thế nào.
