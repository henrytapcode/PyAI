import pandas as pd
import pytest

from exercise import load_and_clean

SAMPLE_CSV = """request_id,model,tokens,latency_ms,status,rating
r01, GPT-4o,"1,200",850,ok,5
r02,gpt_4o,900,920,ok,4
r02,gpt-4o,950,999,error,1
r03,GPT-4o ,"1,100",N/A,error,
r04,gpt_4o,800,790,error,9
r05,gpt_4o,,600,ok,4
r06,Claude ,750,620,ok,5
r07,claude,650,timeout,ok,0
r08,mini,300,210,ok,1"""


def test_returns_expected_columns_in_exact_order():
    csv_reordered = """rating,status,latency_ms,tokens,model,request_id
5,ok,200,300,mini,r01"""
    result = load_and_clean(csv_reordered)
    assert list(result.columns) == [
        "request_id",
        "model",
        "tokens",
        "latency_ms",
        "status",
        "rating",
    ]


def test_normalises_model_names():
    result = load_and_clean(SAMPLE_CSV)
    assert result["model"].tolist() == [
        "gpt-4o",
        "gpt-4o",
        "gpt-4o",
        "gpt-4o",
        "claude",
        "claude",
        "mini",
    ]


def test_parses_comma_tokens_and_casts_to_int64():
    result = load_and_clean(SAMPLE_CSV)
    assert str(result["tokens"].dtype) == "int64", "drop missing tokens first, then cast to int64"
    assert result["tokens"].tolist()[:3] == [1200, 900, 1100]


def test_coerces_bad_latency_to_nan_as_float():
    result = load_and_clean(SAMPLE_CSV)
    assert result["latency_ms"].dtype == "float64"
    assert result.loc[0, "latency_ms"] == pytest.approx(850.0)
    assert pd.isna(result.loc[2, "latency_ms"]), "N/A latency should become NaN"
    assert pd.isna(result.loc[5, "latency_ms"]), "non-numeric latency should become NaN"


def test_sets_missing_and_out_of_range_ratings_to_nan():
    result = load_and_clean(SAMPLE_CSV)
    assert result["rating"].dtype == "float64"
    assert result.loc[0, "rating"] == pytest.approx(5.0)
    assert result.loc[6, "rating"] == pytest.approx(1.0), "boundary ratings 1 and 5 are valid"
    assert pd.isna(result.loc[2, "rating"]), "blank rating should be NaN"
    assert pd.isna(result.loc[3, "rating"]), "rating 9 is out of 1..5 and should become NaN"
    assert pd.isna(result.loc[5, "rating"]), "rating 0 is out of 1..5 and should become NaN"


def test_drops_duplicate_request_ids_keeping_first():
    result = load_and_clean(SAMPLE_CSV)
    r02_rows = result[result["request_id"] == "r02"]
    assert len(r02_rows) == 1
    assert int(r02_rows.iloc[0]["tokens"]) == 900, "keep the first row when request_id repeats"
    assert r02_rows.iloc[0]["status"] == "ok"


def test_drops_rows_with_missing_or_invalid_tokens():
    csv_bad_tokens = """request_id,model,tokens,latency_ms,status,rating
r01,mini,250,100,ok,4
r02,mini,,120,ok,5
r03,mini,N/A,130,error,3"""
    result = load_and_clean(csv_bad_tokens)
    assert result["request_id"].tolist() == ["r01"]


def test_resets_index_starting_from_zero():
    result = load_and_clean(SAMPLE_CSV)
    assert result.index.tolist() == list(range(len(result)))


def test_returns_empty_dataframe_with_six_columns_when_all_rows_invalid():
    csv_all_bad = """request_id,model,tokens,latency_ms,status,rating
r01,gpt-4o,,100,ok,5
r02,mini,bad,200,error,4"""
    result = load_and_clean(csv_all_bad)
    assert len(result) == 0
    assert list(result.columns) == [
        "request_id",
        "model",
        "tokens",
        "latency_ms",
        "status",
        "rating",
    ]
    assert str(result["tokens"].dtype) == "int64"
