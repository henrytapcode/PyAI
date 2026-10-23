Build the first half of the text-cleaning toolkit: a frozen `CleanConfig`, the two small functions `normalize_spaces` and `remove_urls`, and `clean_text`, which uses them according to the config. The editor holds a skeleton with `# TODO` steps. Write your code inside the class and the functions. Lesson sections 2 to 4 show every piece.

**Example**

```python
normalize_spaces("  a   b \n")                          # "a b"
remove_urls("see https://example.com now")              # "see now"
clean_text("  Read https://x.io  TODAY ")               # "read today"
clean_text("Hello  WORLD", CleanConfig(lowercase=False))  # "Hello WORLD"
clean_text("hello brave new world", CleanConfig(max_chars=11))  # "hello brave"
```

**Rules**
- `CleanConfig` is a frozen dataclass with `lowercase=True`, `drop_urls=True` and `max_chars=None`.
- `normalize_spaces` turns any run of spaces, tabs and newlines into one space and trims both ends.
- `remove_urls` drops the words that start with `http://` or `https://` and joins the others with one space. `www.example.com` is not a link for this task.
- `clean_text` runs the steps in this order: remove URLs (if `drop_urls`), fix spaces, lowercase (if `lowercase`), cut to `max_chars` and strip the right end (if `max_chars` is not `None`). `max_chars=0` gives an empty string.
- `clean_text(text)` with no config uses `CleanConfig()`.
- If `text` is not a string, `raise TypeError("text must be a string")`.
