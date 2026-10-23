# Một họ các model

**Ví dụ này cho thấy:** một class cha và ba class con, mỗi class trả lời `generate` theo cách riêng, được dùng trong cùng một vòng lặp.

**Từng bước**
1. Dòng 2-10 định nghĩa `Model`: lưu tên, có `generate` bắt buộc phải override (nó raise `NotImplementedError`), và `describe` mà mọi class con đều thừa hưởng.
2. Dòng 13-15 định nghĩa `EchoModel`. Nó chỉ override `generate`; `__init__` và `describe` đến từ `Model`.
3. Dòng 18-24 định nghĩa `CannedModel`. `__init__` của nó gọi `super().__init__(name)` trước, rồi mới thêm `reply`.
4. Dòng 27-33 định nghĩa `ChatModel` tương tự, với văn bản `system` được đặt trước prompt.
5. Dòng 36-44 đặt mỗi loại một object vào list. Vòng lặp không quan tâm đang cầm loại nào: nó gọi `describe`, `generate` và `isinstance` y như nhau mỗi lần.

**Để ý:** `describe` chỉ viết một lần, trong `Model`, mà chạy được cho cả ba class con.

**Tự thử:** thêm `ShoutModel(Model)` có `generate` trả về `prompt.upper()`, rồi thêm nó vào list. Bạn sẽ thấy thêm một khối ba dòng.
