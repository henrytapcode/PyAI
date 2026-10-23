You have a text file with one prompt per line, but it is messy: some lines have extra spaces, and some lines are empty. Write `read_clean_lines(path)` so it opens the file, strips every line, skips the empty ones, and returns the rest as a list of strings. Write your code inside the function and `return` the answer. Lesson section 3 shows how to loop over a file.

**Example**

| File content | Returns |
|---|---|
| `"  hello \n\nworld\n"` | `["hello", "world"]` |
| `"Xin chào\n"` | `["Xin chào"]` |
| `""` (empty file) | `[]` |

**Rules**
- Open the file with `encoding="utf-8"`.
- Do not change the file; only read it.
- Return a list of strings without any `\n`.
