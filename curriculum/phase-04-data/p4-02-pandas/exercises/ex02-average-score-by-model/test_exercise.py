import pandas as pd

from exercise import average_score_by_model


def test_averages_ok_rows_and_skips_error_models():
    df = pd.DataFrame({
        "model": ["gpt-4o", "gpt-4o", "claude", "llama"],
        "status": ["ok", "ok", "error", "ok"],
        "score": [0.90, 0.96, 0.0, 0.80],
    })
    result = average_score_by_model(df)
    assert result == {"gpt-4o": 0.93, "llama": 0.8}
    assert "claude" not in result, "models with no 'ok' rows must not appear"


def test_rounds_means_to_two_decimal_places():
    df = pd.DataFrame({
        "model": ["m1", "m1", "m1", "m2", "m2"],
        "status": ["ok", "ok", "ok", "ok", "error"],
        "score": [0.80, 0.90, 0.90, 0.75, 0.10],
    })
    result = average_score_by_model(df)
    assert result == {"m1": 0.87, "m2": 0.75}


def test_returns_plain_python_floats():
    df = pd.DataFrame({
        "model": ["gpt-4o", "gpt-4o"],
        "status": ["ok", "ok"],
        "score": [0.81, 0.83],
    })
    result = average_score_by_model(df)
    assert type(result) is dict
    assert all(type(v) is float for v in result.values()), (
        "values must be plain Python float, not np.float64"
    )


def test_returns_empty_dict_when_no_rows_are_ok():
    df = pd.DataFrame({
        "model": ["gpt-4o", "claude"],
        "status": ["error", "timeout"],
        "score": [0.0, 0.0],
    })
    assert average_score_by_model(df) == {}


def test_returns_empty_dict_for_empty_dataframe():
    df = pd.DataFrame({"model": [], "status": [], "score": []})
    assert average_score_by_model(df) == {}


def test_does_not_modify_input_dataframe():
    df = pd.DataFrame({
        "model": ["gpt-4o", "claude"],
        "status": ["ok", "error"],
        "score": [0.9, 0.2],
    })
    snapshot = df.to_dict("list")
    _ = average_score_by_model(df)
    assert df.to_dict("list") == snapshot, "do not mutate the input DataFrame"
