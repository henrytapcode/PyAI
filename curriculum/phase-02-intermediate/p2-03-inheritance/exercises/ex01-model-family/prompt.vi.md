Hãy viết hai class. `Model` là class cha. `CannedModel` là class con trả lời bằng các câu có sẵn, lần lượt từng câu, và quay lại từ đầu sau câu cuối. Viết code bên trong các method và `return` kết quả. (`pass` nghĩa là "chưa làm gì": hãy thay nó bằng code của bạn.)

**Ví dụ**

```python
bot = CannedModel("c1", ["Hi!", "Bye!"])
bot.generate("anything")   # "Hi!"
bot.generate("anything")   # "Bye!"
bot.generate("anything")   # "Hi!"  (quay lại từ đầu)
bot.describe()             # "model: c1 (2 replies)"
```

**Quy tắc**
- `Model(name)` lưu tên vào `self.name`.
- `Model.generate(prompt)` phải raise `NotImplementedError`: các class con phải tự viết nó.
- `Model.describe()` trả về `"model: "` rồi đến tên, ví dụ `"model: base"`.
- `CannedModel(name, replies)` kế thừa từ `Model`, gán tên bằng cách gọi `super().__init__`, và giữ list trong `self.replies`.
- `CannedModel.generate(prompt)` bỏ qua prompt và trả về câu tiếp theo. Mỗi object `CannedModel` tự đếm số lần gọi của mình. Gợi ý: `i % n` là phần dư của `i` chia cho `n`, nên `5 % 3` bằng `2`.
- `CannedModel.describe()` dùng `super().describe()` rồi thêm một dấu cách và `(N replies)` ở cuối, với `N` là số câu trả lời. Luôn viết `replies`, kể cả khi `N` là 1.

Bấm **Kiểm tra** để chạy test.
