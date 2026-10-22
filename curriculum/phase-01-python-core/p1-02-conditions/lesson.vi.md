## 1. Đưa ra quyết định với `if`

Từ đầu đến giờ code của bạn chạy hết mọi dòng từ trên xuống dưới. Với **điều kiện** (condition), chương trình có thể tự lựa chọn. Điều kiện là một biểu thức cho ra `True` hoặc `False`, như các phép so sánh ở bài 1:

```python
print(5 > 3)    # True
print(5 == 3)   # False
print(5 != 3)   # True
print(4 <= 4)   # True
```

Sáu toán tử so sánh là `==`, `!=`, `<`, `>`, `<=`, `>=`. Đặt điều kiện sau `if`, và đoạn code bên dưới **chỉ chạy khi điều kiện là `True`**:

```python
temperature = 31

if temperature > 30:
    print("It's hot")
print("Done")
```

## 2. Thụt lề và dấu hai chấm

Có hai chi tiết rất quan trọng:

- Dòng `if` kết thúc bằng dấu hai chấm `:`.
- Các dòng thuộc về `if` phải được **thụt lề** (indentation), dùng 4 dấu cách. Python dựa vào thụt lề để biết khối code bắt đầu và kết thúc ở đâu.

```python
age = 15

if age >= 18:
    print("Adult")
    print("You may vote")
print("This line always runs")  # không thụt lề: nằm ngoài if
```

> [!WARNING]
> Quên `:` sẽ gây `SyntaxError`. Thụt lề sai hoặc thiếu gây `IndentationError`. Ngoài ra `if x = 5` là sai: phải dùng `==` để so sánh.

## 3. `else`: con đường còn lại

`else` chạy khi điều kiện là `False`:

```python
score = 45

if score >= 50:
    print("Pass")
else:
    print("Fail")
```

## 4. `elif`: nhiều hơn hai lựa chọn

Dùng `elif` (viết tắt của "else if") để thêm các phép kiểm tra. Python kiểm tra **từ trên xuống dưới và chỉ chạy nhánh đầu tiên đúng**:

```python
score = 85

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "F"

print(grade)  # B
```

> [!TIP]
> Thứ tự rất quan trọng. `85 >= 90` được kiểm tra trước và sai, nên ta đi tiếp và đến `B`. Nếu bạn viết `score >= 70` lên đầu, mọi điểm từ 70 trở lên đều nhận `C`.

## 5. Kết hợp điều kiện: `and`, `or`, `not`

| Toán tử | Ý nghĩa | Ví dụ |
|---|---|---|
| `and` | cả hai đều True | `age >= 18 and has_id` |
| `or` | ít nhất một cái True | `is_weekend or is_holiday` |
| `not` | đảo True/False | `not is_raining` |

```python
age = 20
has_ticket = True
is_vip = False

print(age >= 18 and has_ticket)  # True
print(is_vip or age >= 65)       # False
print(not is_vip)                # True

if age >= 18 and has_ticket:
    print("Welcome in")
```

Bạn cũng có thể viết kiểm tra khoảng giá trị rất tự nhiên: `0 <= score <= 100`.

> [!NOTE]
> Khi trộn lẫn, `not` được tính trước, rồi đến `and`, rồi đến `or`. Nếu không chắc, hãy thêm ngoặc: `(a or b) and c`.

## 6. Truthiness: rỗng và số 0 là False

Trong `if`, Python không cần một giá trị `bool` thật sự. Những giá trị sau được coi là **False**: `0`, `0.0`, `""` (chuỗi rỗng). Hầu hết mọi thứ còn lại được coi là **True**.

```python
name = ""

if name:
    print(f"Hello, {name}")
else:
    print("Please enter a name")

print(bool(0), bool(""), bool("0"), bool(7))  # False False True True
```

Lưu ý `bool("0")` là `True`: đó là một chuỗi không rỗng, không phải số không.

## 7. `if` lồng nhau và `elif`

Bạn có thể đặt một `if` bên trong `if` khác (**nested if**, if lồng nhau). Nó chạy được nhưng nhanh chóng khó đọc:

```python
age = 16
has_id = True

if age >= 18:
    if has_id:
        print("Enter")
```

Khi các kiểm tra cùng xoay quanh một câu hỏi, hãy ưu tiên `and`, hoặc một chuỗi `elif` phẳng:

```python
age = 16
has_id = True

if age >= 18 and has_id:
    print("Enter")
elif age >= 18:
    print("Bring your ID")
else:
    print("Too young")
```

## Tóm tắt

- Điều kiện là biểu thức cho ra `True` hoặc `False`; so sánh bằng `== != < > <= >=`.
- `if`, `elif`, `else` kết thúc bằng `:`; khối code bên dưới được thụt lề 4 dấu cách.
- Python chỉ chạy nhánh đúng đầu tiên, nên hãy sắp xếp thứ tự các `elif` cẩn thận.
- `and`, `or`, `not` kết hợp các điều kiện; không chắc thì thêm ngoặc.
- `0`, `0.0` và `""` được coi là False; chuỗi không rỗng và số khác 0 được coi là True.
- Ưu tiên chuỗi `elif` phẳng hoặc `and` thay vì nhiều tầng `if` lồng nhau.
