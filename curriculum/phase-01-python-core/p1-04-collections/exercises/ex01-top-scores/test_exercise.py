from exercise import word_count


def test_returns_empty_dict_for_empty_list():
    assert word_count([]) == {}


def test_counts_a_single_word():
    assert word_count(["ai"]) == {"ai": 1}


def test_counts_repeated_words():
    assert word_count(["ai", "is", "fun", "ai"]) == {"ai": 2, "is": 1, "fun": 1}


def test_words_are_case_sensitive():
    assert word_count(["AI", "ai", "AI"]) == {"AI": 2, "ai": 1}


def test_counts_a_longer_sentence():
    words = ["to", "be", "or", "not", "to", "be"]
    assert word_count(words) == {"to": 2, "be": 2, "or": 1, "not": 1}
