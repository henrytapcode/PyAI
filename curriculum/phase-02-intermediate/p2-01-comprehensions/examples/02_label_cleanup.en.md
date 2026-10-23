# Label cleanup

**What it shows:** a set comprehension to remove duplicates, a dict comprehension to count, and `x if condition else y` inside a list comprehension.

**Step by step**
1. Line 2 holds labels typed by different people: capital letters, extra spaces, repeats.
2. Line 4 cleans every label with `strip()` then `lower()`. Now `"POSITIVE "` and `"positive"` are the same text.
3. Line 7 uses `{...}` without a colon, which makes a **set**: it keeps each value once. `sorted(...)` turns it back into a tidy list.
4. Line 10 builds a dict from label to count. For each name, the inner `[x for x in cleaned if x == name]` collects the matching labels and `len(...)` counts them.
5. Line 13 picks `"ok"` or `"rare"` for each label with `value_if_true if condition else value_if_false`.

**Notice:** the `if` at the end of the inner comprehension (line 10) *filters*. The `if ... else ...` at the front (line 13) *chooses a value*. They look alike but do different jobs.

**Try it yourself:** change `>= 2` on line 13 to `>= 3`. Which labels are still `"ok"`?
