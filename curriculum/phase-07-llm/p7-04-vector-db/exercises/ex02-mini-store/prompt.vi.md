Cài đặt class `MiniStore` trong `starter.py` hỗ trợ `add()` theo lô, `search()` top-k có lọc trước, `delete()` và `len(store)`.

Hãy viết code bên trong các phương thức của class và `return` đúng giá trị yêu cầu.

## Ví dụ

```python
client = FakeLLM(embed_dim=256)
store = MiniStore(client)
store.add(["c1", "c2"], ["cheap car rental", "fast laptop repair"], [{"lang": "en"}, {"lang": "vi"}])
store.search("affordable automobile", k=1, where={"lang": "en"})  # -> [("c1", 0.816)]
len(store)  # -> 2
```

## Quy tắc

- `add(ids, texts, metadatas=None)` phải gọi `client.embed(texts)` **đúng một lần** cho mỗi lần `add` không rỗng, mặc định mỗi phần tử là `{}` khi `metadatas=None`, và báo `ValueError` mà không thêm gì nếu có `id` trùng trong store hoặc trùng ngay trong `ids`.
- `search(query, k=3, where=None)` phải lọc trước theo `where` rồi mới lấy top-k, trả về danh sách `(id, score)` giảm dần (hòa điểm thì bản ghi thêm trước đứng trước), mỗi `score` là `float` Python làm tròn 3 chữ số thập phân.
- Trả về `[]` và không báo lỗi khi store rỗng, `k <= 0` hoặc không có bản ghi nào khớp `where`.
- `delete(doc_id)` phải xóa cả bản ghi lẫn vector của nó, hoặc báo `KeyError` nếu không tìm thấy `doc_id`.
- `__len__()` phải trả về số lượng bản ghi đang lưu.
