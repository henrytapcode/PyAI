You have a CSV file with the columns `name` and `score`, and you need the same data as a JSON Lines file with one object per line. The function is already written, but four words are replaced by `___`. Replace each `___` so that `csv_to_jsonl(csv_path, jsonl_path)` writes every row as a JSON object (with the score as a number) and returns how many rows it wrote. Lesson sections 6 and 8 show every piece you need.

**Example**

| CSV file | JSON Lines file |
|---|---|
| `name,score` | |
| `Lan,9.5` | `{"name": "Lan", "score": 9.5}` |
| `Minh,7` | `{"name": "Minh", "score": 7.0}` |

The function returns `2`.

**Rules**
- Replace only the `___` blanks; the rest of the code is correct.
- CSV values are text, so the score must be converted to a number.
- Keep non-English letters as they are (`ensure_ascii=False`).
