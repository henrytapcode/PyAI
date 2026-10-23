A log file can have millions of lines, so you read it lazily. The two functions are already written, but three words are replaced by `___`. Replace each `___` so that `error_lines(lines)` yields every line that contains `ERROR` (with the spaces and the new line at both ends removed), and `count_errors(lines)` returns how many such lines there are. Then press **Check**.

**Example**

| call | result |
|---|---|
| `list(error_lines(["ok\n", "ERROR disk full\n"]))` | `["ERROR disk full"]` |
| `count_errors(["ERROR a\n", "ok\n", "ERROR b\n"])` | `2` |

**Rules**
- `lines` can be any iterable of strings: a list, an open file, or a generator.
- Match the exact text `ERROR` (capital letters). A line with `error` in lower case does not count.
- `error_lines` is a generator: it reads only as many lines as needed for the item you ask for.
- Keep the order of the lines.
