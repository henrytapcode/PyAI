# Điều hướng đường dẫn với PurePosixPath

**Ví dụ này minh họa:** cách Python biểu diễn thư mục làm việc hiện tại (`cwd`), thư mục cha và nối các đường dẫn tương đối mà không đụng vào ổ đĩa thật.

**Từng bước một**
1. Dòng 3 tạo một `PurePosixPath` đại diện cho `cwd`.
2. Dòng 5–6 xem `.parent` (nơi `cd ..` sẽ đi tới) và `.parts` (từng đoạn thư mục).
3. Dòng 8 nối các đoạn tương đối `"src"` và `"main.py"` bằng `/`.
4. Dòng 10–12 đọc `.name`, `.suffix` và kiểm tra `.is_absolute()`.

**Tự thử:** đổi `main_file` thành `cwd.parent / "shared" / "utils.py"` rồi chạy lại để xem đường dẫn mới.
