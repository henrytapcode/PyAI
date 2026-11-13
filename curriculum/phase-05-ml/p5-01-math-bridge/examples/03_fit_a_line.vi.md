# Khớp đường thẳng bằng gradient descent

**Nội dung minh họa:** Huấn luyện đường thẳng `y = w * x + b` trên dữ liệu token-độ trễ qua 50 bước gradient descent, in mức giảm của loss và vẽ đường khớp lên biểu đồ.

**Từng bước**
1. Dòng 5–6 tạo năm cặp đo thực tế `(tokens_k, latency_s)` xấp xỉ nằm trên một đường thẳng.
2. Dòng 8–11 khởi tạo `w` và `b` bằng `0.0`, đặt `lr = 0.04` và tạo danh sách `losses`.
3. Dòng 13–19 lặp 50 lần: tính dự đoán, tính sai số, lưu MSE loss, tính gradient MSE `grad_w` và `grad_b`, rồi bước cả hai tham số theo hướng giảm loss.
4. Dòng 21–23 in `w`, `b`, loss ban đầu và loss cuối cùng đã làm tròn; dòng 25–33 vẽ các điểm dữ liệu và đường thẳng khớp trên cùng hệ trục.

**Lưu ý:** Chỉ sau 50 bước, loss đã rơi từ `4.836` xuống `0.002`, và đường thẳng khớp đi qua sát giữa các điểm đo.

**Tự thử:** Tăng `lr` từ `0.04` lên `0.1` rồi quan sát xem loss cuối cùng có thấp hơn nữa hay bắt đầu bật tăng ngược lại.
