# Rotate a copy of the replies

This version keeps a copy of the list in `self.queue`. Each call takes the first reply off the front with `pop(0)` and puts it at the back with `append`, so the queue turns around like a wheel and there is no counter or `%`. The original `self.replies` is never changed, which is why `describe` can still count it. It is neat for short lists, but the counter version is easier to follow in a debugger, and `pop(0)` gets slower on very long lists.
