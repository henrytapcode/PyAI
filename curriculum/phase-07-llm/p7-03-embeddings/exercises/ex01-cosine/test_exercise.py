import pytest
from exercise import cosine_sim


def test_same_direction_returns_one():
    result = cosine_sim([3.0, 4.0], [6.0, 8.0])
    assert result is not None, "cosine_sim returned None: did you fill in all blanks?"
    assert type(result) is float
    assert result == 1.0


def test_perpendicular_vectors_return_zero():
    result = cosine_sim([1.0, 0.0], [0.0, 1.0])
    assert result == 0.0


def test_opposite_vectors_return_minus_one():
    result = cosine_sim([2.0, -1.0], [-2.0, 1.0])
    assert result == -1.0


def test_scaling_does_not_change_similarity():
    base = cosine_sim([1.0, 2.0, 3.0], [2.0, 3.0, 4.0])
    scaled = cosine_sim([10.0, 20.0, 30.0], [200.0, 300.0, 400.0])
    assert base == pytest.approx(0.993, abs=1e-3)
    assert scaled == base


def test_zero_vector_returns_zero():
    assert cosine_sim([0.0, 0.0], [1.0, 2.0]) == 0.0
    assert cosine_sim([1.0, 2.0], [0.0, 0.0]) == 0.0


def test_different_lengths_raise_value_error():
    with pytest.raises(ValueError):
        cosine_sim([1.0, 2.0], [1.0, 2.0, 3.0])
