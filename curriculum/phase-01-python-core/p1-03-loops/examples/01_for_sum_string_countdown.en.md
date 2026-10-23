# Three kinds of for loop

**What it shows:** a `for` loop over `range()`, over a string, and counting down, plus the accumulator pattern from the lesson.

**Step by step**
1. Line 2 creates the accumulator `total` and sets it to 0, **before** the loop.
2. Line 3 starts the loop: `n` takes the values 1, 2, 3, 4, 5 (`range(1, 6)` stops before 6).
3. Line 4 adds `n` to `total`. Line 5 prints both values, so the output shows `total` growing: 1, 3, 6, 10, 15.
4. Line 6 is not indented, so it runs once, after the loop is finished.
5. Lines 8-9 loop over the string `"AI"`: `letter` is `"A"`, then `"I"`.
6. Lines 11-12 use `range(10, 0, -3)`: start at 10, subtract 3 each time, stop before 0. That gives 10, 7, 4, 1.

**Notice:** the loop variable (`n`, `letter`, `step`) is just a normal variable. Python sets it for you at the start of every round.

**Try it yourself:** press **Visualize** and watch `total` change at line 4. Then change `range(1, 6)` to `range(1, 11)` and predict the final sum before you run it.
