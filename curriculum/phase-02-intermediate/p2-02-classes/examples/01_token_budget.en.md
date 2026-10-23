# Token budgets

**What it shows:** one class, two objects. Each feature (`chat`, `search`) gets its own `TokenCounter` with its own limit and its own running total.

**Step by step**
1. Lines 3–6 are `__init__`. They store the three attributes `name`, `limit` and `total` (which starts at 0).
2. Lines 8–9 are `add`. It changes the object: `self.total += n`.
3. Lines 11–12 are `remaining`. It only asks a question and **returns** the answer.
4. Lines 14–15 are `__repr__`, so `print(chat)` shows a readable line instead of a memory address.
5. Lines 18–19 build two objects from the same class. Lines 21–24 add token counts to each one in a loop.
6. Lines 28–32 loop over a list of objects. The same code works for both because both have the same methods.

**Notice:** `chat` ends at 870 and `search` at 220. Adding to one never changed the other, because each object has its own `total`.

**Try it yourself:** add a third counter, `summary = TokenCounter("summary", 50)`, call `summary.add(60)`, and add it to the list in the last loop. It should report that it is over budget by 10.
