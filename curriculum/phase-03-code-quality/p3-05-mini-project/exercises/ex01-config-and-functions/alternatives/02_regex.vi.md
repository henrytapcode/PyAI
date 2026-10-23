# Regular expression

Module `re` tìm các mẫu (pattern) trong văn bản. `\s+` nghĩa là "một hoặc nhiều ký tự khoảng trắng", và `https?://\S+` nghĩa là "`http` kèm một `s` tùy chọn, rồi `://`, rồi các ký tự không phải khoảng trắng", nên `re.sub` có thể thay cả đường link chỉ bằng một lời gọi. Kết quả giống lời giải chính. Regular expression là bản xem trước của một chủ đề sau này: chúng mạnh và gọn, nhưng khó đọc hơn và dễ sai tinh vi. Với những việc đơn giản như thế này, `split` và `startswith` rõ ràng hơn; hãy dùng `re` khi mẫu phức tạp hơn mức "các từ bắt đầu bằng".
