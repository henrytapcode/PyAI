# Fit a straight line y = w * x + b to token-latency data using PyTorch autograd.
import torch

tokens_k = torch.tensor([1.0, 2.0, 3.0, 4.0, 5.0])
latency_s = torch.tensor([0.9, 1.4, 2.1, 2.6, 3.2])

w = torch.tensor(0.0, requires_grad=True)
b = torch.tensor(0.0, requires_grad=True)
lr = 0.05

for step in range(41):
    pred = w * tokens_k + b
    loss = ((pred - latency_s) ** 2).mean()
    if step % 20 == 0:
        print(f"step={step}: loss={round(loss.item(), 3)}")
    loss.backward()
    with torch.no_grad():
        w -= lr * w.grad
        b -= lr * b.grad
    w.grad.zero_()
    b.grad.zero_()

print(f"Fitted line: w={round(w.item(), 3)}, b={round(b.item(), 3)}")
