# Dùng thuần pandas `groupby().agg()` thay vì SQLite (để so sánh)

Lưu ý: đề bài Exercise 2 yêu cầu tổng hợp bằng SQLite nên bài giải chính của bạn vẫn cần dùng SQL—cách thay thế này cố ý không dùng SQL chỉ để so sánh hai phong cách. Thay vì chép `DataFrame` sang SQLite, nó tạo một cột phụ `is_error` dạng số thực rồi dùng cú pháp **named aggregation** `agg(new_col=("col", "func"))`, cho phép đặt tên từng cột kết quả (`requests=("request_id", "count")`, `total_tokens=("tokens", "sum")`) ngay trong một lệnh `.agg(...)` trước khi làm tròn và sắp xếp.

Nên dùng **SQL** khi log vốn đã nằm sẵn trong database (giúp lọc và gom nhóm trước khi tải về Python) hoặc khi cả nhóm dùng chung các câu truy vấn báo cáo; nên dùng **pandas** khi bảng đã nằm trên RAM ngay sau bước làm sạch và bạn không muốn mất bước ghi sang database tạm.
