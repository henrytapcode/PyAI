# So sánh đường cong underfit, vừa khớp và overfit

**Nội dung minh họa:** Khớp các đa thức bậc `1`, `3` và `6` trên 8 điểm train có nhiễu, in sai số train/test MSE và vẽ cả ba đường cong cùng các điểm train và test.

**Từng bước**
1. Dòng 5–7 tạo 12 điểm có nhiễu dọc theo một đường cong vòng cung với `x` trong `[0, 1]`.
2. Dòng 9–11 xáo chỉ số bằng seed `27` rồi tách `8` điểm cho train và `4` điểm cho test.
3. Dòng 13–16 tạo lưới `grid` 100 điểm mượt mà và vẽ các điểm train, test lên biểu đồ.
4. Dòng 18–23 khớp bậc `1`, `3` và `6` bằng `np.polyfit` chỉ trên `x_train`, in `train_mse` cùng `test_mse`, rồi vẽ từng đường bằng `np.polyval`.
5. Dòng 25–30 đặt tiêu đề, nhãn trục, chú thích, lưới và hiển thị biểu đồ.

**Lưu ý:** Bậc `1` bị underfit (`test_mse = 0.283`), bậc `3` vừa khớp (`test_mse = 0.018`), còn bậc `6` bị overfit nặng (`train_mse = 0.004` nhưng `test_mse = 1.66`).

**Tự thử:** Thêm bậc `2` vào danh sách `[1, 3, 6]` và xem parabol có đạt `test_mse` tốt hơn bậc `3` không.
