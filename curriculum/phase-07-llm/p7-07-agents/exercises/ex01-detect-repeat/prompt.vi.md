Hoàn thiện hàm `is_repeat(history, name, args)` trong `starter.py` bằng cách thay từng chỗ trống `___` để agent nhận ra khi nó lặp lại đúng tool call của bước ngay trước.

Viết code bên trong hàm và `return` một giá trị `bool`.

## Ví dụ

```python
is_repeat([("lookup_order", {"order_id": "1042"})], "lookup_order", {"order_id": "1042"})
# -> True

is_repeat([("lookup_order", {"order_id": "1042"})], "lookup_order", {"order_id": "1043"})
# -> False
```

## Quy tắc

- Trả về `False` khi `history` rỗng.
- Chỉ so sánh với bước **ngay trước đó** (`history[-1]`), không so với các bước cũ hơn.
- Chỉ trả về `True` khi tên tool trùng khớp **và** dictionary `args` bằng với dictionary tham số của bước ngay trước (`==`).
- Không làm thay đổi `history` hoặc `args`.
