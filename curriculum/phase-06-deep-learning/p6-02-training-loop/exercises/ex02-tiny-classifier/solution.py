import torch
import torch.nn as nn


class TinyClassifier(nn.Module):
    """Two-layer MLP classifier: Linear -> ReLU -> Linear.

    Example: TinyClassifier(2, 8, 3)(torch.zeros(4, 2)).shape == (4, 3)
    """

    def __init__(self, in_features: int, hidden: int, classes: int) -> None:
        super().__init__()
        self.hidden = nn.Linear(in_features, hidden)
        self.relu = nn.ReLU()
        self.out = nn.Linear(hidden, classes)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.out(self.relu(self.hidden(x)))


def accuracy(model: nn.Module, xs: torch.Tensor, ys: torch.Tensor) -> float:
    """Return classification accuracy on (xs, ys) rounded to 3 decimals as a Python float.

    Example: accuracy(model, xs, ys) -> 0.95
    """
    model.eval()
    with torch.no_grad():
        preds = model(xs).argmax(dim=1)
        return round((preds == ys).to(torch.float32).mean().item(), 3)
