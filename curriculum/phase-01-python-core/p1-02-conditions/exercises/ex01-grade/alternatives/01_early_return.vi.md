# Các `if` riêng lẻ với `return` sớm

Ở đây mỗi phép kiểm tra là một `if` riêng, không có `elif` hay `else`. Cách này vẫn đúng vì `return` thoát khỏi hàm ngay lập tức: khi `score` là 85, dòng `return "B"` kết thúc hàm và các phép kiểm tra phía sau không bao giờ chạy. Dùng `elif` khi bạn muốn nhìn thấy cả chuỗi lựa chọn trong một cái nhìn; dùng `return` sớm khi mỗi nhánh chỉ đơn giản trả về một đáp án.
