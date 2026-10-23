# Scope and shadowing

**What it shows:** which variables a function can see, and what happens when a local variable has the same name as a global one.

**Step by step**
1. Line 2 creates `rate` at the top of the file. It is a **global** variable: every function can read it.
2. Lines 5–7: `add_tax` creates `tax`, which is **local**: it exists only while `add_tax` runs. Line 6 *reads* the global `rate`, which is fine.
3. Lines 10–12: `broken_reset` writes `rate = 0`. Because it assigns inside a function, Python creates a **new local** `rate` and the global one is hidden. This is called **shadowing**.
4. Line 15 prints `110.0`. Line 16 prints `0`, the local value. Line 17 prints `0.1`: the global `rate` was never touched.

**Notice:** a function can read a global, but assigning to the same name inside the function makes a separate local variable. The usual fix is to pass values in as parameters and `return` the result.

**Try it yourself:** add `print(tax)` as the last line. You get a `NameError`, because `tax` does not exist outside `add_tax`.
