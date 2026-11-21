import torch


def slope_at(w_value: float, xs: torch.Tensor, ys: torch.Tensor) -> float:
    """Return the gradient of MSE((w * xs - ys) ** 2) at w_value, rounded to 3 decimals.

    Example: slope_at(1.0, torch.tensor([1.0, 2.0]), torch.tensor([3.0, 6.0])) -> -10.0
    """
    w = torch.tensor(float(w_value), requires_grad=True)
    loss = ((w * xs - ys) ** 2).mean()
    loss.backward()
    return round(w.grad.item(), 3)


def fit_slope(xs: torch.Tensor, ys: torch.Tensor, lr: float, steps: int) -> float:
    """Fit y = w * x starting at w = 0.0 for `steps` autograd steps, rounded to 3 decimals.

    Example: fit_slope(torch.tensor([1.0, 2.0]), torch.tensor([3.0, 6.0]), 0.1, 20) -> 3.0
    """
    w = torch.tensor(0.0, requires_grad=True)
    for _ in range(steps):
        residual = w * xs - ys
        torch.mean(residual ** 2).backward()
        with torch.no_grad():
            w -= lr * w.grad
            w.grad.zero_()
    return round(w.item(), 3)
