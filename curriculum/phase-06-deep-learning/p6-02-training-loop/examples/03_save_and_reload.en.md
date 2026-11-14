# Saving and reloading a model's state_dict

**What it shows:** Training a model briefly, saving its `state_dict` inside a `tempfile.TemporaryDirectory()`, loading those weights into a fresh `TinyNet` instance with `weights_only=True`, and verifying identical predictions.

**Step by step**
1. Lines 7–33 create 120 synthetic 2D points and train `TinyNet` for 20 epochs.
2. Lines 35–38 compute the original model's predictions `pred_a` and accuracy `acc_a` under `model.eval()` and `torch.no_grad()`.
3. Lines 40–42 save `model.state_dict()` to a temporary file (`tinynet.pt`) that is cleaned up automatically when the `with` block exits.
4. Lines 44–49 instantiate a brand-new `TinyNet()`, load the saved parameters with `torch.load(path, weights_only=True)`, and compute `pred_b` and `acc_b` in `eval()` mode.
5. Lines 51–53 print both accuracies and `torch.equal(pred_a, pred_b)` (`True`).

**Notice:** `state_dict()` stores only the parameter tensors (weights and biases), not the `TinyNet` class code, so you always create a fresh `TinyNet()` first and then call `load_state_dict(...)`. Here we measure accuracy on `X_train` only to compare the original and reloaded models; to measure how well the model generalizes, still use validation and test splits.

**Try it yourself:** Comment out `reloaded.load_state_dict(...)` for one run to verify that an untrained `TinyNet()` produces different predictions (`same predictions: False`).
