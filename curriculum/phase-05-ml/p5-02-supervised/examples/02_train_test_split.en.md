# Train/test split and gradient descent

**What it shows:** Shuffling a 10-row DataFrame with a fixed seed, holding out 20% as a test set, fitting a straight line on train with gradient descent, and comparing train and test MSE.

**Step by step**
1. Lines 5–9 build a 10-request DataFrame with `id`, `tokens`, and `latency` columns.
2. Lines 11–13 create a seeded generator (`42`) and split the shuffled row indices into `8` train indices and `2` test indices.
3. Lines 15–17 print which request IDs landed in each split using `.tolist()`.
4. Lines 19–28 scale tokens into thousands (`x`) and run 50 gradient descent steps using `x_train` and `y_train` only.
5. Lines 30–33 evaluate MSE on both splits and print the fitted line alongside `Train MSE` and `Test MSE`.

**Notice:** `Test MSE` (`0.002`) stays very close to `Train MSE` (`0.001`), which tells us the straight-line model generalized cleanly to unseen requests.

**Try it yourself:** Change the seed from `42` to `7` and check how `Train IDs` and `Test IDs` change while `Test MSE` stays small.
