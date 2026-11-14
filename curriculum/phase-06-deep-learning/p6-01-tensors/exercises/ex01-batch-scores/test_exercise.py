import pytest
import torch

from exercise import score_batch


def test_computes_scores_for_multi_row_batch():
    features = torch.tensor([[1.2, 0.4, 2.0], [4.5, 2.1, 8.0], [2.0, 0.8, 3.0]])
    weights = torch.tensor([0.4, 1.1, 0.15])
    result = score_batch(features, weights, bias=-0.5)
    assert result is not None, "score_batch returned None: did you forget to return the value?"
    assert result == pytest.approx([0.72, 4.81, 1.63])


def test_returns_list_of_python_floats():
    features = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
    weights = torch.tensor([0.5, 1.0])
    result = score_batch(features, weights, bias=0.0)
    assert isinstance(result, list), "score_batch must return a Python list"
    assert all(type(v) is float for v in result), "every element must be a built-in Python float"


def test_single_row_batch_returns_one_element_list():
    features = torch.tensor([[2.0, 3.0, 4.0]])
    weights = torch.tensor([0.5, 1.0, -0.25])
    result = score_batch(features, weights, bias=1.0)
    assert result is not None, "score_batch returned None: did you forget to return the value?"
    assert len(result) == 1
    assert result == pytest.approx([4.0])


def test_mismatched_weights_length_raises_runtime_error():
    features = torch.tensor([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
    weights = torch.tensor([0.5, 1.0])
    with pytest.raises(RuntimeError):
        score_batch(features, weights, bias=0.0)


def test_does_not_modify_input_tensors():
    features = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
    weights = torch.tensor([0.5, -0.5])
    orig_features = features.clone()
    orig_weights = weights.clone()
    result = score_batch(features, weights, bias=0.25)
    assert result is not None, "score_batch returned None: did you forget to return the value?"
    assert torch.equal(features, orig_features)
    assert torch.equal(weights, orig_weights)
