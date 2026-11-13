Write a function `clean_ratings(df)` that cleans a raw DataFrame containing `user` and `rating` columns. Write your code inside the function and `return` the cleaned `DataFrame`.

**Example**

Input `df`:

```text
   user  rating
0   An      " 4 "
1  binh    "five"
2  an       "5"
3  chi      "7"
```

Returned `DataFrame`:

```text
  user  rating
0   an       5
```

**Rules**

- Normalise `user` with `.strip()` and `.lower()`.
- Convert `rating` to numbers with `pd.to_numeric(..., errors="coerce")`, and drop rows that cannot be parsed (`""`, `None`, `"five"`) or are outside `1` to `5` inclusive.
- For duplicate `user` names (after normalising), keep only the **last** valid row.
- The returned `DataFrame` must have columns `["user", "rating"]` in that order, `rating` dtype `"int64"`, and a reset index starting at `0`.
- Do not modify the input `df`.
