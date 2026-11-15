# Checking citations against retrieved chunks

**What it shows:** Using `FakeLLM(script=[...])` to simulate a grounded reply, a hallucinated `[3]` citation when only `2` chunks exist, and an uncited reply, then catching both issues in Python.

**Step by step**
1. Lines 7–15 define `check_citations(answer, n_chunks)`, parsing `[n]` markers and separating `valid` indexes (`1 <= n <= n_chunks`) from out-of-range `invalid` indexes while flagging `missing: True` when no markers appear.
2. Lines 18–28 supply two retrieved chunks and script `FakeLLM` with three contrasting answers.
3. Lines 29–33 call `client.chat()` for each case and print the validation dictionary.

**Notice:** Checking only for `[1]` or crashing on `hits[n - 1]` misses silent failures; `check_citations()` flags both nonexistent `[3]` citations and completely uncited claims.

**Try it yourself:** Add a fourth scripted reply `"Refunds take 30 days. [0] [2]"` and observe how `[0]` is placed in `invalid` while `[2]` is accepted in `valid`.
