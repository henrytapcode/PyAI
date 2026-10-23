# Whole-file helpers with `Path`

Here the file work is done with `Path.write_text` and `Path.read_text` plus `json.dumps` and `json.loads` (the `s` versions that work on strings), as in the files lesson. There is no `with open(...)` block, because these helpers open and close the file for you. The date is split with `partition`, a string method that cuts at the first `-` and gives three parts (before, the dash, after).

This is the shortest way to handle small files. `json.load` also reads the whole file at once, so the real difference is control: use `with open(...)` when you write a file in pieces (e.g. JSON Lines, one `json.dumps` per line) or need control over how the file is opened.
