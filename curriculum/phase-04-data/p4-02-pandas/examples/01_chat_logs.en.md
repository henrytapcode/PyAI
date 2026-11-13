# Chatbot session logs

**What it shows:** building a DataFrame from a dict of lists, filtering rows by rating, and sorting by multiple columns.

**Step by step**
1. Lines 4–8 create a `logs` DataFrame with five chatbot sessions and their user ratings.
2. Line 10 prints the total session count using `len(logs)`.
3. Lines 11–13 filter for sessions with `rating <= 2`, sort by lowest rating first and highest message count second, and renumber the rows with `.reset_index(drop=True)`.
4. Line 16 prints the filtered, sorted table.

**Notice:** `ascending=[True, False]` sorts `rating` from lowest to highest while breaking ties by `messages` from highest to lowest, and `.reset_index(drop=True)` resets the row labels to `0, 1, 2`.

**Try it yourself:** change `rating <= 2` on line 11 to `rating <= 4` and check which sessions appear.
