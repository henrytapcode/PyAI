# A call log: model, check, save

**What it shows:** stage 1 of a tracker, built for a different job: a log of LLM API calls. A frozen dataclass holds one call, a function checks it, and the whole log is saved to a JSON file and read back.

**Step by step**
1. Lines 8–13 define `ApiCall` as a frozen dataclass with four fields.
2. Lines 16–22 define `check_call`. It raises `ValueError` as soon as one rule is broken, and returns nothing when everything is fine.
3. Lines 25–28 define `save_calls`. It checks **every** call first, and only then writes the file with `write_text`.
4. Lines 31–33 define `load_calls`. `ApiCall(**record)` spreads each dict into keyword arguments.
5. Lines 42–47 save three calls into a temporary folder, load them back and compare. Two lists of dataclass objects are equal when all fields are equal.
6. Lines 49–54 try to save a call with `0` tokens. The save is refused, and the old file is untouched.
7. Lines 56–59 show that a frozen object cannot be edited.

**Notice:** the bad call is refused **before** the file is touched. That is why the file still has 3 calls.

**Try it yourself:** in the `bad` call, change the last argument `0.0` to `-1.0` and the tokens (the argument before it) to `10`. Predict the message (`cost must not be negative, got -1.0`).
