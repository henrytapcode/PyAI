import torch


def slope_at(w_value: float, xs: torch.Tensor, ys: torch.Tensor) -> float:
    """Return the gradient of MSE((w * xs - ys) ** 2) at w_value, rounded to 3 decimals.

    Example: slope_at(1.0, torch.tensor([1.0, 2.0]), torch.tensor([3.0, 6.0])) -> -10.0
    """
    # TODO: create a leaf tensor for w_value with requires_grad=True
    # TODO: compute MSE loss, call backward(), and return round(w.grad.item(), 3)
    pass


def fit_slope(xs: torch.Tensor, ys: torch.Tensor, lr: float, steps: int) -> float:
    """Fit y = w * x starting at w = 0.0 for `steps` autograd steps, rounded to 3 decimals.

    Example: fit_slope(torch.tensor([1.0, 2.0]), torch.tensor([3.0, 6.0]), 0.1, 20) -> 3.0
    """
    # TODO: create w = torch.tensor(0.0, requires_grad=True)
    # TODO: loop `steps` times: loss -> backward -> no_grad update -> zero_()
    # TODO: return round(w.item(), 3)
    pass
