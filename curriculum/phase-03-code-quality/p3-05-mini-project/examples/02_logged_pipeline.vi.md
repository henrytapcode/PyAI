# Một lần chạy làm sạch có log

**Ví dụ này cho thấy:** một dataset có `None`, một con số, một văn bản rỗng, một văn bản chỉ có link và một mục trùng đi qua `clean_dataset`. Mục lạ được cảnh báo, những thứ bị loại đã biết trước chỉ được đếm, và một dòng `INFO` tổng kết lần chạy.

**Từng bước**
1. Dòng 5–12 cài đặt logging một lần và tạo logger `textclean`. Format hiện level, tên logger và thông báo.
2. Dòng 15–17 là một `clean_text` ngắn: bỏ các từ là link, nối bằng khoảng trắng đơn, chuyển chữ thường.
3. Dòng 20–25 là báo cáo, một dataclass thường (không frozen), vì hàm cộng dồn vào các bộ đếm của nó.
4. Dòng 28–45 là `clean_dataset`. Một mục không phải string nhận một `WARNING` kèm vị trí và bị bỏ qua. Với string, kết quả rỗng cộng vào `empty`, kết quả đã có trong set `seen` cộng vào `duplicates`, còn lại thì được giữ.
5. Các dòng cuối tạo list thô và in báo cáo: hai mục được giữ, và các bộ đếm `2 2 1` cho skipped, empty và duplicates.

**Lưu ý:** văn bản chỉ có link và văn bản rỗng đều thành rỗng, nên được tính là `empty`. Câu hỏi reset thứ hai trùng với câu đầu khi link và chữ hoa đã bị bỏ.

**Thử tự làm:** đổi `level` ở dòng 8 thành `logging.WARNING`. Dòng tổng kết `INFO` biến mất và hai warning vẫn còn.
