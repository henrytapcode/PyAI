A search engine, a recommender and a retriever all do the same thing: score many items, then keep the best few. Write `top_scores(scores, n)`. It receives a list of numbers and a whole number `n`, and returns a **new list** with the `n` biggest numbers, **biggest first**.

**Example**

| Call | Result |
|---|---|
| `top_scores([0.5, 0.9, 0.7, 0.8], 2)` | `[0.9, 0.8]` |
| `top_scores([3, 1, 2], 5)` | `[3, 2, 1]` |
| `top_scores([], 3)` | `[]` |

**Rules**

- Write your code inside the function and `return` the answer.
- If `n` is bigger than the list, return all the scores (still biggest first).
- Do not change the list that was passed in.

Press **Check** to run the tests.
