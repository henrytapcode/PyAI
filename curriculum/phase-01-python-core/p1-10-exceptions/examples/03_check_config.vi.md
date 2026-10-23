# Kiểm tra config từ sớm

**Ví dụ này cho thấy:** dùng `raise` để tạo lỗi rõ ràng của riêng bạn, cùng với `except ... as err`, `else` và `finally` phối hợp với nhau.

**Từng bước**
1. Dòng 3–4 dừng sớm nếu thiếu key `model` bắt buộc, kèm thông báo nói rõ cần sửa gì.
2. Dòng 5 đọc `temperature` bằng `.get()` với giá trị mặc định `0.7`, nên thiếu temperature cũng không sao.
3. Dòng 6–7 từ chối temperature nằm ngoài khoảng 0 đến 2. F-string đưa giá trị sai vào thông báo, giúp debug nhanh hơn nhiều.
4. Dòng 17–25 thử từng config. Nếu `check_config` raise, `except ValueError as err` in thông báo ra.
5. Khối `else` (dòng 22) chỉ chạy khi không có lỗi nào được raise. Khối `finally` (dòng 24) chạy mọi lần, nên bạn thấy `-- checked one config` ba lần.

**Để ý:** hàm kiểm tra không in gì và không quyết định phải làm gì. Nó chỉ raise. Bên gọi mới quyết định hiện thông báo, dùng giá trị mặc định hay dừng hẳn.

**Tự thử:** đổi config thứ hai thành `{"model": "small", "temperature": -1}`. Thông báo nào hiện ra? (`temperature must be between 0 and 2, got -1`.)
