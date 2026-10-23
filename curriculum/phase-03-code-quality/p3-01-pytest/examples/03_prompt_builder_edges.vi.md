# Các trường hợp biên của prompt builder

**Ví dụ này cho thấy:** một prompt builder thêm tài liệu vào cho tới khi hết ngân sách số từ, được test ở các rìa của nó bằng thói quen Arrange, Act, Assert và một hàm phụ `check` nhỏ.

**Từng bước**
1. Dòng 2–3 định nghĩa một bộ đếm token đơn giản: một token cho mỗi từ.
2. Dòng 6–17 định nghĩa `build_prompt`. Nó giữ câu hỏi, rồi thêm từng tài liệu miễn là tổng vẫn nằm trong `max_tokens`, và dừng ở tài liệu đầu tiên không vừa.
3. Dòng 22–29 định nghĩa `check`, so sánh kết quả thật với kết quả mong đợi và in PASS hoặc FAIL.
4. Dòng 32–34 chuẩn bị dữ liệu: một câu hỏi 3 từ và hai tài liệu 2 từ.
5. Dòng 36–41 chạy sáu phép kiểm: không có tài liệu, tất cả đều vừa, vừa khít (5 trên 5 từ), dư một từ (4 từ), giới hạn nhỏ hơn câu hỏi, và câu hỏi rỗng.
6. Dòng 43 in bản tóm tắt.

**Để ý:** hai phép kiểm hữu ích nhất là vừa khít và dư một từ. Chúng nằm ở hai phía của ranh giới, nơi lỗi lệch một đơn vị dễ ẩn nấp.

**Tự thử:** đổi `>` thành `>=` ở dòng 12 rồi chạy lại. Phép kiểm vừa khít chuyển đỏ, và chỉ mình nó.
