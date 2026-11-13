# Vòng lặp từng hàng với itertuples

Cách làm này duyệt qua `df.itertuples(index=False)` và cộng dồn tổng điểm cùng số lần đếm vào hai dict Python, đồng thời tự nhiên trả về `{}` khi không có hàng `"ok"` nào. Dù logic biến tích lũy rất quen thuộc từ Phase 1, `.groupby("model")["score"].mean()` của pandas ngắn gọn hơn nhiều và chạy nhanh hơn đáng kể trên bảng dữ liệu lớn vì việc gom nhóm và tính trung bình được thực hiện bằng code biên dịch sẵn thay vì vòng lặp Python.
