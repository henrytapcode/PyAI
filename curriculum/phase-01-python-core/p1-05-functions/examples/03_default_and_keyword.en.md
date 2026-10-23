# Default and keyword arguments

**What it shows:** how a caller can skip a parameter, or pass it by name.

**Step by step**
1. Line 2: `greeting="Hello"` gives the parameter a **default value**. If the caller does not provide one, Python uses `"Hello"`.
2. Line 10: `greet("Lan")` passes only `name`, so `greeting` is `"Hello"`. Output: `Hello, Lan!`.
3. Line 11: the second argument is matched by position, so `greeting` becomes `"Hi"`.
4. Line 12: `greeting="Xin chao"` is a **keyword argument**: we name the parameter we mean. This reads well and the order stops mattering.
5. Lines 6–7 do the same with `rate=0.1`. Line 13 uses the default, line 14 overrides it with `rate=0.2`. The results are floats because `price * rate` is a float.

**Notice:** the parameter with a default (`greeting`, `rate`) comes **after** the one without. Python requires that order.

**Try it yourself:** call `greet(greeting="Hey", name="Minh")`. The order of keyword arguments does not matter.
