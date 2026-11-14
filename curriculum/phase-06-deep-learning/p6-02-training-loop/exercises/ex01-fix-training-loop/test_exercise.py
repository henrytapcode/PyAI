import pytest
import torch
import torch.nn as nn

from exercise import train


def _make_line_problem():
    torch.manual_seed(0)
    xs = torch.tensor([[1.0], [2.0], [3.0], [4.0]])
    ys = 2.0 * xs + 1.0
    model = nn.Linear(1, 1)
    return model, xs, ys


def test_returns_one_python_float_loss_per_epoch():
    model, xs, ys = _make_line_problem()
    losses = train(model, xs, ys, lr=0.05, epochs=30)
    assert isinstance(losses, list), "train must return a Python list"
    assert len(losses) == 30, "losses must contain one entry per epoch"
    assert all(type(v) is float for v in losses), "each loss must be a Python float, not a tensor"


def test_final_loss_is_smaller_than_initial_loss():
    model, xs, ys = _make_line_problem()
    losses = train(model, xs, ys, lr=0.05, epochs=30)
    assert losses[-1] < losses[0], "final loss must be smaller than initial loss"


def test_final_loss_drops_below_threshold():
    model, xs, ys = _make_line_problem()
    losses = train(model, xs, ys, lr=0.05, epochs=30)
    assert losses[-1] < 0.05, (
        "loss stayed too high; check whether gradients are zeroed each epoch"
    )


def test_trained_weight_converges_near_two():
    model, xs, ys = _make_line_problem()
    train(model, xs, ys, lr=0.05, epochs=30)
    assert model.weight.item() == pytest.approx(2.0, abs=0.1)
