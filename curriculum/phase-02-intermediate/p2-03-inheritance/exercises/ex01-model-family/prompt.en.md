Write two classes. `Model` is a base class. `CannedModel` is a subclass that answers with ready-made replies, one after another, and starts over after the last one. Write your code inside the methods and `return` the answer. (`pass` means "do nothing yet": replace it with your code.)

**Example**

```python
bot = CannedModel("c1", ["Hi!", "Bye!"])
bot.generate("anything")   # "Hi!"
bot.generate("anything")   # "Bye!"
bot.generate("anything")   # "Hi!"  (starts over)
bot.describe()             # "model: c1 (2 replies)"
```

**Rules**
- `Model(name)` stores the name in `self.name`.
- `Model.generate(prompt)` must raise `NotImplementedError`: children have to write it.
- `Model.describe()` returns `"model: "` followed by the name, for example `"model: base"`.
- `CannedModel(name, replies)` inherits from `Model`, sets the name by calling `super().__init__`, and keeps the list in `self.replies`.
- `CannedModel.generate(prompt)` ignores the prompt and returns the next reply. Each `CannedModel` object counts its own calls. Tip: `i % n` is the remainder of `i` divided by `n`, so `5 % 3` is `2`.
- `CannedModel.describe()` uses `super().describe()` and adds a space and `(N replies)` at the end, where `N` is the number of replies. Write `replies` even when `N` is 1.

Press **Check** to run the tests.
