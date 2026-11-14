import torch
import torch.nn as nn


def train(
    model: nn.Module,
    xs: torch.Tensor,
    ys: torch.Tensor,
    lr: float,
    epochs: int,
) -> list[float]:
    """Train model on (xs, ys) with MSELoss and SGD, returning rounded loss per epoch.

    Example: train(nn.Linear(1, 1), xs, 2 * xs + 1, lr=0.05, epochs=30)[-1] < 0.05
    """
    # TODO: this function runs, but has 2 bugs: find and fix them.
    loss_fn = nn.MSELoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=lr)
    losses = []
    for _ in range(epochs):
        preds = model(xs)
        loss = loss_fn(preds, ys)
        loss.backward()
        optimizer.step()
        losses.append(loss)
    return losses
