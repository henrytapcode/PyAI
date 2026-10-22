## 1. The scenario

Ms. Lan is a teacher. She keeps each student's scores in a Python list of dicts:

```python
students = [
    {"name": "An", "scores": [8, 7.5, 9]},
    {"name": "Binh", "scores": [9, 9.5, 8.5]},
    {"name": "Chi", "scores": [5, 6, 4.5]},
]
print(len(students), "students")
print(students[0]["name"], students[0]["scores"])
```

She wants a program that turns this data into a **grade report**: each student's average, a letter grade, and some class statistics. You will build it from small functions, using everything from phase 1.

## 2. What you will build

Four functions, each one building on the previous:

| Function | Input | Output |
|---|---|---|
| `average(scores)` | list of numbers | the mean, or `0.0` for an empty list |
| `letter_grade(avg)` | a number | `"A"`, `"B"`, `"C"`, `"D"` or `"F"` |
| `build_report(students)` | list of dicts | list of text lines, best student first |
| `class_stats(students)` | list of dicts | a dict with count, mean, best, worst, grade counts |

Grades use a 10-point scale:

| Average | Grade |
|---|---|
| 8.5 and above | A |
| 7 and above | B |
| 5.5 and above | C |
| 4 and above | D |
| below 4 | F |

> [!TIP]
> Small functions are easier to test. Once `average` works, you never have to think about it again while writing `build_report`.

## 3. New tool: two small tricks for this project

You only need two new things, and both are tiny.

**Trick 1: two decimals.** `round(x, 2)` gives a number rounded to 2 decimals. An f-string with `:.2f` shows a number with exactly 2 decimals, even when they are zeros:

```python
x = 8.16666
print(round(x, 2))
print(f"{x:.2f}")
print(f"{9:.2f}")
```

Use `round` when you need a rounded number, and `:.2f` when you only want to display it.

**Trick 2: `sorted` with a `key`.** You already know `sorted(items)`. With `key=some_function`, Python calls your function on each item and sorts by what it returns. Write the helper with a normal `def`, and pass its name **without parentheses**:

```python
def by_length(word):
    return len(word)

words = ["pear", "fig", "banana"]
print(sorted(words, key=by_length))
```

What if the key should be two things, such as "highest average first, then name"? A key can return a **tuple**: two values in parentheses, like `(7.0, "An")`. Python compares tuples one value at a time. It looks at the first values, and only if they are equal does it look at the second ones:

```python
print((1, "b") < (2, "a"))
print((2, "b") < (2, "a"))
```

To put the highest average first, flip its sign: `-9.0` is smaller than `-7.0`, so 9.0 comes first. Names are the second value, so equal averages are ordered A to Z:

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
> `sorted` returns a new list and leaves the original alone.

## 4. Step 1: the average

Add the scores up and divide by how many there are. An empty list would mean dividing by zero, so handle it first:

```python
def average(scores):
    if not scores:        # an empty list counts as "false"
        return 0.0
    return sum(scores) / len(scores)

print(average([8, 7.5, 9]))
print(average([]))
```

## 5. Step 2: the letter grade

Check from the highest threshold down. The first condition that is true wins, so each `if` needs only one comparison:

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
> Boundaries matter: exactly `8.5` is an `A`, exactly `7` is a `B`. Use `>=`, not `>`.

## 6. Step 3: the class report

Loop over the students, compute each average, then sort with the `sort_key` idea from the tricks section. The key `(-avg, name)` puts the highest average first and breaks ties alphabetically:

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

Each row is a small dict, so `sort_key` can read `row["avg"]` and `row["name"]`. In the exercise, your function returns the lines in a list instead of printing them.

## 7. Step 4: class statistics

Once every student has an average, statistics are a few more loops: count the students, take the mean of the averages, find the best and worst with a loop (keep the best so far and replace it when you see a higher average; on a tie keep the name that comes first alphabetically), and count how many students got each letter. A dict is perfect for the counts:

```python
grades = ["B", "A", "B", "F"]
counts = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
for grade in grades:
    counts[grade] += 1
print(counts)
```

## 8. Sample output

For the three students above, the final report looks like this:

```text
Binh: 9.00 (A)
An: 8.17 (B)
Chi: 5.17 (D)
```

And `class_stats` gives `{"count": 3, "mean": 7.44, "best": "Binh", "worst": "Chi", "grade_counts": {"A": 1, "B": 1, "C": 0, "D": 1, "F": 0}}` (the mean is rounded here for display only).

## 9. Your turn

Open the two exercises. Exercise 1 covers Steps 1 to 3, exercise 2 covers Step 4. Write your code inside the functions and `return` the answer. Press **Check** often: getting one test green at a time is a great way to build a program.

## 10. Stretch goals

Done early? Try these on your own in the editor:

- Make the last score (the exam) count double.
- Drop the lowest score of each student before averaging.
- Print a simple bar for each student, e.g. `"#" * round(avg)`.
- Write `top_n(students, n)` that returns only the names of the best `n` students.

## Recap

- A real program is small functions that each do one job and call each other.
- `average` guards against the empty list; `letter_grade` checks thresholds from high to low.
- `sorted(items, key=helper)` sorts by what a `def` helper returns; a tuple key like `(-avg, name)` gives "highest first, ties by name".
- `round(x, 2)` rounds a number; `f"{x:.2f}"` shows exactly 2 decimals.
- Dicts are great for counting.
