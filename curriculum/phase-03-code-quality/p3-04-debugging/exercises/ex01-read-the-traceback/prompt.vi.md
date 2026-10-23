Đoạn code bên dưới đọc các dòng log của một dịch vụ LLM và tóm tắt chúng, nhưng nó bị crash. Hai traceback thật được hiện ở đây. Hãy đọc từng cái **từ dưới lên**, tìm nguyên nhân, và sửa code bên trong hai hàm.

Lần crash đầu đến từ `parse_line("model=small tokens=120 latency=0.84s")`:

```text
Traceback (most recent call last):
  File "exercise.py", line 23, in summarize
    records = [parse_line(line) for line in lines]
  File "exercise.py", line 12, in parse_line
    "latency": float(parts["latency"]),
ValueError: could not convert string to float: '0.84s'
```

Lần thứ hai đến từ một list có chứa một dòng trống:

```text
Traceback (most recent call last):
  File "exercise.py", line 23, in summarize
    records = [parse_line(line) for line in lines]
  File "exercise.py", line 10, in parse_line
    "model": parts["model"],
KeyError: 'model'
```

**Ví dụ**

| lời gọi | kết quả |
|---|---|
| `parse_line("model=a tokens=5 latency=0.5s")` | `{"model": "a", "tokens": 5, "latency": 0.5}` |
| `summarize(["model=a tokens=100 latency=1.0s", "", "model=a tokens=50 latency=2.0s"])` | `(150, 1.5)` |
| `summarize([])` | `(0, 0.0)` |

**Quy tắc**
- Latency có thể được viết có hoặc không có chữ `s` ở cuối.
- Các dòng trống và dòng chỉ có khoảng trắng bị bỏ qua.
- Hãy sửa code bên trong các hàm; giữ nguyên tên và giá trị trả về của chúng.
