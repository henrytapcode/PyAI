Write two functions to store and query model ratings in an in-memory SQLite database: `create_feedback_db(rows)` creates the `feedback(user TEXT, model TEXT, rating INTEGER)` table and inserts `(user, model, rating)` tuples, and `low_rated_users(conn, max_rating)` returns the sorted list of unique users who gave at least one rating `<= max_rating`. Write your code inside each function and `return` the requested value.

**Example**

```python
conn = create_feedback_db([
    ("binh", "mini", 2),
    ("an", "gpt-4o", 5),
    ("an", "mini", 1),
    ("binh", "claude", 1),
])
low_rated_users(conn, 2)  # ["an", "binh"]
```

**Rules**

- Always use `?` placeholders for inserted rows and query parameters (names like `"O'Brien"` must work).
- Return each matching user at most once, sorted ascending alphabetically.
- Include ratings equal to `max_rating` (`rating <= max_rating`).
- Return `[]` when the table is empty or no rating qualifies.
