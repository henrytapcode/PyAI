# Filtering and deduplicating in Python

This alternative fetches every `(user, rating)` row with `SELECT user, rating FROM feedback`, filters `rating <= max_rating` using a Python `set` comprehension to remove duplicates, and sorts the result with `sorted(...)`. It works on small tables, but letting SQL run `WHERE rating <= ?`, `DISTINCT`, and `ORDER BY` is much better as data grows because only the matching usernames leave the database instead of loading millions of rows into Python memory.
