Almost nothing in AI is a single value. A batch of messages to send to a model is a **list**. The JSON a chat API sends back is a **dictionary**: labelled fields such as `"model"`, `"text"` and `"tokens"`. Lists and dictionaries are how Python keeps many values together, and you will use them in every lesson from now on.

## 1. A list holds many values in order

Think of a **list** as a row of numbered lockers. Each locker holds one value, and the lockers stay in the order you put things in. Use square brackets:

```python
scores = [0.82, 0.91, 0.78]
names = ["Lan", "Minh", "Hoa"]
empty = []
print(scores)       # [0.82, 0.91, 0.78]
print(len(names))   # 3
```

`len()` is a built-in function that tells you how many items something holds. Notice that `empty` is a valid list with zero items, so `len(empty)` is `0`.

## 2. Indexing: finding an item by position

Each item has a position, called its **index**. Counting starts at **0**, not 1. Negative numbers count from the end:

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

`names[0]` is the first item and `names[-1]` is the last one. The last valid positive index is always `len(names) - 1`.

## 3. Slicing: taking a piece

A **slice** `[start:stop]` copies a piece of the list. It includes `start` but stops **before** `stop`. The easiest way to see this is to number the *gaps* between items:

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

| Slice | Meaning |
|---|---|
| `names[1:3]` | from gap 1 to gap 3 |
| `names[:2]` | from the beginning to gap 2 (the first two items) |
| `names[2:]` | from gap 2 to the end |
| `names[-2:]` | the last two items |

> [!TIP]
> `items[:n]` always means "the first `n` items". If the list is shorter than `n`, you just get the whole list. A slice never crashes.

## 4. Changing a list

Lists are **mutable**: you can change them after creating them.

```python
scores = [0.82, 0.91]
scores.append(0.78)    # add to the end
scores[0] = 0.85       # replace the item at index 0
print(scores)          # [0.85, 0.91, 0.78]
print(0.91 in scores)  # True
print(0.5 in scores)   # False
```

`.append(x)` adds `x` at the end, assigning to `scores[0]` replaces one item, and `in` asks "is this value somewhere in the list?" and answers with a `bool`.

Notice the dot in `scores.append(...)`. `.append` is a **method**: a function that belongs to a value and is called with a dot after the value.

One trap: `b = a` does **not** copy a list. It gives the same list a second name, so a change through one name shows up in the other. A slice with no start and no stop, `a[:]`, makes a real copy:

```python
a = [1, 2]
b = a           # b is NOT a copy: it is a second name for the same list
b.append(3)
print(a)        # [1, 2, 3]  (a changed too!)

c = a[:]        # a[:] makes a real copy
c.append(4)
print(a)        # [1, 2, 3]
print(c)        # [1, 2, 3, 4]
```

## 5. Sorting and looping

`sorted()` gives you a new, sorted list and leaves the original alone:

```python
scores = [0.82, 0.91, 0.78]
print(sorted(scores))                # [0.78, 0.82, 0.91]
print(sorted(scores, reverse=True))  # [0.91, 0.82, 0.78]
print(scores)                        # [0.82, 0.91, 0.78]
print(sorted(["Minh", "Lan"]))        # ['Lan', 'Minh']
```

You already know `for`. It can walk straight through a list, with no `range()` needed. Combine it with the accumulator pattern from the last lesson:

```python
scores = [0.82, 0.91, 0.78, 0.95]

total = 0
for s in scores:
    total = total + s

average = total / len(scores)
print(f"Average: {round(average, 3)}")  # Average: 0.865
```

`round(x, 3)` rounds a number to 3 decimal places. Python also has shortcuts for common jobs: `sum(scores)` adds all the numbers, `max(scores)` finds the biggest and `min(scores)` the smallest.

```python
scores = [0.82, 0.91, 0.78, 0.95]
print(max(scores), min(scores))  # 0.95 0.78
```

> [!TIP]
> Prefer `for item in items:` over `for i in range(len(items)):` unless you really need the position.

## 6. Dictionaries: values with labels

A list finds things by position. A **dictionary** (`dict`) finds them by a **key** that you choose, like looking up a word in a real dictionary. Each entry is a `key: value` pair, written inside curly braces:

```python
student = {"name": "Lan", "score": 0.91}
print(student["name"])   # Lan
print(student["score"])  # 0.91
```

| key | value |
|---|---|
| `"name"` | `"Lan"` |
| `"score"` | `0.91` |

Reading a key that does not exist with `[]` crashes with `KeyError`. `.get()` is the safe way, and it takes an optional default:

