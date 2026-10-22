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

## 3. Bước 1: điểm trung bình

Cộng các điểm rồi chia cho số lượng. List rỗng sẽ gây chia cho 0, nên hãy xử lý trường hợp đó trước:

```python
def average(scores):
    if not scores:        # an empty list counts as "false"
        return 0.0
    return sum(scores) / len(scores)

print(average([8, 7.5, 9]))
print(average([]))
```

## 4. Bước 2: xếp loại

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

## 5. Bước 3: bảng điểm cả lớp

Duyệt qua các học sinh, tính điểm trung bình của từng người, rồi sắp xếp. Sắp xếp theo `(-avg, name)` đưa điểm cao nhất lên đầu, và nếu bằng điểm thì xếp theo tên:

```python
def average(scores):
    return sum(scores) / len(scores) if scores else 0.0

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

rows = []
for student in students:
    avg = average(student["scores"])
    rows.append((student["name"], avg))

rows.sort(key=lambda row: (-row[1], row[0]))

for name, avg in rows:
    print(f"{name}: {avg:.2f} ({letter_grade(avg)})")
```

`{avg:.2f}` định dạng số với đúng 2 chữ số thập phân. Trong bài tập, hàm của bạn trả về các dòng trong một list thay vì in ra.

## 6. Bước 4: thống kê cả lớp

Khi mỗi học sinh đã có điểm trung bình, thống kê chỉ là vài vòng lặp nữa: đếm số học sinh, lấy trung bình của các điểm trung bình, tìm người cao nhất và thấp nhất, và đếm số học sinh theo từng loại. Dict rất hợp để đếm:

```python
grades = ["B", "A", "B", "F"]
counts = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
for grade in grades:
    counts[grade] += 1
print(counts)
```

## 7. Kết quả mẫu

Với ba học sinh ở trên, bảng điểm cuối cùng trông như sau:

```text
Binh: 9.00 (A)
An: 8.17 (B)
Chi: 5.17 (D)
```

Còn `class_stats` trả về `{"count": 3, "mean": 7.44, "best": "Binh", "worst": "Chi", "grade_counts": {"A": 1, "B": 1, "C": 0, "D": 1, "F": 0}}` (mean ở đây chỉ làm tròn để hiển thị).

## 8. Đến lượt bạn

Mở hai bài tập. Bài 1 gồm Bước 1 đến 3, bài 2 là Bước 4. Viết code bên trong hàm và `return` kết quả. Hãy bấm **Check** thường xuyên: cho từng test xanh một là cách tốt để xây dựng chương trình.

## 9. Thử thách thêm

Xong sớm? Tự thử trong editor nhé:

- Cho điểm cuối cùng (bài thi) tính gấp đôi.
- Bỏ điểm thấp nhất của mỗi học sinh trước khi tính trung bình.
- In một thanh đơn giản cho mỗi học sinh, ví dụ `"#" * round(avg)`.
- Viết `top_n(students, n)` chỉ trả về tên của `n` học sinh giỏi nhất.

## Tóm tắt

- Một chương trình thật là các hàm nhỏ, mỗi hàm làm một việc và gọi lẫn nhau.
- `average` phải xử lý list rỗng; `letter_grade` kiểm tra ngưỡng từ cao xuống thấp.
- Sắp xếp với key như `(-avg, name)` cho kết quả "cao nhất trước, bằng điểm thì theo tên".
- Dict rất hợp để đếm; f-string với `:.2f` giúp định dạng số gọn gàng.
