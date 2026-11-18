# Báo cáo phân vị độ trễ

**Ví dụ này cho thấy:** Tính `min`, `mean`, `p50`, `p90`, `p95` và `max` trên 20 độ trễ request bằng phương pháp nearest-rank, sau đó in ra 3 `request_id` chậm nhất.

**Từng bước**
1. Dòng 7–10 cài đặt `percentile(values, p)` bằng cách sắp xếp `values` rồi lấy phần tử ở chỉ số `math.ceil(p / 100 * len(ordered)) - 1`.
2. Dòng 14–35 khai báo 20 mẫu `(request_id, latency_ms)`, trong đó 16 request xong trong 180–250 ms và 4 request ở phần đuôi mất 880–2.650 ms.
3. Dòng 37–50 tính 6 chỉ số tổng hợp và in thành bảng `metric | value`.
4. Dòng 52–55 sắp xếp `samples` giảm dần theo độ trễ để in ra 3 request chậm nhất (`req-14`, `req-05`, `req-19`).

**Để ý:** Một nửa số request hoàn thành từ `215` ms trở xuống (`p50`), nhưng `mean` bị kéo lên `462.5` ms còn `p95` vọt lên `1420` ms—cho thấy số trung bình dễ che lấp phần đuôi chậm trong khi `p95` chỉ thẳng ra vấn đề.

**Tự thử:** Đổi `2650` ms của `req-14` thành `260` ms rồi xem `mean` và `max` giảm xuống thế nào trong khi `p50` giữ nguyên không đổi.
