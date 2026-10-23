def count_vowels(text):
    """Return how many lowercase vowels (a, e, i, o, u) are in text.

    Example: count_vowels("banana") -> 3
    """
    # TODO: this runs, but count_vowels("banana") gives 1 instead of 3.
    #       Find the bug and fix it.
    count = 0
    for letter in text:
        if letter in "aeiou":
            count = 1
    return count
