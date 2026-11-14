# Đối chiếu autograd với độ dốc ước lượng bằng số

**Điều cần thấy:** So sánh gradient do `autograd` của PyTorch tính cho hai tham số (`w` và `b`) với công thức ước lượng độ dốc bằng số từ bài `p5-01-math-bridge`.

**Từng bước**
1. Dòng 4–5 tạo năm cặp điểm `(x, y)` nằm trên đường thẳng `y = 2.0 * x + 0.5`.
2. Dòng 7–8 khởi tạo hai leaf tensor `w` và `b` tại `1.0` với `requires_grad=True`.
3. Dòng 10–13 tính MSE loss, gọi `loss.backward()` rồi đọc `w.grad.item()` và `b.grad.item()`.
4. Dòng 16–23 tự tính lại cùng hàm loss khi nhích `+h` và `-h` (`h = 0.001`) riêng cho từng tham số.
5. Dòng 25–28 kiểm tra hai cách tính khớp nhau trong ngưỡng `1e-3` và in ra `match: True`.

**Lưu ý:** Autograd tính xong cả `w.grad` và `b.grad` chỉ trong một lượt `loss.backward()`, còn ước lượng bằng số phải chạy lại hàm loss hai lần cho mỗi tham số.

**Thử tự sửa:** Đổi giá trị khởi tạo của `w` và `b` từ `1.0` sang `2.0` và `0.5` (đúng đường thẳng gốc) và xem cả hai gradient đều về `0.0`.
