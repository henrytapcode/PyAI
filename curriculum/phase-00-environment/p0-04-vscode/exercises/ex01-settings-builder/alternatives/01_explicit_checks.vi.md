# Kiểm tra từng key tường minh

Thay vì lặp qua tuple `REQUIRED_KEYS`, phiên bản này kiểm tra từng key bắt buộc bằng câu lệnh `if ... not in parsed:` riêng theo đúng thứ tự yêu cầu. Với 3 key cố định, cách viết tường minh rất dễ đọc; còn vòng lặp qua tuple sẽ mở rộng tốt hơn nếu danh sách key bắt buộc dài ra sau này.
