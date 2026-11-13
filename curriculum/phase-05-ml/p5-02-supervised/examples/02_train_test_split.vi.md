# Chia train/test và gradient descent

**Nội dung minh họa:** Xáo trộn một DataFrame gồm 10 request bằng seed cố định, giữ lại 20% làm tập test, khớp đường thẳng trên tập train bằng gradient descent rồi so sánh train MSE và test MSE.

**Từng bước**
1. Dòng 5–9 tạo DataFrame gồm 10 request với ba cột `id`, `tokens` và `latency`.
2. Dòng 11–13 tạo bộ sinh số ngẫu nhiên có seed (`42`) và tách chỉ số đã xáo thành `8` dòng train và `2` dòng test.
3. Dòng 15–17 in ra danh sách `id` nằm trong từng tập bằng `.tolist()`.
4. Dòng 19–28 quy đổi `tokens` sang đơn vị nghìn (`x`) và chạy 50 bước gradient descent chỉ trên `x_train` và `y_train`.
5. Dòng 30–33 tính MSE trên cả hai tập rồi in đường thẳng khớp cùng `Train MSE` và `Test MSE`.

**Lưu ý:** `Test MSE` (`0.002`) rất sát với `Train MSE` (`0.001`), cho thấy mô hình đường thẳng đã tổng quát hóa tốt sang các request chưa từng thấy.

**Tự thử:** Đổi seed từ `42` sang `7` và kiểm tra xem `Train IDs`, `Test IDs` và `Test MSE` thay đổi ra sao.
