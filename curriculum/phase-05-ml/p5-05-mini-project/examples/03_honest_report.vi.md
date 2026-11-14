# Chọn ngưỡng trên CV tập train và viết báo cáo trung thực

**Ví dụ này cho thấy:** Chọn ngưỡng quyết định hoàn toàn từ xác suất out-of-fold trên tập train (`cross_val_predict`), chấm tập test giữ riêng đúng một lần và in báo cáo nhiều dòng gồm cỡ mẫu, baseline, độ lệch chuẩn CV và cảnh báo khi hai mô hình chênh nhau chưa tới một độ lệch chuẩn.

**Từng bước**
1. Các dòng 54–68 tính CV F1 của `logreg` và `tree` trên `X_train`, rồi dùng `cross_val_predict(..., method="predict_proba")` trên `X_train` để tìm ngưỡng lớn nhất trong `[0.5, 0.4, 0.3, 0.2]` đạt `target_recall` (`0.80` ở dòng 62, chọn ra `0.2`), hoặc giữ `chosen_t = None` nếu không ngưỡng nào đạt.
2. Các dòng 70–78 huấn luyện `DummyClassifier` trên `173` dòng train rồi in cỡ mẫu test (`58`, `14` khẩn cấp), baseline (`acc=0.759 F1=0.000`) và CV `mean +/- std` của cả hai mô hình.
3. Các dòng 79–92 dừng lại và in `"no threshold reaches recall >= ..."` nếu `chosen_t is None`; ngược lại sẽ huấn luyện `logreg` trên toàn bộ tập train, chấm `58` dòng test đúng một lần tại ngưỡng `0.2`, in confusion matrix `[[31, 13], [1, 13]]`, precision/recall/F1 trên test và câu lưu ý hòa về mặt thống kê.

**Để ý:** Việc chọn ngưỡng trên `X_train` giữ `X_test` hoàn toàn nguyên vẹn cho tới lần kiểm tra cuối cùng (`13` trong `14` ticket khẩn cấp được bắt trúng, `recall=0.929`).

**Tự thử:** Nâng `target_recall` từ `0.80` lên `0.90` ở dòng 62 để thấy không ngưỡng nào trong `[0.5, 0.4, 0.3, 0.2]` đạt mục tiêu (`chosen_t = None`), nên chương trình in `"no threshold reaches recall >= 0.90"` và không chấm `X_test`.
