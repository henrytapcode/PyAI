# Train TinyNet briefly, save state_dict to a temp folder, and verify reloaded predictions match.
import tempfile
from pathlib import Path
import torch
import torch.nn as nn

torch.manual_seed(0)

c0 = torch.randn(60, 2) * 0.7 + torch.tensor([-1.0, -1.0])
c1 = torch.randn(60, 2) * 0.7 + torch.tensor([1.0, 1.0])
X_train = torch.cat([c0, c1], dim=0)
y_train = torch.cat([torch.zeros(60, dtype=torch.int64), torch.ones(60, dtype=torch.int64)])


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

for _ in range(20):
    loss = loss_fn(model(X_train), y_train)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

model.eval()
with torch.no_grad():
    pred_a = model(X_train).argmax(dim=1)
    acc_a = round((pred_a == y_train).to(torch.float32).mean().item(), 3)

with tempfile.TemporaryDirectory() as tmp:
    path = Path(tmp) / "tinynet.pt"
    torch.save(model.state_dict(), path)

    reloaded = TinyNet()
    reloaded.load_state_dict(torch.load(path, weights_only=True))
    reloaded.eval()
    with torch.no_grad():
        pred_b = reloaded(X_train).argmax(dim=1)
        acc_b = round((pred_b == y_train).to(torch.float32).mean().item(), 3)

print("original accuracy:", acc_a)
print("reloaded accuracy:", acc_b)
print("same predictions:", torch.equal(pred_a, pred_b))
