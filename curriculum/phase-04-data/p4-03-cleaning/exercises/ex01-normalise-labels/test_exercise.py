import pandas as pd

from exercise import normalise_labels


def test_strips_lowercases_and_replaces_separators():
    labels = pd.Series([" Bug_Report ", "FEATURE-REQ", "  Account_Help-desk "])
    result = normalise_labels(labels)
    assert isinstance(result, pd.Series), "return a pandas Series, not a list"
    assert result.tolist() == ["bug report", "feature req", "account help desk"]


def test_preserves_original_index():
    labels = pd.Series([" A_B ", "C-D"], index=[10, 20])
    result = normalise_labels(labels)
    assert result.index.tolist() == [10, 20], "preserve the input Series index"
    assert result.tolist() == ["a b", "c d"]


def test_handles_empty_series():
    labels = pd.Series([], dtype="object")
    result = normalise_labels(labels)
    assert result.tolist() == []


def test_does_not_modify_input_series():
    labels = pd.Series([" Raw_Label ", "OTHER-ONE"])
    snapshot = labels.tolist()
    _ = normalise_labels(labels)
    assert labels.tolist() == snapshot, "do not mutate the input Series"
