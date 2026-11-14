# Đánh đổi precision và recall theo ngưỡng quyết định

**Ví dụ này cho thấy:** Quét năm ngưỡng quyết định trên xác suất `predict_proba` của tập validation tách từ train để chọn ngưỡng cao nhất đạt `recall >= 0.8`, rồi mới chấm tập test một lần duy nhất.

**Từng bước**
1. Dòng 10–18 tạo bộ dữ liệu lệch lớp 85/15 rồi chia thành `train_full` / `test`, sau đó tách tiếp `train_full` thành `train` và `val` có `stratify` để việc chọn ngưỡng không chạm vào `test`.
2. Dòng 20–25 huấn luyện pipeline `LogisticRegression` trên `X_train`, lấy xác suất trên tập validation `.predict_proba(X_val)[:, 1]` và đặt `target_recall = 0.8`.
3. Dòng 27–35 quét năm ngưỡng từ `0.5` xuống `0.1` trên `val`, in precision, recall, số ticket gắn khẩn cấp, và chọn ngưỡng lớn nhất đạt `recall >= target_recall` (`0.3`).
4. Dòng 37–45 in ra ngưỡng được chọn (`0.3`) và chấm `X_test` đúng một lần với ngưỡng đó (`precision=0.875`, `recall=0.778`).

**Để ý:** Hạ ngưỡng từ `0.5` xuống `0.3` trên tập validation kéo recall từ `0.400` lên `0.800` với precision `0.667`; khi áp dụng ngưỡng `t = 0.3` một lần lên `X_test` chưa từng thấy, mô hình đạt `precision=0.875` và `recall=0.778`.

**Tự thử:** Tăng `target_recall` ở dòng 24 từ `0.8` lên `0.95` và xem `best_threshold` thành `None` vì không có ngưỡng nào trong năm ngưỡng đạt `0.95` trên tập validation.
