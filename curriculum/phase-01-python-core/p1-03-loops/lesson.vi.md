## 1. Vì sao cần vòng lặp?

Máy tính rất giỏi những việc nhàm chán và lặp đi lặp lại. Thay vì chép một dòng 100 lần, bạn viết một lần rồi bảo Python **lặp** nó. Đó là **vòng lặp** (loop).

```python
for i in range(3):
    print("Hello!")
```

Dòng thụt lề là **thân vòng lặp** (body). Nó chạy một lần mỗi vòng. Thụt lề (4 dấu cách) là cách Python biết dòng nào thuộc về vòng lặp.

## 2. `for` và `range()`

`range()` tạo ra một dãy số nguyên. `for` đi qua từng số và gán vào một biến:

```python
for i in range(5):
    print(i)  # 0 1 2 3 4
```

`range` có ba dạng:

| Lệnh gọi | Các số tạo ra |
|---|---|
| `range(5)` | 0, 1, 2, 3, 4 |
| `range(2, 6)` | 2, 3, 4, 5 |
| `range(0, 10, 3)` | 0, 3, 6, 9 |
| `range(5, 0, -1)` | 5, 4, 3, 2, 1 |

```python
for n in range(2, 11, 2):
    print(n)  # các số chẵn 2..10
```

> [!WARNING]
> Giá trị **stop** (điểm dừng) không bao giờ được tính. `range(1, 5)` cho 1, 2, 3, 4. Muốn đếm từ 1 đến `n`, hãy viết `range(1, n + 1)`. Lỗi "lệch một đơn vị" (off by one) này là lỗi vòng lặp phổ biến nhất.

## 3. Lặp qua một chuỗi

Chuỗi là một dãy ký tự, nên `for` có thể đi qua từng ký tự một:

```python
for letter in "Hanoi":
    print(letter)
```

`letter in "aeiou"` hỏi: *ký tự này có nằm trong các chữ cái kia không?* Kết quả là `True` hoặc `False`, nên dùng được trong `if`:

```python
for letter in "banana":
    if letter in "aeiou":
        print(letter, "is a vowel")
```

## 4. Mẫu tích lũy (accumulator)

Phần lớn vòng lặp tạo ra một kết quả cuối cùng. Hãy khai báo một biến **tích lũy** (accumulator) trước vòng lặp, rồi cập nhật nó bên trong:

```python
total = 0
for n in range(1, 6):
    total += n
print(total)  # 15
```

`total += n` là cách viết gọn của `total = total + n`. Mẹo này dùng được với `-=`, `*=` và các toán tử khác.

**Đếm** (counting) là cùng một mẫu, chỉ khác là bạn cộng 1 thay vì cộng một giá trị:

```python
count = 0
for n in range(1, 21):
    if n % 3 == 0:
        count += 1
print(count)  # 6 bội số của 3
```

> [!TIP]
> Luôn đặt biến tích lũy **trước** vòng lặp. Nếu viết `total = 0` bên trong vòng lặp, nó sẽ bị reset về 0 ở mỗi vòng.

## 5. Vòng lặp `while`

Dùng `for` khi biết trước số vòng. Dùng `while` khi muốn lặp **cho đến khi điều kiện sai**:

```python
n = 1
while n <= 3:
    print("round", n)
    n += 1
```

> [!WARNING]
> Bên trong `while` phải có thứ gì đó cuối cùng làm điều kiện thành sai. Quên `n += 1` thì vòng lặp không bao giờ dừng (**vòng lặp vô hạn**, infinite loop). Nếu gặp tình huống này trong editor, hãy dừng chương trình.

## 6. `break` và `continue`

- `break` thoát khỏi vòng lặp ngay lập tức.
- `continue` bỏ qua phần còn lại của vòng hiện tại và nhảy sang vòng kế tiếp.

```python
for n in range(1, 10):
    if n % 2 == 0:
        continue  # bỏ qua số chẵn
    if n > 7:
        break     # dừng hẳn
    print(n)      # 1 3 5 7
```

## Tóm tắt

- `for x in range(start, stop, step)` lặp theo dãy số; `stop` không được tính. Chuỗi cũng lặp được: `for letter in text`.
- Tích lũy: đặt `total = 0` trước vòng lặp, rồi `total += value` bên trong. Đếm thì cộng 1.
- `while condition:` lặp cho đến khi điều kiện sai, nên hãy chắc chắn nó có thể thành sai.
- `break` dừng vòng lặp; `continue` nhảy sang vòng kế tiếp.
