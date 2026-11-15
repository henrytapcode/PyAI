# Cổng duyệt của con người (approval gate)

**Điểm nổi bật:** Cho agent tạm dừng với `stopped_reason == "needs_approval"` khi đề xuất tool có tác dụng phụ (`issue_refund`), và chỉ thực thi sau khi biến duyệt xác nhận.

**Từng bước**
1. Dòng 6–34 đưa `"issue_refund"` vào tập `APPROVAL_REQUIRED`, còn `"lookup_order"` vẫn là tool chỉ đọc an toàn.
2. Dòng 37–58 chạy `run_with_approval()`: `lookup_order` tự chạy ở bước 1 và vào `trace`, còn `issue_refund` ở bước 2 làm vòng lặp dừng ngay với `"needs_approval"` và trả về `pending`.
3. Dòng 61–64 định nghĩa `handle_approval()`, chỉ gọi `REGISTRY[pending["tool"]]` khi `approved` là `True`.
4. Dòng 67–81 chạy tác vụ theo `script` và in nhật ký cho cả hai trường hợp `approved_by_human = False` lẫn `approved_by_human = True`.

**Lưu ý:** Agent không bao giờ tự chạy `issue_refund` bên trong vòng lặp—nó chỉ đề xuất hành động đang chờ duyệt để code ứng dụng bên ngoài kiểm soát quyền xác nhận.

**Tự thử:** Thêm `"lookup_order"` vào `APPROVAL_REQUIRED` để xem agent dừng ngay ở bước 1 với `trace` rỗng.
