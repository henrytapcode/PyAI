# Kiểm tra log API thô

**Ví dụ này cho thấy:** cách quét nhanh bảng log CSV thô để xem kích thước, số ô thiếu theo cột, các biến thể tên model và số `request_id` bị lặp trước khi bắt đầu làm sạch.

**Từng bước**
1. Dòng 5–19 lưu trực tiếp 14 dòng log chatbot thô dưới dạng chuỗi CSV.
2. Dòng 21 nạp CSV vào DataFrame bằng `pd.read_csv(io.StringIO(csv_text))`.
3. Dòng 22–26 in kích thước bảng, số ô thiếu từng cột, danh sách tên model thô khác nhau và số `request_id` trùng lặp.

**Để ý:** `latency_ms` lúc này mới báo `1` ô thiếu (`N/A`), dù dòng `r09` chứa chữ `"timeout"`—`pd.read_csv` giữ `"timeout"` dạng chuỗi cho tới khi ta ép kiểu sang số.

**Tự thử:** in thêm `df.dtypes` ngay sau `pd.read_csv(...)` để xem những cột trông như số nào đang bị đọc thành `object`.
