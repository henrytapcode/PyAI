# Verify that PyTorch autograd gradients match numerical slopes for two parameters.
import torch

xs = torch.tensor([1.0, 2.0, 3.0, 4.0, 5.0])
ys = torch.tensor([2.5, 4.5, 6.5, 8.5, 10.5])

w = torch.tensor(1.0, requires_grad=True)
b = torch.tensor(1.0, requires_grad=True)

loss = ((w * xs + b - ys) ** 2).mean()
loss.backward()
gw_auto = w.grad.item()
gb_auto = b.grad.item()


def mse_loss(w_val: float, b_val: float) -> float:
    return ((w_val * xs + b_val - ys) ** 2).mean().item()


h = 0.001
gw_num = (mse_loss(1.0 + h, 1.0) - mse_loss(1.0 - h, 1.0)) / (2 * h)
gb_num = (mse_loss(1.0, 1.0 + h) - mse_loss(1.0, 1.0 - h)) / (2 * h)

match = abs(gw_auto - gw_num) < 1e-3 and abs(gb_auto - gb_num) < 1e-3
print(f"w grad: autograd={round(gw_auto, 3)}, numeric={round(gw_num, 3)}")
print(f"b grad: autograd={round(gb_auto, 3)}, numeric={round(gb_num, 3)}")
print(f"match: {match}")
