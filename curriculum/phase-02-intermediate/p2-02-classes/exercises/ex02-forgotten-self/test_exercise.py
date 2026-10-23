from exercise import MessageLog


def test_new_log_is_empty():
    log = MessageLog()
    assert log.count() == 0, "__init__ must store the list as self.messages"


def test_add_stores_a_message():
    log = MessageLog()
    log.add("hi")
    assert log.count() == 1, "add needs self as its first parameter"


def test_count_after_several_messages():
    log = MessageLog()
    for text in ["a", "bb", "ccc"]:
        log.add(text)
    assert log.count() == 3


def test_add_returns_nothing():
    log = MessageLog()
    assert log.add("hi") is None


def test_longest_message():
    log = MessageLog()
    log.add("hi")
    log.add("hello there")
    log.add("hey")
    assert log.longest() == "hello there"


def test_longest_returns_first_when_tied():
    log = MessageLog()
    log.add("abc")
    log.add("xyz")
    assert log.longest() == "abc"


def test_longest_of_empty_log_is_empty_text():
    assert MessageLog().longest() == ""


def test_each_log_keeps_its_own_messages():
    first = MessageLog()
    second = MessageLog()
    first.add("one")
    first.add("two")
    second.add("only")
    assert first.count() == 2
    assert second.count() == 1
    assert second.longest() == "only"

