## 1. Biến là tên gọi cho một giá trị

**Biến** (variable) giống như cái nhãn bạn dán lên một giá trị để dùng lại sau. Tạo biến bằng dấu `=`:

```python
city = "Hanoi"
population = 8_500_000
print(city, population)
```

Hãy đọc `=` là *"lưu giá trị bên phải vào cái tên bên trái"*. Nó **không** phải dấu "bằng" trong toán.

> [!TIP]
> Dấu gạch dưới trong số như `8_500_000` chỉ giúp dễ đọc. Python bỏ qua chúng.

Bạn có thể đổi giá trị của biến bất cứ lúc nào:

```python
score = 10
score = score + 5  # lấy giá trị cũ, cộng 5, lưu lại
print(score)
```

**Quy tắc đặt tên:** gồm chữ, số và `_`; không bắt đầu bằng số; phân biệt hoa thường (`Score` ≠ `score`). Nên dùng `snake_case` như `total_price`.

## 2. Bốn kiểu dữ liệu cơ bản

Mỗi giá trị đều có một **kiểu** (type). Hàm `type()` cho bạn biết đó là kiểu gì:

```python
print(type(42))        # int: số nguyên
print(type(3.14))      # float: số thực
print(type("hello"))   # str: văn bản
print(type(True))      # bool: True hoặc False
```

| Kiểu | Ví dụ | Dùng để |
|---|---|---|
| `int` | `42`, `-7` | đếm số lượng |
| `float` | `3.14`, `0.5` | số đo, giá tiền |
| `str` | `"hi"`, `'AI'` | văn bản |
| `bool` | `True`, `False` | câu trả lời có/không |

## 3. Phép tính

```python
a = 7
b = 2
print(a + b, a - b, a * b)  # 9 5 14
print(a / b)                # 3.5  (/ luôn trả về float)
print(a // b, a % b)        # 3 1  (chia lấy phần nguyên, chia lấy dư)
print(a ** b)               # 49   (lũy thừa)
```

> [!NOTE]
> `%` (chia lấy dư) rất tiện: `n % 2 == 0` kiểm tra `n` có chẵn không.

Phép so sánh cho ra giá trị `bool`:

```python
print(5 > 3)       # True
print(5 == 3)      # False (== để so sánh, = để gán)
print("ai" == "ai")  # True
```

## 4. Văn bản và f-string

Nối chuỗi bằng `+` vẫn được, nhưng **f-string** rõ ràng hơn. Đặt `f` trước dấu nháy và để biến trong `{}`:

```python
name = "Lan"
age = 21
print(f"{name} is {age} years old")
print(f"Next year: {age + 1}")
```

## 5. Chuyển đổi kiểu

Dữ liệu từ file, form hay API thường đến dưới dạng **văn bản**. Hãy chuyển kiểu trước khi tính toán:

```python
text = "42"
number = int(text)
print(number + 1)        # 43
print(float("1.75"))     # 1.75
print(str(3) + " cats")  # 3 cats
```

> [!WARNING]
> `"5" + "7"` cho ra `"57"` (nối chuỗi), không phải `12`. Còn `int("1.75")` sẽ lỗi `ValueError`. Dùng `float()` cho số thập phân.

## Tóm tắt

- `name = value` lưu một giá trị; bạn có thể ghi đè sau đó.
- Kiểu cơ bản: `int`, `float`, `str`, `bool`. Kiểm tra bằng `type()`.
- `/` trả về float, `//` chia lấy nguyên, `%` chia lấy dư, `**` lũy thừa.
- Dùng f-string để tạo văn bản dễ đọc, và `int()` / `float()` / `str()` để chuyển kiểu.
