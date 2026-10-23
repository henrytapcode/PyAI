# Màn hình và file

**Ví dụ này cho thấy:** một logger với hai handler. Màn hình chỉ hiện từ `INFO` trở lên, còn file giữ mọi chi tiết từ `DEBUG` trở lên.

**Từng bước**
1. Dòng 6–8 tạo logger `pipeline`, cho nó cho qua mọi thứ từ `DEBUG` trở lên, và không cho nó gửi record lên root logger.
2. Dòng 10–12 tạo handler cho màn hình: in ra `sys.stdout`, hiện từ `INFO` trở lên, và dùng format ngắn.
3. Dòng 15–25 là một hàm nhỏ ghi một dòng `DEBUG` cho mỗi văn bản, một dòng `WARNING` cho văn bản dài, và một dòng `INFO` tóm tắt.
4. Dòng 28–36 tạo handler cho file trong một thư mục tạm (với format dài hơn, có tên hàm) và thêm cả hai handler vào logger.
5. Dòng 37–42 chạy hàm, và trong `finally` gỡ và đóng cả hai handler, nên file được đóng kể cả khi có lỗi.
6. Dòng 44–47 đọc file lại và in ra.

**Để ý:** màn hình hiện hai dòng, nhưng file có năm dòng. Logger kiểm tra mức của nó một lần, rồi mỗi handler áp dụng mức riêng của nó.

**Tự thử:** đổi `console.setLevel(logging.INFO)` ở dòng 11 thành `logging.DEBUG`. Màn hình bây giờ phải hiện đủ năm thông điệp giống file, nhưng với format ngắn hơn.
