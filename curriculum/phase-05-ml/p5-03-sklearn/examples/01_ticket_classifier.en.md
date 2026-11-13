# Ticket urgency classifier

**What it shows:** Splitting 24 labelled support tickets with `train_test_split(..., stratify=y)`, training a `LogisticRegression` classifier, measuring test accuracy, and predicting on three unseen tickets.

**Step by step**
1. Lines 6–10 generate 24 synthetic tickets with two numeric features (`tokens` and `links`) and balanced labels (`0` normal, `1` urgent).
2. Lines 12–14 split 25% of rows into test using `random_state=42` and `stratify=y` so both splits keep a 50/50 class balance.
3. Lines 16–19 create `LogisticRegression(max_iter=1000)`, call `.fit(X_train, y_train)`, and print the rounded test accuracy (`0.833`).
4. Lines 21–23 call `.predict(new_tickets).tolist()` to classify three new tickets as plain Python integers.

**Notice:** Because the normal (`20..159` tokens) and urgent (`120..319` tokens) ranges overlap slightly, test accuracy is `0.833` (5 of 6 test tickets) rather than a suspicious `1.0`.

**Try it yourself:** Change `test_size=0.25` to `0.3` or adjust the `links` count of the third new ticket (`[95.0, 1.0]`) to `[95.0, 5.0]` and see how the prediction changes.
