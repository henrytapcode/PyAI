# Pipeline kiểm tra dạng bảng (table-driven)

Cách tiếp cận này tách từng bước kiểm tra quyền, tham số, chính sách và xác nhận thành các hàm thuần rồi xếp thứ tự trong `_GUARD_PIPELINE`. Phương thức `ScopedRegistry.execute` duyệt qua pipeline, dừng ở lần từ chối đầu tiên và ghi `audit_log` tại một điểm thoát duy nhất. Việc tách bảng kiểm tra khỏi `execute` giúp bạn dễ unit-test từng quy tắc riêng lẻ hoặc thêm/đổi thứ tự kiểm tra mà không làm lồng ghép điều kiện sâu thêm, trong khi cách viết tuần tự ở `solution.py` giúp đọc toàn bộ chuỗi ưu tiên ngay trong một hàm.
