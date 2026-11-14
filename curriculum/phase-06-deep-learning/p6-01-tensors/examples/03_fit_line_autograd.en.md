# Fitting a line with PyTorch autograd

**What it shows:** Rebuilding the straight-line gradient descent fit (`tokens_k` vs `latency_s`) from `p5-01-math-bridge`, replacing manual MSE gradient formulas with `loss.backward()`.

**Step by step**
1. Lines 4–5 store the five prompt-size and latency observations as PyTorch tensors.
2. Lines 7–9 initialise trainable leaf tensors `w` and `b` at `0.0` with `requires_grad=True` and set `lr = 0.05`.
3. Lines 11–20 run 41 gradient descent steps: compute `pred` and MSE `loss`, print the loss every 20 steps, call `loss.backward()`, update `w` and `b` inside `with torch.no_grad():`, and zero both `.grad` fields.
4. Line 22 prints the final fitted slope `w` and intercept `b` rounded to three decimal places.

**Notice:** You never wrote `2 * error * x` or `2 * error` anywhere — autograd inferred both gradients from `pred = w * tokens_k + b` and `loss`.

**Try it yourself:** Increase the loop from `41` steps to `121` steps and observe how `b` climbs closer to `0.3` as the loss settles.
