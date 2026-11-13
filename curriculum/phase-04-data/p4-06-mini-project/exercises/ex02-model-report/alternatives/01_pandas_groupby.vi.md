# Dùng thuần pandas `groupby().agg()` thay vì SQLite

Thay vì chép `DataFrame` sang SQLite để chạy SQL, cách làm này tạo thêm một cột phụ `is_error` dạng số thực trên bản sao, tính toàn bộ chỉ số trực tiếp bằng `groupby("model", as_index=False).agg(...)`, rồi làm tròn và sắp xếp.

Nên dùng **SQL** khi log vốn đã nằm sẵn trong database (giúp lọc và gom nhóm trước khi tải về Python) hoặc khi cả nhóm dùng chung các câu truy vấn báo cáo; nên dùng **pandas** khi bảng đã nằm trên RAM ngay sau bước làm sạch và bạn không muốn mất bước ghi sang database tạm.
