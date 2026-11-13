# Tạo báo cáo theo model bằng SQL

**Ví dụ này cho thấy:** cách làm sạch log thô bằng pandas, đưa bảng sạch vào SQLite trong RAM và tính toàn bộ chỉ số từng model chỉ bằng một câu truy vấn `GROUP BY`.

**Từng bước**
1. Dòng 22–30 chuẩn hóa `model`, chuyển `tokens` sang số (bỏ dấu phẩy), ép kiểu `latency_ms` và `rating`, xóa rating ngoài khoảng 1–5, bỏ `request_id` trùng, loại dòng thiếu `tokens` và ép `tokens` thành `"int64"`.
2. Dòng 32–46 ghi bảng sạch vào SQLite bằng `df.to_sql("requests", conn, index=False)`, chạy một câu `GROUP BY model` qua `pd.read_sql_query(...)`, rồi đóng kết nối.
3. Dòng 48–52 in kết quả từng model trên một dòng f-string gọn gàng.

**Để ý:** `AVG(status = 'error')` chạy gọn trong SQLite vì phép so sánh `status = 'error'` trả về `1` khi lỗi và `0` khi `ok`, nên trung bình cộng chính là tỉ lệ lỗi.

**Tự thử:** đổi `ORDER BY total_tokens DESC, model ASC` thành `ORDER BY error_rate DESC, model ASC` để xếp hạng model từ hay lỗi nhất xuống ổn định nhất.
