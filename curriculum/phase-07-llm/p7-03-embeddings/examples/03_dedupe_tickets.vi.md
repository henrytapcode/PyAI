# Tìm các ticket hỗ trợ gần trùng nhau

**Những gì ví dụ minh họa:** Tính toàn bộ độ tương đồng từng cặp trong một phép nhân `matrix @ matrix.T` rồi chỉ duyệt nửa tam giác trên để phát hiện ticket trùng lặp.

**Từng bước một**
1. Dòng 5–13 liệt kê năm `TICKETS` hỗ trợ và đặt ngưỡng `THRESHOLD = 0.5`.
2. Dòng 15–17 embed cả năm ticket một lần thành `matrix` (shape `(5, 256)`) rồi nhân `matrix @ matrix.T` để thu về bảng điểm `5 x 5`.
3. Dòng 20–25 lặp theo `i` và `j > i` (phần tam giác trên) để mỗi cặp chỉ kiểm một lần và bỏ qua đường chéo chính `(i, i)`.
4. Dòng 23–25 in mọi cặp có điểm cosine lớn hơn hoặc bằng `THRESHOLD`.

**Lưu ý:** Cho `j` chạy từ `i + 1` giúp tránh lặp lại cùng một cặp theo thứ tự ngược `(1, 0)` và bỏ qua trường hợp tự so sánh `(0, 0)` vốn luôn bằng `1.0`.

**Tự thử:** Hạ `THRESHOLD` xuống `0.3` hoặc thêm ticket `"My laptop has a startup failure"` để xem cặp trùng mới xuất hiện.
