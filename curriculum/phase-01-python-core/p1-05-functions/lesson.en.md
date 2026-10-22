## 1. Why functions?

So far you have written code that runs top to bottom. When you need the same steps twice, you copy and paste. That gets messy fast. A **function** is a named block of code you write once and run whenever you want.

Functions give you two things: **reuse** (write once, call many times) and **names** (`bmi(...)` tells the reader what happens without showing how). You have already used built-in functions: `print()`, `len()`, `int()`.

## 2. Defining and calling

Use `def`, a name, parentheses, a colon, and an indented body:

```python
def say_hello():
    print("Hello!")


say_hello()
say_hello()
```

`def` only *defines* the function; nothing runs until you **call** it with `name()`.

## 3. Parameters and arguments

A **parameter** is a variable name in the `def` line. An **argument** is the actual value you pass when calling:

```python
def square(n):          # n is a parameter
    print(n * n)


square(5)               # 5 is an argument
square(12)
```

A function can take several parameters, separated by commas. Arguments are matched by position:

```python
def rectangle_area(width, height):
    print(width * height)


rectangle_area(3, 4)
```

## 4. return vs print

This is the most common beginner confusion.

- `print(x)` **shows** a value on the screen. The program cannot use it afterwards.
- `return x` **hands the value back** to the code that called the function, so you can store it or compute with it.

```python
def double_print(n):
    print(n * 2)


def double_return(n):
    return n * 2


a = double_print(4)    # prints 8
b = double_return(4)   # prints nothing
print("a is", a)
print("b is", b)
print("b + 1 =", b + 1)
```

A function with no `return` gives back `None` ("nothing"). That is why `a` is `None` and `a + 1` would crash.

> [!WARNING]
> If you see `None` where you expected a number, or `TypeError: unsupported operand type(s) ... 'NoneType'`, you probably used `print` (or forgot `return`) inside the function.

`return` also **ends** the function immediately; code after it never runs:

```python
def sign(n):
    if n < 0:
        return "negative"
    if n == 0:
        return "zero"
    return "positive"


print(sign(-3), sign(0), sign(8))
```

> [!TIP]
> Rule of thumb: functions that *compute* something should `return` it. Let the caller decide whether to print.

## 5. Default and keyword arguments

Give a parameter a **default value** with `=`. The caller may then skip it:

```python
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"


print(greet("Lan"))
print(greet("Lan", "Hi"))
print(greet("Lan", greeting="Xin chao"))   # keyword argument
```

In the last call we wrote `greeting=...` by name: a **keyword argument**. It makes calls easier to read and the order stops mattering.

> [!NOTE]
> Parameters with defaults must come after the ones without: `def f(a, b=1)` is fine, `def f(a=1, b)` is a syntax error.

## 6. Docstrings

A string on the first line of the body documents what the function does. It is called a **docstring**:

```python
def average(numbers):
    """Return the mean of a non-empty list of numbers."""
    return sum(numbers) / len(numbers)


print(average([2, 4, 9]))
help(average)
```

Good names plus a one-line docstring make code readable months later.

## 7. Local scope and functions calling functions

Variables created inside a function are **local**: they exist only while the function runs.

```python
def make_total(price):
    tax = price * 0.1     # local to make_total
    return price + tax


print(make_total(100))
# print(tax)   # NameError: tax does not exist out here
```

Functions can call other functions. Small pieces combine into bigger ones:

```python
def bmi(weight_kg, height_m):
    return weight_kg / height_m ** 2


def describe(weight_kg, height_m):
    value = bmi(weight_kg, height_m)
    return f"BMI is {value:.1f}"


print(describe(52, 1.60))
```

## Recap

- `def name(parameters):` defines a function; `name(arguments)` calls it.
- `print` shows a value; `return` gives it back. No `return` means `None`.
- Default values (`greeting="Hello"`) make parameters optional; keyword arguments pass by name.
- A docstring describes the function; variables inside a function are local.
- Functions can call other functions: build big things from small, named pieces.
