# Leave the last attempt unguarded

The loop handles only the first `times - 1` attempts and swallows their errors with `pass`. The final attempt is a plain call outside the `try`, so if it fails, its error flies out on its own and you never need to store it. This is shorter and avoids `last_error`, but it relies on `times` being at least 1, and the "give up" rule is hidden in the last line, so the `for ... try` version is easier to read.
