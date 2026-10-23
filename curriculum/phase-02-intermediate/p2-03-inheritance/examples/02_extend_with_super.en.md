# A model that counts its calls

**What it shows:** a child that keeps the parent's behavior and adds a little on top, using `super()` in three places.

**Step by step**
1. Lines 14-16: `__init__` calls `super().__init__(name)` so `self.name` exists, then adds `self.calls = 0`.
2. Lines 18-20: `generate` adds 1 to `self.calls`, then returns `super().generate(prompt)`. The real work stays in the parent.
3. Lines 22-23: `describe` takes the parent's text and adds the call count to the end.
4. Lines 26-30 create the object, print its description, call `generate` three times, and print the description again. The count went from 0 to 3.

**Notice:** the child never repeats the parent's code. If `Model.generate` changes, `CountingModel` gets the change for free.

**Try it yourself:** change the loop to use four questions. The last line should say `calls so far: 4`.
