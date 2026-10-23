import exercise


def test_lengths_maps_every_word_to_its_length():
    expected = {"token": 5, "prompt": 6, "model": 5, "ai": 2}
    assert exercise.lengths == expected


def test_lengths_is_a_dict():
    assert isinstance(exercise.lengths, dict)


def test_long_lengths_keeps_words_with_five_or_more_characters():
    expected = {"token": 5, "prompt": 6, "model": 5}
    assert exercise.long_lengths == expected, "words with exactly 5 characters must stay"


def test_long_lengths_drops_short_words():
    assert "ai" not in exercise.long_lengths


def test_long_lengths_is_built_from_lengths():
    for word, n in exercise.long_lengths.items():
        assert exercise.lengths[word] == n


def test_words_list_is_unchanged():
    assert exercise.words == ["token", "prompt", "model", "ai"]

