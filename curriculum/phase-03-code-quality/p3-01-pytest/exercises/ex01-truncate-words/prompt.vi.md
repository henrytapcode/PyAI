Trước khi đưa một tài liệu dài vào prompt, bạn thường cắt nó theo một ngân sách số từ. Hãy viết `truncate_words(text, limit)`: giữ tối đa `limit` từ của `text`, nối chúng bằng một dấu cách, và thêm `...` khi phải cắt bớt. Viết code bên trong hàm và `return` đáp án. Các test bên dưới chính là những test sẽ chấm bài của bạn, nên hãy đọc chúng như một bản đặc tả.

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

**Ví dụ**

| lời gọi | kết quả |
|---|---|
| `truncate_words("one two three four", 2)` | `"one two..."` |
| `truncate_words("one two three", 3)` | `"one two three"` |
| `truncate_words("", 3)` | `""` |

**Quy tắc**
- Các từ được ngăn cách bởi bất kỳ khoảng trắng nào. Kết quả dùng đúng một dấu cách giữa các từ và không có dấu cách ở hai đầu.
- Chỉ thêm `...` (ngay sau từ cuối) khi có từ bị cắt đi.
- Nếu `limit` là số âm, `raise ValueError`.
