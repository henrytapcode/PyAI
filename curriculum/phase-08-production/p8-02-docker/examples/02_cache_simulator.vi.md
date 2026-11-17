# Mô phỏng tái sử dụng build cache trong Docker

**Ví dụ này cho thấy:** So sánh thứ tự `Dockerfile` tốt (`COPY requirements.txt .` trước `COPY . .`) với thứ tự xấu khi chỉ sửa mỗi file `main.py`.

**Từng bước**
1. Dòng 3–18 khai báo `GOOD_ORDER` và `BAD_ORDER`, gắn mỗi lệnh với tập các file mà nếu thay đổi sẽ làm bước đó mất cache.
2. Dòng 21–35 viết hàm `simulate_build(steps, changed_files, has_cache)`: một khi có bước bị trượt cache (do `has_cache` là `False` hoặc `watched & changed_files` khác rỗng), cờ `cache_broken` bật `True` khiến mọi bước phía sau đều phải `REBUILD`.
3. Dòng 38–46 mô phỏng lần build đầu chưa có cache và lần build thứ hai sau khi sửa `main.py`, in trạng thái `[CACHED]` hay `[REBUILD]` cho từng dòng.

**Để ý:** Ở `BAD ORDER`, sửa `main.py` làm trượt cache ngay tại `COPY . .` ở bước 3, kéo theo `RUN pip install` ở bước 4 phải chạy lại dù `requirements.txt` không hề đổi.

**Tự thử:** Đổi `{"main.py"}` ở dòng 40 thành `{"requirements.txt"}` và kiểm tra xem cả hai thứ tự lúc này đều phải chạy lại `RUN pip install` vì file thư viện thật sự đã đổi.
