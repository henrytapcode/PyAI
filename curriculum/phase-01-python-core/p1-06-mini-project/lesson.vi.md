## 1. Bối cảnh

Cô Lan là giáo viên. Cô lưu điểm của từng học sinh trong một list các dict của Python:

```python
students = [
    {"name": "An", "scores": [8, 7.5, 9]},
    {"name": "Binh", "scores": [9, 9.5, 8.5]},
    {"name": "Chi", "scores": [5, 6, 4.5]},
]
print(len(students), "students")
print(students[0]["name"], students[0]["scores"])
```

Cô muốn một chương trình biến dữ liệu này thành **bảng điểm**: điểm trung bình của từng học sinh, xếp loại, và vài thống kê của cả lớp. Bạn sẽ xây nó từ các hàm nhỏ, dùng mọi thứ đã học ở phase 1.

## 2. Bạn sẽ xây gì

Bốn **hàm** (function), mỗi hàm dựa trên hàm trước:

| Hàm | Đầu vào | Đầu ra |
|---|---|---|
| `average(scores)` | list các số | điểm trung bình, hoặc `0.0` nếu list rỗng |
| `letter_grade(avg)` | một số | `"A"`, `"B"`, `"C"`, `"D"` hoặc `"F"` |
| `build_report(students)` | list các dict | list các dòng chữ, học sinh giỏi nhất đứng đầu |
| `class_stats(students)` | list các dict | dict gồm số lượng, trung bình, tốt nhất, kém nhất, đếm xếp loại |

Xếp loại theo thang điểm 10:

| Điểm trung bình | Xếp loại |
|---|---|
| từ 8.5 trở lên | A |
| từ 7 trở lên | B |
| từ 5.5 trở lên | C |
| từ 4 trở lên | D |
| dưới 4 | F |

> [!TIP]
> Hàm nhỏ thì dễ kiểm thử. Khi `average` đã chạy đúng, bạn không cần nghĩ lại về nó lúc viết `build_report`.

## 3. Công cụ mới: hai mẹo nhỏ cho project này

Bạn chỉ cần hai thứ mới, và cả hai đều rất nhỏ.

**Mẹo 1: hai chữ số thập phân.** `round(x, 2)` cho ra số đã làm tròn đến 2 chữ số thập phân. F-string với `:.2f` hiển thị số với đúng 2 chữ số thập phân, kể cả khi đó là số 0:

```python
x = 8.16666
print(round(x, 2))
print(f"{x:.2f}")
print(f"{9:.2f}")
```

Dùng `round` khi bạn cần một số đã làm tròn, và `:.2f` khi bạn chỉ muốn hiển thị.

**Mẹo 2: `sorted` với `key`.** Bạn đã biết `sorted(items)`. Với `key=some_function`, Python gọi hàm của bạn trên từng phần tử và sắp xếp theo giá trị hàm trả về. Hãy viết hàm phụ bằng `def` bình thường, và truyền tên hàm **không có dấu ngoặc**:

```python
def by_length(word):
    return len(word)

words = ["pear", "fig", "banana"]
print(sorted(words, key=by_length))
```

Nếu key cần gồm hai thứ, ví dụ "điểm trung bình cao nhất trước, rồi đến tên" thì sao? Key có thể trả về một **tuple** (bộ giá trị): hai giá trị trong ngoặc tròn, như `(7.0, "An")`. Python so sánh tuple từng giá trị một. Nó xem giá trị đầu tiên trước, và chỉ khi chúng bằng nhau mới xem giá trị thứ hai:

```python
print((1, "b") < (2, "a"))
print((2, "b") < (2, "a"))
```

Để điểm cao nhất đứng đầu, hãy đổi dấu của nó: `-9.0` nhỏ hơn `-7.0`, nên 9.0 đứng trước. Tên là giá trị thứ hai, nên các điểm bằng nhau được xếp theo A đến Z:

```python
rows = [
    {"name": "Zoe", "avg": 7.0},
    {"name": "An", "avg": 9.0},
    {"name": "Bao", "avg": 7.0},
]

def sort_key(row):
    return (-row["avg"], row["name"])

for row in sorted(rows, key=sort_key):
    print(row["name"], row["avg"])
```

> [!NOTE]
> `sorted` trả về một list mới và không thay đổi list gốc.

## 4. Bước 1: điểm trung bình

Cộng các điểm rồi chia cho số lượng. List rỗng sẽ gây chia cho 0, nên hãy xử lý trường hợp đó trước:

```python
def average(scores):
    if not scores:        # an empty list counts as "false"
        return 0.0
    return sum(scores) / len(scores)

print(average([8, 7.5, 9]))
print(average([]))
```

