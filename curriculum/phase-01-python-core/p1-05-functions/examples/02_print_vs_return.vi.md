# print và return

**Ví dụ này cho thấy:** hai hàm trông gần giống nhau nhưng hoạt động rất khác.

**Từng bước**
1. Dòng 2–3: `double_print` tính `n * 2` rồi **hiển thị** bằng `print`. Hàm không có `return` nên trả về `None`.
2. Dòng 6–7: `double_return` tính cùng con số đó và **trả về** cho nơi gọi hàm.
3. Dòng 10 gọi `double_print(4)`. Màn hình hiện `8` (dòng output đầu tiên), nhưng biến `a` nhận được `None`.
4. Dòng 11 gọi `double_return(4)`. Màn hình không hiện gì, nhưng `b` nhận được `8`.
5. Dòng 12–14 in ra giá trị của `a` và `b`. Dòng 14 chạy được vì `b` là số thật: `8 + 1`. Thử `a + 1` bạn sẽ gặp `TypeError`.

**Để ý:** số `8` được in đầu tiên đến từ dòng 3 bên trong hàm, chứ không phải từ dòng `print("a is", a)`.

**Tự thử:** đổi dòng 14 thành `print("a + 1 =", a + 1)` và đọc thông báo lỗi. Sau đó đổi lại.
