Before a long document goes into a prompt, you often cut it to a word budget. Write `truncate_words(text, limit)`: it keeps at most `limit` words of `text`, joins them with single spaces, and adds `...` when it had to cut something. Write your code inside the function and `return` the answer. The tests below are exactly the tests that will check you, so read them as the spec.

```text
import pytest

from exercise import truncate_words


def test_short_text_is_unchanged():
    assert truncate_words("hello world", 5) == "hello world"


def test_long_text_is_cut_and_marked():
    assert truncate_words("one two three four", 2) == "one two..."


def test_exact_limit_is_not_marked():
    assert truncate_words("one two three", 3) == "one two three"


def test_empty_text_gives_empty_text():
    assert truncate_words("", 3) == ""


def test_extra_spaces_are_collapsed():
    assert truncate_words("  one   two  ", 5) == "one two"


def test_zero_limit_cuts_everything():
    assert truncate_words("one two", 0) == "..."


def test_negative_limit_raises_value_error():
    with pytest.raises(ValueError):
        truncate_words("one two", -1)
```

**Example**

| call | result |
|---|---|
| `truncate_words("one two three four", 2)` | `"one two..."` |
| `truncate_words("one two three", 3)` | `"one two three"` |
| `truncate_words("", 3)` | `""` |

**Rules**
- Words are separated by any whitespace. The result uses exactly one space between words and none at the ends.
- Add `...` (directly after the last word) only when words were cut off.
- If `limit` is negative, `raise ValueError`.
