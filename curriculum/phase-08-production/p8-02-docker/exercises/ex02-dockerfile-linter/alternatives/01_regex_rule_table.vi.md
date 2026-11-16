# Tách bằng regex kết hợp bảng quy tắc

Cách làm thay thế này gộp dòng nối `\` và tách `(INSTRUCTION, args)` bằng `re` thay cho biến đệm thủ công, rồi gom từng bước kiểm tra vào bảng `RULES` gồm các cặp `(code, check_fn)`. Hãy chọn bảng quy tắc khi dự án cần thêm nhiều luật kiểm lỗi mới hoặc bật tắt luật theo cấu hình, còn khi chỉ có vài kiểm tra cố định và muốn debug thẳng từng nhánh `if` thì cách viết tường minh ở `solution.py` dễ theo dõi hơn.
