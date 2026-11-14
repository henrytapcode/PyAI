from exercise import count_tokens


def test_counts_known_sentences():
    result = count_tokens(["Great!", "Chatbot logs!"])
    assert result is not None, "count_tokens returned None: did you forget to return counts?"
    assert result == [2, 4], "remember not to count [CLS] and [SEP]"


def test_empty_string_returns_zero():
    result = count_tokens([""])
    assert result is not None, "count_tokens returned None: did you forget to return counts?"
    assert result == [0]


def test_uppercase_and_lowercase_give_same_counts():
    upper = count_tokens(["FAST Answer", "CHATBOT LOGS!"])
    lower = count_tokens(["fast answer", "chatbot logs!"])
    assert upper == lower


def test_empty_list_returns_empty_list():
    result = count_tokens([])
    assert result is not None, "count_tokens returned None: did you forget to return counts?"
    assert result == []


def test_elements_are_python_ints():
    result = count_tokens(["Hello world", "Great!"])
    assert result is not None, "count_tokens returned None: did you forget to return counts?"
    assert all(type(item) is int for item in result)
