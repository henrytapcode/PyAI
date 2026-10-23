The class `MessageLog` keeps a list of chat messages. It should work like this:

- `add(text)` stores a message.
- `count()` returns how many messages are stored.
- `longest()` returns the longest message text (the first one if there is a tie), or `""` if the log is empty.

The code below has **3 bugs**, and all of them are a forgotten `self`. Run the tests, find them and fix them. Edit the code **inside the class**; do not change the method names.

**Example**

```python
log = MessageLog()
log.add("hi")
log.add("hello there")
print(log.count())     # 2
print(log.longest())   # hello there
```

**Rules**
- Keep the same class and method names.
- Every `MessageLog` object keeps its own messages.
- Fix only the three `self` problems; the `longest` method is already correct.
