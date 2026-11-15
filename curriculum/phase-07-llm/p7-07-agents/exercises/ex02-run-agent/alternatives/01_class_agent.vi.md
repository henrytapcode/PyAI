# Class `Agent` lưu trạng thái kèm phương thức `step()`

Thay vì giữ `messages`, `trace`, `steps` và `total_tokens` trong các biến cục bộ của một hàm, cách này gói trạng thái agent vào class `Agent` có phương thức `step()` chạy từng bước một. Tách `step()` khỏi `run()` giúp bạn dễ tạm dừng giữa các bước, gửi tiến độ lên giao diện hoặc chèn bước chờ người duyệt, đổi lại nhiều mã khung hơn so với một hàm thuần.
