# Kiểm tra đăng nhập

**Ví dụ này cho thấy:** `and`, `or`, `not` trong các phép kiểm tra thực tế, và cách văn bản rỗng hoạt động bên trong `if`.

**Từng bước**
1. Dòng 2–4 lưu tên đăng nhập, mật khẩu và số lần thử sai cho tới giờ.
2. Dòng 6 tạo một `bool`: `username != ""` là `True` vì `"lan"` không rỗng. Dòng 7 làm tương tự với `len(password) >= 8` (`len()` đếm số ký tự; `"secret123"` có 9 ký tự), kết quả là `True`.
3. Dòng 9 dùng `and`: cả `has_name` và `long_password` đều `True`, nên dòng 10 in `Credentials look valid`.
4. Dòng 12 dùng `or` và `not`: `attempts >= 3` là `False` (2 nhỏ hơn 3) và `not has_name` cũng là `False`. `False or False` là `False`, nên `else` chạy và dòng 15 in `1 attempt(s) left` (3 - 2 = 1).
5. Dòng 17 gán `nickname` là chuỗi rỗng. Dòng 18 `if nickname:` coi `""` là False, nên `else` ở dòng 20 chạy và dòng 21 in `Hi, stranger`.
6. Dòng 23 cho thấy chính quy tắc đó: `bool("")` là `False`, `bool("a")` là `True`, `bool(0)` là `False`, `bool(5)` là `True`.

**Để ý:** `if nickname:` là cách viết ngắn của `if nickname != "":`. Cả hai đều có nghĩa "có nội dung gì đó".

**Tự thử:** đổi `attempts` thành `3` và đoán nhánh nào của `if` thứ hai sẽ chạy. Sau đó đổi `password` thành `"abc"` và xem dòng nào biến mất.
