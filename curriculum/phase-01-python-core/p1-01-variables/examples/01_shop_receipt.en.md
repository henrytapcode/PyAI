# Shop receipt

**What it shows:** variables, arithmetic and f-strings working together in a tiny real program.

**Step by step**
1. Lines 2–4 store the item name (`str`), the unit price (`float`) and the quantity (`int`).
2. Lines 6–8 compute new values from old ones: `subtotal` first, then `tax` from `subtotal`, then `total` from both. Each line can only use variables created above it.
3. Lines 10–13 print the receipt with f-strings. `round(tax, 2)` rounds a number to 2 decimal places, so money looks like money.
4. Line 14 prints the type of `total`: a `float`, because a `float` times an `int` gives a `float`.

**Notice:** the computer never "remembers" a formula. `total` holds the number `8.25`, not "subtotal + tax". If you change `quantity` after line 8, `total` does not update.

**Try it yourself:** change `quantity` to `4` and run again. Predict the total before you press Run (it should be `11.0`).
