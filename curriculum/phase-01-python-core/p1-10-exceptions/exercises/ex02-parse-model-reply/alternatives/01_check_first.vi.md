# Kiểm tra trước rồi mới dùng

Phiên bản này chỉ dùng `try` cho đúng một việc thật sự có thể gây lỗi là `json.loads`. Với mọi thứ còn lại, nó kiểm tra dữ liệu trước khi dùng: `isinstance` hỏi "đây có phải dict không?" và "đây có phải số không?" (ở đây ta xem trước, bạn sẽ gặp lại ở các bài sau), còn `in` hỏi "key có tồn tại không?". Kiểm tra trước thì dễ đọc và không cần `raise`, nhưng các phép kiểm tra sẽ dài ra khi dữ liệu có nhiều trường. Lời giải chính ngắn hơn vì một khối `except` bao quát mọi kiểu thất bại cùng lúc.
