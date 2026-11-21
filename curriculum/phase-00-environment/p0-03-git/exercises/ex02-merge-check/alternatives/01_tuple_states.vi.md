# Bộ tuple trạng thái (có mặt, giá trị)

Cách giải thay thế này biểu diễn trạng thái của mỗi nhánh cho một đường dẫn bằng tuple `(in_branch, value)` thay vì dùng đối tượng sentinel, và kiểm tra tiêu đề commit bằng một biểu thức boolean duy nhất.
