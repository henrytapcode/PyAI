import pytest

from exercise import count_errors, error_lines


def tracked(items, seen):
    """Hand out items one by one and record every item that was read."""
    for item in items:
        seen.append(item)
        yield item


LOG = [
    "INFO model loaded\n",
    "ERROR timeout after 30s\n",
    "INFO request done\n",
    "  ERROR disk full  \n",
]


def test_yields_only_error_lines_without_spaces_or_newline():
    assert list(error_lines(LOG)) == ["ERROR timeout after 30s", "ERROR disk full"]


def test_matches_error_in_the_middle_of_a_line():
    assert list(error_lines(["2026-01-01 ERROR: boom\n"])) == ["2026-01-01 ERROR: boom"]


def test_lower_case_error_does_not_count():
    assert list(error_lines(["error in lower case\n", "Error mixed\n"])) == []


def test_no_matching_lines_gives_nothing():
    assert list(error_lines(["ok\n", "fine\n"])) == []
    assert list(error_lines([])) == []


def test_error_lines_is_a_generator():
    result = error_lines(LOG)
    assert next(result) == "ERROR timeout after 30s", "use yield so next(...) works"
    assert next(result) == "ERROR disk full"
    with pytest.raises(StopIteration):
        next(result)


def test_is_lazy_and_stops_reading_after_the_first_match():
    seen = []
    result = error_lines(tracked(["ok\n", "ERROR a\n", "ERROR b\n", "ok\n"], seen))
    assert seen == [], "nothing should be read before the first next(...)"
    assert next(result) == "ERROR a"
    assert seen == ["ok\n", "ERROR a\n"], "stop reading right after the first match"


def test_keeps_the_order_of_the_lines():
    result = list(error_lines(["ERROR 2\n", "ERROR 1\n", "ERROR 3\n"]))
    assert result == ["ERROR 2", "ERROR 1", "ERROR 3"]


def test_count_errors_counts_matching_lines():
    assert count_errors(LOG) == 2
    assert count_errors(["ERROR a\n", "ok\n", "ERROR b\n"]) == 2


def test_count_errors_returns_zero_when_there_are_none():
    assert count_errors(["ok\n"]) == 0
    assert count_errors([]) == 0


def test_count_errors_works_on_a_one_shot_generator():
    seen = []
    assert count_errors(tracked(["ERROR a\n", "ok\n", "ERROR b\n"], seen)) == 2
    assert len(seen) == 3
