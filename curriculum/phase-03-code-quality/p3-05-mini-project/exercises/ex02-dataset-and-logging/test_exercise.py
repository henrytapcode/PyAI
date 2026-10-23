import logging

import pytest

from exercise import CleanConfig, CleanReport, clean_dataset

SAMPLE = [
    "Hello   world",
    "hello world",
    "",
    "   ",
    42,
    "Buy https://x.io",
    "Second doc",
]


@pytest.fixture
def report():
    return clean_dataset(SAMPLE)


def test_an_empty_list_gives_an_empty_report():
    assert clean_dataset([]) == CleanReport(kept=[], skipped=0, empty=0, duplicates=0)


def test_kept_texts_are_clean_and_in_the_original_order(report):
    assert report.kept == ["hello world", "buy", "second doc"]


def test_non_strings_are_skipped(report):
    assert report.skipped == 1


def test_empty_results_are_counted(report):
    assert report.empty == 2, "both '' and '   ' are empty after cleaning"


def test_duplicates_are_counted_after_cleaning(report):
    assert report.duplicates == 1, "'Hello   world' and 'hello world' are the same once cleaned"


def test_the_config_is_used():
    report = clean_dataset(["A", "a"], CleanConfig(lowercase=False))
    assert report.kept == ["A", "a"]
    assert report.duplicates == 0


def test_a_non_string_item_logs_one_warning_with_its_position(caplog):
    with caplog.at_level(logging.DEBUG):
        clean_dataset(SAMPLE)
    warnings = [r for r in caplog.records if r.levelname == "WARNING"]
    assert len(warnings) == 1
    assert warnings[0].getMessage() == "skipping item 4: not a string"


def test_one_info_summary_line_is_logged(caplog):
    with caplog.at_level(logging.DEBUG):
        clean_dataset(SAMPLE)
    infos = [r for r in caplog.records if r.levelname == "INFO"]
    assert len(infos) == 1, "log one summary line, not one line per text"
    assert infos[0].getMessage() == "kept 3 of 7 texts"


def test_empty_and_duplicate_texts_are_not_logged_above_debug(caplog):
    with caplog.at_level(logging.INFO):
        clean_dataset(["", "a", "a"])
    assert [r.levelname for r in caplog.records] == ["INFO"]


def test_the_input_list_is_not_changed():
    texts = ["  A  ", None]
    clean_dataset(texts)
    assert texts == ["  A  ", None]
