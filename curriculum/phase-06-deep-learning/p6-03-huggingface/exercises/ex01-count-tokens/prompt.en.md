Fill in the blanks inside `count_tokens(texts)` so it returns the number of non-special tokens (excluding `[CLS]` and `[SEP]`) for each string in `texts`, using the preloaded `tokenizer`.

Write your code inside the function and `return` the answer.

**Example**

```python
count_tokens(["Great!", "Chatbot logs!"])  # [2, 4]
count_tokens([""])                         # [0]
count_tokens([])                           # []
```

**Rules**

- Do not count special tokens `[CLS]` or `[SEP]`.
- Every element in the returned list must be a built-in Python `int`.
- An empty string `""` must count as `0` tokens, and an empty list `[]` must return `[]`.
