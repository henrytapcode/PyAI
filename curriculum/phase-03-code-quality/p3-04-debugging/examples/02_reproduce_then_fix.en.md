# Reproduce, then fix

**What it shows:** a function that splits a list into chunks loses items. The report only says "some documents go missing". Shrinking the input finds the smallest failing call, and that call becomes a test.

**Step by step**
1. Lines 2–3 define `chunk` with a bug: the `range` stops too early, at `len(items) - size + 1`.
2. Lines 7–9 try three inputs, from big to small. The first is fine, the second loses the `3`, and the third returns `[]`.
3. The smallest failing call is `chunk([1], 2)`. One item and a chunk size of 2 is enough to see the bug, and it points at the end of the `range`.
4. Lines 12–13 fix it: the `range` must go up to `len(items)`.
5. Lines 17–21 keep the cases as `assert` lines. They all pass now, and they would fail if the bug came back.

**Notice:** the fix is one small change, but finding the smallest failing input is what made the cause easy to see.

**Try it yourself:** add the case `assert chunk([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]`. It should still pass.
