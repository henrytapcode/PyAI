# Using an explicit while loop

This alternative replaces `enumerate()` with an explicit index counter `idx` and a `while` loop, returning immediately when `hit` is `True`. Using `for ... in enumerate(...)` is more idiomatic in Python because you cannot forget `idx += 1`, while the `while` version shows the exact index stepping a debugger performs.
