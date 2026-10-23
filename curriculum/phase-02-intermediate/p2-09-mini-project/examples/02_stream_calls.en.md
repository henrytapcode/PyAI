# Streaming the expensive calls

**What it shows:** a generator that reads lines **lazily**, and a decorator that logs every parse. Together they show how little work a lazy pipeline does when you ask for only two results.

**Step by step**
1. Lines 5–12 define `logged`. The wrapper calls the original function, prints what it received and returned, and then returns the result. `@wraps` keeps the name.
2. Lines 15–18 decorate `parse_line`, which turns `"large,0.40"` into `("large", 0.4)`.
3. Lines 21–25 define the generator `expensive_calls`. It parses one line at a time and `yield`s only the calls that cost at least `limit`.
4. Line 30 creates the generator. Nothing runs yet, which is why `nothing parsed yet` is true.
5. Lines 32–33 ask for two results with `next`. Each `next` resumes the loop only until the next `yield`.
6. Line 34 prints the function name, which `@wraps` kept as `parse_line`.

**Notice:** the last line `small,0.03` is never parsed. A list comprehension would have parsed all five lines first.

**Try it yourself:** add `print("third:", next(stream))` at the end. The generator runs out of lines and ends with a `StopIteration` error. Remove the line again afterwards.
