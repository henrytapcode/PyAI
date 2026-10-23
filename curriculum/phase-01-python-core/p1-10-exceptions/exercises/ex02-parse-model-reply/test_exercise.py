import pytest

from exercise import count_unknown, parse_reply

UNKNOWN = {"label": "unknown", "score": 0.0}


def test_good_reply_is_parsed():
    result = parse_reply('{"label": "spam", "score": 0.9}')
    assert result == {"label": "spam", "score": 0.9}


def test_extra_keys_are_ignored():
    result = parse_reply('{"label": "ham", "score": 0.25, "note": "ok"}')
    assert result == {"label": "ham", "score": 0.25}


def test_chatty_text_gives_unknown():
    assert parse_reply("Sure! Here is the JSON you asked for.") == UNKNOWN


def test_empty_text_gives_unknown():
    assert parse_reply("") == UNKNOWN


@pytest.mark.parametrize("text", [
        '{"label": "ham"}',
        '{"score": 0.5}',
        '["spam", 0.9]',
        '{"label": "ham", "score": "high"}',
    ])
def test_missing_or_wrong_shape_gives_unknown(text):
    assert parse_reply(text) == UNKNOWN


@pytest.mark.parametrize("score", ["1.5", "-0.1"])
def test_score_out_of_range_gives_unknown(score):
    text = '{"label": "ham", "score": ' + score + "}"
    assert parse_reply(text) == UNKNOWN


@pytest.mark.parametrize("score", ["0", "1"])
def test_limits_are_valid_scores(score):
    text = '{"label": "ham", "score": ' + score + "}"
    assert parse_reply(text)["label"] == "ham"


def test_count_unknown_counts_only_bad_replies():
    replies = [
        '{"label": "ham", "score": 0.5}',
        "hello",
        '{"label": "spam"}',
        '{"label": "spam", "score": 0.8}',
    ]
    assert count_unknown(replies) == 2


def test_count_unknown_of_empty_list_is_zero():
    assert count_unknown([]) == 0
