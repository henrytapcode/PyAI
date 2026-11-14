import torch


def score_batch(features: torch.Tensor, weights: torch.Tensor, bias: float) -> list[float]:
    """Return rounded weighted scores for a 2D batch of feature vectors.

    Example: score_batch(torch.tensor([[1.0, 2.0]]), torch.tensor([0.5, 1.0]), 0.5) -> [3.0]
    """
    return [round(v, 3) for v in (features @ weights + bias).tolist()]
