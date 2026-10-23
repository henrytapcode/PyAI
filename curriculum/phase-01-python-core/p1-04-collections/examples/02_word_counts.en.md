# Word counts

**What it shows:** how a dictionary counts things, and how to read it back with `[]`, `.get()` and `.items()`.

**Step by step**
1. Line 2 is the data: 7 words, some repeated. Line 4 starts with an empty dict.
2. The loop on lines 5–9 visits each word. If the word is already a key (line 6), add 1 to its count. Otherwise (line 8) this is the first time we see it, so store `1`.
3. Line 11 prints the whole dict. Words stay in the order they were first seen.
4. Line 12 reads one count with `[]`: `3`.
5. Line 13 asks for a word that is not there. `.get("python", 0)` returns `0` instead of crashing with `KeyError`.
6. Lines 14–15 loop over `counts.items()`, unpacking each pair into `word` and `n`.

**Notice:** this is the long version of `counts[word] = counts.get(word, 0) + 1` from the lesson. Both do the same thing. Try to see how lines 6–9 become that one line.

**Try it yourself:** add `"python"` to the end of `words` and run again. `counts.get("python", 0)` now prints `1`.
