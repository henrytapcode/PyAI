# Bảo vệ tool có tác dụng phụ

**Điểm nổi bật:** Bảo vệ hàm hoàn tiền `issue_refund` bằng allowlist, xác nhận của con người và trần tự động `100.0`, đồng thời ghi nhật ký mọi quyết định.

**Từng bước**
1. Dòng 6–18 khai báo `ORDERS`, `ALLOWED_TOOLS`, ngưỡng `MAX_AUTO_REFUND = 100.0`, danh sách `ACTION_LOG` và hàm `issue_refund()`.
2. Dòng 21–34 cài đặt `guarded_dispatch()`, chặn mọi tool ngoài `ALLOWED_TOOLS`, chặn thao tác chưa được xác nhận và chặn số tiền vượt `MAX_AUTO_REFUND` trước khi `issue_refund()` được phép chạy.
3. Dòng 37–42 dùng `FakeLLM(script=...)` mô phỏng model đề nghị hoàn `$45` (được duyệt) rồi hoàn `$250` (bị chặn).
4. Dòng 49–65 đưa cả hai lượt qua `guarded_dispatch()`, gửi kết quả tool lại cho `scripted.chat()` và in toàn bộ `ACTION_LOG`.

**Lưu ý:** Dù model đề nghị `amount=250.0` và `user_confirmed=True`, lớp kiểm tra trong `guarded_dispatch()` đã chặn giao dịch trước khi `issue_refund()` chạy và ghi lại vào `ACTION_LOG`.

**Tự thử:** Đổi `user_confirmed` ở dòng 45 thành `False` để thấy ngay cả khoản hoàn `$45` cũng bị chặn và ghi log.
