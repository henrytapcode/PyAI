import numpy as np

from exercise import split_data


def test_returns_expected_split_sizes():
    X = np.arange(20.0).reshape(10, 2)
    y = np.arange(10)
    X_train, X_test, y_train, y_test = split_data(X, y, 0.2, seed=42)
    assert X_train.shape == (8, 2)
    assert X_test.shape == (2, 2)
    assert y_train.shape == (8,)
    assert y_test.shape == (2,)


def test_train_and_test_cover_all_rows_without_overlap():
    X = np.arange(16.0).reshape(8, 2)
    y = np.arange(8)
    X_train, X_test, y_train, y_test = split_data(X, y, 0.25, seed=7)
    combined_y = sorted(y_train.tolist() + y_test.tolist())
    assert combined_y == y.tolist(), "train and test together must include every row exactly once"
    combined_rows = sorted(X_train.tolist() + X_test.tolist())
    assert combined_rows == sorted(X.tolist())


def test_same_seed_gives_identical_split():
    X = np.arange(20.0).reshape(10, 2)
    y = np.arange(10)
    first = split_data(X, y, 0.3, seed=99)
    second = split_data(X, y, 0.3, seed=99)
    for arr_a, arr_b in zip(first, second, strict=True):
        assert np.array_equal(arr_a, arr_b), "same seed should produce the exact same split"


def test_features_and_labels_stay_aligned():
    row_ids = np.arange(12)
    X = np.column_stack([row_ids, row_ids * 10]).astype(float)
    y = row_ids * 100
    X_train, X_test, y_train, y_test = split_data(X, y, 0.25, seed=5)
    assert np.array_equal(y_train, X_train[:, 0] * 100), "X_train and y_train became misaligned"
    assert np.array_equal(y_test, X_test[:, 0] * 100), "X_test and y_test became misaligned"


def test_does_not_modify_input_arrays():
    X = np.arange(12.0).reshape(6, 2)
    y = np.array([0, 1, 0, 1, 0, 1])
    X_copy = X.copy()
    y_copy = y.copy()
    split_data(X, y, 0.33, seed=42)
    assert np.array_equal(X, X_copy)
    assert np.array_equal(y, y_copy)
