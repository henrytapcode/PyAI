# Cache for repeated texts

**What it shows:** a decorator that remembers earlier results, so the same text is never embedded twice.

**Step by step**
1. Line 6 creates the dict `saved` **inside** `cache_results`. It lives in the closure, so every decorated function gets its own dict.
2. Lines 9–13 define the wrapper. If the arguments `args` (a tuple) are not a key in `saved` yet, it calls the real function and stores the result. Then it returns the saved value.
3. Line 16 creates the list `calls`, which records every time the real `embed_text` runs.
4. Lines 19–22 decorate `embed_text` with a fake embedding: `[length, how many "a"]`.
5. Lines 25–27 ask for `"banana"` twice and `"kiwi"` once. Lines 28–29 show that the real function ran only twice.

**Notice:** the second `"banana"` returns the same list without running `embed_text`. This wrapper accepts only positional arguments (`*args`), because dict keys must be unchangeable (immutable), and `kwargs` is a dict, so it cannot be a key.

**Try it yourself:** add `print(embed_text("kiwi"))` before line 28. The number of real calls must stay at 2.
