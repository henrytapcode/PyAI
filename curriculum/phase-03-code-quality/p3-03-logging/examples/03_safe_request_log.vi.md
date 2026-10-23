# Log request an toàn

**Ví dụ này cho thấy:** cách ghi log một request tới model với các trường hữu ích (model và tokens qua `extra=`) mà vẫn giữ secret key và prompt riêng tư ra khỏi log.

**Từng bước**
1. Dòng 5–10 thiết lập format. Sau thông điệp, nó in hai trường thêm là `model` và `tokens`, lấy từ `extra=`.
2. Dòng 14–15 định nghĩa `mask_key`. Nó chỉ giữ bốn ký tự cuối của key, với `...` ở phía trước.
3. Dòng 18–24 ghi log một request. Thông điệp chứa key đã che và **độ dài** của prompt, không bao giờ chứa chính prompt. Dict `extra` cung cấp `model` và `tokens`.
4. Dòng 27–32 ghi log một lỗi ở mức `ERROR`. Record này cũng phải mang `model` và `tokens`, vì format cần chúng.
5. Dòng 35–36 gọi cả hai hàm với một key giả và một prompt có chứa địa chỉ email.

**Để ý:** output không chứa key đầy đủ cũng không chứa địa chỉ email. Log được nhiều người và nhiều công cụ đọc, nên nó chỉ nên chứa những gì họ được phép thấy.

**Tự thử:** xóa `"tokens": 0` khỏi dict `extra` ở dòng 31 rồi chạy lại. Logging sẽ in một lỗi về trường bị thiếu thay vì thông điệp của bạn, đó là lý do mọi record cần cùng các trường extra.
