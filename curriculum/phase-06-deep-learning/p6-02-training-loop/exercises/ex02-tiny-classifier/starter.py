import torch
import torch.nn as nn


class TinyClassifier(nn.Module):
    """Two-layer MLP classifier: Linear -> ReLU -> Linear.

    Example: TinyClassifier(2, 8, 3)(torch.zeros(4, 2)).shape == (4, 3)
    """

    def __init__(self, in_features: int, hidden: int, classes: int) -> None:
        super().__init__()
        # TODO: create Linear(in_features, hidden), ReLU(), and Linear(hidden, classes)
        pass

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # TODO: pass x through hidden -> ReLU -> output layer and return logits
        return None


def accuracy(model: nn.Module, xs: torch.Tensor, ys: torch.Tensor) -> float:
    """Return classification accuracy on (xs, ys) rounded to 3 decimals as a Python float.

    Example: accuracy(model, xs, ys) -> 0.95
    """
    # TODO: call model.eval(), evaluate inside torch.no_grad(), and return rounded float
    return None
