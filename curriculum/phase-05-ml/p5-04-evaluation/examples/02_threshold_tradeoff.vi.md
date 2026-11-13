# Đánh đổi precision và recall theo ngưỡng quyết định

**Ví dụ này minh họa:** Thử năm ngưỡng quyết định trên xác suất `predict_proba` để quan sát sự đánh đổi giữa precision và recall, rồi chọn ngưỡng cao nhất đạt `recall >= 0.8`.

**Từng bước**
1. Dòng 11–19 tạo tập chia 85/15, huấn luyện pipeline `LogisticRegression` và lấy xác suất lớp 1 bằng `.predict_proba(X_test)[:, 1]`.
2. Dòng 21–24 định nghĩa năm ngưỡng từ `0.5` xuống `0.1` và in tiêu đề bảng.
3. Dòng 25–32 biến xác suất thành nhãn `0/1` theo từng ngưỡng, tính precision, recall, số ticket gắn khẩn cấp, và lưu lại ngưỡng lớn nhất đạt `recall >= 0.8`.
4. Dòng 34 in ra ngưỡng được chọn (`0.3`).

**Điểm đáng chú ý:** Hạ ngưỡng từ `0.5` xuống `0.3` kéo recall từ `0.222` lên `0.889` mà precision vẫn đạt `0.889`; hạ tiếp xuống `0.1` chỉ làm tăng báo động giả (`17` ticket) chứ không bắt thêm được ca nào.

**Tự thử thêm:** Tăng điều kiện ở dòng 31 từ `0.8` lên `0.95` xem trong năm ngưỡng trên có ngưỡng nào đạt được không.
