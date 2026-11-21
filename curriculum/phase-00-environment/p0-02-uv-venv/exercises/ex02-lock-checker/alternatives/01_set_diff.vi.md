# Tìm kiếm bằng generator & phép toán tập hợp

Phiên bản thay thế này dùng `next(..., None)` để tìm gói không phân biệt hoa thường mà không cần tạo dictionary trung gian, và tính `diff_lockfiles` bằng phép toán tập hợp (`new_keys - old_keys`, `old_keys - new_keys`, `old_keys & new_keys`). Cả hai cách đều cho cùng kết quả; các phép toán tập hợp giúp ba nhóm thay đổi trở nên rất rõ ràng khi so sánh hai lockfile.
