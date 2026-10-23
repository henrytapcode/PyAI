`Pipeline` cho văn bản đi qua một list model, lần lượt từng cái. Nó được dựng bằng composition: nó **có** các model, nó không phải là một model. Các model đã được viết sẵn cho bạn. Hãy thay mỗi `___` trong `Pipeline` bằng code đúng.

**Ví dụ**

```python
pipe = Pipeline([ShoutModel("s"), EchoModel("e")])
pipe.run("hi")     # "echo: HI"  ("hi" -> "HI" -> "echo: HI")
pipe.size()        # 2
```

**Quy tắc**
- `Pipeline(steps)` giữ list trong `self.steps`.
- `add(model)` đặt model vào **cuối** `self.steps`.
- `run(text)` đưa văn bản cho `generate` của bước đầu tiên, đưa kết quả đó cho bước kế tiếp, và cứ thế. Nó trả về văn bản cuối cùng. Nếu không có bước nào, nó trả về văn bản nguyên vẹn.
- `size()` trả về số bước của pipeline.
- `Pipeline` vẫn là một class riêng: đừng cho nó kế thừa từ `Model`.

Bấm **Kiểm tra** để chạy test.
