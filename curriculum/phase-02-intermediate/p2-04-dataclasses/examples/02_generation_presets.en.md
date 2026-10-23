# Generation presets

**What it shows:** a frozen dataclass with defaults, used as a set of read-only settings. Presets are stored in a dict and described with a method.

**Step by step**
1. Lines 5–9 define `GenerationConfig`. `model` is required; `temperature` and `max_tokens` have defaults. `frozen=True` makes every object read-only.
2. Lines 11–19 add two methods. `describe` calls `is_deterministic` through `self`, which is allowed because a dataclass is a normal class.
3. Lines 22–26 create three presets. Each one only spells out the fields that differ from the defaults.
4. Lines 28–29 loop over the dict and print each preset's description.
5. Lines 31–35 try to change a value. The frozen object refuses, and the `except AttributeError` branch runs.
6. Lines 38–40 build a **new** config from the old one with a lower temperature. The two objects differ, so `==` gives `False`.

**Notice:** "changing" a frozen object means building a new one. That keeps the original safe for any other part of the program that still uses it.

**Try it yourself:** remove `frozen=True` from line 5. The line `config.temperature = 2.0` now works, and `presets are read-only` is no longer printed.
