# Phạm vi biến và shadowing

**Ví dụ này cho thấy:** hàm nhìn thấy những biến nào, và chuyện gì xảy ra khi biến cục bộ trùng tên với biến toàn cục.

**Từng bước**
1. Dòng 2 tạo `rate` ở đầu file. Đây là biến **toàn cục** (global): mọi hàm đều đọc được.
2. Dòng 5–7: `add_tax` tạo `tax`, là biến **cục bộ** (local): chỉ tồn tại khi `add_tax` đang chạy. Dòng 6 *đọc* `rate` toàn cục, điều này không sao.
3. Dòng 10–12: `broken_reset` viết `rate = 0`. Vì gán giá trị bên trong hàm, Python tạo ra một biến `rate` **cục bộ mới** và biến toàn cục bị che đi. Hiện tượng này gọi là **shadowing** (che khuất).
4. Dòng 15 in `110.0`. Dòng 16 in `0`, là giá trị cục bộ. Dòng 17 in `0.1`: `rate` toàn cục chưa hề bị đổi.

**Để ý:** hàm có thể đọc biến toàn cục, nhưng gán cho cùng tên bên trong hàm sẽ tạo ra một biến cục bộ riêng. Cách làm thông thường là truyền giá trị vào bằng tham số và `return` kết quả.

**Tự thử:** thêm `print(tax)` làm dòng cuối. Bạn sẽ gặp `NameError`, vì `tax` không tồn tại bên ngoài `add_tax`.
