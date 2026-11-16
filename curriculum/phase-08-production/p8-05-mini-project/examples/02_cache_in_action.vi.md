# TTL cache hoạt động thực tế

**Bài này minh họa:** Cách một TTL cache tất định bên trong `create_app` chuẩn hóa khoảng trắng, tách riêng các giá trị `top_k` khác nhau, lưu cả câu từ chối và cho hết hạn khi `FakeClock` tiêm vào vượt `ttl`.

**Từng bước**
1. Các dòng 17–25 cài đặt `FakeClock` có `__call__()` và `advance(seconds)` để app đọc thời gian mà không chạm đồng hồ hệ thống.
2. Các dòng 46–49 tạo `make_key` bằng cách cắt khoảng trắng dư, gộp khoảng trắng liên tiếp rồi băm JSON `{"question": clean, "top_k": top_k}` với `sort_keys=True`.
3. Các dòng 87–102 gửi 6 request theo mốc thời gian (`t=0` tới `t=50`), sau đó tua đồng hồ thêm `350` giây (`t=400 >= 300`) để gây trượt cache do hết hạn.

**Lưu ý:** Tại `t=10` câu hỏi thừa khoảng trắng vẫn trúng cache (`chat` giữ ở `1`), tại `t=20` đổi sang `top_k=1` bị trượt cache (`chat` lên `2`), và tại `t=50` câu từ chối cũng được lưu lại.

**Tự thử:** Gửi lại `"Can I pay with crypto?"` tại `t=60` và kiểm tra `cached` chuyển thành `True` trong khi `chat` vẫn là `3`.
