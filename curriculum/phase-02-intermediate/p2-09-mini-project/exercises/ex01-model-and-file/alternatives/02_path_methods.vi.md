# Hàm đọc ghi cả file với `Path`

Ở đây việc với file dùng `Path.write_text` và `Path.read_text` cùng `json.dumps` và `json.loads` (các bản có chữ `s`, làm việc với chuỗi), như trong bài về file. Không có khối `with open(...)`, vì các hàm này tự mở và đóng file cho bạn. Ngày được tách bằng `partition`, một method của chuỗi cắt tại dấu `-` đầu tiên và cho ra ba phần (phần trước, dấu gạch, phần sau).

Đây là cách ngắn nhất để xử lý file nhỏ. `json.load` cũng đọc cả file một lượt, nên khác biệt thật sự là khả năng kiểm soát: hãy dùng `with open(...)` khi bạn ghi file từng phần (ví dụ JSON Lines, mỗi dòng một `json.dumps`) hoặc cần kiểm soát cách mở file.
