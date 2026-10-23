import logging

import pytest

from exercise import load_scores


def test_returns_the_good_scores_in_order(caplog):
    with caplog.at_level(logging.DEBUG):
        result = load_scores(["10", "7", "3"])
    assert result == [10, 7, 3]


def test_returns_only_the_good_scores_when_some_are_bad(caplog):
    with caplog.at_level(logging.DEBUG):
        result = load_scores(["5", "abc", "x1", "8"])
    assert result == [5, 8], "skip the bad texts and keep the good ones in order"


def test_logs_one_info_record_with_the_counts(caplog):
    with caplog.at_level(logging.DEBUG):
        load_scores(["10", "7", "3"])
    assert len(caplog.records) == 1, "a clean list should produce exactly one log record"
    assert caplog.records[0].levelname == "INFO"
    assert caplog.records[0].getMessage() == "loaded 3 of 3 scores"


def test_logs_one_warning_for_each_bad_score(caplog):
    with caplog.at_level(logging.DEBUG):
        load_scores(["5", "abc", "x1", "8"])
    warnings = [r for r in caplog.records if r.levelname == "WARNING"]
    assert [r.getMessage() for r in warnings] == [
        "skipping bad score: abc",
        "skipping bad score: x1",
    ]


def test_the_summary_is_the_last_record_and_counts_only_good_scores(caplog):
    with caplog.at_level(logging.DEBUG):
        load_scores(["5", "abc", "x1", "8"])
    last = caplog.records[-1]
    assert last.levelname == "INFO"
    assert last.getMessage() == "loaded 2 of 4 scores"


def test_logs_exactly_one_record_per_event(caplog):
    with caplog.at_level(logging.DEBUG):
        load_scores(["5", "abc", "x1", "8"])
    assert len(caplog.records) == 3, "two warnings and one summary, nothing else"


def test_empty_list_logs_only_the_summary(caplog):
    with caplog.at_level(logging.DEBUG):
        result = load_scores([])
    assert result == []
    assert [(r.levelname, r.getMessage()) for r in caplog.records] == [
        ("INFO", "loaded 0 of 0 scores")
    ]


def test_uses_logging_not_print(capsys, caplog):
    with caplog.at_level(logging.DEBUG):
        load_scores(["1", "oops"])
    assert capsys.readouterr().out == "", "use logger.warning / logger.info instead of print"


@pytest.mark.parametrize(
    "raw, expected_message",
    [
        (["1"], "loaded 1 of 1 scores"),
        (["x", "y"], "loaded 0 of 2 scores"),
        (["4", "5", "z"], "loaded 2 of 3 scores"),
    ],
)
def test_summary_message_for_different_inputs(caplog, raw, expected_message):
    with caplog.at_level(logging.DEBUG):
        load_scores(raw)
    assert caplog.records[-1].getMessage() == expected_message
