# Token counts, batch padding, and truncation

**What it shows:** Using only `AutoTokenizer` to count subword tokens, inspect the padded batch matrix shape, and see `max_length` truncation in action.

**Step by step**
1. Lines 4–7 load the pinned tokenizer from cache with `local_files_only=True` (no model weights are loaded).
2. Lines 9–18 call `tokenizer.tokenize(text)` on four sentences to count subword pieces without `[CLS]` or `[SEP]`, and print the maximum count (`10`).
3. Lines 20–21 tokenize all four sentences as a batch with `padding=True, truncation=True, return_tensors="pt"` and print the matrix shape `(4, 12)` (longest count `10` plus `[CLS]` and `[SEP]`).
4. Lines 23–26 tokenize a longer sentence with `truncation=True, max_length=8` and print the resulting 8 tokens.

**Notice:** The longest sentence has `10` non-special tokens, yet the padded batch width is `12` because `tokenizer(...)` adds `[CLS]` at the start and `[SEP]` at the end.

**Try it yourself:** Change `max_length=8` to `max_length=10` and watch `'##point'` and `'timed'` appear before `[SEP]`.
