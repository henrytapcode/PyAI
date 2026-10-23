def count_tokens(tokens: list[str]) -> int:
    """Return how many tokens there are.

    Example: count_tokens(["Hello", "world"]) -> 2
    """
    return len(tokens)


def build_prompt(question: str, system: str | None = None) -> str:
    """Put the system prompt (if there is one) before the question.

    Example: build_prompt("Hi") -> "Hi"
             build_prompt("Hi", "Be brief.") -> "Be brief." + newline + "Hi"
    """
    if system is None:
        return question
    return system + "\n" + question


def word_lengths(words: list[str]) -> dict[str, int]:
    """Map each word to its length.

    Example: word_lengths(["hi", "hello"]) -> {"hi": 2, "hello": 5}
    """
    lengths = {}
    for word in words:
        lengths[word] = len(word)
    return lengths


def first_and_count(tokens: list[str]) -> tuple[str, int]:
    """Return the first token and the number of tokens.

    Example: first_and_count(["a", "b"]) -> ("a", 2)
    """
    return tokens[0], len(tokens)
