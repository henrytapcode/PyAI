# Kho phiên tách biệt với TTL và giới hạn số phiên bằng FakeClock

**Những gì ví dụ minh họa:** Lưu lịch sử trò chuyện riêng cho từng phiên trong một dict có giới hạn dung lượng, trong đó phiên cũ tự hết hạn theo TTL của `FakeClock` và khi đầy sẽ loại phiên ít được dùng gần nhất.

**Từng bước một**
1. Dòng 2–10 định nghĩa class `FakeClock` chuẩn để kiểm soát thời gian tất định.
2. Dòng 13–47 định nghĩa `SessionStore` lưu `{"history", "last_seen"}` cho mỗi `session_id`, tự dọn phiên hết hạn khi truy cập, giữ nguyên lịch sử nếu gọi `create` cho `sid` đang hoạt động và xóa phiên có `last_seen` nhỏ nhất khi đạt `max_sessions=2`.
3. Dòng 50–63 tạo `"alice"` lúc `t=0`, tạo `"bob"` lúc `t=20`, rồi tương tác lại với `"alice"` lúc `t=30`.
4. Dòng 65–71 tạo `"carol"` lúc `t=40` (loại `"bob"` thay vì `"alice"`), sau đó tua tới `t=90` để `"alice"` hết hạn trong khi `"carol"` vẫn còn hiệu lực.

**Lưu ý:** Lần cập nhật `"alice"` ở `t=30` đã đẩy `last_seen` của `"alice"` lên `30`, nên khi `"carol"` tới ở `t=40`, hệ thống loại `"bob"` (`last_seen=20`) chứ không loại `"alice"`.

**Tự thử:** Xóa lệnh `append_turn("alice", ...)` ở `t=30` rồi chạy lại để kiểm chứng rằng `"alice"` (`last_seen=0`) sẽ bị loại thay cho `"bob"`.
