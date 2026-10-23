# The same job with while

You can do the same thing with `while`: keep your own counter `number`, repeat as long as `number <= n`, and add 1 to the counter at the end of every round. It works, but it is longer and you must remember `number += 1` (forget it and the loop never ends). When you know how many rounds you need, `for` with `range` is simpler and safer.
