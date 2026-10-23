# Dọn dẹp label

**Ví dụ này cho thấy:** set comprehension để bỏ trùng lặp, dict comprehension để đếm, và `x if condition else y` bên trong list comprehension.

**Từng bước**
1. Dòng 2 chứa các label do nhiều người gõ: chữ hoa chữ thường lẫn lộn, thừa dấu cách, bị lặp.
2. Dòng 4 làm sạch mỗi label bằng `strip()` rồi `lower()`. Giờ `"POSITIVE "` và `"positive"` là cùng một chuỗi.
3. Dòng 7 dùng `{...}` không có dấu hai chấm, tạo ra một **set**: mỗi giá trị chỉ được giữ một lần. `sorted(...)` đổi nó lại thành một list gọn gàng.
4. Dòng 10 tạo dict từ label sang số lần xuất hiện. Với mỗi tên, `[x for x in cleaned if x == name]` gom các label khớp và `len(...)` đếm chúng.
5. Dòng 13 chọn `"ok"` hoặc `"rare"` cho từng label bằng `value_if_true if condition else value_if_false`.

**Để ý:** `if` ở cuối comprehension bên trong (dòng 10) dùng để *lọc*. `if ... else ...` ở đầu (dòng 13) dùng để *chọn giá trị*. Hai chỗ nhìn giống nhau nhưng làm việc khác nhau.

**Tự thử:** đổi `>= 2` ở dòng 13 thành `>= 3`. Những label nào vẫn còn là `"ok"`?
