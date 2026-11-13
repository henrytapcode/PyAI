import pandas as pd

from exercise import clean_ratings


def test_cleans_users_coerces_ratings_and_filters_range():
    df = pd.DataFrame({
        "user": [" An ", "Binh", "Chi", "Dung", "Em", "Gia"],
        "rating": [" 4 ", "five", "", None, "7", "0"],
    })
    result = clean_ratings(df)
    assert result.to_dict("list") == {"user": ["an"], "rating": [4]}


def test_keeps_last_valid_rating_for_duplicate_users():
    df = pd.DataFrame({
        "user": [" An ", "Binh", "an", "binh"],
        "rating": [" 2 ", "5", "4", "bad"],
    })
    result = clean_ratings(df)
    assert result.to_dict("list") == {
        "user": ["binh", "an"],
        "rating": [5, 4],
    }, "normalise user before deduplicating and keep the last valid rating"


def test_rating_dtype_is_int64_and_columns_ordered():
    df = pd.DataFrame({
        "extra": ["x", "y"],
        "rating": ["1", " 5 "],
        "user": ["A", "B"],
    })
    result = clean_ratings(df)
    assert list(result.columns) == ["user", "rating"]
    assert str(result["rating"].dtype) == "int64", "cast rating to int64 after dropping NaNs"
    assert result.to_dict("list") == {"user": ["a", "b"], "rating": [1, 5]}


def test_resets_index_starting_from_zero():
    df = pd.DataFrame({
        "user": ["a", "b", "c"],
        "rating": ["bad", "3", "5"],
    })
    result = clean_ratings(df)
    assert result.index.tolist() == [0, 1], "reset index with drop=True"


def test_returns_empty_two_column_dataframe_when_all_rows_invalid():
    df = pd.DataFrame({
        "user": ["An", "Binh", "Chi"],
        "rating": ["five", None, "9"],
    })
    result = clean_ratings(df)
    assert list(result.columns) == ["user", "rating"]
    assert str(result["rating"].dtype) == "int64"
    assert result.to_dict("list") == {"user": [], "rating": []}


def test_does_not_modify_input_dataframe():
    df = pd.DataFrame({
        "user": [" An ", "an"],
        "rating": [" 4 ", "five"],
    })
    snapshot = df.to_dict("list")
    _ = clean_ratings(df)
    assert df.to_dict("list") == snapshot, "do not mutate the input DataFrame"
