# Khớp đường thẳng bằng autograd của PyTorch

**Điều cần thấy:** Làm lại bài toán khớp đường thẳng bằng gradient descent (`tokens_k` theo `latency_s`) từ `p5-01-math-bridge`, thay công thức đạo hàm viết tay bằng `loss.backward()`.

**Từng bước**
1. Dòng 4–5 lưu năm cặp quan sát kích thước prompt và độ trễ dưới dạng tensor PyTorch.
2. Dòng 7–9 khởi tạo hai leaf tensor `w` và `b` bằng `0.0` với `requires_grad=True` và đặt `lr = 0.05`.
3. Dòng 11–20 chạy 41 bước gradient descent: tính `pred` và MSE `loss`, in loss mỗi 20 bước, gọi `loss.backward()`, cập nhật `w` và `b` trong `with torch.no_grad():` rồi xóa `.grad` của cả hai.
4. Dòng 22 in ra hệ số góc `w` và hệ số chặn `b` sau khi khớp, làm tròn 3 chữ số thập phân.

**Lưu ý:** Bạn không hề phải viết `2 * error * x` hay `2 * error` ở đâu cả — autograd tự suy ra cả hai gradient từ biểu thức `pred = w * tokens_k + b` và `loss`.

**Thử tự sửa:** Tăng số bước lặp từ `41` lên `121` và quan sát `b` tiến sát hơn tới `0.3` khi loss ổn định.
