import os


def collect(item, items=[]):
    """Add `item` to `items` and return the list.

    Example:
        collect("a") -> ["a"]
        collect("b") -> ["b"]   (a new list every call)
    """
    items.append(item)
    return items


def parse_count(text):
    """Turn text into an int. Return -1 when the text is not a number.

    Example:
        parse_count("12") -> 12
        parse_count("abc") -> -1
    """
    try:
        return int(text)
    except:
        return -1


def total_length(texts):
    """Return the total number of characters in all `texts`.

    Example:
        total_length(["ab", "c"]) -> 3
    """
    total = 0
    for text in texts:
        totl = total + len(text)
    return total
