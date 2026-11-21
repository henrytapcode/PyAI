# Mô phỏng vòng đời Git

**Ví dụ này minh họa:** cách các file di chuyển từ Working Tree vào Staging Area rồi tới bản lưu đã commit.

**Từng bước**
1. Dòng 1–3 khởi tạo ba dictionary đại diện cho `committed`, `staged` và `working`.
2. Dòng 5–7 phát hiện file `untracked` (mới có trong `working`) và file `modified` (đã thay đổi so với `staged`).
3. Dòng 9–11 mô phỏng `git add` bằng cách chép cả hai file vào `staged`.
4. Dòng 13–14 mô phỏng `git commit` bằng cách lưu một bản sao của `staged` làm `committed` mới.

**Tự thử:** thêm `"notes.txt": "draft"` vào `working` mà không stage, rồi chạy lại để xem nó xuất hiện trong danh sách nào.
