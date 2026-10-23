Hầu như không có thứ gì trong AI chỉ là một giá trị đơn lẻ. Một loạt tin nhắn cần gửi cho mô hình là một **list** (danh sách). JSON mà API chat trả về là một **dictionary** (từ điển): các trường có nhãn như `"model"`, `"text"` và `"tokens"`. List và dictionary là cách Python gom nhiều giá trị lại với nhau, và từ giờ bài nào bạn cũng sẽ dùng đến chúng.

## 1. List chứa nhiều giá trị theo thứ tự

Hãy hình dung **list** như một dãy tủ khóa được đánh số. Mỗi ngăn tủ chứa một giá trị, và các ngăn giữ nguyên thứ tự bạn bỏ đồ vào. Dùng dấu ngoặc vuông:

```python
scores = [0.82, 0.91, 0.78]
names = ["Lan", "Minh", "Hoa"]
empty = []
print(scores)       # [0.82, 0.91, 0.78]
print(len(names))   # 3
```

`len()` là một hàm có sẵn (built-in) cho biết một thứ đang chứa bao nhiêu phần tử. Lưu ý `empty` là một list hợp lệ với 0 phần tử, nên `len(empty)` là `0`.

## 2. Indexing: tìm phần tử theo vị trí

Mỗi phần tử có một vị trí gọi là **index** (chỉ số). Đếm bắt đầu từ **0**, không phải 1. Số âm đếm từ cuối lên:

```text
index:      0       1        2       3
          ["Lan",  "Minh",  "Hoa",  "Nam"]
index:     -4      -3       -2      -1
```

```python
names = ["Lan", "Minh", "Hoa", "Nam"]
print(names[0])    # Lan
print(names[2])    # Hoa
print(names[-1])   # Nam
```

`names[0]` là phần tử đầu và `names[-1]` là phần tử cuối. Index dương hợp lệ lớn nhất luôn là `len(names) - 1`.

## 3. Slicing: cắt lấy một đoạn

Một **slice** (lát cắt) `[start:stop]` sao chép một đoạn của list. Nó lấy từ `start` nhưng dừng **trước** `stop`. Cách dễ nhất để hình dung là đánh số các *khe* (gap) giữa các phần tử:

```text
gap:    0       1        2       3       4
        | "Lan" | "Minh" | "Hoa" | "Nam" |
                ^----------------^
                names[1:3]
```

```python
names = ["Lan", "Minh", "Hoa", "Nam"]
print(names[1:3])  # ['Minh', 'Hoa']
print(names[:2])   # ['Lan', 'Minh']
print(names[2:])   # ['Hoa', 'Nam']
print(names[-2:])  # ['Hoa', 'Nam']
```

| Slice | Ý nghĩa |
|---|---|
| `names[1:3]` | từ khe 1 đến khe 3 |
| `names[:2]` | từ đầu đến khe 2 (hai phần tử đầu) |
| `names[2:]` | từ khe 2 đến hết |
| `names[-2:]` | hai phần tử cuối |

> [!TIP]
> `items[:n]` luôn có nghĩa là "`n` phần tử đầu tiên". Nếu list ngắn hơn `n`, bạn chỉ nhận lại cả list. Slice không bao giờ gây lỗi.

## 4. Thay đổi list

List là **mutable** (có thể thay đổi): bạn sửa được nó sau khi đã tạo.

```python
scores = [0.82, 0.91]
scores.append(0.78)    # thêm vào cuối
scores[0] = 0.85       # thay phần tử ở index 0
print(scores)          # [0.85, 0.91, 0.78]
print(0.91 in scores)  # True
print(0.5 in scores)   # False
```

`.append(x)` thêm `x` vào cuối, gán vào `scores[0]` thay một phần tử, còn `in` hỏi "giá trị này có nằm đâu đó trong list không?" và trả lời bằng một `bool`.

Hãy để ý dấu chấm trong `scores.append(...)`. `.append` là một **method** (phương thức): một hàm thuộc về một giá trị và được gọi bằng dấu chấm đặt sau giá trị đó.

Một cái bẫy: `b = a` **không** sao chép list. Nó chỉ đặt cho cùng một list một cái tên thứ hai, nên đổi qua tên này thì tên kia cũng thấy. Một slice không có start và không có stop, `a[:]`, mới tạo bản sao thật sự:

