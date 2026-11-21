# Phân quyền tool theo phạm vi, giới hạn ghi và audit log

**Những gì ví dụ minh họa:** Áp dụng allowlist (danh sách cho phép) theo từng request, giới hạn `max_amount` cho thao tác ghi và cổng xác nhận cho thao tác phá hủy trong `ScopedRegistry`, đồng thời ghi mọi kết quả vào `audit_log`.

**Từng bước một**
1. Dòng 7–21 định nghĩa `ToolSpec` (thông tin tool, mức `risk`, `max_amount` tùy chọn) và `RequestContext` (`role`, `allowed_tools`, `confirmation_token` tùy chọn).
2. Dòng 24–58 cài đặt `ScopedRegistry.execute()`, kiểm tra tool không tồn tại, phạm vi allowlist, tham số bắt buộc, giới hạn `max_amount` và `confirm_fn` theo đúng thứ tự ưu tiên trước khi ghi vào `audit_log`.
3. Dòng 61–67 đăng ký ba tool (`lookup_order`, `issue_refund` giới hạn `50.0`, `delete_account`) rồi tạo `support_ctx` và `admin_ctx`.
4. Dòng 69–73 chạy bốn lượt gọi—đọc hợp lệ, hoàn tiền vượt ngưỡng, xóa ngoài phạm vi, và xóa có xác nhận của admin—rồi in kết quả cùng các trạng thái trong `audit_log`.

**Lưu ý:** Cả hai lượt bị từ chối (`"denied_policy"` và `"denied_scope"`) đều chặn không cho hàm bên dưới chạy, nhưng vẫn ghi đầy đủ một bản ghi vào `audit_log`.

**Tự thử:** Đổi `support_ctx` gọi `issue_refund` với `amount: 25.0` để kiểm tra trạng thái chuyển từ `"denied_policy"` sang `"ok"`.
