# Ma trận điểm số

**Ví dụ này cho thấy:** cách tổng hợp mảng 2D theo `axis=0` (theo cột) và `axis=1` (theo hàng), rồi tìm người cao nhất bằng `argmax()`.

**Từng bước**
1. Dòng 4–10 khai báo tên bốn học viên và ma trận điểm kích thước `(4, 3)` (4 học viên × 3 bài kiểm tra).
2. Dòng 12 tính `scores.mean(axis=0)` để lấy trung bình dọc theo từng cột, cho ra điểm trung bình của mỗi bài.
3. Dòng 13 tính `scores.mean(axis=1)` để lấy trung bình ngang theo từng hàng, cho ra điểm trung bình của mỗi học viên.
4. Dòng 17 gọi `student_means.argmax()` để lấy chỉ số (`2`) của người có trung bình cao nhất, và dòng 18 tra tên `"Chi"` trong `students`.

**Để ý:** `argmax()` trả về vị trí (`2`), không phải điểm số (`9.0`). Dùng `int(...)` để đổi số nguyên NumPy thành `int` thuần của Python khi truy cập `students`.

**Tự thử:** đổi điểm bài thứ ba của Chi (`8.5` ở dòng 8) thành `5.0` rồi chạy lại để xem ai vươn lên đứng đầu.
