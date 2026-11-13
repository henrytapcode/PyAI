# Row-by-row loop with a user dictionary

This approach iterates over `(user, rating)` pairs one row at a time, parses and range-checks each rating in plain Python, and stores the latest valid score in a `dict` keyed by the normalised `user` (removing any earlier entry with `.pop()` so row order matches `keep="last"`). It is easy to extend when each row needs custom validation or logging, though it runs much slower than vectorised pandas methods on large tables.
