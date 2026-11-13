import pandas as pd

from exercise import slow_requests


def test_filters_strictly_above_limit_and_sorts_descending():
    df = pd.DataFrame({
        "endpoint": ["/chat", "/health", "/embed", "/search"],
        "latency_ms": [200, 350, 520, 150],
        "status": [200, 200, 500, 200],
    })
    result = slow_requests(df, 200)
    assert list(result.columns) == ["endpoint", "latency_ms"]
    assert result.to_dict("list") == {
        "endpoint": ["/embed", "/health"],
        "latency_ms": [520, 350],
    }, "filter strictly > limit_ms and sort descending"


def test_resets_index_starting_from_zero():
    df = pd.DataFrame({
        "endpoint": ["/a", "/b", "/c"],
        "latency_ms": [100, 400, 300],
    })
    result = slow_requests(df, 200)
    assert result.index.tolist() == [0, 1], "reset index with drop=True so rows start at 0"


def test_returns_empty_dataframe_when_none_exceed_limit():
    df = pd.DataFrame({
        "endpoint": ["/chat", "/health"],
        "latency_ms": [120, 200],
    })
    result = slow_requests(df, 200)
    assert list(result.columns) == ["endpoint", "latency_ms"]
    assert result.to_dict("list") == {"endpoint": [], "latency_ms": []}


def test_does_not_modify_input_dataframe():
    df = pd.DataFrame({
        "endpoint": ["/chat", "/embed"],
        "latency_ms": [100, 500],
        "status": [200, 500],
    })
    snapshot = df.to_dict("list")
    _ = slow_requests(df, 200)
    assert df.to_dict("list") == snapshot, "do not mutate the input DataFrame"
