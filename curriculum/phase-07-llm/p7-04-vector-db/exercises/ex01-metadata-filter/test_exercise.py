import pytest
from exercise import filter_indexes, matches


@pytest.mark.parametrize(
    ("metadata", "where", "expected"),
    [
        ({"lang": "vi", "topic": "faq"}, None, True),
        ({"lang": "vi", "topic": "faq"}, {}, True),
        ({"lang": "vi", "topic": "faq"}, {"lang": "vi"}, True),
        ({"lang": "vi", "topic": "faq"}, {"lang": "vi", "topic": "faq"}, True),
        ({"lang": "vi"}, {"lang": "vi", "topic": "faq"}, False),
        ({"lang": "en", "topic": "faq"}, {"lang": "vi"}, False),
    ],
)
def test_matches_metadata_cases(metadata, where, expected):
    result = matches(metadata, where)
    assert result is not None, "matches returned None: did you fill in all blanks?"
    assert result is expected


def test_matches_missing_key_with_none_value_is_false():
    assert matches({}, {"lang": None}) is False


def test_filter_indexes_preserves_order():
    metadatas = [
        {"lang": "en", "topic": "billing"},
        {"lang": "vi", "topic": "billing"},
        {"lang": "vi", "topic": "support"},
        {"lang": "vi", "topic": "billing"},
        {"lang": "en", "topic": "billing"},
    ]
    assert filter_indexes(metadatas, {"lang": "vi", "topic": "billing"}) == [1, 3]
    assert filter_indexes(metadatas, None) == [0, 1, 2, 3, 4]
    assert filter_indexes(metadatas, {"topic": "travel"}) == []
