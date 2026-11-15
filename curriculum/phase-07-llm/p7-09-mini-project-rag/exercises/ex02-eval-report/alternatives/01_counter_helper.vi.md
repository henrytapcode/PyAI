# Tách hàm phân loại từng câu kết hợp `collections.Counter`

Cách tiếp cận này tách phần chấm từng câu hỏi thành hàm riêng `_classify_case(row, out)` rồi cộng dồn mọi chỉ số bằng `collections.Counter`. Tách biệt logic phân loại một dòng khỏi vòng lặp tổng hợp giúp viết unit test riêng cho từng ca lỗi dễ hơn và thuận tiện mở rộng thêm bộ đếm mới về sau.
