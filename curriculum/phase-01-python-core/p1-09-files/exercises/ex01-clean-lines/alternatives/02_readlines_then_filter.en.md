# readlines, then filter

`f.readlines()` returns every line in a list (with the `\n` still attached). The file closes right after the `with` block, and the cleaning happens afterwards in a normal loop. This keeps file work and cleaning work apart, which can be easier to read. The cost is that all lines sit in memory at once, so use it for small files only.