```python
a = [1, 2]
b = a           # b KHÔNG phải bản sao: nó là tên thứ hai của cùng một list
b.append(3)
print(a)        # [1, 2, 3]  (a cũng bị đổi!)

c = a[:]        # a[:] tạo một bản sao thật sự
c.append(4)
print(a)        # [1, 2, 3]
print(c)        # [1, 2, 3, 4]
```

## 5. Sắp xếp và lặp

`sorted()` trả về một list mới đã sắp xếp và giữ nguyên list gốc:

```python
scores = [0.82, 0.91, 0.78]
print(sorted(scores))                # [0.78, 0.82, 0.91]
print(sorted(scores, reverse=True))  # [0.91, 0.82, 0.78]
print(scores)                        # [0.82, 0.91, 0.78]
print(sorted(["Minh", "Lan"]))        # ['Lan', 'Minh']
```

Bạn đã biết `for`. Nó đi thẳng qua từng phần tử của list, không cần `range()`. Hãy kết hợp với mẫu accumulator (biến tích lũy) ở bài trước:

```python
scores = [0.82, 0.91, 0.78, 0.95]

total = 0
for s in scores:
    total = total + s

average = total / len(scores)
print(f"Average: {round(average, 3)}")  # Average: 0.865
```

`round(x, 3)` làm tròn một số tới 3 chữ số thập phân. Python cũng có sẵn đường tắt cho những việc hay gặp: `sum(scores)` cộng tất cả các số, `max(scores)` tìm số lớn nhất và `min(scores)` tìm số nhỏ nhất.

```python
scores = [0.82, 0.91, 0.78, 0.95]
print(max(scores), min(scores))  # 0.95 0.78
```

> [!TIP]
> Nên dùng `for item in items:` thay vì `for i in range(len(items)):`, trừ khi bạn thật sự cần vị trí.

## 6. Dictionary: giá trị có nhãn

List tìm đồ theo vị trí. **Dictionary** (`dict`) tìm đồ theo một **key** (khóa) do bạn tự chọn, giống như tra một từ trong từ điển thật. Mỗi mục là một cặp `key: value`, viết trong dấu ngoặc nhọn:

```python
student = {"name": "Lan", "score": 0.91}
print(student["name"])   # Lan
print(student["score"])  # 0.91
```

| key | value |
|---|---|
| `"name"` | `"Lan"` |
| `"score"` | `0.91` |

Đọc một key không tồn tại bằng `[]` sẽ gây lỗi `KeyError`. `.get()` là cách đọc an toàn, và nhận thêm một giá trị mặc định (default):

```python
student = {"name": "Lan", "score": 0.91}
print(student.get("age"))      # None
print(student.get("age", 0))   # 0
```

Thêm hoặc cập nhật một mục bằng cách gán vào key. Từ khóa `in` kiểm tra **key**:

```python
student = {"name": "Lan"}
student["score"] = 0.91   # thêm key mới
student["score"] = 0.95   # cập nhật key đã có
print(student)            # {'name': 'Lan', 'score': 0.95}
print("name" in student)  # True
```

## 7. Lặp qua dictionary

`.items()` đưa cho bạn từng key cùng với value của nó:

```python
grades = {"Lan": 9, "Minh": 7, "Hoa": 8}
for name, grade in grades.items():
    print(f"{name} got {grade}")  # Lan got 9, rồi Minh got 7, rồi Hoa got 8

for name in grades:  # lặp trực tiếp qua dict thì nhận được các key
    print(name)      # Lan, rồi Minh, rồi Hoa
```

## 8. Đếm từ: hạt giống của NLP

Xử lý ngôn ngữ tự nhiên (NLP, Natural Language Processing) bắt đầu từ một câu hỏi đơn giản: mỗi từ xuất hiện bao nhiêu lần? Dict là công cụ hoàn hảo, với từ là key và số lần đếm là value:

```python
words = ["ai", "is", "fun", "ai", "is", "ai"]

counts = {}
for word in words:
    counts[word] = counts.get(word, 0) + 1

print(counts)  # {'ai': 3, 'is': 2, 'fun': 1}
```

`counts.get(word, 0)` nghĩa là "số đếm hiện tại, hoặc 0 nếu mình chưa gặp từ này". Sau đó ta cộng 1 và lưu lại. Bấm **Visualize** ở khối code này để xem `counts` lớn dần từng từ một. Các pipeline NLP thật làm đúng việc này, chỉ là ở quy mô lớn hơn nhiều.

