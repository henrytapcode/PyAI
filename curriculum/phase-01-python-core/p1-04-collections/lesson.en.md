## 1. A list holds many values

So far a variable held one value. A **list** holds many, in order. Use square brackets:

```python
scores = [0.82, 0.91, 0.78]
names = ["Lan", "Minh", "Hoa"]
empty = []
print(scores)
print(len(names))  # how many items
```

`len()` gives the number of items. Lists can mix types, but in practice you keep one kind per list.

## 2. Indexing and slicing

Each item has a position, called an **index**, and counting starts at **0**. Negative numbers count from the end:

```python
names = ["Lan", "Minh", "Hoa", "Nam"]
print(names[0])    # Lan   (first)
print(names[2])    # Hoa
print(names[-1])   # Nam   (last)
```

A **slice** `[start:stop]` takes a piece of the list. It includes `start` but **not** `stop`:

```python
names = ["Lan", "Minh", "Hoa", "Nam"]
print(names[1:3])  # ['Minh', 'Hoa']
print(names[:2])   # ['Lan', 'Minh']  (from the beginning)
print(names[2:])   # ['Hoa', 'Nam']   (to the end)
```

> [!WARNING]
> Asking for an index that does not exist, like `names[10]`, crashes with `IndexError`. The last valid index is `len(names) - 1`.

## 3. Changing a list

Lists are **mutable**: you can change them after creating them.

```python
scores = [0.82, 0.91]
scores.append(0.78)   # add to the end
scores[0] = 0.85      # replace an item
print(scores)
print(0.91 in scores) # True: membership test with `in`
print(0.5 in scores)  # False
```

To get a sorted copy, use `sorted()`. The original list is left alone:

```python
scores = [0.82, 0.91, 0.78]
print(sorted(scores))                # [0.78, 0.82, 0.91]
print(sorted(scores, reverse=True))  # [0.91, 0.82, 0.78]
print(scores)                        # unchanged
```

## 4. Looping over a list

You already know `for`. It can walk straight through a list, no `range()` needed. Combine it with an accumulator from the last lesson:

```python
scores = [0.82, 0.91, 0.78, 0.95]

total = 0
for s in scores:
    total = total + s

print(f"Average: {round(total / len(scores), 3)}")
```

> [!TIP]
> Prefer `for item in items:` over `for i in range(len(items)):` unless you really need the position.

## 5. Dictionaries: values with labels

A list finds things by position. A **dictionary** (`dict`) finds them by a **key** you choose. Use curly braces with `key: value` pairs:

```python
student = {"name": "Lan", "score": 0.91}
print(student["name"])   # Lan
print(student["score"])  # 0.91
```

Reading a missing key with `[]` crashes with `KeyError`. `.get()` is the safe way, and takes a default:

```python
student = {"name": "Lan", "score": 0.91}
print(student.get("age"))      # None
print(student.get("age", 0))   # 0
```

Add or update an entry by assigning to a key. `in` checks keys:

```python
student = {"name": "Lan"}
student["score"] = 0.91   # add
student["score"] = 0.95   # update
print(student)
print("name" in student)  # True
```

## 6. Looping over a dict

`.items()` gives you each key and value together:

```python
grades = {"Lan": 9, "Minh": 7, "Hoa": 8}
for name, grade in grades.items():
    print(f"{name} got {grade}")

for name in grades:  # looping a dict alone gives the keys
    print(name)
```

## 7. Counting words: the seed of NLP

Natural Language Processing starts with a simple question: how often does each word appear? A dict is the perfect tool, with the word as the key and the count as the value:

```python
words = ["ai", "is", "fun", "ai", "is", "ai"]

counts = {}
for word in words:
    counts[word] = counts.get(word, 0) + 1

print(counts)  # {'ai': 3, 'is': 2, 'fun': 1}
```

`counts.get(word, 0)` means "the current count, or 0 if I have not seen this word yet". Real NLP pipelines do exactly this at a much bigger scale.

## 8. A quick word on tuples

A **tuple** is like a list that cannot be changed, written with round brackets:

```python
point = (3, 4)
print(point[0], len(point))
x, y = point  # unpack into two variables
print(x + y)
```

Use tuples for small fixed groups, such as coordinates. `point[0] = 9` would crash.

## Recap

- A list `[a, b, c]` is ordered; index from `0`, negative from the end, slice with `[start:stop]`.
- `append`, `in`, `len` and `sorted()` cover most everyday list work.
- `for item in items:` walks a list; combine it with an accumulator.
- A dict `{key: value}` looks things up by key. Use `[]` to read, `.get(key, default)` to read safely, assignment to add or update.
- `for key, value in d.items():` loops a dict. Counting with `counts.get(w, 0) + 1` is the seed of NLP.
- A tuple is a list you cannot change.
