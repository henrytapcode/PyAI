Embedding services accept a limited number of texts per call, so you send documents in small batches. Write the generator function `batched(items, n)`. It goes through `items` and yields lists of up to `n` items, one list at a time. Write your code inside the function and `yield` each batch.

**Example**

| call | what you get one by one |
|---|---|
| `batched([1, 2, 3, 4, 5], 2)` | `[1, 2]`, then `[3, 4]`, then `[5]` |
| `batched("abcd", 2)` | `["a", "b"]`, then `["c", "d"]` |
| `batched([], 3)` | nothing |

**Rules**
- `items` can be any iterable: a list, a tuple, a string, a `range`, or another generator. `n` is at least 1.
- Every batch is a list, in the original order. The last batch may be shorter than `n`, but never empty.
- Each batch must be its own new list. Do not reuse and empty one list.
- Be lazy: after the first batch is asked for, read only as many items as that batch needs.
- Do not change the input.
