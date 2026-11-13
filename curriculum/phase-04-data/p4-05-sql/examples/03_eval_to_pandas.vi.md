# Đưa kết quả eval từ SQLite sang pandas

**Ví dụ này cho thấy:** cách lọc dòng ngay trong SQL bằng `pd.read_sql_query(sql, conn, params=...)` rồi tính điểm trung bình theo từng model trong pandas.

**Từng bước**
1. Dòng 4–12 tạo bảng `eval_runs` (`model`, `task`, `score`).
2. Dòng 14–26 chèn sáu lượt chạy đánh giá của ba model trên hai tác vụ.
3. Dòng 28–34 gọi `pd.read_sql_query` với `params=(0.75,)` để SQL loại bớt lượt `0.74` trước khi dữ liệu sang pandas.
4. Dòng 35–43 gom nhóm DataFrame theo `"model"`, tính trung bình `"score"`, làm tròn 2 chữ số, sắp giảm dần và in bảng tóm tắt gọn.

**Để ý:** lọc trước bằng `WHERE score >= ?` trong SQL giúp những dòng không cần thiết không đi vào DataFrame ngay từ đầu, tiết kiệm bộ nhớ khi bảng lớn.

**Tự thử:** hạ `params=(0.75,)` xuống `params=(0.70,)` rồi xem điểm trung bình của `mini` thay đổi thế nào khi tính cả `0.74`.
