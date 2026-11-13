# Row-by-row cleaning with `csv.DictReader`

Instead of loading the whole CSV into pandas first, this approach streams each line through Python's standard `csv.DictReader`, checks duplicates with a `seen_ids` set, parses numbers row by row, and constructs the `DataFrame` at the end.

It is easier to log or inspect individual rejected rows when debugging a giant log file, while vectorized pandas methods in the main solution are shorter and faster for medium in-memory tables.
