# Kiểm tra từ trên xuống

Ở đây `bmi` dùng một bước có tên (`height_squared`) nên công thức dễ đọc thành lời. `bmi_category` kiểm tra các mốc từ **lớn** xuống nhỏ (`>= 30`, `>= 25`, `>= 18.5`) và kết thúc bằng trường hợp còn lại. Vì mỗi `return` kết thúc hàm, thứ tự kiểm tra chính là thứ làm cho code đúng: đổi thứ tự thì `35` sẽ bị gọi là "normal".
