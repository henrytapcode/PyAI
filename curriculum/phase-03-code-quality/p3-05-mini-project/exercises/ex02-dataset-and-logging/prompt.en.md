Now the second half of the toolkit: clean a whole list of texts and report what happened. `CleanConfig`, `clean_text` and `CleanReport` are already written in the editor. Write your code inside `clean_dataset` and `return` the report. Lesson section 5 shows the loop and the logging.

**Example**

```python
report = clean_dataset(["Hi  there", "hi there", "", 7])
report.kept         # ["hi there"]
report.skipped      # 1   (the number 7)
report.empty        # 1   ("")
report.duplicates   # 1   ("hi there" the second time)
```

The run also writes two log records:

| level | message |
|---|---|
| `WARNING` | `skipping item 3: not a string` |
| `INFO` | `kept 1 of 4 texts` |

**Rules**
- Go through `texts` in order. Do not change the list you receive.
- An item that is not a string is **skipped**: log one `WARNING` `skipping item N: not a string` (N is its position, starting at 0) and count it in `skipped`.
- Clean a string with `clean_text(item, config)`. An empty result is counted in `empty`. A result already seen before is counted in `duplicates`. Any other result is added to `kept`, in the original order.
- Do not log empty or duplicate texts one by one. Log exactly **one** `INFO` summary line at the end: `kept K of N texts`, where `K` is how many were kept and `N` is the length of `texts`.
- Use `logger.warning(...)` and `logger.info(...)` with `%d` arguments, not f-strings.
