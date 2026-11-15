Hoàn thành `matches(metadata, where)` và `filter_indexes(metadatas, where)` trong `starter.py` bằng cách thay mọi chỗ trống `___` để lọc trước bản ghi theo metadata trước khi xếp hạng top-k.

Hãy viết code bên trong các hàm và `return` giá trị boolean hoặc danh sách chỉ số nguyên khớp điều kiện.

## Ví dụ

```python
matches({"lang": "vi", "topic": "faq"}, {"lang": "vi"})        # -> True
matches({"lang": "vi"}, {"lang": "vi", "topic": "faq"})        # -> False
filter_indexes([{"lang": "en"}, {"lang": "vi"}], {"lang": "vi"})  # -> [1]
```

## Quy tắc

- Nếu `where` là `None` hoặc `{}` (rỗng), `matches()` trả về `True` cho mọi bản ghi.
- Mọi cặp key/value trong `where` đều phải khớp; nếu thiếu key trong `metadata`, trả về `False`.
- `filter_indexes()` phải trả về các chỉ số khớp theo đúng thứ tự tăng dần ban đầu.
