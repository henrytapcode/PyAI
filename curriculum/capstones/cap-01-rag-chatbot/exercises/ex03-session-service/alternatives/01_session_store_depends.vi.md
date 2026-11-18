# Lớp SessionStore dùng OrderedDict LRU và FastAPI Depends

**Cách hoạt động:** Thay vì quản lý dict thường và quét `min(...)` trong các hàm closure, cách này tách vòng đời phiên sang lớp `SessionStore` dùng `collections.OrderedDict`. Mỗi lần truy cập đều gọi `move_to_end(sid)` để giữ thứ tự từ ít dùng gần nhất tới mới dùng nhất, giúp loại phiên bằng `popitem(last=False)` trong thời gian O(1), còn `Depends(get_active_session)` của FastAPI gom việc dọn phiên hết hạn và kiểm tra `404` vào một nơi dùng chung cho các route có `{sid}`.

**Khi nào nên chọn:** Hãy chọn thiết kế này khi `max_sessions` lớn (tránh quét O(N) mỗi lần đầy bộ nhớ), khi bạn muốn viết unit test riêng cho `SessionStore` tách khỏi tầng HTTP, hoặc khi nhiều endpoint cùng dùng chung bước kiểm tra phiên.
