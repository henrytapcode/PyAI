# Làm sạch từng dòng với `csv.DictReader`

Thay vì nạp cả file CSV vào pandas ngay từ đầu, cách làm này duyệt từng dòng qua `csv.DictReader` của thư viện chuẩn, kiểm tra trùng lặp bằng một `set`, chuyển kiểu từng ô rồi mới dựng `DataFrame` ở bước cuối.

Cách này thuận tiện hơn khi bạn cần ghi log chi tiết từng dòng bị loại trên file rất lớn, còn các phép vector hóa của pandas ở lời giải chính sẽ ngắn gọn và nhanh hơn cho bảng vừa trong RAM.
