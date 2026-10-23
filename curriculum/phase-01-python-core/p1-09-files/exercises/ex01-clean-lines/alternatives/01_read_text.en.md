# Read everything, then split

Here `Path(path).read_text(...)` loads the whole file as one string, and `splitlines()` cuts it into lines without the `\n`. It is shorter because there is no `with` block, and it is a good choice for small files. For a huge file, the line-by-line loop in the main solution is safer, because it never holds more than one line in memory.
