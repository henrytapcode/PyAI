# Chat history log in SQLite

**What it shows:** creating a `messages` table, inserting multiple chat turns with `?` placeholders, retrieving one user's messages in `id` order, and counting messages per `role`.

**Step by step**
1. Lines 4–12 open an in-memory SQLite database and create the `messages` table with an `INTEGER PRIMARY KEY` column `id`.
2. Lines 14–25 insert five turns inside `with conn:` using `executemany` and `?` placeholders.
3. Lines 27–36 query only `"an"`'s turns ordered by `id ASC` and print each message with its id and role.
4. Lines 38–49 group all rows by `role`, count each group, and sort by `role ASC` before closing the connection.

**Notice:** passing `("an",)` with a trailing comma makes a one-element tuple; writing `("an")` without the comma passes a 2-character string instead and raises `ProgrammingError`.

**Try it yourself:** change the parameter `("an",)` on line 32 to `("binh",)` and check how many messages appear in the thread.
