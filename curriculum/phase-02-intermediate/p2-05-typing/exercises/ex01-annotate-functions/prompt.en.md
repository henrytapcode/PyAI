Four functions below are already written, but their type hints are missing. Replace every `___` with the right hint, so that each hint tells the truth about what the function takes and returns. Do not change the code inside the functions.

**Example**

| function | what goes in | what comes out |
|---|---|---|
| `count_tokens(["Hello", "world"])` | a list of texts | `2` |
| `build_prompt("Hi")` | a question, no system prompt | `"Hi"` |
| `build_prompt("Hi", "Be brief.")` | a question and a system prompt | `"Be brief.\nHi"` |
| `word_lengths(["hi", "hello"])` | a list of words | `{"hi": 2, "hello": 5}` |
| `first_and_count(["a", "b"])` | a list of tokens | `("a", 2)` |

**Rules**
- Replace all 5 blanks with hints. Use the built-in forms such as `list[str]` and `str | None`.
- `build_prompt` must keep working without a system prompt, so its `system` hint must allow `None`.
- Keep the function names, parameter names and default value.
- Python does not check hints, so the tests read the hints stored in `__annotations__` (the way a type checker would) and also call each function.
