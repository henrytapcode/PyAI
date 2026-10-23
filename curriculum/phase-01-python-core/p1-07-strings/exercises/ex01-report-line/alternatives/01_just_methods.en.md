# Build each column, then join them

This version formats each number on its own, then pads the text with the string methods `ljust()` and `rjust()` (a small preview of a later topic: they pad a string to a width). Finally it joins the three columns with `+`. It is longer than one f-string, but each step is easy to test on its own. The single f-string in the solution is shorter and is the usual choice.
