# Checking autograd against numerical slopes

**What it shows:** Comparing PyTorch `autograd` gradients for two parameters (`w` and `b`) against the numerical central-difference slope formula from `p5-01-math-bridge`.

**Step by step**
1. Lines 4–5 define five `(x, y)` data points on the line `y = 2.0 * x + 0.5`.
2. Lines 7–8 create two leaf tensors `w` and `b` at `1.0` with `requires_grad=True`.
3. Lines 10–13 compute the MSE loss, run `loss.backward()`, and read `w.grad.item()` and `b.grad.item()`.
4. Lines 16–23 evaluate the same loss numerically at `+h` and `-h` (`h = 0.001`) for each parameter independently.
5. Lines 25–28 check that both pairs agree within `1e-3` and print `match: True`.

**Notice:** Autograd computes both `w.grad` and `b.grad` in a single `loss.backward()` pass, whereas numerical differentiation has to re-run the loss twice per parameter.

**Try it yourself:** Change the starting values of `w` and `b` from `1.0` to `2.0` and `0.5` (the exact line) and check that both gradients drop to `0.0`.
