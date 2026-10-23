def count_vowels(text):
    """Return how many lowercase vowels (a, e, i, o, u) are in text."""
    count = 0
    for letter in text:
        if letter not in "aeiou":
            continue
        count += 1
    return count
