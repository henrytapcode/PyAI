import numpy as np
import pytest

from exercise import min_max_scale


def test_scales_1d_array_to_zero_one_range():
    result = min_max_scale(np.array([10, 20, 30]))
    assert isinstance(result, np.ndarray), "return a NumPy ndarray"
    assert result.tolist() == pytest.approx([0.0, 0.5, 1.0])


def test_minimum_becomes_zero_and_maximum_becomes_one():
    result = min_max_scale(np.array([5.0, 12.0, 25.0, 9.0]))
    assert float(result.min()) == pytest.approx(0.0)
    assert float(result.max()) == pytest.approx(1.0)


def test_preserves_2d_shape():
    data = np.array([[0.0, 2.0], [4.0, 8.0]])
    result = min_max_scale(data)
    assert result.shape == data.shape
    assert result.ravel().tolist() == pytest.approx([0.0, 0.25, 0.5, 1.0])


def test_handles_negative_numbers():
    result = min_max_scale(np.array([-10.0, 0.0, 10.0]))
    assert result.tolist() == pytest.approx([0.0, 0.5, 1.0])


def test_does_not_modify_input_array():
    original = np.array([10.0, 20.0, 30.0])
    result = min_max_scale(original)
    assert original.tolist() == [10.0, 20.0, 30.0], "do not change the input array"
    assert result is not original
