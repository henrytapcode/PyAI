# Đọc hết rồi mới tách dòng

Ở đây `Path(path).read_text(...)` nạp cả file thành một chuỗi, rồi `splitlines()` cắt thành các dòng không có `\n`. Cách này ngắn hơn vì không cần khối `with`, và hợp với file nhỏ. Với file rất lớn, vòng lặp từng dòng ở lời giải chính an toàn hơn vì không bao giờ giữ quá một dòng trong bộ nhớ.
