## 1. Vì sao cần hàm?

Từ đầu đến giờ code của bạn chạy từ trên xuống dưới. Khi cần lặp lại cùng các bước, bạn copy-paste, và mọi thứ nhanh chóng trở nên lộn xộn. **Hàm** (function) là một khối code có tên: viết một lần, chạy bất cứ khi nào cần.

Hàm mang lại hai thứ: **tái sử dụng** (viết một lần, gọi nhiều lần) và **đặt tên** (`bmi(...)` cho người đọc biết chuyện gì xảy ra mà không cần xem chi tiết). Bạn đã dùng các hàm có sẵn: `print()`, `len()`, `int()`.

## 2. Định nghĩa và gọi hàm

Dùng `def`, tên hàm, dấu ngoặc, dấu hai chấm, rồi phần thân thụt lề:

```python
def say_hello():
    print("Hello!")


say_hello()
say_hello()
```

`def` chỉ *định nghĩa* hàm; không có gì chạy cho đến khi bạn **gọi** (call) nó bằng `name()`.

## 3. Tham số và đối số

**Tham số** (parameter) là tên biến nằm ở dòng `def`. **Đối số** (argument) là giá trị thực tế bạn truyền vào khi gọi:

```python
def square(n):          # n is a parameter
    print(n * n)


square(5)               # 5 is an argument
square(12)
```

Hàm có thể nhận nhiều tham số, ngăn cách bằng dấu phẩy. Đối số được ghép theo vị trí:

```python
def rectangle_area(width, height):
    print(width * height)


rectangle_area(3, 4)
```

## 4. return và print

Đây là chỗ người mới hay nhầm nhất.

- `print(x)` **hiển thị** giá trị lên màn hình. Chương trình không thể dùng nó sau đó.
- `return x` **trả giá trị về** cho đoạn code đã gọi hàm, để bạn lưu vào biến hoặc tính tiếp.

```python
def double_print(n):
    print(n * 2)


def double_return(n):
    return n * 2


a = double_print(4)    # prints 8
b = double_return(4)   # prints nothing
print("a is", a)
print("b is", b)
print("b + 1 =", b + 1)
```

Hàm không có `return` sẽ trả về `None` ("không có gì"). Vì vậy `a` là `None` và `a + 1` sẽ gây lỗi.

> [!WARNING]
> Nếu bạn thấy `None` ở chỗ đáng lẽ là một con số, hoặc lỗi `TypeError: unsupported operand type(s) ... 'NoneType'`, rất có thể bạn đã dùng `print` (hoặc quên `return`) trong hàm.

`return` cũng **kết thúc** hàm ngay lập tức; code phía sau nó không chạy:

```python
def sign(n):
    if n < 0:
        return "negative"
    if n == 0:
        return "zero"
    return "positive"


print(sign(-3), sign(0), sign(8))
```

> [!TIP]
> Quy tắc nhớ nhanh: hàm *tính toán* nên `return` kết quả. Để nơi gọi hàm quyết định có in ra hay không.

## 5. Tham số mặc định và keyword argument

Cho tham số một **giá trị mặc định** (default value) bằng dấu `=`. Khi đó người gọi có thể bỏ qua nó:

```python
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"


print(greet("Lan"))
print(greet("Lan", "Hi"))
print(greet("Lan", greeting="Xin chao"))   # keyword argument
```

Ở lần gọi cuối ta viết `greeting=...` theo tên: đó là **keyword argument** (đối số theo tên). Nó giúp lời gọi dễ đọc hơn và thứ tự không còn quan trọng.

> [!NOTE]
> Tham số có giá trị mặc định phải đứng sau tham số không có: `def f(a, b=1)` hợp lệ, còn `def f(a=1, b)` là lỗi cú pháp.

## 6. Docstring

Một chuỗi ở dòng đầu tiên của thân hàm dùng để mô tả hàm làm gì. Nó gọi là **docstring**:

```python
def average(numbers):
    """Return the mean of a non-empty list of numbers."""
    return sum(numbers) / len(numbers)


print(average([2, 4, 9]))
help(average)
```

Tên hàm tốt cộng một dòng docstring giúp code vẫn dễ đọc sau nhiều tháng.

## 7. Phạm vi cục bộ và hàm gọi hàm

Biến tạo bên trong hàm là biến **cục bộ** (local): chỉ tồn tại khi hàm đang chạy.

```python
def make_total(price):
    tax = price * 0.1     # local to make_total
    return price + tax


print(make_total(100))
# print(tax)   # NameError: tax does not exist out here
```

Hàm có thể gọi hàm khác. Những mảnh nhỏ ghép lại thành mảnh lớn:

```python
def bmi(weight_kg, height_m):
    return weight_kg / height_m ** 2


def describe(weight_kg, height_m):
    value = bmi(weight_kg, height_m)
    return f"BMI is {value:.1f}"


print(describe(52, 1.60))
```

## Tóm tắt

- `def name(parameters):` định nghĩa hàm; `name(arguments)` gọi hàm.
- `print` hiển thị giá trị; `return` trả giá trị về. Không có `return` nghĩa là `None`.
- Giá trị mặc định (`greeting="Hello"`) làm tham số thành tùy chọn; keyword argument truyền theo tên.
- Docstring mô tả hàm; biến bên trong hàm là biến cục bộ.
- Hàm có thể gọi hàm khác: xây thứ lớn từ những mảnh nhỏ có tên.
