Hãy viết hai hàm mô phỏng thao tác gộp nhánh ba chiều và kiểm tra tính hợp lệ của commit message:

1. `three_way_merge(base: dict[str, str], main: dict[str, str], feature: dict[str, str]) -> dict`
   Gộp tất cả đường dẫn file xuất hiện trong `base`, `main` và `feature`, trả về `{"merged": dict[str, str], "conflicts": list[str]}`:
   - Nếu `main` và `feature` có cùng trạng thái cho một đường dẫn (cùng nội dung hoặc cả hai đều xóa), giữ trạng thái đó (bỏ qua nếu bị xóa).
   - Nếu một nhánh giữ nguyên như `base`, lấy trạng thái của nhánh còn lại (xóa khỏi `"merged"` nếu nhánh kia đã xóa file).
   - Nếu cả hai nhánh đều thay đổi khác `base` và khác nhau, thêm đường dẫn vào danh sách `"conflicts"` (đã sắp xếp tăng dần) và giữ giá trị của `main` trong `"merged"` nếu `main` vẫn còn file đó.

2. `is_valid_commit_msg(msg: str) -> bool`
   Lấy dòng tiêu đề (phần trước ký tự `\n` đầu tiên, đã cắt khoảng trắng hai đầu) và trả về `True` khi và chỉ khi:
   - Tiêu đề không rỗng.
   - `len(subject) <= 72`.
   - Tiêu đề không kết thúc bằng dấu `"."`.
   - Tiêu đề bắt đầu bằng một chữ cái ASCII (`a`–`z` hoặc `A`–`Z`).

Bấm **Check** để chạy kiểm thử.
