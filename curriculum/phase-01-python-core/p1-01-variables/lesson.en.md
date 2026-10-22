## 1. A variable is a name for a value

A **variable** is a label you stick on a value so you can use it later. You create one with `=`:

```python
city = "Hanoi"
population = 8_500_000
print(city, population)
```

Read `=` as *"store the value on the right under the name on the left"*. It is **not** "equals" from maths.

> [!TIP]
> Underscores in numbers like `8_500_000` are just for readability. Python ignores them.

You can change what a variable holds at any time:

```python
score = 10
score = score + 5  # take the old value, add 5, store it back
print(score)
```

**Naming rules:** letters, digits and `_`; cannot start with a digit; case-sensitive (`Score` ≠ `score`). Use `snake_case` like `total_price`.

## 2. The four basic types

Every value has a **type**. `type()` tells you which one:

```python
print(type(42))        # int: whole number
print(type(3.14))      # float: decimal number
print(type("hello"))   # str: text
print(type(True))      # bool: True or False
```

| Type | Example | Used for |
|---|---|---|
| `int` | `42`, `-7` | counting things |
| `float` | `3.14`, `0.5` | measurements, prices |
| `str` | `"hi"`, `'AI'` | text |
| `bool` | `True`, `False` | yes/no answers |

## 3. Arithmetic

```python
a = 7
b = 2
print(a + b, a - b, a * b)  # 9 5 14
print(a / b)                # 3.5  (/ always gives a float)
print(a // b, a % b)        # 3 1  (floor division, remainder)
print(a ** b)               # 49   (power)
```

> [!NOTE]
> `%` (remainder) is handy: `n % 2 == 0` checks whether `n` is even.

Comparisons produce a `bool`:

```python
print(5 > 3)       # True
print(5 == 3)      # False (== compares, = assigns)
print("ai" == "ai")  # True
```

## 4. Text and f-strings

Joining text with `+` works, but **f-strings** are clearer. Put `f` before the quotes and variables inside `{}`:

```python
name = "Lan"
age = 21
print(f"{name} is {age} years old")
print(f"Next year: {age + 1}")
```

## 5. Converting between types

Data from files, forms and APIs often arrives as **text**. Convert it before doing maths:

```python
text = "42"
number = int(text)
print(number + 1)        # 43
print(float("1.75"))     # 1.75
print(str(3) + " cats")  # 3 cats
```

> [!WARNING]
> `"5" + "7"` gives `"57"` (text joined), not `12`. And `int("1.75")` crashes with `ValueError`. Use `float()` for decimals.

## Recap

- `name = value` stores a value; you can overwrite it later.
- Basic types: `int`, `float`, `str`, `bool`. Check with `type()`.
- `/` gives a float, `//` floor division, `%` remainder, `**` power.
- Use f-strings for readable text, and `int()` / `float()` / `str()` to convert.
