import logging

from exercise import check_reply


def test_a_reply_with_text_returns_true(caplog):
    with caplog.at_level(logging.DEBUG):
        assert check_reply("hello", 1) is True


def test_a_reply_with_text_logs_one_debug_record(caplog):
    with caplog.at_level(logging.DEBUG):
        check_reply("hello", 1)
    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == "DEBUG", "a detail for bug hunting is DEBUG"
    assert caplog.records[0].getMessage() == "reply has 5 characters"


def test_an_empty_reply_returns_false(caplog):
    with caplog.at_level(logging.DEBUG):
        assert check_reply("", 1) is False


def test_an_early_empty_reply_logs_a_warning(caplog):
    with caplog.at_level(logging.DEBUG):
        check_reply("", 1)
    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == "WARNING", "something odd, but the program carries on"
    assert caplog.records[0].getMessage() == "empty reply, retrying (attempt 1)"


def test_the_last_empty_reply_logs_an_error(caplog):
    with caplog.at_level(logging.DEBUG):
        result = check_reply("", 3)
    assert result is False
    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == "ERROR", "the operation failed"
    assert caplog.records[0].getMessage() == "giving up after 3 attempts"


def test_a_custom_attempt_limit_is_respected(caplog):
    with caplog.at_level(logging.DEBUG):
        check_reply("", 2, max_attempts=2)
    assert caplog.records[0].levelname == "ERROR"
