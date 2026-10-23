# While, continue and break together

**What it shows:** a `while True` loop that adds up odd numbers, skips the even ones with `continue`, and stops itself with `break`.

**Step by step**
1. Lines 2-3 set up two variables: `total` (the accumulator) and `number` (the counter the loop will change).
2. Line 4, `while True:`, means "repeat forever", so something inside must call `break`.
3. Line 5 adds 1 to `number` at the start of every round: 1, 2, 3, ...
4. Lines 6-7: if `number` is even, `continue` skips the rest of the round. That is why 2, 4, 6, 8 never appear in the output.
5. Line 8 adds the odd `number` to `total`; line 9 prints it. The totals are 1, 4, 9, 16, 25.
6. Lines 10-11: when `total` goes over 20 (it happens at `number = 9`, total 25), `break` ends the loop at once.
7. Line 12 runs after the loop and prints the last `number`: 9.

**Notice:** the order matters. `number += 1` comes **before** the `continue`. If it came after, an even number would hit `continue` without ever being increased, and the loop would get stuck forever.

**Try it yourself:** change `20` to `50` and predict where it stops.
