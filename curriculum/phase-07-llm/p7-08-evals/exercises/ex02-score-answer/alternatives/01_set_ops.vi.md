# Dùng hiệu tập hợp với `dict.fromkeys` và `sum` trên generator

Thay vì cộng dồn `matched`, `citations` và `unsupported` bằng nhiều vòng lặp `for` tường minh, cách này tính `facts` bằng `sum(...)` trên generator, loại trùng `citations` qua `dict.fromkeys(...)`, rồi tìm `missing = set(ans_words) - ctx_set` trước khi lọc `dict.fromkeys(ans_words)` để giữ thứ tự xuất hiện đầu tiên không trùng. Các phép toán tập hợp giúp code ngắn và nhanh với ngữ cảnh lớn, còn `dict.fromkeys` giữ tính tất định cho cả `citations` lẫn `unsupported`.
