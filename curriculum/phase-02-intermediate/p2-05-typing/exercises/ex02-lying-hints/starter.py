def average_length(words: list[str]) -> int:
    """Return the average length of the words.

    Example: average_length(["ab", "abcd"]) -> 3.0. An empty list gives 0.0.
    """
    if len(words) == 0:
        return 0.0
    total = 0
    for word in words:
        total += len(word)
    return total / len(words)


def find_system(messages: list[dict[str, str]]) -> str:
    """Return the text of the first message whose role is "system".

    Return None if there is no such message.
    """
    for message in messages:
        if message["role"] == "system":
            return message["text"]
    return None


def repeat(word: int, times: int) -> str:
    """Repeat a word. Example: repeat("ab", 2) -> "abab"."""
    return word * times


def shout(text: str) -> str:
    """Return the text in capital letters. Example: shout("hi") -> "HI"."""
    text.upper()
