# Bỏ qua điểm số lỗi

**Ví dụ này cho thấy:** một manager giấu một loại lỗi và đếm xem nó đã giấu bao nhiêu lần, dùng để làm sạch dữ liệu bẩn.

**Từng bước**
1. Dòng 3–5 lưu loại lỗi cần giấu và đặt bộ đếm bằng 0.
2. Dòng 7–8 là `__enter__`: nó trả về `self`.
3. Dòng 10–14 là `__exit__`: nếu lỗi đúng loại mong đợi thì đếm và trả về `True` (giấu); nếu không thì trả về `False` (để lỗi đi qua).
4. Dòng 17–23 duyệt qua chuỗi thô. Cùng một manager `skip` được dùng lại ở mỗi vòng. Giá trị xấu như `"n/a"` raise `ValueError`, bị giấu, và vòng lặp tiếp tục.
5. Dòng 28–32 thử `float(None)`. Nó raise `TypeError`, là loại khác, nên không bị giấu và `except` bắt được.

**Để ý:** bộ đếm vẫn là 2 sau `TypeError`, vì `__exit__` trả về `False` cho lỗi đó.

**Tự thử:** đổi `SkipErrors(ValueError)` ở dòng 19 thành `SkipErrors(TypeError)`. Vòng lặp đầu giờ sẽ lỗi ở `"n/a"`, vì `ValueError` không còn bị giấu.
