# Lấy n phần tử mỗi lần bằng islice

Cách này dùng một công cụ của thư viện chuẩn mà khóa học này không đề cập: `islice(iterator, n)` trong module `itertools` lấy tối đa `n` phần tử từ một iterator. `iter(items)` tạo bookmark như ở §1, `list(...)` gom đoạn vừa lấy, và một lô rỗng nghĩa là dữ liệu đã hết. Lệnh `return` đứng một mình trong generator chỉ đơn giản là kết thúc nó. Cách này ngắn hơn bản viết tay và cũng lười như vậy, nhưng bạn cần biết `islice` và mẫu `while True`, nên với người mới vòng lặp thường dễ đọc hơn.
