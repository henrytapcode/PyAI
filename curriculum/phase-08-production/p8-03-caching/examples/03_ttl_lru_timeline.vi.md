# Dòng thời gian kết hợp TTL và LRU cache

**What it shows:** Theo dõi đồng thời cơ chế đẩy phần tử theo LRU (`maxsize=3`) và hết hạn theo TTL (`ttl=30.0`) qua 9 thao tác với đồng hồ tiêm vào `FakeClock`.

**Step by step**
1. Dòng 6–11 định nghĩa `FakeClock` với `advance(seconds)` tất định để không cần đồng hồ hệ thống hay `sleep`.
2. Dòng 14–36 cài đặt `TTLLRUCache` trên `OrderedDict`: đưa key vừa trúng lên cuối (`move_to_end`), đẩy phần tử lâu nhất khi vượt `maxsize` (`popitem(last=False)`), và xóa entry khi `clock.now >= expires_at`.
3. Dòng 39–66 chạy tuần tự 9 thao tác từ `t=0` đến `t=42` và in bảng trạng thái cùng thứ tự key sau mỗi bước.

**Notice:** Tại `t=12`, lệnh `get k1` đẩy `k1` ra cuối nên `k2` mới là phần tử bị LRU đẩy bỏ khi `k4` vào lúc `t=15`; sau đó tới `t=40`, `k1` vẫn hết hạn theo TTL (`t=0 + 30 = 30`) và bị xóa khi tra cứu (`EXPIRED`).

**Try it yourself:** Đổi `ttl=30.0` thành `ttl=50.0` rồi chạy lại để xem dòng `EXPIRED` nào chuyển thành `HIT`.
