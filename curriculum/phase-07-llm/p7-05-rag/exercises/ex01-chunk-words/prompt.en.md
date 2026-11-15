Complete `chunk_words(text, size, overlap)` in `starter.py` by replacing every `___` blank so documents are split into overlapping word chunks.

Write your code inside the function and `return` the list of chunk strings.

## Example

```python
chunk_words("a b c d e", size=3, overlap=1)   # -> ["a b c", "c d e"]
chunk_words("a b c d", size=4, overlap=2)     # -> ["a b c d"]
chunk_words("one two", size=5, overlap=1)     # -> ["one two"]
chunk_words("   ", size=3, overlap=1)         # -> []
```

## Rules

- Split `text` on whitespace and join each window's words with a single space (`" "`).
- Stopping rule: the final window may be shorter than `size`, **but never create a window whose words are already completely contained inside the previous window** (stop as soon as the current slice reaches or passes the end of the word list, e.g. for `"a b c d"` with `size=4, overlap=2`, stop after `["a b c d"]` instead of emitting `"c d"`).
- Raise `ValueError` if `size <= 0`, `overlap < 0`, or `overlap >= size`.
- Return `[]` if `text` contains no non-whitespace words.
