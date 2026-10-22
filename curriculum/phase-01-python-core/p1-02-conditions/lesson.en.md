## 1. Making a decision with `if`

So far your code ran every line, top to bottom. With a **condition** you let the program choose. A condition is any expression that gives `True` or `False`, like the comparisons from lesson 1:

```python
print(5 > 3)    # True
print(5 == 3)   # False
print(5 != 3)   # True
print(4 <= 4)   # True
```

The six comparison operators are `==`, `!=`, `<`, `>`, `<=`, `>=`. Put a condition after `if` and the code under it runs **only when it is `True`**:

```python
temperature = 31

if temperature > 30:
    print("It's hot")
print("Done")
```

## 2. Indentation and the colon

Two details matter a lot:

- The line with `if` ends with a colon `:`.
- The lines that belong to the `if` are **indented** (use 4 spaces). Python uses indentation to know where the block starts and ends.

```python
age = 15

if age >= 18:
    print("Adult")
    print("You may vote")
print("This line always runs")  # not indented: outside the if
```

> [!WARNING]
> Forgetting the `:` gives `SyntaxError`. Wrong or missing indentation gives `IndentationError`. Also, `if x = 5` is wrong: use `==` to compare.

## 3. `else`: the other path

`else` runs when the condition is `False`:

```python
score = 45

if score >= 50:
    print("Pass")
else:
    print("Fail")
```

## 4. `elif`: more than two choices

Use `elif` ("else if") for extra checks. Python tests them **from top to bottom and runs only the first one that is True**:

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
> Order matters. `85 >= 90` is checked first and fails, so we move on and reach `B`. If you wrote `score >= 70` first, every score from 70 up would get `C`.

## 5. Combining conditions: `and`, `or`, `not`

| Operator | Meaning | Example |
|---|---|---|
| `and` | both must be True | `age >= 18 and has_id` |
| `or` | at least one is True | `is_weekend or is_holiday` |
| `not` | flips True/False | `not is_raining` |

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

You can also write a range check naturally: `0 <= score <= 100`.

> [!NOTE]
> When mixing, `not` is applied first, then `and`, then `or`. Add parentheses when unsure: `(a or b) and c`.

## 6. Truthiness: empty and zero are False

In an `if`, Python does not need a real `bool`. These values count as **False**: `0`, `0.0`, `""` (empty string). Almost everything else counts as **True**.

```python
name = ""

if name:
    print(f"Hello, {name}")
else:
    print("Please enter a name")

print(bool(0), bool(""), bool("0"), bool(7))  # False False True True
```

Notice `bool("0")` is `True`: it is a non-empty string, not the number zero.

## 7. Nested `if` vs `elif`

You can put an `if` inside another `if`. It works, but gets hard to read quickly:

```python
age = 16
has_id = True

if age >= 18:
    if has_id:
        print("Enter")
```

When the checks are about the same question, prefer `and`, or a flat `elif` chain:

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

## Recap

- A condition is an expression that gives `True` or `False`; compare with `== != < > <= >=`.
- `if`, `elif` and `else` end with `:`; the block under them is indented by 4 spaces.
- Python runs only the first matching branch, so order your `elif`s carefully.
- `and`, `or`, `not` combine conditions; use parentheses when unsure.
- `0`, `0.0` and `""` count as False; non-empty text and non-zero numbers count as True.
- Prefer a flat `elif` chain or `and` over deeply nested `if`s.
