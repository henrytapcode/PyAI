Fill in the `___` blanks inside `normalise_labels(labels)` so it cleans a pandas `Series` of messy text labels: trim outer whitespace, convert to lowercase, and replace both `"_"` and `"-"` with a single space `" "`. Write your code inside the function and `return` the cleaned `Series`.

**Example**

```python
s = pd.Series([" Bug_Report ", "FEATURE-REQ", "  gpt_4o "])
normalise_labels(s).tolist()  # ["bug report", "feature req", "gpt 4o"]
```

**Rules**

- Keep the original row index of `labels`.
- Do not modify the input `Series` in place.
- Return a pandas `Series` (not a Python `list`).
