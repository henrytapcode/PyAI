# Train TinyNet on two 2D point clouds with full-batch SGD.
import torch
import torch.nn as nn

torch.manual_seed(0)

c0 = torch.randn(100, 2) * 0.6 + torch.tensor([-1.0, -1.0])
c1 = torch.randn(100, 2) * 0.6 + torch.tensor([1.0, 1.0])
X = torch.cat([c0, c1], dim=0)
y = torch.cat([torch.zeros(100, dtype=torch.int64), torch.ones(100, dtype=torch.int64)])


class TinyNet(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.hidden = nn.Linear(2, 8)
        self.relu = nn.ReLU()
        self.out = nn.Linear(8, 2)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.out(self.relu(self.hidden(x)))


model = TinyNet()
loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.2)

for epoch in range(1, 31):
    logits = model(X)
    loss = loss_fn(logits, y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    if epoch % 10 == 0:
        print(f"epoch={epoch:2d}  loss={round(loss.item(), 3)}")

model.eval()
with torch.no_grad():
    preds = model(X).argmax(dim=1)
    acc = (preds == y).to(torch.float32).mean().item()
print("final train accuracy:", round(acc, 3))