```python
student = {"name": "Lan", "score": 0.91}
print(student.get("age"))      # None
print(student.get("age", 0))   # 0
```

Add or update an entry by assigning to a key. The word `in` checks the **keys**:

```python
student = {"name": "Lan"}
student["score"] = 0.91   # add a new key
student["score"] = 0.95   # update an existing key
print(student)            # {'name': 'Lan', 'score': 0.95}
print("name" in student)  # True
```

## 7. Looping over a dictionary

`.items()` hands you each key and its value together:

```python
grades = {"Lan": 9, "Minh": 7, "Hoa": 8}
for name, grade in grades.items():
    print(f"{name} got {grade}")  # Lan got 9, then Minh got 7, then Hoa got 8

for name in grades:  # looping over a dict alone gives the keys
    print(name)      # Lan, then Minh, then Hoa
```

## 8. Counting words: the seed of NLP

Natural Language Processing (NLP) starts with a simple question: how often does each word appear? A dict is the perfect tool, with the word as the key and the count as the value:

```python
words = ["ai", "is", "fun", "ai", "is", "ai"]

counts = {}
for word in words:
    counts[word] = counts.get(word, 0) + 1

print(counts)  # {'ai': 3, 'is': 2, 'fun': 1}
```

`counts.get(word, 0)` means "the current count, or 0 if I have not seen this word yet". Then we add 1 and store it back. Press **Visualize** on this block and watch `counts` grow one word at a time. Real NLP pipelines do exactly this at a much bigger scale.

## 9. Tuples: small fixed groups

A **tuple** is like a list that cannot be changed after you create it. Write it with round brackets. It is ideal for one small record, such as a name and a score:

```python
pair = ("Lan", 9)
print(pair[0], len(pair))        # Lan 2
name, score = pair               # unpacking: one variable per item
print(f"{name} scored {score}")  # Lan scored 9
```

You have already met tuples without knowing it: `grades.items()` gives you `(key, value)` pairs, and `for name, grade in ...` unpacks each pair. Trying `pair[0] = "Minh"` crashes with `TypeError`, because tuples cannot be changed.

## 10. List or dict?

| Use a... | when... | Example |
|---|---|---|
| list | order matters, or you have many similar items | the scores of 100 test cases |
| dict | each value has a name, or you look things up by key | one student: name, score, age |
| tuple | a small fixed record that should not change | `(latitude, longitude)` |

## 11. Common mistakes

**Using `len(items)` as an index.** A list of 3 items has indexes `0, 1, 2`, so `items[len(items)]` crashes with `IndexError: list index out of range`. The last item is `items[len(items) - 1]`, or simply `items[-1]`:

```python
items = ["a", "b", "c"]
print(items[len(items) - 1])  # c
print(items[-1])              # c
```

**Reading a missing key with `[]`.** `student["age"]` crashes with `KeyError: 'age'` when the key is missing. Use `.get()` when the key might not exist:

```python
student = {"name": "Lan"}
print(student.get("age", "unknown"))  # unknown
```

**Changing a list while looping over it.** Adding or removing items of a list inside `for item in that_list:` makes Python skip items or loop forever. Here we try to remove every number (`.remove(x)` deletes the first `x` it finds), but the loop skips some:

```python
numbers = [2, 4, 6, 8]
for n in numbers:
    numbers.remove(n)
print(numbers)  # [4, 8]  (expected [])
```

Build a **new** list instead of editing the one you loop over:

```python
numbers = [1, 2, 3, 4, 5, 6]
odds = []
for n in numbers:
    if n % 2 == 1:
        odds.append(n)
print(odds)  # [1, 3, 5]
```

**Expecting `list.sort()` to return the list.** `.sort()` sorts the list in place and returns `None`:

```python
scores = [0.82, 0.91, 0.78]
result = scores.sort()
print(result)  # None
print(scores)  # [0.78, 0.82, 0.91]
```

> [!WARNING]
> If you want a sorted result, write `result = sorted(scores)`. Writing `scores = scores.sort()` throws your list away and leaves `None`.

## Recap

- A list `[a, b, c]` is ordered. Index from `0`, negative from the end, slice with `[start:stop]` (stop is not included).
- `len`, `append`, `in`, `sorted`, `sum`, `max` and `min` cover most everyday list work.
- `for item in items:` walks a list; combine it with an accumulator.
- A dict `{key: value}` looks things up by key: `[]` to read, `.get(key, default)` to read safely, assignment to add or update.
- `for key, value in d.items():` loops a dict. Counting with `counts.get(w, 0) + 1` is the seed of NLP.
- A tuple `(a, b)` is a small fixed group; unpack it with `a, b = pair`.
