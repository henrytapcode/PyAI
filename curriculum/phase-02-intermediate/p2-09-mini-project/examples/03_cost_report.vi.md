# Báo cáo chi phí với ledger an toàn

**Ví dụ này cho thấy:** một context manager nhỏ, `ledger`, đọc các dòng dữ liệu đã lưu, cho bạn sửa chúng, và lưu lại khi khối kết thúc. Sau đó một hàm gom nhóm tạo ra hai bản tổng hợp, và vòng lặp "tốt nhất cho đến lúc này" tìm model đứng đầu, kèm một trường hợp hòa để bạn suy nghĩ.

**Từng bước**
1. Dòng 12–16 định nghĩa `ledger`. Chuẩn bị: đọc các dòng, hoặc bắt đầu bằng list rỗng nếu file chưa tồn tại. Rồi `yield rows`. Sau khối: lưu.
2. Dòng 30–36 thêm dòng dữ liệu trong hai phiên riêng. Phiên thứ hai thấy các dòng của phiên đầu.
3. Dòng 38–43 thêm dòng thứ ba rồi bị crash. Dòng `path.write_text(...)` sau `yield` bị bỏ qua, nên file không đổi.
4. Dòng 19–24 định nghĩa `cost_by`. Hàm cộng `cost` cho mỗi giá trị của `field`, và trả về dict có key đã sắp xếp và tổng đã làm tròn.
5. Dòng 47–50 in một bản tổng hợp theo `model` và một bản theo `day`, với đúng 4 chữ số thập phân.
6. Dòng 52–61 tìm model đắt nhất bằng vòng lặp "tốt nhất cho đến lúc này". Ở đây `large` và `mid` có cùng tổng, nên chương trình in thêm ai đang hòa.

**Để ý:** trong `ledger` **không** có `try/finally` quanh `yield`, và đó là cố ý. Việc dọn dẹp phải luôn chạy, còn việc lưu công việc dang dở thì không. Khi khối bị lỗi, ta muốn bỏ qua bước lưu. Cũng để ý `>=` ở vòng lặp cuối: khi hòa, tên đứng sau (`mid`) thay thế `large`.

**Tự thử:** đổi `"cost": 9.99` thành `0.5` và xóa dòng `raise`. Hãy đoán số `rows saved` mới (5). Sau đó đổi `>=` thành `>` ở vòng lặp cuối và đoán ai thắng khi hòa (`large`).
