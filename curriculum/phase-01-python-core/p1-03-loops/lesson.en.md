## 1. Why loops?

Computers are great at boring, repetitive work. Instead of copying a line 100 times, you write it once and tell Python to **repeat** it. That is a **loop**.

```python
for i in range(3):
    print("Hello!")
```

The indented line is the **body**. It runs once per round. Indentation (4 spaces) is how Python knows what belongs to the loop.

## 2. `for` and `range()`

`range()` produces a sequence of whole numbers. `for` walks through them, putting each one in a variable:

```python
for i in range(5):
    print(i)  # 0 1 2 3 4
```

`range` has three forms:

| Call | Numbers produced |
|---|---|
| `range(5)` | 0, 1, 2, 3, 4 |
| `range(2, 6)` | 2, 3, 4, 5 |
| `range(0, 10, 3)` | 0, 3, 6, 9 |
| `range(5, 0, -1)` | 5, 4, 3, 2, 1 |

```python
for n in range(2, 11, 2):
    print(n)  # even numbers 2..10
```

> [!WARNING]
> The **stop** value is never included. `range(1, 5)` gives 1, 2, 3, 4. To count from 1 to `n`, write `range(1, n + 1)`. This "off by one" mistake is the most common loop bug.

## 3. Looping over a string

A string is a sequence of characters, so `for` can walk through it one character at a time:

```python
for letter in "Hanoi":
    print(letter)
```

`letter in "aeiou"` asks: *is this character one of those letters?* It gives `True` or `False`, so it works inside `if`:

```python
for letter in "banana":
    if letter in "aeiou":
        print(letter, "is a vowel")
```

## 4. The accumulator pattern

Most loops build up one answer. Start with an **accumulator** variable before the loop, then update it inside:

```python
total = 0
for n in range(1, 6):
    total += n
print(total)  # 15
```

`total += n` is shorthand for `total = total + n`. The same trick works for `-=`, `*=` and so on.

**Counting** is the same pattern, but you add 1 instead of a value:

```python
count = 0
for n in range(1, 21):
    if n % 3 == 0:
        count += 1
print(count)  # 6 multiples of 3
```

> [!TIP]
> Always set the accumulator **before** the loop. If you put `total = 0` inside the loop, it resets every round.

## 5. `while` loops

Use `for` when you know how many rounds. Use `while` when you repeat **until a condition becomes false**:

```python
n = 1
while n <= 3:
    print("round", n)
    n += 1
```

> [!WARNING]
> Something inside a `while` must eventually make the condition false. Forget `n += 1` and the loop never ends (an **infinite loop**). If that happens in your editor, stop the run.

## 6. `break` and `continue`

- `break` leaves the loop immediately.
- `continue` skips the rest of this round and jumps to the next one.

```python
for n in range(1, 10):
    if n % 2 == 0:
        continue  # skip even numbers
    if n > 7:
        break     # stop completely
    print(n)      # 1 3 5 7
```

## Recap

- `for x in range(start, stop, step)` repeats with numbers; `stop` is excluded. Strings work too: `for letter in text`.
- Accumulator: set `total = 0` before the loop, then `total += value` inside. Counting adds 1.
- `while condition:` repeats until the condition is false, so make sure it can become false.
- `break` stops the loop; `continue` skips to the next round.
