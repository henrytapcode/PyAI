# Phân tích dòng log

**Ví dụ này cho thấy:** dùng `startswith()` để lọc dòng, `split(",")` để tách một dòng thành các trường, và `join()` để dựng bản tóm tắt.

**Từng bước**
1. Dòng 2–6 chứa bốn dòng log. Mỗi dòng là một chuỗi có ba trường ngăn cách bằng dấu phẩy.
2. Dòng 9 tạo list rỗng `errors` để gom kết quả.
3. Dòng 10–11 lặp qua các dòng và chỉ giữ những dòng bắt đầu bằng `"ERROR"`.
4. Dòng 12 tách một dòng như `"ERROR,gpt-large,timeout"` thành list `["ERROR", "gpt-large", "timeout"]`. Dòng 13–15 lấy từng trường theo index.
5. Dòng 16 dựng một thông báo ngắn bằng f-string rồi thêm vào list. Dòng 18–19 in số lỗi và nối tất cả thông báo bằng `" | "`.

**Để ý:** `split` và `join` ở đây dùng theo hai chiều ngược nhau: một để tách dòng ra, một để ghép bản báo cáo lại.

**Tự thử:** gom cả các dòng `INFO` vào một list thứ hai và in ra có bao nhiêu dòng.
