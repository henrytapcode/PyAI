# Một test runner thu nhỏ

**Ví dụ này cho thấy:** cách một công cụ như pytest hoạt động về tinh thần. Nó tìm mọi hàm có tên bắt đầu bằng `test_`, gọi từng hàm, và in PASS hoặc FAIL. Một test đỏ có chủ ý vì `clean_text` có lỗi.

**Từng bước**
1. Dòng 2–4 định nghĩa `clean_text` có lỗi: `replace("  ", " ")` chỉ biến hai dấu cách thành một, nên ba dấu cách thành hai.
2. Dòng 7–17 định nghĩa ba test. Test cuối có thông báo assert cho biết hàm thật sự trả về gì.
3. Dòng 22 lặp qua `globals()`, một dict chứa mọi tên đã được định nghĩa tới lúc này. `list(...)` tạo một bản sao trước, vì chính vòng lặp thêm vào các tên `name` và `func`.
4. Dòng 23–30 chỉ giữ các tên bắt đầu bằng `test_`, gọi từng hàm trong `try`, rồi đếm số pass và fail. Một `assert` sai raise `AssertionError`, và `except` bắt nó để các test khác vẫn chạy.
5. Dòng 32 in bản tóm tắt.

**Để ý:** test thất bại là test có chuỗi dấu cách dài hơn. Hai test dễ đã pass, nên lỗi ẩn đi cho tới khi có test nhìn vào trường hợp biên.

**Tự thử:** đổi thân của `clean_text` thành `" ".join(text.split()).lower()` rồi chạy lại. Cả ba test phải pass.
