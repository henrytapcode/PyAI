# Train TinyNet with mini-batches (DataLoader) and train/val/test splits.
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

torch.manual_seed(0)

c0 = torch.randn(100, 2) * 1.1 + torch.tensor([-1.0, -1.0])
c1 = torch.randn(100, 2) * 1.1 + torch.tensor([1.0, 1.0])
X = torch.cat([c0, c1], dim=0)
y = torch.cat([torch.zeros(100, dtype=torch.int64), torch.ones(100, dtype=torch.int64)])

perm = torch.randperm(len(X))
X, y = X[perm], y[perm]
X_train, y_train = X[:120], y[:120]
X_val, y_val = X[120:160], y[120:160]
X_test, y_test = X[160:], y[160:]

loader = DataLoader(
    TensorDataset(X_train, y_train),
    batch_size=32,
    shuffle=True,
    num_workers=0,
    generator=torch.Generator().manual_seed(0),
)


class TinyNet(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.hidden = nn.Linear(2, 8)
        self.relu = nn.ReLU()
        self.out = nn.Linear(8, 2)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.out(self.relu(self.hidden(x)))


def eval_accuracy(model: nn.Module, xs: torch.Tensor, ys: torch.Tensor) -> float:
    model.eval()
    with torch.no_grad():
        preds = model(xs).argmax(dim=1)
        return round((preds == ys).to(torch.float32).mean().item(), 3)


model = TinyNet()
loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.02)

for epoch in range(1, 21):
    model.train()
    for xb, yb in loader:
        loss = loss_fn(model(xb), yb)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    if epoch % 5 == 0:
        print(f"epoch={epoch:2d}  val_acc={eval_accuracy(model, X_val, y_val)}")

print("test_acc:", eval_accuracy(model, X_test, y_test))
