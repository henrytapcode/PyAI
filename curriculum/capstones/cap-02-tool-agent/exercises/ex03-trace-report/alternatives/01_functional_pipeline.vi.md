# Pipeline hàm thuần với `collections.Counter` và các hàm phụ trợ

Cách tiếp cận này tách việc tạo span (`_build_span`), tính phân vị p95 (`_nearest_rank_p95`) và cắt dòng (`_clamp_line`) thành các hàm thuần nhỏ, đồng thời dùng `collections.Counter` với generator expression trong `summarize_traces`. So với vòng lặp `for` duyệt một lần ở `solution.py`, cách viết này mang tính khai báo (declarative) và gọn hơn, đổi lại phải duyệt danh sách `spans` nhiều lượt (vẫn là `O(N)` và không đáng kể với các lô trace agent thông thường).
