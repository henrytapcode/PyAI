# Mini-batch training with DataLoader and train/val/test splits

**What it shows:** Splitting synthetic data into train/validation/test sets, iterating over shuffled mini-batches with `DataLoader`, checking validation accuracy every 5 epochs, and evaluating the test set once at the end.

**Step by step**
1. Lines 5–16 generate 200 shuffled 2D points and split them into 120 train, 40 validation, and 40 test examples.
2. Lines 18–24 wrap the training tensors in `TensorDataset` and a `DataLoader` with `batch_size=32`, `shuffle=True`, `num_workers=0`, and a seeded `torch.Generator`.
3. Lines 38–42 define `eval_accuracy`, which calls `model.eval()` and wraps inference in `with torch.no_grad():`.
4. Lines 49–56 train for 20 epochs, resetting `model.train()` before iterating through batches and printing validation accuracy every 5 epochs.
5. Line 58 computes `test_acc` exactly once after training finishes.

**Notice:** Calling `model.train()` at the start of each epoch switches the model back out of evaluation mode after `eval_accuracy` called `model.eval()`.

**Try it yourself:** Change `batch_size=32` to `batch_size=16` so each epoch performs more gradient updates, and compare validation accuracy at epoch 5.