## 5. Bước 2: xếp loại

Kiểm tra từ ngưỡng cao nhất xuống thấp. Điều kiện nào đúng trước thì thắng, nên mỗi `if` chỉ cần một phép so sánh:

```python
def letter_grade(avg):
    if avg >= 8.5:
        return "A"
    if avg >= 7:
        return "B"
    if avg >= 5.5:
        return "C"
    if avg >= 4:
        return "D"
    return "F"

print(letter_grade(8.5), letter_grade(7.2), letter_grade(3.9))
```

> [!WARNING]
> Chú ý các điểm biên: đúng `8.5` là `A`, đúng `7` là `B`. Dùng `>=`, không dùng `>`.

## 6. Bước 3: bảng điểm cả lớp

Duyệt qua các học sinh, tính điểm trung bình của từng người, rồi sắp xếp theo ý tưởng `sort_key` ở phần mẹo. Key `(-avg, name)` đưa điểm cao nhất lên đầu, và nếu bằng điểm thì xếp theo tên:

```python
def average(scores):
    if not scores:
        return 0.0
    return sum(scores) / len(scores)

def letter_grade(avg):
    if avg >= 8.5:
        return "A"
    if avg >= 7:
        return "B"
    if avg >= 5.5:
        return "C"
    if avg >= 4:
        return "D"
    return "F"

students = [
    {"name": "An", "scores": [8, 7.5, 9]},
    {"name": "Binh", "scores": [9, 9.5, 8.5]},
]

def sort_key(row):
    return (-row["avg"], row["name"])

rows = []
for student in students:
    avg = average(student["scores"])
    rows.append({"name": student["name"], "avg": avg})

for row in sorted(rows, key=sort_key):
    print(f"{row['name']}: {row['avg']:.2f} ({letter_grade(row['avg'])})")
```

Mỗi dòng là một dict nhỏ, nên `sort_key` đọc được `row["avg"]` và `row["name"]`. Trong bài tập, hàm của bạn trả về các dòng trong một list thay vì in ra.

## 7. Bước 4: thống kê cả lớp

Khi mỗi học sinh đã có điểm trung bình, thống kê chỉ là vài vòng lặp nữa: đếm số học sinh, lấy trung bình của các điểm trung bình, tìm người cao nhất và thấp nhất bằng vòng lặp (giữ người tốt nhất cho đến lúc này và thay thế khi gặp điểm trung bình cao hơn; nếu bằng điểm thì giữ tên đứng trước theo bảng chữ cái), và đếm số học sinh theo từng loại. Dict rất hợp để đếm:

```python
grades = ["B", "A", "B", "F"]
counts = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
for grade in grades:
    counts[grade] += 1
print(counts)
```

## 8. Kết quả mẫu

Với ba học sinh ở trên, bảng điểm cuối cùng trông như sau:

```text
Binh: 9.00 (A)
An: 8.17 (B)
Chi: 5.17 (D)
```

Còn `class_stats` trả về `{"count": 3, "mean": 7.44, "best": "Binh", "worst": "Chi", "grade_counts": {"A": 1, "B": 1, "C": 0, "D": 1, "F": 0}}` (mean ở đây chỉ làm tròn để hiển thị).

## 9. Đến lượt bạn

Mở hai bài tập. Bài 1 gồm Bước 1 đến 3, bài 2 là Bước 4. Viết code bên trong hàm và `return` kết quả. Hãy bấm **Kiểm tra** thường xuyên: cho từng test xanh một là cách tốt để xây dựng chương trình.

## 10. Thử thách thêm

Xong sớm? Tự thử trong editor nhé:

- Cho điểm cuối cùng (bài thi) tính gấp đôi.
- Bỏ điểm thấp nhất của mỗi học sinh trước khi tính trung bình.
- In một thanh đơn giản cho mỗi học sinh, ví dụ `"#" * round(avg)`.
- Viết `top_n(students, n)` chỉ trả về tên của `n` học sinh giỏi nhất.

## Tóm tắt

- Một chương trình thật là các hàm nhỏ, mỗi hàm làm một việc và gọi lẫn nhau.
- `average` phải xử lý list rỗng; `letter_grade` kiểm tra ngưỡng từ cao xuống thấp.
- `sorted(items, key=helper)` sắp xếp theo giá trị mà hàm phụ `def` trả về; key tuple như `(-avg, name)` cho kết quả "cao nhất trước, bằng điểm thì theo tên".
- `round(x, 2)` làm tròn số; `f"{x:.2f}"` hiển thị đúng 2 chữ số thập phân.
- Dict rất hợp để đếm.
