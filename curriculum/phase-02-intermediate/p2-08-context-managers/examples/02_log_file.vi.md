# File log luôn được đóng

**Ví dụ này cho thấy:** một context manager viết dưới dạng class. Nó mở file log khi khối bắt đầu và đóng khi khối kết thúc, dù có lỗi hay không.

**Từng bước**
1. Dòng 6–8 lưu đường dẫn trong `__init__`. File chưa được mở.
2. Dòng 10–13 là `__enter__`: nó mở file và trả về `self`, nên `as run` đưa cho bạn chính manager.
3. Dòng 15–16 là một method bình thường, `log`, ghi một dòng.
4. Dòng 18–21 là `__exit__`: nó đóng file và trả về `False`, nên lỗi không bị giấu.
5. Dòng 27–30 dùng manager bình thường. Dòng 32–38 dùng lại nhưng gây lỗi trong khối; file vẫn được đóng và lỗi đến được `except`.
6. Dòng 40–41 đọc file lại. Lần thứ hai mở bằng `"w"` đã thay thế nội dung lần đầu.

**Để ý:** `closed: True` được in cả hai lần. `run.file.closed` được kiểm tra sau khối `with`, khi file đã đóng.

**Tự thử:** đổi `"w"` thành `"a"` ở dòng 11. Dòng cuối bây giờ phải hiện cả ba thông điệp.
