## 1. List chứa nhiều giá trị

Đến giờ mỗi biến chỉ giữ một giá trị. **List** (danh sách) giữ nhiều giá trị theo thứ tự. Dùng dấu ngoặc vuông:

```python
scores = [0.82, 0.91, 0.78]
names = ["Lan", "Minh", "Hoa"]
empty = []
print(scores)
print(len(names))  # có bao nhiêu phần tử
```

`len()` cho biết số phần tử. List có thể trộn nhiều kiểu, nhưng thực tế mỗi list thường chỉ chứa một loại.

## 2. Chỉ số và slice

Mỗi phần tử có một vị trí gọi là **chỉ số** (index), và đếm bắt đầu từ **0**. Số âm đếm từ cuối lên:

```python
names = ["Lan", "Minh", "Hoa", "Nam"]
print(names[0])    # Lan   (đầu tiên)
print(names[2])    # Hoa
print(names[-1])   # Nam   (cuối cùng)
```

**Slice** (lát cắt) `[start:stop]` lấy một đoạn của list. Nó lấy `start` nhưng **không** lấy `stop`:

```python
names = ["Lan", "Minh", "Hoa", "Nam"]
print(names[1:3])  # ['Minh', 'Hoa']
print(names[:2])   # ['Lan', 'Minh']  (từ đầu)
print(names[2:])   # ['Hoa', 'Nam']   (đến cuối)
```

> [!WARNING]
> Truy cập chỉ số không tồn tại, như `names[10]`, sẽ báo lỗi `IndexError`. Chỉ số hợp lệ cuối cùng là `len(names) - 1`.

## 3. Thay đổi list

List là **mutable** (có thể sửa): bạn thay đổi được nó sau khi tạo.

```python
scores = [0.82, 0.91]
scores.append(0.78)   # thêm vào cuối
scores[0] = 0.85      # thay một phần tử
print(scores)
print(0.91 in scores) # True: kiểm tra có mặt bằng `in`
print(0.5 in scores)  # False
```

Muốn có bản đã sắp xếp, dùng `sorted()`. List gốc không bị đổi:

```python
scores = [0.82, 0.91, 0.78]
print(sorted(scores))                # [0.78, 0.82, 0.91]
print(sorted(scores, reverse=True))  # [0.91, 0.82, 0.78]
print(scores)                        # không đổi
```

## 4. Lặp qua list

Bạn đã biết `for`. Nó đi thẳng qua từng phần tử của list, không cần `range()`. Kết hợp với biến tích lũy (accumulator) của bài trước:

```python
scores = [0.82, 0.91, 0.78, 0.95]

total = 0
for s in scores:
    total = total + s

print(f"Average: {round(total / len(scores), 3)}")
```

> [!TIP]
> Ưu tiên `for item in items:` hơn `for i in range(len(items)):`, trừ khi bạn thật sự cần vị trí.

## 5. Dictionary: giá trị có nhãn

List tìm phần tử theo vị trí. **Dictionary** (`dict`, từ điển) tìm theo một **key** (khóa) do bạn chọn. Dùng ngoặc nhọn với các cặp `key: value`:

```python
student = {"name": "Lan", "score": 0.91}
print(student["name"])   # Lan
print(student["score"])  # 0.91
```

Đọc key không tồn tại bằng `[]` sẽ báo lỗi `KeyError`. `.get()` an toàn hơn và nhận giá trị mặc định:

```python
student = {"name": "Lan", "score": 0.91}
print(student.get("age"))      # None
print(student.get("age", 0))   # 0
```

Thêm hoặc cập nhật bằng cách gán vào một key. `in` kiểm tra key:

```python
student = {"name": "Lan"}
student["score"] = 0.91   # thêm
student["score"] = 0.95   # cập nhật
print(student)
print("name" in student)  # True
```

## 6. Lặp qua dict

`.items()` đưa cho bạn cả key và value cùng lúc:

```python
grades = {"Lan": 9, "Minh": 7, "Hoa": 8}
for name, grade in grades.items():
    print(f"{name} got {grade}")

for name in grades:  # lặp dict trực tiếp chỉ cho ra các key
    print(name)
```

## 7. Đếm từ: hạt giống của NLP

Xử lý ngôn ngữ tự nhiên (NLP) bắt đầu từ một câu hỏi đơn giản: mỗi từ xuất hiện bao nhiêu lần? Dict rất hợp: từ là key, số lần là value:

```python
words = ["ai", "is", "fun", "ai", "is", "ai"]

counts = {}
for word in words:
    counts[word] = counts.get(word, 0) + 1

print(counts)  # {'ai': 3, 'is': 2, 'fun': 1}
```

`counts.get(word, 0)` nghĩa là "số đếm hiện tại, hoặc 0 nếu chưa thấy từ này". Các pipeline NLP thật làm đúng việc này ở quy mô lớn hơn nhiều.

## 8. Nhắc nhanh về tuple

**Tuple** giống list nhưng không thể sửa, viết bằng ngoặc tròn:

```python
point = (3, 4)
print(point[0], len(point))
x, y = point  # tách ra thành hai biến
print(x + y)
```

Dùng tuple cho nhóm nhỏ cố định, ví dụ tọa độ. `point[0] = 9` sẽ báo lỗi.

## Tóm tắt

- List `[a, b, c]` có thứ tự; chỉ số bắt đầu từ `0`, số âm đếm từ cuối, cắt bằng `[start:stop]`.
- `append`, `in`, `len` và `sorted()` đủ cho phần lớn việc hằng ngày với list.
- `for item in items:` duyệt list; kết hợp với accumulator.
- Dict `{key: value}` tra cứu theo key. Dùng `[]` để đọc, `.get(key, default)` để đọc an toàn, gán để thêm hoặc cập nhật.
- `for key, value in d.items():` lặp qua dict. Đếm bằng `counts.get(w, 0) + 1` là hạt giống của NLP.
- Tuple là list không thể sửa.
