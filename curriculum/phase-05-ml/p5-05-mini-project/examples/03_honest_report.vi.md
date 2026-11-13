# Chọn ngưỡng trên CV tập train và viết báo cáo trung thực

**Ví dụ minh họa:** Chọn ngưỡng quyết định hoàn toàn từ xác suất out-of-fold trên tập train (`cross_val_predict`), chấm tập test giữ riêng đúng một lần và in báo cáo nhiều dòng gồm cỡ mẫu, baseline, độ lệch chuẩn CV và cảnh báo khi hai mô hình chênh nhau chưa tới một độ lệch chuẩn.

**Từng bước**
1. Các dòng 56–66 tính CV F1 của `logreg` và `tree` trên `X_train`, rồi dùng `cross_val_predict(..., method="predict_proba")` trên `X_train` để tìm ngưỡng lớn nhất trong `[0.5, 0.4, 0.3, 0.2]` đạt `recall >= 0.80` (ra `0.2`).
2. Các dòng 68–71 huấn luyện `DummyClassifier` và `logreg` trên toàn bộ `173` dòng train và chấm `58` dòng test đúng một lần với ngưỡng `0.2`.
3. Các dòng 73–86 in báo cáo trung thực: cỡ mẫu test (`58`, `14` khẩn cấp), baseline (`acc=0.759 F1=0.000`), CV `mean +/- std` của cả hai mô hình, confusion matrix `[[31, 13], [1, 13]]`, precision/recall/F1 trên test và câu lưu ý hòa về mặt thống kê.

**Lưu ý:** Việc chọn ngưỡng trên `X_train` giữ `X_test` hoàn toàn nguyên vẹn cho tới lần kiểm tra cuối cùng (`13` trong `14` ticket khẩn cấp được bắt trúng, `recall=0.929`).

**Tự thử:** Nâng mục tiêu recall trên tập train từ `0.80` lên `0.90` ở dòng 64 rồi quan sát `chosen_t` và precision trên test thay đổi ra sao.
