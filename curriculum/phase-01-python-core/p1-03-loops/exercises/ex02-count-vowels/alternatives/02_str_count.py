def count_vowels(text):
    """Return how many lowercase vowels (a, e, i, o, u) are in text."""
    count = 0
    for vowel in "aeiou":
        count += text.count(vowel)
    return count
