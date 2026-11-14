# Training a classifier on two 2D blobs

**What it shows:** Defining a two-layer `TinyNet(nn.Module)` and training it with full-batch `SGD` and `CrossEntropyLoss` for 30 epochs on two synthetic 2D point clouds.

**Step by step**
1. Lines 5–10 seed PyTorch (`torch.manual_seed(0)`) and generate 200 synthetic 2D points: 100 around `(-1, -1)` labelled `0` and 100 around `(1, 1)` labelled `1`.
2. Lines 13–21 define `TinyNet` with `nn.Linear(2, 8)`, `nn.ReLU()`, and `nn.Linear(8, 2)`.
3. Lines 24–26 instantiate `model`, `nn.CrossEntropyLoss()`, and `torch.optim.SGD(model.parameters(), lr=0.2)`.
4. Lines 28–35 run 30 full-batch epochs of the five-line loop (`model(X)` -> `loss_fn` -> `zero_grad` -> `backward` -> `step`), printing rounded loss every 10 epochs.
5. Lines 37–41 switch to `model.eval()` and `torch.no_grad()` to compute and print the final training accuracy.

**Notice:** Calling `optimizer.zero_grad()` inside every epoch prevents gradients from piling up across epochs, so loss drops smoothly from `0.19` at epoch 10 down to `0.079` at epoch 30.

**Try it yourself:** Increase the number of epochs from `30` to `60` (or try `lr=0.4`) and watch how much lower the loss drops by the final epoch.
