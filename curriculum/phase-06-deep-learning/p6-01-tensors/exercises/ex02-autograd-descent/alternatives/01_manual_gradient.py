import torch


def slope_at(w_value: float, xs: torch.Tensor, ys: torch.Tensor) -> float:
    """Return the gradient of MSE((w * xs - ys) ** 2) at w_value using the closed-form formula."""
    grad = (2.0 * (w_value * xs - ys) * xs).mean()
    return round(grad.item(), 3)


def fit_slope(xs: torch.Tensor, ys: torch.Tensor, lr: float, steps: int) -> float:
    """Fit y = w * x starting at w = 0.0 using the hand-written MSE gradient formula."""
    w = 0.0
    for _ in range(steps):
        grad = (2.0 * (w * xs - ys) * xs).mean().item()
        w = w - lr * grad
    return round(float(w), 3)
