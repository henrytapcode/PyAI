# Chấm điểm cả batch request bằng tensor

**Điều cần thấy:** Dùng phép nhân ma trận-vector (`@`) để chấm điểm một batch `(4, 3)` request trong một biểu thức duy nhất, rồi đọc điểm đã làm tròn và chỉ số request cao nhất.

**Từng bước**
1. Dòng 5–10 gom bốn API request (mỗi request gồm ba feature: số nghìn token, độ trễ giây và số tin nhắn) vào một tensor `(4, 3)`.
2. Dòng 11–12 khai báo vector `weights` dài `3` dùng chung và hằng số `bias`.
3. Dòng 14 tính cả bốn điểm cùng lúc bằng `requests @ weights + bias`, tự động broadcast `bias` cho từng hàng.
4. Dòng 15–19 lấy chỉ số của điểm cao nhất bằng `.argmax().item()` rồi in `tuple(requests.shape)` cùng danh sách điểm đã làm tròn.

**Lưu ý:** Đổi sang list bằng `.tolist()` rồi làm tròn giúp output sạch sẽ thay vì in tensor thô, còn `.argmax().item()` chuyển tensor chỉ số 0 chiều thành `int` chuẩn của Python.

**Thử tự sửa:** Đổi trọng số của độ trễ trong `weights` từ `1.1` xuống `0.1` và tăng trọng số số tin nhắn từ `0.15` lên `1.5`, rồi xem bốn điểm thay đổi thế nào.
