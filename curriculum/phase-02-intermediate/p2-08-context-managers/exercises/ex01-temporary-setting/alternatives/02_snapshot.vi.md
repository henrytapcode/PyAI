# Lưu một bản sao của cả dict

Thay vì nhớ một key, hãy sao chép cả dict trước (`dict(config)`) và trong `finally` thì xóa sạch dict rồi nạp lại từ bản sao:

- `dict(config)` tạo bản sao.
- `config.clear()` xóa sạch dict gốc.
- `config.update(snapshot)` nạp lại các mục đã lưu.

 Cách này xử lý key chưa tồn tại mà không cần `if`. Đổi lại: nó cũng hoàn tác mọi thay đổi khác lên dict trong khối, và nó sao chép toàn bộ nên chậm với dict lớn. Chọn cách này khi bạn muốn "trả dict về y như cũ", và chọn bản một key khi chỉ key đó cần khôi phục.
