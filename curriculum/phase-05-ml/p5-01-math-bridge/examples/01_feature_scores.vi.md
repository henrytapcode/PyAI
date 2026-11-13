# Chấm điểm request bằng tích vô hướng

**Nội dung minh họa:** Dùng toán tử `@` để biến vector feature của từng request cùng một vector trọng số chung thành một điểm số duy nhất, rồi chọn request có điểm cao nhất.

**Từng bước**
1. Dòng 5–9 lưu mỗi API request thành một vector NumPy gồm ba feature: số nghìn token, độ trễ (giây) và số lần thử lại.
2. Dòng 11–12 định nghĩa `weights` (mỗi feature một trọng số) và `bias` của mô hình.
3. Dòng 14–18 lặp qua từng request, tính `weights @ features + bias` dưới dạng `float` Python và in ra điểm đã làm tròn.
4. Dòng 20–22 dùng `np.argmax(scores)` để tìm chỉ số của điểm cao nhất rồi in mã request tương ứng.

**Lưu ý:** `weights @ features` trả về một con số duy nhất cho mỗi request thay vì một mảng, và bọc kết quả bằng `float(...)` giúp việc định dạng ở Python gọn gàng.

**Tự thử:** Đổi trọng số cho số lần thử lại trong `weights` từ `0.8` lên `3.0` rồi xem điểm của `req-102` và `req-103` tăng thế nào so với `req-101`.
