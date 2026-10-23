# F-strings and a counter

This version counts the skipped texts in `skipped` and works out the number of good scores by subtraction. It also builds the messages with f-strings. The result is the same, so the tests pass, but each f-string is built even when the log level would drop the message (§5). Prefer the `%s` arguments in code that logs inside a busy loop. The counter is a fine idea when you want the number of skipped lines for a report, and then you can reuse `skipped`.
