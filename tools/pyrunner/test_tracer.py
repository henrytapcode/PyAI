import pytest

from tools.pyrunner.tracer import MAX_TABLE_COLS, MAX_TABLE_ROWS, trace


def _last_var(code: str, name: str) -> dict:
    result = trace(code)
    assert result["error"] is None
    last_step = result["steps"][-1]
    for frame in reversed(last_step["stack"]):
        for var in frame["vars"]:
            if var["name"] == name:
                return var
    raise AssertionError(f"Variable {name!r} not found in final step")


def test_dataframe_basic():
    code = """
import pandas as pd
df = pd.DataFrame(
    {"tokens": [100, 200, 300], "score": [0.9, 0.85, 0.7]},
    index=["a", "b", "c"],
)
"""
    var = _last_var(code, "df")
    assert var["type"] == "DataFrame"
    assert var["table"] == {
        "kind": "dataframe",
        "shape": [3, 2],
        "columns": ["tokens", "score"],
        "index": ["a", "b", "c"],
        "rows": [["100", "0.9"], ["200", "0.85"], ["300", "0.7"]],
    }


def test_series_named_and_unnamed():
    code = """
import pandas as pd
s_named = pd.Series([10, 20, 30], name="score", index=["r1", "r2", "r3"])
s_unnamed = pd.Series([1, 2])
"""
    named = _last_var(code, "s_named")
    assert named["table"] == {
        "kind": "series",
        "shape": [3, 1],
        "columns": ["score"],
        "index": ["r1", "r2", "r3"],
        "rows": [["10"], ["20"], ["30"]],
    }
    unnamed = _last_var(code, "s_unnamed")
    assert unnamed["table"] == {
        "kind": "series",
        "shape": [2, 1],
        "columns": [""],
        "index": ["0", "1"],
        "rows": [["1"], ["2"]],
    }


def test_ndarray_2d_and_non_2d():
    code = """
import numpy as np
mat = np.array([[1, 2, 3], [4, 5, 6]])
vec = np.array([1, 2, 3])
cube = np.zeros((2, 2, 2))
scalar = np.float64(3.5)
"""
    mat = _last_var(code, "mat")
    assert mat["table"] == {
        "kind": "array",
        "shape": [2, 3],
        "columns": ["0", "1", "2"],
        "index": ["0", "1"],
        "rows": [["1", "2", "3"], ["4", "5", "6"]],
    }
    for non_2d in ("vec", "cube", "scalar"):
        assert "table" not in _last_var(code, non_2d)


def test_dataframe_truncated_to_limits():
    code = """
import pandas as pd
df = pd.DataFrame({f"c{c}": list(range(20)) for c in range(10)})
"""
    var = _last_var(code, "df")
    table = var["table"]
    assert table["shape"] == [20, 10]
    assert len(table["rows"]) == MAX_TABLE_ROWS
    assert len(table["index"]) == MAX_TABLE_ROWS
    assert len(table["columns"]) == MAX_TABLE_COLS
    assert all(len(row) == MAX_TABLE_COLS for row in table["rows"])


@pytest.mark.parametrize(
    ("expr", "expected"),
    [
        ("float('nan')", "NaN"),
        ("0.1 + 0.2", "0.3"),
        ("np.float64(0.1 + 0.2)", "0.3"),
        ("np.float64('nan')", "NaN"),
        ("np.bool_(True)", "True"),
        ("None", "None"),
        ("'a' * 30", "a" * 23 + "…"),
    ],
)
def test_cell_formatting(expr: str, expected: str):
    code = f"""
import numpy as np
import pandas as pd
df = pd.DataFrame({{"v": [{expr}]}})
"""
    var = _last_var(code, "df")
    assert var["table"]["rows"] == [[expected]]
    assert "np.float64" not in var["table"]["rows"][0][0]


def test_numpy_float_in_ndarray_no_np_repr():
    code = """
import numpy as np
arr = np.array([[0.1 + 0.2, np.nan]])
"""
    var = _last_var(code, "arr")
    assert var["table"]["rows"] == [["0.3", "NaN"]]


def test_plain_python_has_no_table_key():
    code = """
x = [1, 2]
y = {"a": 1}
"""
    x_var = _last_var(code, "x")
    y_var = _last_var(code, "y")
    assert set(x_var.keys()) == {"name", "type", "repr"}
    assert set(y_var.keys()) == {"name", "type", "repr"}


def test_broken_cell_does_not_leak_stdout_or_crash_trace():
    code = """
import pandas as pd

class Loud:
    def __str__(self):
        print("LEAKED")
        return "ok"

class Broken:
    def __str__(self):
        raise RuntimeError("boom")

df_loud = pd.DataFrame({"x": [Loud()]})
df_broken = pd.DataFrame({"x": [Broken()]})
"""
    result = trace(code)
    assert result["error"] is None
    assert "LEAKED" not in result["stdout"]
    last_vars = {v["name"]: v for v in result["steps"][-1]["stack"][-1]["vars"]}
    assert last_vars["df_loud"]["table"]["rows"] == [["ok"]]
    assert "table" not in last_vars["df_broken"]
