# A family of models

**What it shows:** one base class and three subclasses that all answer `generate` in their own way, used in one loop.

**Step by step**
1. Lines 2-10 define `Model`: it stores a name, has a `generate` that must be overridden (it raises `NotImplementedError`), and a `describe` that every child inherits.
2. Lines 13-15 define `EchoModel`. It only overrides `generate`; `__init__` and `describe` come from `Model`.
3. Lines 18-24 define `CannedModel`. Its `__init__` calls `super().__init__(name)` first, then adds `reply`.
4. Lines 27-33 define `ChatModel` the same way, with a `system` text that it puts in front of the prompt.
5. Lines 36-44 put one of each in a list. The loop does not care which kind it holds: it calls `describe`, `generate` and `isinstance` the same way every time.

**Notice:** `describe` is written once, in `Model`, and works for all three children.

**Try it yourself:** add a `ShoutModel(Model)` whose `generate` returns `prompt.upper()`, and add it to the list. You should get one more block of three lines.
