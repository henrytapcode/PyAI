# Keep every amount

Instead of updating two running numbers, this version stores each amount in a list `self.amounts` and works out `total` and `calls` from it with `sum` and `len`. It is easy to extend later (for example to find the biggest amount), but it uses more memory because it remembers every call. The `__repr__` here builds the text with `+` and `str(...)` instead of an f-string, which gives the same result.
