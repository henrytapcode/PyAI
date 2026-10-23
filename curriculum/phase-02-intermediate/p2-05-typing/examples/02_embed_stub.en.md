# A typed embedding stub

**What it shows:** a fake `embed` function with the same signature as a real one, and what happens when you break its hint.

**Step by step**
1. Lines 2–6 turn each text into a vector of two floats (its length and the number of `"a"`s; `text.count("a")` counts how many times `"a"` appears). Hint: `list[str]` in, `list[list[float]]` out.
2. Lines 9–13 take two vectors and return their dot product (multiply the numbers in the same positions, then add them up) as a `float`.
3. Lines 16–18 embed two words and print the vectors and their dot product.
4. Line 21 passes a single `str` instead of a list. This breaks the hint.
5. Line 22 prints the hints that Python stored on the function.

**Notice:** line 21 runs without any error. Looping over `"cat"` visits `c`, `a`, `t`, so you get three vectors instead of one. A type checker would have caught this call before you ran it.

**Try it yourself:** call `embed(["cat"])` (a list with one word) and compare the result with line 21.
