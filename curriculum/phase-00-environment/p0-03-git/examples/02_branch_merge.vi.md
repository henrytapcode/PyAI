# Gộp nhánh ba chiều (three-way merge)

**Ví dụ này minh họa:** cách Git so sánh `base`, `main` và `feature` để gộp các sửa đổi không xung đột và đánh dấu xung đột.

**Từng bước**
1. Dòng 1–3 định nghĩa ba bản lưu: tổ tiên chung `base`, `main` và `feature`.
2. Dòng 8–11 duyệt qua mọi tên file xuất hiện ở cả ba bản lưu theo thứ tự bảng chữ cái.
3. Dòng 13–21 chọn nhánh có thay đổi khi chỉ một nhánh sửa file (`app.py` lấy `"v2"` từ `feature`).
4. Dòng 22–25 ghi nhận xung đột khi cả hai nhánh sửa `config.py` khác nhau, đồng thời giữ giá trị của `main` trong `merged`.

**Tự thử:** đổi `feature["config.py"]` thành `"port=9000"` (giống `main`) rồi chạy lại để thấy `Conflicts` trở thành `[]`.
