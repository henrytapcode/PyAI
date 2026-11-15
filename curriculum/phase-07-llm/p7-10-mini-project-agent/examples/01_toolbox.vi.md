# Toolbox an toàn cho hệ thống hỗ trợ đơn hàng

**Ví dụ này minh họa:** Bọc bốn tool cửa hàng sau một hàm `invoke()` duy nhất để kiểm tra allowlist, xác thực tham số bắt buộc, lọc bỏ tham số thừa, bắt ngoại lệ và chuyển `dict` sang JSON bằng `json.dumps()`.

**Từng bước một**
1. Dòng 4–29 định nghĩa dữ liệu mẫu của cửa hàng (`ORDERS`, `SHIPMENTS`, `REFUNDS`) và bốn hàm tool bằng Python.
2. Dòng 32–52 đăng ký từng hàm vào `REGISTRY` kèm JSON schema và cờ `side_effect`.
3. Dòng 55–69 viết `invoke(name, args)` kiểm tra allowlist, kiểm tra `required`, chỉ giữ các tham số trong `properties` và trả chuỗi `"error: ..."` thay vì làm sập chương trình.
4. Dòng 72–80 chạy năm ca hợp lệ lẫn lỗi rồi in ra chuỗi kết quả quan sát của từng ca.

**Điểm đáng chú ý:** Truyền thêm khóa lạ `"extra": 1` cho `lookup_order` vẫn chạy bình thường vì `invoke()` lọc `args` theo `properties` của schema trước khi bung `**clean`.

**Tự thử:** Thêm một bộ dữ liệu thứ sáu `("missing_amt", "issue_refund", {"order_id": "1042"})` vào `cases` và kiểm tra xem `invoke()` có trả `"error: missing amount"` mà không ghi vào `REFUNDS` hay không.
