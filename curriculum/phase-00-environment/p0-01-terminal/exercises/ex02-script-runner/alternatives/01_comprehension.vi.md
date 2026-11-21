# List comprehension & unpacking

Cách viết thay thế này dùng một biểu thức sinh có sắp xếp (`sorted(...)`) cho `find_python_files` và dùng list unpacking (`[*runner, clean, *(args or [])]`) để ghép danh sách lệnh. Code gọn hơn vòng lặp `append` mà vẫn giữ nguyên kiểm tra ranh giới thư mục `"/"`.
