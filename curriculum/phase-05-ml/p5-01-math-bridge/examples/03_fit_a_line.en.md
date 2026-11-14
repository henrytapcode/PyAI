# Fitting a line with gradient descent

**What it shows:** Training a straight line `y = w * x + b` on measured token-latency pairs with 50 gradient descent steps, printing the loss drop, and plotting the fitted line.

**Step by step**
1. Lines 5–6 define five measured `(tokens_k, latency_s)` points that follow a roughly straight trend.
2. Lines 8–11 initialise `w` and `b` at `0.0`, pick `lr = 0.04`, and prepare a `losses` list.
3. Lines 13–20 loop 50 times: compute predictions, find errors, record MSE loss, compute the MSE gradients `grad_w` and `grad_b`, and step both parameters downhill.
4. Lines 22–24 print the rounded `w`, `b`, starting loss, and ending loss; lines 26–34 plot the scatter points and the fitted line on the same axes.

**Notice:** In just 50 steps the loss drops from `4.836` down to `0.002`, and the fitted line passes right through the middle of the scatter points.

**Try it yourself:** Increase `lr` from `0.04` to `0.1` — it overshoots the valley so the loss explodes instead of dropping (try `0.06` to see a faster stable fit).
