# Dòng thời gian kết hợp TTL và LRU cache

**Ví dụ này cho thấy:** Theo dõi đồng thời cơ chế đẩy phần tử theo LRU (`maxsize=3`) và hết hạn theo TTL (`ttl=30.0`) qua 9 thao tác với đồng hồ truyền vào (inject) `FakeClock`.

**Từng bước**
1. Dòng 6–14 định nghĩa `FakeClock` gọi được như hàm (`__call__` trả về `self.t`) kèm `advance(seconds)` tất định để không cần đồng hồ hệ thống hay `sleep`.
2. Dòng 17–40 cài đặt `TTLLRUCache` trên `OrderedDict`: đưa key vừa trúng lên cuối (`move_to_end`), đẩy phần tử lâu nhất khi vượt `maxsize` (`popitem(last=False)`), và xóa entry khi `self.clock() >= expires_at`.
3. Dòng 43–70 chạy tuần tự 9 thao tác từ `t=0` đến `t=42` và in bảng trạng thái cùng thứ tự key sau mỗi bước.

**Để ý:** Tại `t=12`, lệnh `get k1` đẩy `k1` ra cuối nên `k2` mới là phần tử bị LRU đẩy bỏ khi `k4` vào lúc `t=15`; sau đó tới `t=40`, `k1` vẫn hết hạn theo TTL (`t=0 + 30 = 30`) và bị xóa khi tra cứu (`EXPIRED`).

**Tự thử:** Đổi `ttl=30.0` thành `ttl=50.0` rồi chạy lại để xem dòng `EXPIRED` nào chuyển thành `HIT`.