## 9. Tuple: nhóm nhỏ cố định

**Tuple** giống như một list mà bạn không thể thay đổi sau khi tạo. Viết nó trong dấu ngoặc tròn. Tuple rất hợp để chứa một bản ghi nhỏ, ví dụ một cái tên và một điểm số:

```python
pair = ("Lan", 9)
print(pair[0], len(pair))        # Lan 2
name, score = pair               # unpacking (tách ra): mỗi phần tử một biến
print(f"{name} scored {score}")  # Lan scored 9
```

Thật ra bạn đã gặp tuple mà không biết: `grades.items()` cho bạn các cặp `(key, value)`, và `for name, grade in ...` tách từng cặp ra. Thử `pair[0] = "Minh"` sẽ gây lỗi `TypeError`, vì tuple không thay đổi được.

## 10. List hay dict?

| Dùng... | khi... | Ví dụ |
|---|---|---|
| list | thứ tự quan trọng, hoặc có nhiều phần tử cùng loại | điểm của 100 test case |
| dict | mỗi giá trị có một cái tên, hoặc bạn tra cứu theo key | một học viên: tên, điểm, tuổi |
| tuple | một bản ghi nhỏ cố định, không nên bị đổi | `(latitude, longitude)` |

## 11. Lỗi thường gặp

**Dùng `len(items)` làm index.** List có 3 phần tử thì có index `0, 1, 2`, nên `items[len(items)]` gây lỗi `IndexError: list index out of range`. Phần tử cuối là `items[len(items) - 1]`, hoặc đơn giản là `items[-1]`:

```python
items = ["a", "b", "c"]
print(items[len(items) - 1])  # c
print(items[-1])              # c
```

**Đọc key không tồn tại bằng `[]`.** `student["age"]` gây lỗi `KeyError: 'age'` khi thiếu key. Hãy dùng `.get()` khi key có thể không tồn tại:

```python
student = {"name": "Lan"}
print(student.get("age", "unknown"))  # unknown
```

**Thay đổi list trong lúc đang lặp qua nó.** Thêm hoặc xóa phần tử của list bên trong `for item in that_list:` sẽ làm Python bỏ sót phần tử hoặc lặp mãi. Ở đây ta thử xóa mọi số (`.remove(x)` xóa phần tử `x` đầu tiên nó tìm thấy), nhưng vòng lặp bỏ sót vài số:

```python
numbers = [2, 4, 6, 8]
for n in numbers:
    numbers.remove(n)
print(numbers)  # [4, 8]  (đáng lẽ phải là [])
```

Hãy tạo một list **mới** thay vì sửa list đang lặp qua:

```python
numbers = [1, 2, 3, 4, 5, 6]
odds = []
for n in numbers:
    if n % 2 == 1:
        odds.append(n)
print(odds)  # [1, 3, 5]
```

**Mong `list.sort()` trả về list.** `.sort()` sắp xếp ngay trên list gốc và trả về `None`:

```python
scores = [0.82, 0.91, 0.78]
result = scores.sort()
print(result)  # None
print(scores)  # [0.78, 0.82, 0.91]
```

> [!WARNING]
> Nếu muốn có kết quả đã sắp xếp, hãy viết `result = sorted(scores)`. Viết `scores = scores.sort()` sẽ làm mất list của bạn và chỉ còn `None`.

## Tóm tắt

- List `[a, b, c]` có thứ tự. Index bắt đầu từ `0`, số âm đếm từ cuối, slice bằng `[start:stop]` (không lấy `stop`).
- `len`, `append`, `in`, `sorted`, `sum`, `max` và `min` đủ cho phần lớn việc thường ngày với list.
- `for item in items:` đi qua từng phần tử; kết hợp với accumulator.
- Dict `{key: value}` tra cứu theo key: dùng `[]` để đọc, `.get(key, default)` để đọc an toàn, gán để thêm hoặc cập nhật.
- `for key, value in d.items():` lặp qua dict. Đếm bằng `counts.get(w, 0) + 1` là hạt giống của NLP.
- Tuple `(a, b)` là một nhóm nhỏ cố định; tách ra bằng `a, b = pair`.
