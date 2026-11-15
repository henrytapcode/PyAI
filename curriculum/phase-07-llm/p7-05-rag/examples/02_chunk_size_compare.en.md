# Comparing chunk sizes and overlaps

**What it shows:** Running the same three policy questions across four `(size, overlap)` chunking settings and counting how often the top-1 retrieved chunk contains the target answer phrase.

**Step by step**
1. Lines 5–15 define one multi-sentence guide string `DOC` and three `(question, needle)` test pairs.
2. Lines 18–28 define `chunk_words(text, size, overlap)` using `step = size - overlap` and stopping once a window reaches the end of `words`.
3. Lines 31–44 loop through `(5, 0)`, `(8, 0)`, `(8, 3)`, and `(12, 3)`, embed each chunk set, and print the chunk count alongside top-1 retrieval hits.

**Notice:** Increasing `size` from `5` to `8` without overlap catches only `1/3` answers, while adding `overlap=3` raises it to `2/3` and `12/3` reaches `3/3`.

**Try it yourself:** Test `(10, 4)` in the loop and see how many chunks and retrieval hits it produces.
