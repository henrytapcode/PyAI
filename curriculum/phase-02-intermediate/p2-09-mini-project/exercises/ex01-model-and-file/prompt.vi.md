Hãy xây nửa đầu của expense tracker: model `Expense`, một hàm kiểm tra từ chối dữ liệu sai, hai hàm lưu list khoản chi vào file JSON rồi đọc lại, và một context manager để sửa list đã lưu một cách an toàn. Editor đã có sẵn khung với các bước `# TODO`. Hãy viết code bên trong class và các hàm, và thêm hàm phụ nếu bạn muốn. Các phần 2 đến 5 của bài học có mọi công cụ bạn cần.

**Ví dụ**

```python
lunch = Expense("2024-03-05", "food", 4.5, "pho")
save_expenses("e.json", [lunch])
load_expenses("e.json")            # [Expense(date='2024-03-05', category='food', amount=4.5, note='pho')]
check_expense(Expense("2024-3-5", "food", 4.5))   # raises ValueError (bad date)

with edit_expenses("e.json") as expenses:
    expenses.append(Expense("2024-03-06", "fun", 9.0))
# the file now holds two expenses
```

**Quy tắc**

- `Expense` là một dataclass **frozen** với các field `date`, `category`, `amount` và `note`, theo đúng thứ tự đó. `note` là tùy chọn và mặc định là `""`.
- `check_expense(expense)` trả về `None` khi khoản chi hợp lệ, và raise `ValueError` khi vi phạm bất kỳ quy tắc nào:
  - `date` là text dạng `YYYY-MM-DD`: ba phần cách nhau bởi `-`, có 4, 2 và 2 chữ số;
  - `category` là text không rỗng sau khi `strip()`;
  - `amount` là một số (`int` hoặc `float`) lớn hơn `0`.
  - `date` hoặc `category` không phải text (ví dụ số `20240305`) cũng raise `ValueError`.
- `save_expenses(path, expenses)` kiểm tra **tất cả** khoản chi trước. Nếu có một khoản sai, hàm raise `ValueError` và **không** tạo hay thay đổi file. Nếu không, hàm ghi một list JSON, mỗi khoản chi là một object, với các key `date`, `category`, `amount` và `note`.
- `load_expenses(path)` trả về list các object `Expense`, theo thứ tự trong file:
  - file không tồn tại thì raise `FileNotFoundError`;
  - text không phải JSON, giá trị JSON không phải list, record không phải object có đúng key (thiếu hoặc thừa key), và record vi phạm một quy tắc của `check_expense` đều raise `ValueError`.
- Lưu rồi đọc lại phải cho ra các khoản chi bằng nhau.
- `edit_expenses(path)` là một context manager viết bằng `@contextmanager`. Nó đọc các khoản chi của `path` và đưa list đó cho khối `with` (`as expenses`). File không tồn tại thì bắt đầu là `[]`. Khi khối kết thúc **mà không có lỗi**, nó lưu list bằng `save_expenses`, nên mọi khoản chi được kiểm tra trước. Nếu khối raise lỗi, hoặc có một khoản chi sai trong list, file giữ nguyên hoàn toàn như cũ.

Bấm **Kiểm tra** để chạy test.
