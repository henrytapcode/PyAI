Hãy viết hai hàm mô phỏng lệnh kiểm tra trạng thái và vùng chờ (staging) của Git bằng dictionary ánh xạ đường dẫn file tới nội dung:

1. `git_status(committed: dict[str, str], staged: dict[str, str], working: dict[str, str]) -> dict[str, list[str]]`
   Trả về dictionary gồm bốn danh sách đường dẫn **đã sắp xếp tăng dần**:
   - `"staged"`: các đường dẫn có `staged.get(p) != committed.get(p)` (được thêm, sửa hoặc xóa trong `staged` so với `committed`).
   - `"untracked"`: các đường dẫn có trong `working` nhưng không có trong `committed` lẫn `staged`.
   - `"modified"`: các đường dẫn có trong `working` và có trong `staged` với `working[p] != staged[p]`.
   - `"deleted"`: các đường dẫn có trong `staged` nhưng vắng mặt trong `working`.

2. `stage_files(staged: dict[str, str], working: dict[str, str], paths: list[str]) -> dict[str, str]`
   Trả về một dictionary `staged` **mới** (không bao giờ làm thay đổi `staged` đầu vào) sau khi stage từng đường dẫn trong `paths`:
   - Nếu đường dẫn có trong `working`, chép `working[p]` vào dict mới.
   - Nếu đường dẫn không có trong `working` nhưng có trong `staged`, xóa nó khỏi dict mới.
   - Nếu đường dẫn vắng mặt ở cả `working` và `staged`, ném ra `KeyError`.

Bấm **Check** để chạy kiểm thử.
