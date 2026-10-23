# A one-line average

This version writes `self.total = self.total + n` in full instead of `+=`, and squeezes `average` into one line with `A if condition else B`. This is the **conditional expression** from the Comprehensions lesson (§4), which picks one of two values. `self.calls` counts as true when it is not 0. It is shorter, but the plain `if` with an early `return` in the solution is easier for a beginner to read.
