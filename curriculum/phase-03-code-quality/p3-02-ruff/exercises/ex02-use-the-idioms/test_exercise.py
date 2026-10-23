from exercise import describe, is_unknown, switch_state


class AlwaysEqual:
    """An object whose == answers True to anything, like some data-frame types do."""

    def __eq__(self, other):
        return True

    def __hash__(self):
        return 0

    def __len__(self):
        return 3


def test_none_means_no_data():
    assert describe(None) == "no data"


def test_a_list_reports_its_row_count():
    assert describe([1, 2]) == "got 2 rows"


def test_an_empty_list_is_data_not_none():
    assert describe([]) == "got 0 rows"


def test_describe_uses_is_none_not_equals():
    assert describe(AlwaysEqual()) == "got 3 rows", "use `is None`: `== None` can lie (E711)"


def test_a_missing_label_is_unknown():
    assert is_unknown("eggs", {"spam", "ham"}) is True


def test_a_present_label_is_not_unknown():
    assert is_unknown("ham", {"spam", "ham"}) is False


def test_a_non_empty_text_switches_on():
    assert switch_state("yes") == "on", "use `if flag:`, not `if flag == True:` (E712)"


def test_true_and_numbers():
    assert switch_state(True) == "on"
    assert switch_state(5) == "on"
    assert switch_state(0) == "off"
    assert switch_state("") == "off"
